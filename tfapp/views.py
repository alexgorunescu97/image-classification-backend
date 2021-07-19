from django.shortcuts import render

# Create your views here
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.imagenet_utils import decode_predictions
from urllib.request import urlopen, Request
import cv2
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from django.http import HttpResponse
import json

@csrf_exempt
def get_prediction(request):
    if request.FILES.get('image') == None:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        url = body.get('imageUrl')
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        stream = urlopen(req)
        return HttpResponse(process_predict(stream))
    else:
        stream = request.FILES.get('image')
        return HttpResponse(process_predict(stream))

def process_predict(stream):
    img = np.asarray(bytearray(stream.read()), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    img = cv2.resize(img, dsize=(224, 224), interpolation=cv2.INTER_AREA)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)

    model = ResNet50(weights="imagenet")
    prediction = model.predict(img)
    return decode_predictions(prediction, top=1)[0]

    
