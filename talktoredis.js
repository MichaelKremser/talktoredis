var https = require('https');
var fs = require('fs');
var redis = require('redis'),
        client = redis.createClient();
var url = require('url');

var options = {
  hostname: 'yourhostname',
  port: 8443,
  passphrase: 'yourpassphrase',
  key: fs.readFileSync('keyfile.pem'),
  cert: fs.readFileSync('certfile.pem')
};

function logWithDateTime(msg) {
        console.log(new Date().toISOString().replace('T', ' ') + ': ' + msg);
}

logWithDateTime('talktoredis 0.2 started!');

https.createServer(options, function (req, res) {
  var powermode = '';
  query = url.parse(req.url,true).query;
  var header = req.headers['authorization']||'',        // get the header
  token=header.split(/\s+/).pop()||'',            // and the encoded auth token
  auth=new Buffer(token, 'base64').toString(),    // convert from base64
  parts=auth.split(/:/),                          // split on colon
  username=parts[0],
  password=parts[1];
  if (username === 'yourusername' && password === 'yourpassword') {
    if (query.newvalue == 'on' || query.newvalue == 'off' || query.newvalue == 'reset') {
      client.set("wlan.powermode", query.newvalue);
      logWithDateTime('Host ' + req.connection.remoteAddress + ' changed state to ' + query.newvalue);
      res.writeHead(302, {'Location': 'http://somehost/wlanstate.html'});
      res.write("You're going to be redirected to the log...");
      res.end();
    }
    else {
      client.get("wlan.powermode", function (err, reply) {
        res.writeHead(200, {'Content-Type': 'text/html'});
        powermode = reply.toString();
        logWithDateTime('powermode = ' + powermode);
        logWithDateTime('Sending options to ' + req.connection.remoteAddress);
        res.write('<html><head><title>Wireless LAN Power Management</title><meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=10.0, user-scalable=yes" /></head>');
        res.write('<body style="background-color: Black; color: White;">');
        res.write('<a href="?newvalue=on">Turn WLAN on</a> ');
        res.write('<a href="?newvalue=off">Turn WLAN off</a> <br />');
        res.write('<a href="?newvalue=reset">Reset WLAN</a>');
        res.write('</body></html>');
        res.end();
      });
    }
  }
  else {
    logWithDateTime('Auth failed for ' + req.connection.remoteAddress);
    res.writeHead(401, {'Content-Type': 'text/html', 'WWW-Authenticate': 'Basic realm="noderedis"' });
    res.write('<html><head><title>Wireless LAN Power Management</title></head>');
    res.write('<body>401 Unauthorized. This incident has been logged. Logs are contiuously supervised by men.</body></html>');
    res.end();
  }
}).listen(8443);
