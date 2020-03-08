<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class AppController extends Controller
{
    public function log($name)
    {
        $file_to_open = ($name == 'bot') ? '/var/log/custom.log' : '/var/log/geckodriver.log';
        $lines = [];
        if ($fh = fopen($file_to_open, 'r')) {
            while (!feof($fh)) {
                $line = fgets($fh);
                $lines[] = $line;
            }
            fclose($fh);
        }
        return view('pages.admin_log', ['lines' => $lines, 'log' => $name]);
    }

    public function clearLog($name)
    {
        $file = ($name == "driver") ? "geckodriver.log" : "custom.log";
        shell_exec(">/var/log/{$file}");
        return redirect("/admin/log/{$name}");
    }

    public function stopBots()
    {
        shell_exec("killall python3");
        shell_exec("killall geckodriver");
        shell_exec("killall firefox");
        return view('pages.admin_start_bot', ['stopped' => true]);
    }

    public function bots(Request $request)
    {
        $bot = ($request->input('bot') == "new") ? "new_bot" : "old_bot";
        $proxies = preg_split('/\n|\r\n?/', $request->input('proxies'));
        $keywords = preg_split('/\n|\r\n?/', $request->input('keywords'));
        $chunked = array_chunk($proxies, floor(count($proxies)/intval($request->input('threads'))));
        $sleep = 0;
        foreach ($chunked as $chunk)
        {
            $encoded = json_encode([
                "accounts"  => $request->input('accounts'),
                "comments"  => $request->input('comments'),
                "proxies"   => $chunk,
                "keywords"  => $keywords,
                "video"     => $request->input('video'),
                "threads"   => intval($request->input('threads')),
                "min_time"  => intval($request->input('min_time')),
                "max_time"  => intval($request->input('max_time')),
                "sleep"     => $sleep
            ]);
            $encrypted = base64_encode($encoded);
            shell_exec("python3 ../../{$bot}/bot.py {$encrypted} >> /var/log/custom.log 2>&1 &");
            $sleep += 3;
        }
        return view('pages.admin_start_bot', ['success' => true]);
    }

    public function login(Request $request)
    {
        $username = $request->input('username');
        $password = $request->input('password');
        if($username == env('ADMIN_USERNAME') && $password == env('ADMIN_PASSWORD'))
        {
            $request->session()->put('isAdminLogged', true);
            return redirect('/admin/bots');
        }
        else
            return view('pages.admin_login', ['success' => false]);
    }
    
    public function logout(Request $request)
    {
        $request->session()->forget('isAdminLogged');
        return redirect('/admin/login?logout=true');
    }
}
