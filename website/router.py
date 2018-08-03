from app import app, colorize_images, caption_images
from flask import render_template, request, redirect, url_for, abort
import cv2 as cv
from utils import colorize_predict, caption_predict

logger = app.logger


@app.route('/')
def index():
    return redirect(url_for("show_colorize"))


# -------colorize pages----------------
@app.route('/colorize/upload_photo', methods=['GET', 'POST'])
def colorize_upload():
    if request.method == 'POST' and 'photo' in request.files:
        photo_file = request.files['photo']
        photo_name = colorize_images.save(photo_file)
        return redirect(url_for('show_colorize', name=photo_name))

    return redirect(url_for('show_colorize'))


# three kinds of route
@app.route('/colorize/')
@app.route('/colorize/<name>/')
@app.route('/colorize/<sample>/<name>')
def show_colorize(name=None, sample=None):
    # default case
    if name is None:
        name = "b1.jpg"
        sample = "sample"

    # upload or sample
    if sample is None:
        photo_url = 'uploads/colorize/' + name
        src_url = colorize_images.url(name)
    else:
        if sample == "sample":
            # photo url from the .py directory, so we don't need leading slash
            photo_url = 'static/images/colorize/' + name
            # src url will transfer to the .html, so we need a leading slash to go to the root directory
            src_url = '/static/images/colorize/' + name
        else:
            abort(404)

    # colorize the photo
    gray = cv.imread(photo_url, 0)
    out = colorize_predict(gray)

    # save the output image
    # cv will write the file from the .py directory, so we don't need leading slash
    cv.imwrite('static/images/colorize/output_' + name, out)

    # dst url will transfer to the .html, so we need a leading slash to go to the root directory
    dst_url = '/static/images/colorize/output_' + name

    # read the sample pictures
    initial = []
    for i in range(1, 13):
        initial.append("b" + str(i) + ".jpg")
    sample_pictures = [initial[0:4], initial[4:8], initial[8:12]]

    return render_template('colorize.html', src_url=src_url, dst_url=dst_url, sample_pictures=sample_pictures)


# -------caption pages----------------
@app.route('/caption/upload_photo', methods=['GET', 'POST'])
def caption_upload():
    if request.method == 'POST' and 'photo' in request.files:
        photo_file = request.files['photo']
        photo_name = caption_images.save(photo_file)

        return redirect(url_for('show_caption', name=photo_name))

    return redirect(url_for('show_caption'))


@app.route('/caption/')
@app.route('/caption/<name>/')
# @app.route('/caption/<type>/<name>')
def show_caption(name=None):
    if name is None:
        # default
        photo_url = 'static/images/caption/sample.png'
        src_url = '../static/images/caption/sample.png'
    else:
        photo_url = 'uploads/caption/' + name
        src_url = caption_images.url(name)

    sentence = caption_predict(photo_url)

    return render_template('caption.html', src_url=src_url, sentence=sentence)
