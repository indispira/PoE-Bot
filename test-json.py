from flask import Flask, request, jsonify
import json
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
import re

item = "Chaos%20Orb"
datetime_array = {'hour':'1h', 'halfday':'12h', 'day':'1d', 'week':'7d'}

def dump(obj):
   for attr in dir(obj):
       if hasattr( obj, attr ):
           print( "obj.%s = %s" % (attr, getattr(obj, attr)))

# if 'datetime' not in data['nlp']['entities'] and 'duration' not in data['nlp']['entities']:
# 	time = '1h'
# elif 'datetime' in data['nlp']['entities'] and 'duration' not in data['nlp']['entities']:
# 	time = datetime_array[data['nlp']['entities']['datetime'][0]['accuracy']]
# # elif 'duration' in data['nlp']['entities']:
# print time

address = "http://poe-rates.com/index.php?league=Abyss&item="+item+"&interval=7d"

driver = webdriver.PhantomJS()

waiting_time = 0
value_median = -1
while value_median == -1 and waiting_time < 8:
	waiting_time += 1
	driver.implicitly_wait(1)
	driver.get(address)

	# Catch the value inside the html code
	elems = driver.find_elements_by_class_name('value')
	for e in elems:
		print e.get_attribute('class')
		if e.get_attribute('class') == "value green-text":
			print e.text
			value_median = e.text
			break
	print value_median

# tables = driver.find_elements_by_class_name('for-one-chaos')
table = driver.find_element_by_class_name('currency-table')
print table
tbody = table.find_element_by_tag_name('tbody')
print tbody
trs = tbody.find_elements_by_tag_name('tr')
print trs
for tr in trs:
	tds = tr.find_elements_by_tag_name('td')
	for td in tds:
		print td.text
# for t in tables:
# 	print "FOUND"
# 	print len(t.text)

# value_min = 0
# divs = driver.find_elements_by_tag_name('div')
# for d in divs:
# 	tab = re.findall(r'\nMin [0-9.]*\n', d.text)
# 	for s in tab:
# 		if s[0] == '\n':
# 			value_min = float(s[5:len(s) - 1])
# 			break
# 	if value_min != 0: break
# print value_min

# dump(driver)
# print "Graph test"
# Catch the first and last value of the median price graph
# first_value_median = 0
# last_value_median = 0
# paths = driver.find_elements_by_tag_name('path')
# for path in paths:
# 	if path.get_attribute('stroke') == '#00dddd' and path.get_attribute('d')[-9:] == 'M0,0 L0,0':
# 		coords = path.get_attribute('d')
# 		# print coords
# 		first_value_median = float(coords[coords.find(',') + 1:coords.find(' ')])
# 		coords = coords[:len(coords) - 10]
# 		last_value_median = float(coords[coords.rfind(',') + 1:])
# 		print first_value_median, last_value_median
# 		break

# Catch the first and last value of the min price graph
# first_value_min = 0
# last_value_min = 0
# for path in paths:
# 	if path.get_attribute('stroke') == '#00dd00' and path.get_attribute('d')[-9:] == 'M0,0 L0,0':
# 		coords = path.get_attribute('d')
# 		# print coords
# 		first_value_min = float(coords[coords.find(',') + 1:coords.find(' ')])
# 		coords = coords[:len(coords) - 10]
# 		last_value_min = float(coords[coords.rfind(',') + 1:])
# 		print first_value_min, last_value_min
# 		break

# print "Calcul en cours"
# scale = (last_value_min - last_value_median) / (float(value_median) - float(value_min))
# value_median_at_date = float(value_median) + ((last_value_median - first_value_median) / scale)
# print int(value_median_at_date)

	# print path.get_attribute('stroke')
# driver.set_window_size(1040, 720)
# divs = driver.find_elements_by_tag_name('svg')
# for d in divs:
# 	print d.get_attribute('style')
# 	print d.location
	# if d.get_attribute('id') == 'evolution-ExaltedOrb':
	# 	graphic = d
	# 	print "FOUND"
	# 	break
# actions = ActionChains(driver)
# # actions.move_to_element_with_offset(graphic, 200, 200).perform()
# print driver.get_window_position()
# print driver.get_window_size()
# actions.move_by_offset(10, 10)
# hover = ActionsChains(driver).moveToElement(driver.find_element_by_class_name('amcharts-chart-div'))
# actions.perform()
# graph = driver.find_elements_by_class_name('graph')
# for g in graph:
# 	print "A"
# temp = driver.find_elements_by_tag_name('div')
# for x in temp:
# 	print x.get_attribute('id')
