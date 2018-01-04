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

  # Check if 'number' is present on the json
  if 'number' not in data['nlp']['entities']:
    number = 1
  else:
    number = data['nlp']['entities']['number'][0]['scalar']
  print number

  # Call the page to be loaded
  address = "http://poe-rates.com/index.php?league=Abyss&item="+item_addr+"&interval=1h"
  driver = webdriver.PhantomJS()

  # Wait until the page is fully loaded
  waiting_time = 0
  value = -1
  while value == -1 and waiting_time < 7:
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
  if waiting_time > 6:
    content = 'The website take too long to respond, try again later.'
  elif number != 1:
    # item_name = string.replace(item_name, "Orb", "Orbs")
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