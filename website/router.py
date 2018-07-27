from app import app, photos
from flask import render_template, request, redirect, url_for, abort
import cv2 as cv
from utils import predict

logger = app.logger

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    if request.method == 'POST' and 'photo' in request.files:
        photo_file = request.files['photo']
        photo_name = photos.save(photo_file)
        photo_url = 'uploads/' + photo_name
        gray = cv.imread(photo_url, 0)
        out = predict(gray)
        cv.imwrite('static/output_' + photo_name, out)

        return redirect(url_for('show', name=photo_name))

    return render_template('index.html')


@app.route('/photo/<name>')
def show(name):
    if name is None:
        abort(404)
    src_url = photos.url(name)
    dst_url = '../static/output_' + name
    return render_template('show.html', src_url=src_url, dst_url=dst_url)
