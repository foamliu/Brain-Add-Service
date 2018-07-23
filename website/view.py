import os
import cv2 as cv
from utils import predict
from app import photos

def predict_image(image_name)
    gray = cv.imread(image_name, 0)
    out = predict(gray)
    cv.imwrite('images/output.png', out)