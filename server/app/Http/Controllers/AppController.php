<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class AppController extends Controller
{
    public function startBot(Request $request)
    {
        $bot = ($request->input('bot') == "new") ? "new_bot" : "old_bot";
        $encryped = base64_encode(json_encode([
            "accounts" => $request->input('accounts'),
            "comments" => $request->input('comments'),
            "proxies" => $request->input('proxies'),
            "keywords" => $request->input('keywords'),
            "video" => $request->input('video'),
            "threads" => $request->input('threads'),
            "min_time" => $request->input('min_time'),
            "max_time" => $request->input('max_time')
        ]));
        // dont wait for it
        shell_exec("python3 ../../{$bot}/bot.py {$encryped} > /var/log/custom.log 2>&1 &");
        //wait for it
        // shell_exec("python3 ../../{$bot}/bot.py {$encryped}");
        return view('admin_start_bot', ['success' => true]);
    }

    public function login(Request $request)
    {
        $username = $request->input('username');
        $password = $request->input('password');
        if($username == env('ADMIN_USERNAME') && $password == env('ADMIN_PASSWORD'))
        {
            $request->session()->put('isAdminLogged', true);
            return redirect('/admin/startBot');
        }
        else
            return view('admin_login', ['success' => false]);
    }
    
    public function logout(Request $request)
    {
        $request->session()->put('isAdminLogged', false);
        $request->session()->forget('isAdminLogged');
        return redirect('/admin/login');
    }
}
