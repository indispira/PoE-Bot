from flask import Flask, request, jsonify 
import json
import requests
from selenium import webdriver
import string

app = Flask(__name__) 
port = '5000'

@app.route('/', methods=['POST'])
def index(): 
  data = json.loads(request.get_data())

  # Catch the item name and configure for the web address page
  item_name = data['conversation']['memory']['item']['raw'].title()
  item_addr = string.replace(item_name, " ", "%20")
  item_addr = string.replace(item_addr, "Orbs", "Orb")
  print item_name, item_addr

  # Check if 'number' is present in the json
  if 'number' not in data['nlp']['entities']:
    number = 1
  else:
    number = data['nlp']['entities']['number'][0]['scalar']
  print number

  # Check if 'duration' or 'datetime' are present in the json
  time_mode = 0
  datetime_array = {'hour':'1h', 'halfday':'12h', 'day':'1d', 'week':'7d'}
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
  print time

  # Call the page to be loaded
  address = "http://poe-rates.com/index.php?league=Abyss&item="+item_addr+"&interval="+time
  driver = webdriver.PhantomJS()
  print address

  # Wait until the page is fully loaded
  waiting_time = 0
  value = -1
  while value == -1 and waiting_time < 8:
    waiting_time += 1
    driver.implicitly_wait(1)
    driver.get(address)

    # Catch the value inside the html code
    elems = driver.find_elements_by_class_name('value')
    for e in elems:
      print e.get_attribute('class')
      if e.get_attribute('class') == "value green-text":
        print e.text
        value = e.text
        break
    print value

  # Configure the content of the message
  if waiting_time > 7 and value == -1:
    content = 'The website take too long to respond, try again later.'
  elif number != 1:
    content = 'The %d %s cost %d chaos orbs at the moment.' % (number, item_name, int(value) * int(number))
  else:
    content = 'The %s cost %d chaos orbs at the moment.' % (item_name, int(value) * int(number))

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
