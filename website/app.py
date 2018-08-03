from flask import Flask
from flask_uploads import UploadSet, IMAGES, configure_uploads, ALL
from settings import *
from datetime import timedelta


app = Flask(__name__)

# configure debug
# app.debug = DEBUG

# configure upload set
app.config['UPLOADED_COLORIZE_DEST'] = UPLOAD_FOLDER + '/colorize'
app.config['UPLOADED_COLORIZE_ALLOW'] = IMAGES
app.config['UPLOADED_CAPTION_DEST'] = UPLOAD_FOLDER + '/caption'
app.config['UPLOADED_CAPTION_ALLOW'] = IMAGES
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

colorize_images = UploadSet('COLORIZE')
configure_uploads(app, colorize_images)

caption_images = UploadSet('CAPTION')
configure_uploads(app, caption_images)

# import router view
from router import *
if __name__ == '__main__':
    app.run(port=5001, threaded=True, debug=True, host=('0.0.0.0'))
