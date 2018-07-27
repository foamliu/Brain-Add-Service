from flask import Flask
from flask_uploads import UploadSet, IMAGES, configure_uploads, ALL
from settings import *

app = Flask(__name__)

# configure debug
app.debug = DEBUG

# configure upload set
app.config['UPLOADED_PHOTO_DEST'] = UPLOAD_FOLDER
app.config['UPLOADED_PHOTO_ALLOW'] = IMAGES
photos = UploadSet('PHOTO')
configure_uploads(app, photos)

# import router view
from router import *

if __name__ == '__main__':
    app.run(port=5001, threaded=True)