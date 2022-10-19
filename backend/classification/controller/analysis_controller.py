import base64
import io

import cv2 as cv
import numpy
from flask import Blueprint, jsonify, request
from PIL import Image
from service.analysis_service import orchestrate_analysis

analysis_blueprint = Blueprint('analysis_blueprint', __name__)

@analysis_blueprint.route('', methods = ['POST'])
def start_analysis():
    img_data = base64.b64decode(request.json["image"])
    filtr = request.json["filter"]
    pil_img = Image.open(io.BytesIO(img_data))
    img = cv.cvtColor(numpy.array(pil_img), cv.COLOR_BGR2RGB)

    result_image, solders_classification = orchestrate_analysis(img, filtr)

    return jsonify({"image": result_image, "classification": solders_classification})
