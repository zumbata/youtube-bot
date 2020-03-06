<nav class="navbar navbar-expand-lg navbar-dark navbar-custom">
  <a class="navbar-brand" href="#">Navbar</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
    <div class="navbar-nav">
      <a class="nav-item nav-link active" href="/admin">Home</a>
      @if(Session::has('isAdminLogged'))
      <a class="nav-item nav-link" href="/admin/logout">Logout</a>
      <a class="nav-item nav-link" href="/admin/log">Bot Log</a>
      <a class="nav-item nav-link" href="/admin/geckodriver_log">Geckodriver Log</a>
      @else
      <a class="nav-item nav-link" href="/admin/login">Login</a>
      @endif
    </div>
  </div>
</nav>