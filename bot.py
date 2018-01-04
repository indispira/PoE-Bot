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

  # FETCH THE ITEM NAME
  item_name = data['conversation']['memory']['item']['raw'].title()
  item_addr = string.replace(item_name, " ", "%20")
  print item_name, item_addr

  # CALL THE PAGE TO BE LOADED
  address = "http://poe-rates.com/index.php?league=Abyss&item="+item_addr+"&interval=1h"
  driver = webdriver.PhantomJS()

  # WAIT UNTIL THE PAGE FULLY LOADED
  value = -1
  while value == -1:
    driver.implicitly_wait(1)
    driver.get(address)

    # CATCH THE RIGHT VALUE
    elems = driver.find_elements_by_class_name('value')
    for e in elems:
      print e.get_attribute('class')
      if e.get_attribute('class') == "value green-text":
        print e.text
        value = e.text
        break
    print value

  # RETURN MESSAGE TO THE BOT BUILDER
  return jsonify( 
    status=200, 
    replies=[{ 
      'type': 'text',
      'content': 'The %s cost %s chaos orbs at the moment.' % (item_name, value),
    }]
  ) 
 
@app.route('/errors', methods=['POST']) 
def errors(): 
  print(json.loads(request.get_data())) 
  return jsonify(status=200) 
 
app.run(port=int(port))