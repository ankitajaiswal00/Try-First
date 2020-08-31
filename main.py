import os
import urllib.request
import time
import glob
import cv2
from app import app
from app2 import app2
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from flask_caching import Cache
from PIL import Image
from script import predict
from evaluate import execute
from pose_parser import pose_parse
from wsize import women_size_predict
from wsize1 import women_size_predict1
from msize import men_size_predict
import mask_the_face
# from mask_the_face import execu0te_mask_face

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
	fish = glob.glob('./static/outputs/output_f/*')
	for f in fish:
		os.remove(f)
	cloth = ['Casual-Yellow', 'Casual-Pink', 'Casual-Violet', 'Casual-White', 'Dark_ORANGE', 'Flowers-White', 'Grey_North' , 'Multicolo-White', 'Pine-Grey',  'Sky_Blue', 'TheNORTHface', 'Yellow62']
	for i in range(len(cloth)):
		cloth[i] = (str(cloth[i])+".jpg")
	return render_template('casuals.html', casuals = cloth, text=text)

# ============1. FUNCTION TO DISPALY CASUALS =================

@app.route('/static/Database/val/cloth/<casuals>')
def display_casuals(casuals):
	# time.wait(10)
	return send_from_directory(app2.config['OUTPUT_FOLDER2'], casuals)
	
# ============1. FUNCTION TO INPUT AND PROCESS TRY ON ==========

@app.route('/casual_form', methods=['POST'])
def upload_image():
	cache.init_app(app2)
	with app2.app_context():
			cache.clear()
	fish = glob.glob('./static/Database/val/person/*')
	for f in fish:
		os.remove(f)
	fish = glob.glob('./static/size/*')
	for f in fish:
		os.remove(f)		
	cloth = ['Casual-Yellow', 'Casual-Pink', 'Casual-Violet', 'Casual-White', 'Dark_ORANGE', 'Flowers-White', 'Grey_North' , 'Light-Pink', 'Multicolo-White', 'Sky_Blue', 'TheNORTHface', 'Yellow62']	
	for i in range(len(cloth)):
		cloth[i] = (str(cloth[i])+".jpg")

	if request.method=="POST":
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		
		text = "casualss"
		file = request.files['file']
		height = request.form['height']
		unit = request.form.get('unit')		

		if file.filename == '':
			flash('No image selected for uploading')
			return redirect(request.url)
		
		if file and allowed_file(file.filename) and text and height and unit:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER2'], filename))
			i_path = 'static/size/'
			file_path = os.path.join(i_path,filename)
			size, file = women_size_predict1(file_path, height, unit) 
			file = Image.fromarray(file, 'RGB')
			#
			file.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))
			i_path = 'static/Database/val/person/'
			input_img = text+'.jpg'
			os.rename(i_path+filename , i_path+input_img)
			filename = text+'.jpg'
			o_path = './output/second/TOM/val'
			# fish = glob.glob('./output/second/TOM/val/*')
			fish = glob.glob('./static/outputs/output_f/*')
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
			return render_template('casuals.html', casuals=cloth, text= text, size = size)
		else:
			flash('Allowed image types are -> png, jpg, jpeg, gif')
			return redirect(request.url)
	return render_template('casuals.html')

# =================1. OUTPUT CASUALS TRYON======================

@app.route('/static/outputs/output_f/<casuals>')
def display_output1(casuals):
	return send_from_directory(app2.config['OUTPUT_FOLDER3'], casuals)

# =============================================================================================================================================================================
# =================================================================================2. REDIRECT SPORTS =========================================================================
	
@app.route('/sports/')
def sports():
	cache.init_app(app2)
	with app2.app_context():
			cache.clear()
	text = "none"
	fish = glob.glob('./output/second/TOM/val/*')
	for f in fish:
		os.remove(f)
	fish = glob.glob('./static/outputs/output_f/*')
	for f in fish:
		os.remove(f)		
	sport_cloth  = ['ADIDAS-BW', 'ADIDAS_Black', 'FILA_grey', 'FILA-Pink', 'IVY-Black',  'NIKE-grey' ]
	for i in range(len(sport_cloth)):
		sport_cloth[i] = (str(sport_cloth[i])+".jpg")
	return render_template('sports.html', sports = sport_cloth, text=text)

# ============2. FUNCTION TO DISPALY SPORTS =================

@app.route('/static/Database/val/cloth/<sports>')
def display_sports(sports):
	return send_from_directory(app2.config['OUTPUT_FOLDER2'], sports)

# ===========2.FUNCTION TO INPUT AND PROCESS TRY ON ==========

