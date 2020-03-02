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
Route::get('/admin/bots', function () {
    return view('pages.admin_start_bot');
});
Route::get('/admin/bot', function () {
    return redirect('/admin/bots');
});
Route::get('/admin/bot/old', function () {
    return view('pages.admin_bot', ['bot' => 'old']);
});
Route::get('/admin/bot/new', function () {
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
Route::post('/admin/login', "AppController@login");
Route::post('/admin/bots', "AppController@bots");
Route::get('/admin/logout', "AppController@logout");