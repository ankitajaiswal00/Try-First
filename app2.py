from flask import Flask
from flask_caching import Cache
import os

OUTPUT_FOLDER1 = os.path.join('output','second/TOM/val')
OUTPUT_FOLDER2 = os.path.join('static','Database/val/cloth')
OUTPUT_FOLDER3 = os.path.join('static','outputs/output_f')
OUTPUT_FOLDER4 = os.path.join('static','outputs/output_mask')
#'output/second/TOM/val'
#'static/Database/val/tryon-person/'
app2 = Flask(__name__)                
app2.secret_key = "secret key12"
app2.config['OUTPUT_FOLDER1'] = OUTPUT_FOLDER1
app2.config['OUTPUT_FOLDER2'] = OUTPUT_FOLDER2
app2.config['OUTPUT_FOLDER3'] = OUTPUT_FOLDER3
app2.config['OUTPUT_FOLDER4'] = OUTPUT_FOLDER4
app2.config['MAX_CONTENT_LENGTH'] = 16 * 256 * 192

# 
cache = Cache(app2,config={'CACHE_TYPE': 'simple'})


def main():
    cache.init_app(app2, config=your_cache_config)

    with app.app_context():
        cache.clear()