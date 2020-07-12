import os
from app import app
from app2 import app2
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
from script import predict
import time

from evaluate import execute
from pose_parser import pose_parse

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def index():
	return render_template('index.html')
	
@app.route('/about/')
def about():
	return render_template('about.html')	
	
@app.route('/services/')
def services():
	return render_template('services.html')
	
@app.route('/blog/')
def blog():
	return render_template('blog.html')
	
@app.route('/portfoliox/')
def portfoliox():
	return render_template('portfoliox.html')	
	
@app.route('/portfolio/')
def portfolio():
	return render_template('portfolio.html')
	
@app.route('/testimonials/')
def testimonials():
	return render_template('testimonials.html')	
	
@app.route('/pricing/')
def pricing():
	return render_template('pricing.html')
	
@app.route('/contact/')
def contact():
	return render_template('contact.html')

@app.route('/', methods=['POST'])
def upload_image():
	selected = '001719'
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	text = request.form['input_text']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename) and text:
		filename = secure_filename(file.filename)
		out=str(selected)+ '_1.jpg'
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		flash('upload_image filename: ' + filename)
		flash('Image sucoaded and displayed for : '+ text)
		#
		#
		#
		f_text = str(text) + "_0"
		pose_parse(f_text)
		valpair_file = 'static/Database/val_pairs.txt'
		with open(valpair_file , "w") as f:    
    			f.write(text+'_0.jpg '+ selected +'_1.jpg')
    			f.close()
    			predict()
    			path = './output/second/TOM/val'
    			im = Image.open(os.path.join(path,out))
    			width, height = im.size
    			left = width / 3
    			top = 2 * height / 3
    			right = 2 * width / 3
    			bottom = height
    			im = im.crop((left, top, right, bottom)) 
    			newsize = (200, 270) 
    			im = im.resize(newsize) 
    			im.save(os.path.join(app2.config['OUTPUT_FOLDER'], out))
		#
		#
		#
		return render_template('portfoliox.html', filename=filename, out=out)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)
	

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='Database/val/person/'+filename), code=301)


@app.route('/output/second/val/<out>')
def display_output(out):
	#print(out)
	return send_from_directory(app2.config['OUTPUT_FOLDER'], out)	
	
#@app.route('/output/second/val/<out>')
#def display_crop_output(im):
#    	return send_from_directory(app2.config['OUTPUT_FOLDER'], im)
    	

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
