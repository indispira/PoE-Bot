from flask import Flask, request, jsonify 
import json
import requests
from selenium import webdriver

app = Flask(__name__) 
port = '5000'

@app.route('/', methods=['POST'])
def index(): 
  data = json.loads(request.get_data())

  # FETCH THE ITEM NAME
  item_name = data['conversation']['memory']['item']['raw']

  # CATCH THE PAGE LOADED
  address = "http://poe-rates.com/index.php?league=Abyss&item="+item_name+"&interval=1h"
  driver = webdriver.PhantomJS()
  driver.implicitly_wait(1)
  driver.get(address)

  # CATCH THE RIGHT VALUE
  value = 0
  elems = driver.find_elements_by_class_name('value')
  for e in elems:
    if e.get_attribute('class') == "value green-text":
      print e.text
      value = e.text
      break

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