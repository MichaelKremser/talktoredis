# talktoredis

The project consists of three parts which I would like to explain:

## talktoredis.js

This is a Node JS app that listens on port 8443 using TLS and waits for a user to authenticate. Then the user can click on a link which makes the app writing a predefined value to a Redis server.

## start_talktoredis

Starts the beforementioned Node JS app.

## checkrediskey

This is a shell script that polls the values of some keys of the Redis server in a specified interval. It reacts to changes and executes commands dependent on the key whose value was changed.

# Demonstration video

I've uploaded a demonstration video on YouTube:

https://www.youtube.com/watch?v=cEb_Q4gV6x0

# Future improvements

## talktoredis.js

All the settings should be read from a configuration file rather than being hard coded.
