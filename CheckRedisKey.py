#!/usr/bin/python
# -*- coding: utf-8 -*-
try:
	import redis
except:
	print("import redis - error")
	pass
import time
import datetime
import subprocess

# Reference: https://pypi.python.org/pypi/redis/

# def my_handler(message):
# 	print 'MY HANDLER: ', message['data']

def getKeyDefensive(redisConn, keyName):
	keyValue = redisConn.get(keyName)
	if keyValue is None:
		keyValue = ""
	return keyValue

r = redis.StrictRedis(host='localhost', port=6379, db=0)

var_wlan = ""
oldvar_wlan = ""
var_speak = ""
var_syscmd = ""
quitme = ""
testValue = ""
print("CheckRedisKey.py started")
while quitme != "y":
	var_wlan = getKeyDefensive(r, "wlan.powermode") # r.get("wlan.powermode")
	if oldvar_wlan != "" and var_wlan != oldvar_wlan:
		print("Value has changed from " + oldvar_wlan + " to " + var_wlan)
		if var_wlan == "on":
			print("wlan.powermode --> on")
			subprocess.Popen(["startwlanap"]).wait()
			subprocess.Popen(["espeak", "wireless network has been turned on"]).wait()
		if var_wlan == "off":
			print("wlan.powermode --> off")
			subprocess.Popen(["stopwlanap"]).wait()
			subprocess.Popen(["espeak", "wireless network has been shut down"]).wait()
		if var_wlan == "reset":
			print("wlan.powermode --> off --> on")
			subprocess.Popen(["stopwlanap"]).wait()
			subprocess.Popen(["startwlanap"]).wait()
			subprocess.Popen(["espeak", "wireless network has been turned on"]).wait()
			r.set("wlan.powermode", "on")
			var_wlan = "on"
	oldvar_wlan = var_wlan

#	testValue = r.get("test")
#	if testValue == 'test1':
#		subprocess.Popen(["/home/michael/bin/echowas", "123"])

	var_speak = getKeyDefensive(r, 'speak.text')
	if var_speak != '':
		r.set('speak.text', '')
		subprocess.Popen(["espeak", "-vde", "-s100", var_speak])

	var_syscmd = getKeyDefensive(r, 'syscmd')
	if var_syscmd != '':
		print("Got command " + var_syscmd)
		r.set('syscmd', '')
		if var_syscmd == "restart_ssh":
			subprocess.Popen(["service", "ssh", "restart"])
		if var_syscmd == "restart_nm":
			subprocess.Popen(["service", "network-manager", "restart"])
		if var_syscmd == "log":
			now = datetime.datetime.now()
			print now.strftime("%Y-%m-%d %H:%M:%S")
		if var_syscmd == "quit":
			quitme = "y"

	if quitme != "y":
		time.sleep(2)

# Error: TypeError: subscribe() got an unexpected keyword argument 'my-channel'
# p = r.pubsub()
# p.subscribe(**{'my-channel': my_handler})

print("Good bye!")
