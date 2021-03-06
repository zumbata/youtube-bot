@extends('layouts.default', ['title' => 'Start Bot']) @section('content')
<div class="card card-signin my-5">

    <div class="pt-3 text-center mx-5">
        <h2>Start Bot</h2>
        <form action="/admin/bots" method="POST">
            @csrf @if($bot == 'old')
            <div class="form-row">
                <div class="col-6">
                    <div class="form-group">
                        <label for="accounts">Google Accounts</label>
                        <textarea class="form-control" name="accounts" id="accounts" rows="10" placeholder="Paste the accounts in the following format:
email;password;recovery_email;comment
email;password;recovery_email;comment
email;password;recovery_email;comment

example:
asdasd@gmail.com;asdasd;asd123@gmail.com;1
asdas123@gmail.com;asdasd;asd234@gmail.com;0
asd123asd@gmail.com;asdasd;asd321@gmail.com;0
a123sdasd@gmail.com;asdasd;asd543@gmail.com;1"></textarea>
                    </div>
                </div>
                <div class="col-6">
                    <div class="form-group">
                        <label for="comments">Comments</label>
                        <textarea class="form-control" rows="10" name="comments" placeholder="Paste the comments in the following format:
comment
comment
comment

example:
this is an example comment
this is another example comment
this is third example comment"></textarea>
                    </div>
                </div>
            </div>
            @endif
            <div class="form-row">
                <div class="col-6">
                    <div class="form-group">
                        <label for="proxies">Proxies</label>
                        <textarea class="form-control" name="proxies" id="proxies" rows="10" placeholder="Paste the proxies in the following format:
ip:port
ip:port
ip:port

example:
111.111.111.111:2121
222.222.222.222:1212
333.333.333.333:1313
444.444.444.444:3131"></textarea>
                    </div>
                </div>
                <div class="col-6">
                    <div class="form-group">
                        <label for="videos">Videos</label>
                        <textarea class="form-control" rows="10" name="videos" placeholder="Paste the keywords in the following format:
link;min_time;max_time
link;min_time;max_time
link;min_time;max_time

example:
https://www.youtube.com/watch?v=MxFoEVzxxb8;120;180
https://www.youtube.com/watch?v=asdfsgsdffa;160;200
https://www.youtube.com/watch?v=adfghrsbntr;220;380"></textarea>
                    </div>
                </div>
            </div>
            <!-- <div class="form-row text-left">
                <div class="col">
                    <div class="form-label-group">
                        <input type="number" class="form-control" id="threads" name="threads" placeholder="">
                        <label for="threads">Threads</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-label-group">
                        <input type="number" class="form-control" id="min-time" name="min_time" placeholder="">
                        <label for="min-time">MIN Watch Time (seconds)</label>
                    </div>
                </div>
                <div class="col">
                    <div class="form-label-group">
                        <input type="number" class="form-control" id="max-time" name="max_time" placeholder="">
                        <label for="max-time">MAX Watch Time (seconds)</label>
                    </div>
                </div>
            </div> -->
            <!-- <div class="form-row text-left">
                <div class="col">
                    <div class="form-label-group">
                        <input type="text" class="form-control" id="video" name="video" placeholder="">
                        <label for="video">Link to Video</label>
                    </div>
                </div>
            </div> -->
            @if($bot == 'old')
            <input type="hidden" value="old" name="bot">
            @else
            <input type="hidden" value="new" name="bot">
            @endif
            <div class="form-group py-4">
               <button class="btn btn-lg btn-primary btn-block text-uppercase w-100 mx-auto" type="submit">Start</button>
            </div>
        </form>
    </div>
</div>
@stop