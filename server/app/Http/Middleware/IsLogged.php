<?php

namespace App\Http\Middleware;

use Closure;

class IsLogged
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next)
    {
        if(!$request->session()->has('isAdminLogged') || $request->session()->get('isAdminLogged') == false)
            return redirect('/admin/login');
        return $next($request);
    }
}
