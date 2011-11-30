
javascript error tracking server
================================

This is a small webapp to track the errors thrown in your javascript apps

install
======

- First edit track_settings.py file and change SITE_CODE var to one you like. Keep it secret.

- First deploy this djando app in your server. You can do it in heroku
- add the next tracking code in your aplication

    (function() {
        var SERVER = 'http://yourserver.com';
        var s = document.createElement('script');
        s.type='text/javascript';
        s.async=true;
        s.src = SERVER + '/js/error_track.js?s=' + encodeURI(SERVER);
        (document.getElementsByTagName('head')[0]||document.getElementsByTagName('body')[0]).appendChild(s);
    })();

- point your browser to http://youserver/SITE_CODE. SITE_CODE is the variable you set in the first step.
