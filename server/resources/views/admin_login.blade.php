<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Admin Login</title>
    </head>
    <body style="text-align: center;">
        @if (isset($success) && $success == false)
        <h2>Unsuccessfull login. Try again.</h2><br>
        @endif
        <h1>Admin Login</h1>
        <form action="/admin/login" method="POST">
            @csrf
            <label>Username</label>
            <input type="text" name="username">
            <br>
            <label>Password</label>
            <input type="password" name="password">
            <br>
            <input type="submit" value="Login">
        </form>
    </body>
</html>
