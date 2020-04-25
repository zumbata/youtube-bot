<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class AppController extends Controller
{
    // public function log()
    // {
    //     $lines = [];
    //     if ($fh = fopen('/var/log/custom.log', 'r')) {
    //         while (!feof($fh)) {
    //             $line = fgets($fh);
    //             $lines[] = $line;
    //         }
    //         fclose($fh);
    //     }
    //     return view('pages.admin_log', ['lines' => $lines]);
    // }

    // public function clearLog()
    // {
    //     shell_exec(">/var/log/custom.log");
    //     return redirect("/admin/log");
    // }

    public function stopBots()
    {
        shell_exec("killall python3");
        shell_exec("killall chromedriver");
        shell_exec("killall google-chrome");
        return view('pages.admin_start_bot', ['stopped' => true]);
    }

    public function bots(Request $request)
    {
        // $bot = ($request->input('bot') == "new") ? "new_bot" : "old_bot";
        // $proxies = preg_split('/\n|\r\n?/', $request->input('proxies'));
        // // $keywords = preg_split('/\n|\r\n?/', $request->input('keywords'));
        // $chunked = array_chunk($proxies, floor(count($proxies)/intval($request->input('threads'))));
        // $sleep = 0;
        // foreach ($chunked as $chunk)
        // {
        //     $encoded = json_encode([
        //         "accounts"  => $request->input('accounts'),
        //         "comments"  => $request->input('comments'),
        //         "proxies"   => $chunk,
        //         // "keywords"  => $keywords,
        //         "video"     => $request->input('video'),
        //         // "threads"   => intval($request->input('threads')),
        //         "min_time"  => intval($request->input('min_time')),
        //         "max_time"  => intval($request->input('max_time')),
        //         "sleep"     => $sleep
        //     ]);
        //     $encrypted = base64_encode($encoded);
        //     $cmd = "python3 ../../{$bot}/new_bot.py {$encrypted} >> /var/log/custom.log 2>&1 &";
        //     shell_exec($cmd);
        //     $sleep += 10;
        // }
        $uas = [];
        $bot = ($request->input('bot') == "new") ? "new_bot" : "old_bot";
        if ($file = fopen("../../{$bot}/ua.txt", "r")) {
            while(!feof($file)) {
                $uas[] = preg_replace("/\r|\n/", "", fgets($file));;
            }
            fclose($file);
        }
        $proxies = preg_split('/\n|\r\n?/', $request->input('proxies'));
        $tmp_videos = preg_split('/\n|\r\n?/', $request->input('videos'));
        $videos = array_map(function($val) {
            $tmp_arr = [];
            $splited = explode(';', $val);
            $tmp_arr['href'] = $splited[0];
            $tmp_arr['min_time'] = intval($splited[1]);
            $tmp_arr['max_time'] = intval($splited[2]);
            return $tmp_arr;
        }, $tmp_videos);
        $sleep = 0;
        foreach ($proxies as $proxy)
        {
            $encoded = json_encode([
                "proxy"      => $proxy,
                "videos"     => $videos,
                "user_agent" => $uas[mt_rand(0, count($uas) - 1)],
                "sleep"      => $sleep
            ]);
            $encrypted = base64_encode($encoded);
            $cmd = "python3 ../../{$bot}/new_bot.py {$encrypted} > /dev/null 2>/dev/null &";
            shell_exec($cmd);
            $sleep += 10;
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
