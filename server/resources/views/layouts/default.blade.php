<!doctype html>
<html>
    <head>
        <title>{{ $title }}</title>
        @include('includes.head')
    </head>
    <body>
        @include('includes.header')
        <div class="container">
            <div id="main" class="row">
                <div class="col-12">
                    @yield('content')
                </div>
            </div>

            <footer class="row">
                @include('includes.footer')
            </footer>
        </div>
    </body>
</html>