@app.route('/sports_form', methods=['POST'])
def upload_image2():
	cache.init_app(app2)
	with app2.app_context():
			cache.clear()
	fish = glob.glob('./static/Database/val/person/*')
	for f in fish:
		os.remove(f)
	fish = glob.glob('./static/size/*')
	for f in fish:
		os.remove(f)
	sport_cloth  = ['ADIDAS-BW', 'ADIDAS_Black', 'FILA_grey', 'FILA-Pink', 'IVY-Black', 'NIKE-grey' ]
	for i in range(len(sport_cloth)):
		sport_cloth[i] = (str(sport_cloth[i])+".jpg")

	if request.method=="POST":
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		
		text = "sportss"
		file = request.files['file']
		height = request.form['height']
		unit = request.form.get('unit')
		Go = "False"

		if file.filename == '':
			flash('No image uploaded for size prediction.')
			return redirect(request.url)
					
		if file and allowed_file(file.filename) and height and unit:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER2'], filename))
			i_path = 'static/size/'
			file_path = os.path.join(i_path,filename)
			size, file = women_size_predict1(file_path, height, unit) 
			file = Image.fromarray(file, 'RGB')
			#			
			file.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))
			i_path = 'static/Database/val/person/'
			input_img = text+'.jpg'
			os.rename(i_path+filename , i_path+input_img)
			filename = text+'.jpg'
			o_path = './output/second/TOM/val'
			# fish = glob.glob('./output/second/TOM/val/*')
			fish = glob.glob('./static/outputs/output_f/*')
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
			return render_template('sports.html', sports=sport_cloth, text= text, size=size)
		else:
			flash('Allowed image types are -> png, jpg, jpeg, gif')
			return redirect(request.url)
	return render_template('sports.html')

# =================2. OUTPUT SPORTS TRYON======================

@app.route('/static/outputs/output_f/<sports>')
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
	fish = glob.glob('./static/outputs/output_f/*')
	for f in fish:
		os.remove(f)		
	brand_cloth  = ['Pink-Flayrd', 'Blue-flayrd', 'Flayerd-Yellow', 'Bluish-Flayrd','NIKE-black', 'RED-Flayrd']#'
	for i in range(len(brand_cloth)):
		brand_cloth[i] = (str(brand_cloth[i])+".jpg")
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
	fish = glob.glob('./static/Database/val/person/*')
	for f in fish:
		os.remove(f)
	fish = glob.glob('./static/size/*')
	for f in fish:
		os.remove(f)		
	brand_cloth  = ['Pink-Flayrd', 'Blue-flayrd', 'Flayerd-Yellow', 'Bluish-Flayrd','NIKE-black', 'RED-Flayrd']#'
	for i in range(len(brand_cloth)):
		brand_cloth[i] = (str(brand_cloth[i])+".jpg")

	if request.method=="POST":
		
		text   = "brandss"
		file   = request.files['file']
		height = request.form['height']
		unit   = request.form.get('unit')
		
		if file.filename == '':
			flash('No image selected for uploading')
			return redirect(request.url)
		
		if file and allowed_file(file.filename) and height and unit:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER2'], filename))
			i_path = 'static/size/'
			file_path = os.path.join(i_path,filename)
			size, file = women_size_predict1(file_path, height, unit) 
			file = Image.fromarray(file, 'RGB')
			#
			file.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))
			i_path = 'static/Database/val/person/'
			input_img = text+'.jpg'
			os.rename(i_path+filename , i_path+input_img)
			filename = text+'.jpg'
			o_path = './output/second/TOM/val'
			# fish = glob.glob('./output/second/TOM/val/*')
			fish = glob.glob('./static/outputs/output_f/*')
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
			return render_template('brands.html', brands=brand_cloth, text= text, size=size)
		else:
			flash('Allowed image types are -> png, jpg, jpeg, gif')
			return redirect(request.url)
	return render_template('brands.html')

# =================3. OUTPUT BRANDS TRYON======================

@app.route('/static/outputs/output_f/<brands>')
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
	fish = glob.glob('./static/outputs/output_f/*')
	for f in fish:
		os.remove(f)
	party  = ['Orach-Flayrd', 'MultiColor', 'Butterfly_p','Waved-Black' ,'Shimm' ,'Wavy-Red','Wavy-Pink', 'Reddish-KNOTS']
	for i in range(len(party)):
		party[i] = (str(party[i])+".jpg")
	return render_template('party_wear.html', party = party, text=text)

# ===================================================4. FUNCTION TO DISPALY PARTY ==========================================================

@app.route('/static/Database/val/cloth/<party>')
def display_party(party):
	time.wait(10)
	return send_from_directory(app2.config['OUTPUT_FOLDER2'], party)

 # =================================================4. FUNCTION TO INPUT AND PROCESS TRY ON ===================================================

