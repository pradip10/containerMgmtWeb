from flask import render_template, request
from app import app
import os
import requests
import json
from pprint import pprint

@app.route('/')
@app.route('/index')
@app.route('/images')
def images():
  diDump=d=requests.get("http://localhost:5555/images/json")
  diJSON=json.loads(diDump.text)
  return render_template('images.html', result = diJSON)

@app.route('/allcontainers')
def allcontainers():
  dcaDump=requests.get("http://localhost:5555/containers/json?all=true")
  dcaJSON=json.loads(dcaDump.text)
  return render_template('allcontainers.html', result = dcaJSON)

@app.route('/containers')
def containers():
  dcDump=requests.get("http://localhost:5555/containers/json")
  dcJSON=json.loads(dcDump.text)
  return render_template('containers.html', result = dcJSON)  

@app.route('/create', methods=['GET', 'POST'])
def create_run():
    if request.method == 'POST':  
        image = request.form.get('image')
        createURL = 'http://localhost:5555/containers/create'
        myobj = {'Hostname': 'test',
         'Image': image}
        x = requests.post(createURL, json = myobj)
        xJSON=json.loads(x.text)
        startURL = "http://localhost:5555/containers/"+xJSON['Id']+"/start"
        y = requests.post(startURL)
        return render_template('run.html', containerID = xJSON['Id'], returnCode = y.status_code)

    return render_template('create.html')

@app.route('/stop', methods=['GET', 'POST'])
def stop():
    if request.method == 'POST':
        stopID = request.form.get('image')
        stopURL = "http://localhost:5555/containers/"+stopID+"/stop"
        x = requests.post(stopURL)
        return render_template('stopped.html', containerID = stopID, returnCode = x.status_code)

    return render_template('destroy.html')

if __name__ == "__main__":
    myIP=os.popen("ifconfig | grep -A 8 eth0 | grep \"inet \" | awk '{print $2}'").read()
    print(myIP)
    app.debug = True
    app.run(host = myIP)
