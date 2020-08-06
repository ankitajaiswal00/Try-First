import os
from flask_caching import Cache
from app import app
from app2 import app2
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
from script import predict
import time
import glob
from evaluate import execute
from pose_parser import pose_parse
from wsize import women_size_predict
from msize import men_size_predict

#================ALLOWED FORMATS FOR IMAGE UPLOADS===========

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
cache = Cache()

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ============ REDIRECT HOME PAGE==========================
	
@app.route('/')
def index():
	return render_template('index.html')
	
# ============ REDIRECT ABOUT PAGE=========================

@app.route('/about/')
def about():
	return render_template('about.html')	

# ============ REDIRECT SERVICE: TRY-ON====================

@app.route('/services_tryon/')
def services_tryon():
	return render_template('services_tryon.html')

# ============ REDIRECT BLOG===============================
	
@app.route('/blog/')
def blog():
	return render_template('blog.html')

# ============ REDIRECT CONTACT===========================

@app.route('/contact/')
def contact():
	return render_template('contact.html')

# ==========================================================================================================================================================================
# ============================================================================ REDIRECT SERVICE: SIZE PREDICTOR=============================================================

@app.route('/services_sizep/')
def services_sizep():
	GO = "False"
	return render_template('services_sizep.html')

# ============ FUNCTION TO INPUT & PROCESS SIZE PREDICTION ===========

@app.route("/process_size", methods=['GET','POST'])
def your_size():
	if request.method=="POST":
		if 'file' not in request.files:
			flash('No file part')
			return redirect({{url_for('services_sizep')}})
		
		file = request.files['file']
		gender = request.form.get('gender')
		height = request.form['height']
		unit = request.form.get('unit')
		Go = "False"
		
		if file.filename == '':
			flash('No image selected for uploading')
			return redirect(request.url)
		
		if file and allowed_file(file.filename) and gender and height and unit:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER2'], filename))
			i_path = 'static/size/'
			file_path = os.path.join(i_path,filename)
			if gender == 'Female':
				size = women_size_predict(file_path, height, unit)
			else:
				size = men_size_predict(file_path, height, unit)
			return render_template('services_sizep.html', size=size)
	
		else:
			flash('Allowed image types are -> png, jpg, jpeg, gif')
			return redirect(url_for('services_sizep'))
		# size=None
	Go = "True"	
	return redirect(url_for('services_sizep'))

# =============fUNCTION TO DISPLAY SIZE=====================

@app.route('/display_size/<size>')
def display_size(size):
	if Go == "True":
		GO = "True"
	# time.sleep(5)
	return str(size)

# ================================================================================================================================================================
# ======================================================1. REDIRECT CASUALS ======================================================================================
	
@app.route('/casuals/')
def casuals():
	text = "none"
	fish = glob.glob('./output/second/TOM/val/*')
	for f in fish:
		os.remove(f)
	cloth  = ['000308'  , '000011', '000254','017975' , '000347','017960' ,'017969' ,'017970','018318','018690' ,'019048', '004061' , '013789' , '013410', '013547' ]
	for i in range(len(cloth)):
		cloth[i] = (str(cloth[i])+"_1.jpg")
	return render_template('casuals.html', casuals = cloth, text=text)

# ============1. FUNCTION TO DISPALY CASUALS =================

@app.route('/static/Database/val/cloth/<casuals>')
def display_casuals(casuals):
	# time.wait(10)
	return send_from_directory(app2.config['OUTPUT_FOLDER2'], casuals)
	
# ============1. FUNCTION TO INPUT AND PROCESS TRY ON ==========

