<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Admin Start Bot</title>
    </head>
    <body style="text-align: center;">
        @if (isset($success) && $success == true)
        <h3>Successfully started the bot! Start it again or close the window.</h3><br>
        @endif
        <h1>Admin Start Bot</h1>
        <form action="/admin/startBot" method="POST">
            @csrf
            <input id="old_bot" onclick="show()" type="radio" name="bot" value="old" checked>
            <label for="old_bot">Old Bot (with login and other stuff)</label>
            <input id="new_bot" onclick="hide()" type="radio" name="bot" value="new">
            <label for="new_bot">New Bot (only watch)</label>
            <br><hr>
            <div id="for_old">
                <label>Google Accounts</label>
                <br><hr>
                <textarea rows="10" style="width: 50%; margin: 0 auto;" name="accounts"></textarea><br>
                <pre>
Paste the accounts in the following format:
email;password;recovery_email;comment
email;password;recovery_email;comment
email;password;recovery_email;comment

example:
asdasd@gmail.com;asdasd;asd123@gmail.com;1
asdas123@gmail.com;asdasd;asd234@gmail.com;0
asd123asd@gmail.com;asdasd;asd321@gmail.com;0
a123sdasd@gmail.com;asdasd;asd543@gmail.com;1
                </pre>
                <br>
                <label>Comments</label>
                <br><hr>
                <textarea rows="10" style="width: 50%; margin: 0 auto;" name="comments"></textarea><br>
                <pre>
Paste the comments in the following format:
comment
comment
comment

example:
this is an example comment
this is another example comment
this is third example comment
                </pre>
                <br>
            </div>
            <label>Proxies</label>
            <br><hr>
            <textarea rows="10" style="width: 50%; margin: 0 auto;" name="proxies"></textarea><br>
            <pre>
Paste the proxies in the following format:
ip:port
ip:port
ip:port

example:
111.111.111.111:2121
222.222.222.222:1212
333.333.333.333:1313
444.444.444.444:3131
            </pre>
            <br>
            <label>Keywords</label>
            <br><hr>
            <textarea rows="10" style="width: 50%; margin: 0 auto;" name="keywords"></textarea><br>
            <pre>
Paste the keywords in the following format:
keyword
keyword
keyword

example:
this is an example keyword
this is another example keyword
this is third example keyword
            </pre>
            <br>
            <label>Video</label>
            <br><hr>
            <input style="width: 50%; margin: 0 auto;" type="text" name="video">
            <br><br>
            <label>Number of threads</label>
            <br><hr>
            <input style="width: 50%; margin: 0 auto;" type="number" name="threads">
            <br><br>
            <label>MIN watchtime</label>
            <br><hr>
            <input style="width: 50%; margin: 0 auto;" type="number" name="min_time">
            <br><br>
            <label>MAX watchtime</label>
            <br><hr>
            <input style="width: 50%; margin: 0 auto;" type="number" name="max_time">
            <br><br><br>
            <input type="submit" value="Start the bot">
        </form>
        <br>
        <a href="/admin/logout">Logout</a>
        <script>
            var div = document.getElementById('for_old');
            function hide()
            {
                div.style.display = "none";
            }
            function show()
            {
                div.style.display = "block";
            }
        </script>
    </body>
</html>
