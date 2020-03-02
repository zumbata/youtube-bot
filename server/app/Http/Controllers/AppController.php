<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class AppController extends Controller
{
    public function startBot(Request $request)
    {
        $bot = ""; // get from requests
        $encryped = base64_encode(json_encode([
            //data
        ]));
        shell_exec("python3 ../{$bot} {$encryped} >/dev/null 2>/dev/null &");
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
