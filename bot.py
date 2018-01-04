from flask import Flask, request, jsonify 
import json
import requests
from selenium import webdriver
import string
import re

app = Flask(__name__) 
port = '5000'

@app.route('/', methods=['POST'])
def index(): 
  data = json.loads(request.get_data())

  # Catch the item name and configure for the web address page
  item_name = data['conversation']['memory']['item']['raw'].title()
  item_addr = string.replace(item_name, " ", "%20")
  item_addr = string.replace(item_addr, "Orbs", "Orb")
  print "Item name:", item_name, " | Item address:", item_addr

  # Check if 'number' is present in the json
  if 'number' not in data['nlp']['entities']:
    number = 1
  else:
    number = data['nlp']['entities']['number'][0]['scalar']
  print "Number:", number

  # Check if 'duration' or 'datetime' are present in the json
  time_mode = 0
  datetime_array = {'hour':'1h', 'halfday':'12h', 'day':'1d', 'week':'7d'}
  date_ago_array = {'1h':'1 hour', '6h':'6 hours', '12h':'12 hours', '1d':'a day', '7d':'a week'}
  if 'datetime' not in data['nlp']['entities'] and 'duration' not in data['nlp']['entities']:
    time = '1h'
  elif 'datetime' in data['nlp']['entities'] and 'duration' not in data['nlp']['entities']:
    time = datetime_array[data['nlp']['entities']['datetime'][0]['accuracy']]
    time_mode = 1
  elif 'duration' in data['nlp']['entities']:
    if data['nlp']['entities']['duration'][0]['hours'] <= 1: time = '1h'
    elif data['nlp']['entities']['duration'][0]['hours'] <= 6: time = '6h'
    elif data['nlp']['entities']['duration'][0]['hours'] <= 12: time = '12h'
    elif data['nlp']['entities']['duration'][0]['hours'] <= 24: time = '1d'
    else: time = '7d'
    time_mode = 2
  print "Time bracket:", time

  # Call the page to be loaded
  address = "http://poe-rates.com/index.php?league=Abyss&item="+item_addr+"&interval="+time
  driver = webdriver.PhantomJS()
  print "Address:", address

  # Wait until the page is fully loaded
  waiting_time = 0
  value_median = -1
  while value_median == -1 and waiting_time < 8:
    waiting_time += 1
    driver.implicitly_wait(1)
    driver.get(address)

    # Catch the median value inside the html code
    elems = driver.find_elements_by_class_name('value')
    for e in elems:
      print e.get_attribute('class')
      if e.get_attribute('class') == "value green-text":
        print e.text
        value_median = e.text
        break
    print "Median value:", value_median

  if time_mode != 0:
    # Catch the min value inside the html code
    value_min = 0
    divs = driver.find_elements_by_tag_name('div')
    for d in divs:
      tab = re.findall(r'\nMin [0-9.]*\n', d.text)
      for s in tab:
        if s[0] == '\n':
          value_min = float(s[5:len(s) - 1])
          break
      if value_min != 0:
        break
    print "Min value:", value_min

    # Catch the first and last value of the median price graph
    first_value_median = 0
    last_value_median = 0
    paths = driver.find_elements_by_tag_name('path')
    for path in paths:
      if path.get_attribute('stroke') == '#00dddd' and path.get_attribute('d')[-9:] == 'M0,0 L0,0':
        coords = path.get_attribute('d')
        first_value_median = float(coords[coords.find(',') + 1:coords.find(' ')])
        coords = coords[:len(coords) - 10]
        last_value_median = float(coords[coords.rfind(',') + 1:])
        print "First coord median:", first_value_median, "Last coord median", last_value_median
        break

    # Catch the first and last value of the min price graph
    first_value_min = 0
    last_value_min = 0
    for path in paths:
      if path.get_attribute('stroke') == '#00dd00' and path.get_attribute('d')[-9:] == 'M0,0 L0,0':
        coords = path.get_attribute('d')
        first_value_min = float(coords[coords.find(',') + 1:coords.find(' ')])
        coords = coords[:len(coords) - 10]
        last_value_min = float(coords[coords.rfind(',') + 1:])
        print "First coord min:", first_value_min, "Last coord min:", last_value_min
        break

    # Calculate the median value at the datetime or the start of duration
    scale = (last_value_min - last_value_median) / (float(value_median) - float(value_min))
    value_median_at_date = int(float(value_median) + ((last_value_median - first_value_median) / scale))
    print "First median value of graph:", value_median_at_date

  # Configure the content of the message
  content = 'The '
  if number != 1:
    content += '%d ' % number
  if time_mode == 0:
    content += '%s cost %d Chaos Orbs at the moment.' % (item_name, int(value_median) * int(number))
  elif time_mode == 1:
    content += '%s cost %d Chaos Orbs %s ago.' % (item_name, value_median_at_date * int(number), date_ago_array[time])
  else:
    content += 'IN PROGRESS...'
  if waiting_time > 7 and value_median == -1:
    content = 'The website take too long to respond, try again later.'

  # Return the message to Bot Builder
  return jsonify( 
    status=200, 
    replies=[{ 
      'type': 'text',
      'content': content,
    }]
  ) 
 
@app.route('/errors', methods=['POST']) 
def errors(): 
  print(json.loads(request.get_data())) 
  return jsonify(status=200) 
 
app.run(port=int(port))