@app.route('/', methods=['POST'])
def upload_image():
	cache.init_app(app2)
	with app2.app_context():
			cache.clear()
	cloth  = ['000308'  , '000011', '000254','017975' , '000347','017960' , '013789' , '013410', '013547' ]
	for i in range(len(cloth)):
		cloth[i] = (str(cloth[i])+"_1.jpg")

	if request.method=="POST":
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		
		text = request.form['input_text']
		file = request.files['file']
		
		if file.filename == '':
			flash('No image selected for uploading')
			return redirect(request.url)
		
		if file and allowed_file(file.filename) and text:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))
			i_path = 'static/Database/val/person/'
			input_img = text+'.jpg'
			os.rename(i_path+filename , i_path+input_img)
			filename = text+'.jpg'
			o_path = './output/second/TOM/val'
			# fish = glob.glob('./output/second/TOM/val/*')
			fish = glob.glob('./static/output_f/*')
			for f in fish:
				os.remove(f)
			time.sleep(10)
			#
			#
			#
			# 
			pose_parse(text)
			valpair_file = 'static/Database/val_pairs.txt'
			
			for i in range(len(cloth)):
				with open(valpair_file , "w") as f:
						f.write(text+'.jpg '+ cloth[i] )
						f.close()
						predict()
						im = Image.open(os.path.join(o_path,cloth[i]))
						width, height = im.size
						left = width / 3
						top = 2 * height / 3
						right = 2 * width / 3
						bottom = height
						im = im.crop((left, top, right, bottom)) 
						newsize = (200, 270) 
						im = im.resize(newsize)
						im.save(os.path.join(app2.config['OUTPUT_FOLDER3'],cloth[i]))
			#
			#
			#
			return render_template('casuals.html', casuals=cloth, text= text)
		else:
			flash('Allowed image types are -> png, jpg, jpeg, gif')
			return redirect(request.url)
	return render_template('casuals.html')

# =================1. OUTPUT CASUALS TRYON======================

@app.route('/output/second/TOM/val/<casuals>')
def display_output1(casuals):
	return send_from_directory(app2.config['OUTPUT_FOLDER3'], casuals)

# =============================================================================================================================================================================
# =================================================================================2. REDIRECT SPORTS =========================================================================
	
@app.route('/sports/')
def sports():
	text = "none"
	fish = glob.glob('./output/second/TOM/val/*')
	for f in fish:
		os.remove(f)
	sport_cloth  = ['014142', '014143', '014147', '004710', '018327','010115' ,'014158', '014160', '014146','017121', '017346', '017956', '017975', '017977','002385','000744','017960']
	for i in range(len(sport_cloth)):
		sport_cloth[i] = (str(sport_cloth[i])+"_1.jpg")
	return render_template('sports.html', sports = sport_cloth, text=text)

# ============2. FUNCTION TO DISPALY SPORTS =================

@app.route('/static/Database/val/cloth/<sports>')
def display_sports(sports):
	# time.wait(10)
	return send_from_directory(app2.config['OUTPUT_FOLDER2'], sports)

# ===========2.FUNCTION TO INPUT AND PROCESS TRY ON ==========

@app.route('/sports_form', methods=['POST'])
def upload_image2():
	cache.init_app(app2)
	with app2.app_context():
			cache.clear()
	sport_cloth  = ['014142', '014143', '014147', '004710', '018327','010115' ,'014158', '014160', '014146','017121', '017346', '017956', '017975', '017977','002385','000744','017960']
	for i in range(len(sport_cloth)):
		sport_cloth[i] = (str(sport_cloth[i])+"_1.jpg")

	if request.method=="POST":
		# if 'file' not in request.files:
		# 	flash('No file part')
		# 	return redirect(request.url)
		
		text = request.form['input_text']
		file = request.files['file']
		
		if file.filename == '':
			flash('No image selected for uploading')
			return redirect(request.url)
		
		if file and allowed_file(file.filename) and text:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))
			i_path = 'static/Database/val/person/'
			input_img = text+'.jpg'
			os.rename(i_path+filename , i_path+input_img)
			filename = text+'.jpg'
			o_path = './output/second/TOM/val'
			# fish = glob.glob('./output/second/TOM/val/*')
			fish = glob.glob('./static/output_f/*')
			for f in fish:
				os.remove(f)
			time.sleep(10)
			#
			#
			#
			# 
			pose_parse(text)
			valpair_file = 'static/Database/val_pairs.txt'
			
			for i in range(len(sport_cloth)):
				with open(valpair_file , "w") as f:
						f.write(text+'.jpg '+ sport_cloth[i] )
						f.close()
						predict()
						im = Image.open(os.path.join(o_path,sport_cloth[i]))
						width, height = im.size
						left = width / 3
						top = 2 * height / 3
						right = 2 * width / 3
						bottom = height
						im = im.crop((left, top, right, bottom)) 
						newsize = (200, 270) 
						im = im.resize(newsize)
						im.save(os.path.join(app2.config['OUTPUT_FOLDER3'],sport_cloth[i]))
			#
			#
			#
			return render_template('sports.html', sports=sport_cloth, text= text)
		else:
			flash('Allowed image types are -> png, jpg, jpeg, gif')
			return redirect(request.url)
	return render_template('sports.html')

