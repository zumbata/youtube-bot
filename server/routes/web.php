<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

use Illuminate\Http\Request;

Route::get('/', function () {
    return view('welcome');
});
Route::get('/admin', function () {
    return redirect('/admin/login');
});

/* BOTS */
Route::get('/admin/bots', function (Request $request) {
    if(!$request->session()->has('isAdminLogged') || $request->session()->get('isAdminLogged') == false)
        return redirect('/admin/login');
    return view('pages.admin_start_bot');
});
Route::get('/admin/bot', function (Request $request) {
    if(!$request->session()->has('isAdminLogged') || $request->session()->get('isAdminLogged') == false)
        return redirect('/admin/login');
    return redirect('/admin/bots');
});
Route::get('/admin/bot/old', function (Request $request) {
    if(!$request->session()->has('isAdminLogged') || $request->session()->get('isAdminLogged') == false)
        return redirect('/admin/login');
    return view('pages.admin_bot', ['bot' => 'old']);
});
Route::get('/admin/bot/new', function (Request $request) {
    if(!$request->session()->has('isAdminLogged') || $request->session()->get('isAdminLogged') == false)
        return redirect('/admin/login');
    return view('pages.admin_bot', ['bot' => 'new']);
});

Route::get('/admin/login', function (Request $request) {
    if($request->session()->has('isAdminLogged') && $request->session()->get('isAdminLogged') == true)
        return redirect('/admin/bots');
    return view('pages.admin_login');
});

Route::get('/admin/bots', function (Request $request) {
    if(!$request->session()->has('isAdminLogged') || $request->session()->get('isAdminLogged') == false)
        return redirect('/admin/login');
    return view('pages.admin_start_bot');
});

Route::get('/admin/log/{name}', function ($name){
    $file_to_open = ($name == 'bot') ? '/var/log/custom.log' : '/var/log/geckodriver.log';
    $lines = [];
    if ($fh = fopen($file_to_open, 'r')) {
        while (!feof($fh)) {
            $line = fgets($fh);
            $lines[] = $line;
        }
        fclose($fh);
    }
    return view('pages.admin_log', ['lines' => $lines]);
});

Route::post('/admin/login', "AppController@login");
Route::post('/admin/bots', "AppController@bots");
Route::get('/admin/logout', "AppController@logout");