#our web app framework!

#you could also generate a skeleton from scratch via
#http://flask-appbuilder.readthedocs.io/en/latest/installation.html

#Generating HTML from within Python is not fun, and actually pretty cumbersome because you have to do the
#HTML escaping on your own to keep the application secure. Because of that Flask configures the Jinja2 template engine 
#for you automatically.
#requests are objects that flask handles (get set post, etc)
from flask import Flask, render_template,request
#for matrix math
import numpy as np
#for regular expressions, saves time dealing with string data
import re

#system level operations (like loading files)
import sys 
#for reading operating system data
import os
#tell our app where our saved model is
from recognize import *
#initalize our flask app
app = Flask(__name__)

@app.route('/')
def index():
	#initModel()
	#render out pre-built HTML file right on the index page
	#return render_template("index.html")
	return "Welcome to home page!"


@app.route('/uploadfile',methods=['GET','POST'])
def uploadfile():
	if request.method == 'POST':
		f = request.files['upload']
		filePath = "./images/test.jpg"
		f.save(filePath)

		f = request.files['sound']
		filePath = "./audio/test.aac"
		f.save(filePath)



		# for filename in os.listdir(filePath):
		# 	if (filename.endswith(".aac")): #or .avi, .mpeg, whatever.
		# 	    os.system("ffmpeg -i {0} audio.wav".format(filename))
		# 	else:
		# 	    continue

		response1 = recognize_face()
		print("Face: ",response1)
		response2 = recognize_audio()
		print("Audio: ",response2)
		return "face= {0},audio={1}".format(response1, response2)

# predict_face():
# 	img = request.get_data()
# 	response = recognize_face()
# 	return response



@app.route('/recognize_audio/',methods=['GET','POST'])
def predict_audio():
	audio = request.get_data()
	response = recognize_audio(audio)
	return response
                
@app.route('/recognize_face/',methods=['GET','POST'])
def predict_face():
	print("here")
	if request.method == 'POST':
		f = request.files['upload']
		filePath = "./images/test.jpg"
		f.save(filePath)

		f = request.files['sound']
		filePath = "./audio/test.aac"
		f.save(filePath)

		for filename in os.listdir(filePath):
			if (filename.endswith(".aac")): #or .avi, .mpeg, whatever.
			    os.system("ffmpeg -i {0} audio.wav".format(filename))
			else:
			    continue

		response1 = recognize_face()
		print(response1)
		response2 = recognize_audio()
		print(response2)
		return "face=%s,audio=%s".format(response1, response2)

# @app.route('/predict/',methods=['GET','POST'])
# def predict():
# 	#whenever the predict method is called, we're going
# 	#to input the user drawn character as an image into the model
# 	#perform inference, and return the classification
# 	#get the raw data format of the image
# 	imgData = request.get_data()
# 	#encode it into a suitable format
# 	convertImage(imgData)
# 	print "debug"
# 	#read the image into memory
# 	x = imread('output.png',mode='L')
# 	#compute a bit-wise inversion so black becomes white and vice versa
# 	x = np.invert(x)
# 	#make it the right size
# 	x = imresize(x,(28,28))
# 	#imshow(x)
# 	#convert to a 4D tensor to feed into our model
# 	x = x.reshape(1,28,28,1)
# 	print "debug2"
# 	#in our computation graph
# 	with graph.as_default():
# 		#perform the prediction
# 		out = model.predict(x)
# 		print(out)
# 		print(np.argmax(out,axis=1))
# 		print "debug3"
# 		#convert the response to a string
# 		response = np.array_str(np.argmax(out,axis=1))
#		return response	
	

if __name__ == "__main__":
	#decide what port to run the app in
	#port = int(os.environ.get('PORT', 5000))
	#run the app locally on the givn port
	#app.run(port=8000)
	app.run(host='0.0.0.0', port=8000)
	#optional if we want to run in debugging mode
	#app.run(debug=True)