# =================2. OUTPUT SPORTS TRYON======================

@app.route('/output/second/TOM/val/<sports>')
def display_output2(sports):
	return send_from_directory(app2.config['OUTPUT_FOLDER3'], sports)


# =======================================================================================================================================================================
# ===========================================================3. REDIRECT BRANDS =========================================================================================
	
@app.route('/brands/')
def brands():
	text = "none"
	fish = glob.glob('./output/second/TOM/val/*')
	for f in fish:
		os.remove(f)
	brand_cloth  = ['004710','018327' , '001502', '010115' ,'017975','017956' ,'014406', '017976','014158' , '017121','014160' , '017960' , '017978' , '014379','017979']
	for i in range(len(brand_cloth)):
		brand_cloth[i] = (str(brand_cloth[i])+"_1.jpg")
	return render_template('brands.html', brands = brand_cloth, text=text)

# ============3. FUNCTION TO DISPALY BRANDS =================

@app.route('/static/Database/val/cloth/<brands>')
def display_brands(brands):
	# time.wait(10)
	return send_from_directory(app2.config['OUTPUT_FOLDER2'], brands)

# ===========3.FUNCTION TO INPUT AND PROCESS TRY ON ==========

@app.route('/brands_form', methods=['POST'])
def upload_image3():
	cache.init_app(app2)
	with app2.app_context():
			cache.clear()
	brand_cloth  = ['004710','018327' , '001502', '010115' ,'017975','017956' ,'014406', '017976','014158' , '017121','014160' , '017960' , '017978' , '014379','017979']
	for i in range(len(brand_cloth)):
		brand_cloth[i] = (str(brand_cloth[i])+"_1.jpg")

	if request.method=="POST":
		# if 'file' not in request.files:
		# 	flash('No file part')
		# 	return redirect(request.url)
		
		text = request.form['input_text']
		file = request.files['file']
		
		if file.filename == '':
			flash('No image selected for uploading')
			return redirect(request.url)
		
		if file and allowed_file(file.filename) and text:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))
			i_path = 'static/Database/val/person/'
			input_img = text+'.jpg'
			os.rename(i_path+filename , i_path+input_img)
			filename = text+'.jpg'
			o_path = './output/second/TOM/val'
			# fish = glob.glob('./output/second/TOM/val/*')
			fish = glob.glob('./static/output_f/*')
			for f in fish:
				os.remove(f)
			time.sleep(10)
			#
			#
			#
			# 
			pose_parse(text)
			valpair_file = 'static/Database/val_pairs.txt'
			
			for i in range(len(brand_cloth)):
				with open(valpair_file , "w") as f:
						f.write(text+'.jpg '+ brand_cloth[i] )
						f.close()
						predict()
						im = Image.open(os.path.join(o_path,brand_cloth[i]))
						width, height = im.size
						left = width / 3
						top = 2 * height / 3
						right = 2 * width / 3
						bottom = height
						im = im.crop((left, top, right, bottom)) 
						newsize = (200, 270) 
						im = im.resize(newsize)
						im.save(os.path.join(app2.config['OUTPUT_FOLDER3'],brand_cloth[i]))
			#
			#
			#
			return render_template('brands.html', brands=brand_cloth, text= text)
		else:
			flash('Allowed image types are -> png, jpg, jpeg, gif')
			return redirect(request.url)
	return render_template('brands.html')

