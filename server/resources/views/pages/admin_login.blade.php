@extends('layouts.default', ['title' => 'Log In'])
@section('content')
    <div class="col-sm-9 col-md-7 col-lg-5 mx-auto pt-5">
        <div class="card card-signin my-5">
          <div class="card-body">
            <h5 class="card-title text-center">Log In</h5>
            <!-- if (isset(Session::get('logout')) && Session::get('logout') == true)
                <p class="text-center text-success">Logged out.</p>
            endif -->
            <form class="form-signin" method="POST" action="/admin/login">
                @csrf
                <div class="form-label-group">
                    <input type="text" id="username" name="username" class="form-control" placeholder="" required autofocus>
                    <label for="username">Username</label>
                </div>

                <div class="form-label-group">
                    <input type="password" id="password" name="password" class="form-control" placeholder="" required>
                    <label for="password">Password</label>
                </div>

                @if (isset($success) && $success == false)
                    <p class="text-center text-danger">Unsuccessful login. Try again.</p>
                @endif
                <button class="btn btn-lg btn-primary btn-block text-uppercase" type="submit">Log In</button>
            </form>
          </div>
        </div>
      </div>
<!--     
    <div class="row justify-content-center">
        <div class="col-3">
            <h1 class="text-center">Admin Login</h1>
            <form action="/admin/login" method="POST" class="text-center">
                @csrf
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" name="username">
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password">
                </div>
                <div class="form-group">
                    <input type="submit" class="btn btn-primary w-75" value="Login">
                </div>
            </form>
        </div>
    </div> -->
@stop