@app.route('/party_form', methods=['POST'])
def upload_image4():
	cache.init_app(app2)
	with app2.app_context():
			cache.clear()
	fish = glob.glob('./static/Database/val/person/*')
	for f in fish:
		os.remove(f)
	fish = glob.glob('./static/size/*')
	for f in fish:
		os.remove(f)		
	party  = ['Orach-Flayrd', 'MultiColor', 'Butterfly_p','Waved-Black' ,'Shimm', 'Wavy-Red','Wavy-Pink', 'Reddish-KNOTS']
	for i in range(len(party)):
		party[i] = (str(party[i])+".jpg")

	if request.method=="POST":

		text = "palty"
		file = request.files['file']
		height = request.form['height']
		unit = request.form.get('unit')
		Go = "False"
	
		
		if file.filename == '':
			flash('No image uploaded for trying clothes.')
			return redirect(request.url)

		if file and allowed_file(file.filename) and height and unit and text:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER2'], filename))
			i_path = 'static/size/'
			file_path = os.path.join(i_path,filename)
			size, file = women_size_predict1(file_path, height, unit) 
			file = Image.fromarray(file, 'RGB')
			#
			file.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))
			i_path = 'static/Database/val/person/'
			input_img = text+'.jpg'
			os.rename(i_path+filename , i_path+input_img)
			filename = text+'.jpg'
			o_path = './output/second/TOM/val'
			# fish = glob.glob('./output/second/TOM/val/*')
			fish = glob.glob('./static/outputs/output_f/*')
			for f in fish:
				os.remove(f)
			time.sleep(10)			#
			#
			#
			# 
			pose_parse(text)
			valpair_file = 'static/Database/val_pairs.txt'
			
			for i in range(len(party)):
				with open(valpair_file , "w") as f:
						f.write(text+'.jpg '+ party[i] )
						f.close()
						predict()
						im = Image.open(os.path.join(o_path,party[i]))
						width, height = im.size
						left = width / 3
						top = 2 * height / 3
						right = 2 * width / 3
						bottom = height
						im = im.crop((left, top, right, bottom)) 
						newsize = (200, 270) 
						im = im.resize(newsize)
						im.save(os.path.join(app2.config['OUTPUT_FOLDER3'],party[i]))
			#
			#
			#
			##
			##
			return render_template('party_wear.html', party=party, text= text, size=size)
		else:
			flash('Allowed image types are -> png, jpg, jpeg, gif')
			return redirect(request.url)
	return render_template('party_wear.html')

# =====================================================4. OUTPUT PARTY TRYON=================================================================

@app.route('/static/output/<party>')
def display_output4(party):
	time.sleep(10)
	return send_from_directory(app2.config['OUTPUT_FOLDER3'], party)

#------------------------------------------------------------------------------------------------------------------------------------------ 
#----------------------------------------------------5. T-Shirt Form-----------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------------------

@app.route('/tshirt/')
def tshirt():
	cache.init_app(app2)
	with app2.app_context():
			cache.clear()
	text = "none"
	fish = glob.glob('./output/second/TOM/val/*')
	for f in fish:
		os.remove(f)
	fish = glob.glob('./static/outputs/output_f/*')
	for f in fish:
		os.remove(f)		
	tshirt  = ['POLO_Black', 'POLO-blue', 'POLO-Blue', 'POLO-BLue', 'POLO-orach', 'POLO-Violet']
	for i in range(len(tshirt)):
		tshirt[i] = (str(tshirt[i])+".jpg")
	return render_template('tshirt.html', tshirt = tshirt, text=text)

# ===================================================5. FUNCTION TO DISPALY T-shirt ==========================================================

@app.route('/static/Database/val/cloth/<tshirt>')
def display_tshirt(tshirt):
	time.wait(5)
	return send_from_directory(app2.config['OUTPUT_FOLDER2'], tshirt)

 # =================================================5. FUNCTION TO INPUT AND PROCESS TRY ON ===================================================