# =================3. OUTPUT BRANDS TRYON======================

@app.route('/output/second/TOM/val/<brands>')
def display_output3(brands):
	return send_from_directory(app2.config['OUTPUT_FOLDER3'], brands)

# =========================================================================================================================================================================
# =====================================================================4. REDIRECT PARTY ==================================================================================
	
@app.route('/party/')
def party():
	cache.init_app(app2)
	with app2.app_context():
			cache.clear()
	text = "none"
	fish = glob.glob('./output/second/TOM/val/*')
	for f in fish:
		os.remove(f)
	party_cloth  = ['000003' , '000108', '001719' ,'000178', '000182' , '001428' , '004710' , '017374','002061', '017642', '017377', '017963', '019067','019564', '017643']
	for i in range(len(party_cloth)):
		party_cloth[i] = (str(party_cloth[i])+"_1.jpg")
	return render_template('party_wear.html', party = party_cloth, text=text)

# ============4. FUNCTION TO DISPALY PARTY =================

@app.route('/static/Database/val/cloth/<party>')
def display_party(party):
	time.wait(10)
	return send_from_directory(app2.config['OUTPUT_FOLDER2'], party)

 # ===========4. FUNCTION TO INPUT AND PROCESS TRY ON ==========

@app.route('/party_form', methods=['POST'])
def upload_image4():
	cache.init_app(app2)
	with app2.app_context():
			cache.clear()
	party_cloth = ['000003' , '000108', '001719' ,'017376' ,'000178', '000182' , '001428' , '004710' , '008632' , '017374','002061', '017642', '017377', '017963', '018348', '019067','019564', '017643']
	for i in range(len(party_cloth)):
		party_cloth[i] = (str(party_cloth[i])+"_1.jpg")

	if request.method=="POST":
		# if 'file' not in request.files:
		# 	flash('No file part')
		# 	return redirect(request.url)
		
		text = request.form['input_text']
		file = request.files['file']
		
		if file.filename == '':
			flash('No image selected for uploading')
			return redirect(request.url)
		
		if file and allowed_file(file.filename) and text:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))
			i_path = 'static/Database/val/person/'
			input_img = text+'.jpg'
			os.rename(i_path+filename , i_path+input_img)
			filename = text+'.jpg'
			o_path = './output/second/TOM/val'
			# fish = glob.glob('./output/second/TOM/val/*')
			fish = glob.glob('./static/output_f/*')
			for f in fish:
				os.remove(f)
			time.sleep(10)			#
			#
			#
			# 
			pose_parse(text)
			valpair_file = 'static/Database/val_pairs.txt'
			
			for i in range(len(party_cloth)):
				with open(valpair_file , "w") as f:
						f.write(text+'.jpg '+ party_cloth[i] )
						f.close()
						predict()
						im = Image.open(os.path.join(o_path,party_cloth[i]))
						width, height = im.size
						left = width / 3
						top = 2 * height / 3
						right = 2 * width / 3
						bottom = height
						im = im.crop((left, top, right, bottom)) 
						newsize = (200, 270) 
						im = im.resize(newsize)
						im.save(os.path.join(app2.config['OUTPUT_FOLDER3'],party_cloth[i]))
			#
			#
			#
			return render_template('party_wear.html', party=party_cloth, text= text)
		else:
			flash('Allowed image types are -> png, jpg, jpeg, gif')
			return redirect(request.url)
	return render_template('party_wear.html')

# ================4. OUTPUT PARTY TRYON======================

@app.route('/output/second/TOM/val/<party>')
def display_output4(party):
	return send_from_directory(app2.config['OUTPUT_FOLDER3'], party)

# ================ FLASK APP RUN & DEBUG=======================================================================================================

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)

