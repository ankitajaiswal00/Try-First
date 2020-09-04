from flask import Flask

UPLOAD_FOLDER1 = 'static/Database/val/person/'
UPLOAD_FOLDER2 = 'static/size/'
UPLOAD_FOLDER3 = 'MaskTheFace/data/'

app = Flask(__name__)                #, static_url_path='/Database/val/person/')
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2
app.config['UPLOAD_FOLDER3'] = UPLOAD_FOLDER3
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
