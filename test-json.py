from flask import Flask, request, jsonify
import json
import requests
from selenium import webdriver

item = "Exalted%20Orb"

def dump(obj):
   for attr in dir(obj):
       if hasattr( obj, attr ):
           print( "obj.%s = %s" % (attr, getattr(obj, attr)))

# print(json.loads(request.get_data()))
# r = requests.get("http://poe-rates.com/index.php?league=Abyss&item="+item+"&interval=1h")

address = "http://poe-rates.com/index.php?league=Abyss&item="+item+"&interval=1h"

driver = webdriver.PhantomJS()
driver.implicitly_wait(1)
driver.get(address)

value = 0
elems = driver.find_elements_by_class_name('value')
for e in elems:
	print e.get_attribute('class')
	if e.get_attribute('class') == "value green-text":
		print e.text
		value = e.text
		break
