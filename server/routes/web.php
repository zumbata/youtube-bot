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
use Illuminate\Support\Facades\Route;

Route::view('/', 'welcome');
Route::redirect('/admin', '/admin/login');
Route::redirect('/admin/bot', '/admin/bots')->middleware('isLogged');
Route::view('/admin/bots', 'pages.admin_start_bot')->middleware('isLogged');
Route::get('/admin/bot/{bot}',function ($bot) {
    return view('pages.admin_bot', ['bot' => $bot]);
})->middleware('isLogged');
Route::get('/admin/login', function (Request $request) {
    if($request->session()->has('isAdminLogged') && $request->session()->get('isAdminLogged') == true)
        return redirect('/admin/bots');
    return view('pages.admin_login');
});
Route::get('/admin/log', 'AppController@log');
Route::get('/admin/log/clear', 'AppController@clearLog');
Route::get('/admin/bots/stop', 'AppController@stopBots');
Route::post('/admin/bots', "AppController@bots");
Route::post('/admin/login', "AppController@login");
Route::get('/admin/logout', "AppController@logout");