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
Route::get('/admin/login', function () {
    return view('admin_login');
});
Route::get('/admin/startBot', function (Request $request) {
    if(!$request->session()->has('isAdminLogged') || $request->session()->get('isAdminLogged') != true)
        return redirect('/admin/login');
    return view('admin_start_bot');
});
Route::post('/admin/login', "AppController@login");
Route::post('/admin/startBot', "AppController@startBot");
Route::get('/admin/logout', "AppController@logout");