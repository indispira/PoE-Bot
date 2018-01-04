from flask import Flask, request, jsonify
import json
import requests
from selenium import webdriver

item = "Exalted%20Orb"
datetime_array = {'hour':'1h', 'halfday':'12h', 'day':'1d', 'week':'7d'}

def dump(obj):
   for attr in dir(obj):
       if hasattr( obj, attr ):
           print( "obj.%s = %s" % (attr, getattr(obj, attr)))

if 'datetime' not in data['nlp']['entities'] and 'duration' not in data['nlp']['entities']:
	time = '1h'
elif 'datetime' in data['nlp']['entities'] and 'duration' not in data['nlp']['entities']:
	time = datetime_array[data['nlp']['entities']['datetime'][0]['accuracy']]
# elif 'duration' in data['nlp']['entities']:
print time

address = "http://poe-rates.com/index.php?league=Abyss&item="+item+"&interval="+time

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


# "datetime": [
#         {
#           "formatted": "Thursday, 04 January 2018 at 07:00:00 AM (+0000)",
#           "iso": "2018-01-04T07:00:00+00:00",
#           "accuracy": "halfday",
#           "chronology": "past",
#           "state": "relative",
#           "raw": "this morning",
#           "confidence": 0.97
#         }
#       ]

# "duration": [
#         {
#           "chrono": "06:00:00",
#           "raw": "6 hours",
#           "confidence": 0.59,
#           "hours": 6,
#           "months": 0.00821917808219178,
#           "years": 0.000684844641724794,
#           "days": 0.25,
#           "minutes": 360,
#           "seconds": 21600
#         }
#       ]