@app.route('/tshirt_form', methods=['POST'])
def upload_image5():
	cache.init_app(app2)
	with app2.app_context():
			cache.clear()
	fish = glob.glob('./static/Database/val/person/*')
	for f in fish:
		os.remove(f)
	fish = glob.glob('./static/size/*')
	for f in fish:
		os.remove(f)		
	tshirt  = ['POLO_Black', 'POLO-blue', 'POLO-Blue', 'POLO-BLue', 'POLO-orach', 'POLO-Violet']
	for i in range(len(tshirt)):
		tshirt[i] = (str(tshirt[i])+".jpg")

	if request.method=="POST":
		text   = "tshirtss"
		file   = request.files['file']
		file1  = request.files['file1']
		height = request.form['height']
		unit   = request.form.get('unit')
		Go     = "False"
	
		if file.filename == '':
			flash('No image uploaded for size prediction.')
			return redirect(request.url)
		
		if file1.filename == '':
			flash('No image uploaded for trying clothes.')
			return redirect(request.url)

		if file and allowed_file(file.filename) and file1 and allowed_file(file1.filename) and height and unit and text:
			filename = secure_filename(file.filename)
			filename1 = secure_filename(file1.filename)
			file1.save(os.path.join(app.config['UPLOAD_FOLDER2'], filename1))
			i_path = 'static/size/'
			file_path = os.path.join(i_path,filename1)
			size = women_size_predict(file_path, height, unit) 
			#
			file.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))
			i_path = 'static/Database/val/person/'
			input_img = text+'.jpg'
			os.rename(i_path+filename , i_path+input_img)
			filename = text+'.jpg'
			o_path = './output/second/TOM/val'
			# time.sleep(10)			#
			#
			#
			# 
			pose_parse(text)
			valpair_file = 'static/Database/val_pairs.txt'
			
			for i in range(len(tshirt)):
				with open(valpair_file , "w") as f:
						f.write(text+'.jpg '+ tshirt[i] )
						f.close()
						predict()
						im = Image.open(os.path.join(o_path,tshirt[i]))
						width, height = im.size
						left = width / 3
						top = 2 * height / 3
						right = 2 * width / 3
						bottom = height
						im = im.crop((left, top, right, bottom)) 
						newsize = (200, 270) 
						im = im.resize(newsize)
						im.save(os.path.join(app2.config['OUTPUT_FOLDER3'],tshirt[i]))
			#
			#
			#
			##
			##
			return render_template('tshirt.html', tshirt=tshirt, text=text, size=size)
		else:
			flash('Allowed image types are -> png, jpg, jpeg, gif')
			return redirect(request.url)
	return render_template('tshirt.html')

# =====================================================5. T-SHIRT TRYON=================================================================

@app.route('/static/outputs/output_f/<tshirt>')
def display_output5(tshirt):
	time.sleep(5)
	return send_from_directory(app2.config['OUTPUT_FOLDER3'], tshirt)



#------------------------------------------------------ Mask the Face -------------------------------------------------------------------------


@app.route('/faceMask/')
def facemask():
	cache.init_app(app2)
	with app2.app_context():
			cache.clear()
	text = "none"
	fish = glob.glob('./static/outputs/output_mask/*')
	for f in fish:
		os.remove(f)
	fish = glob.glob('MaskTheFace/data/*')
	for f in fish:
		os.remove(f)		
	return render_template('facemask.html', text=text)

@app.route('/facemask_form', methods=['POST'])
def upload_image6():
	cache.init_app(app2)
	with app2.app_context():
			cache.clear()
	fish = glob.glob('./static/outputs/output_mask/*')
	for f in fish:
		os.remove(f)
	fish = glob.glob('MaskTheFace/data/*')
	for f in fish:
		os.remove(f)		

	if request.method=="POST":
		text   = "Face-Mask"
		file   = request.files['file']
	
		if file.filename == '':
			flash('No image uploaded for size prediction.')
			return redirect(request.url)
		

		if file and allowed_file(file.filename) and text:
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER3'], filename))
			#
			i_path = 'MaskTheFace/data/'
			input_img = text+'.jpg'
			os.rename(i_path+filename , i_path+input_img)
			zpath = os.path.join(i_path, input_img)
			print(i_path)
			# time.sleep(10)			#
			#
			
			opath = 'static/outputs/output_mask/'
			mask_type = ['N95', 'surgical', 'cloth', 'N95', 'surgical', 'cloth', 'N95', 'surgical', 'cloth', 'N95', 'surgical', 'cloth', 'cloth']
			mask_color = ["#fc1c1a","#177ABC","#94B6D2","#A5AB81","#DD8047","#6b425e","#e26d5a","#c92c48","#6a506d","#ffc900","#ffffff","#000000","#49ff00"]

			out_files = []
			for i in range(13):
				mask_the_face.run_function(zpath, mask_type[i], '', '0', mask_color[i], '0','', 'verbose', 'write_original_image')
				out_files.append(text+"_" + str(mask_type[i])+'.jpg')
				im = Image.open(os.path.join(i_path,out_files[-1]))
				im.save(os.path.join(app2.config['OUTPUT_FOLDER4'],out_files[-1]))
				new_name = text + str(i) + '.jpg' 
				os.rename(opath+out_files[-1], opath+new_name)
				out_files[-1] = new_name
			return render_template('facemask.html', text=text, out_files = out_files)
		else:
			flash('Allowed image types are -> png, jpg, jpeg, gif')
			return redirect(request.url)
	return render_template('facemask.html')


@app.route('/static/outputs/output_mask/<out_files>')
def display_output6(out_files):
	time.sleep(50)
	return send_from_directory(app2.config['OUTPUT_FOLDER4'], out_files)

# ====================================================== FLASK APP RUN & DEBUG===================================================================

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)

