from flask import Flask, request, jsonify
import torch
import argparse
import albumentations as A
from albumentations.pytorch import ToTensorV2
import numpy as np
import cv2
from PIL import Image
from unet_model import UNET
import io
import os
from waitress import serve
import logging
import datetime



device = "cuda" if torch.cuda.is_available() else "cpu"

folder_path = "results"
if not os.path.exists(folder_path):
    os.mkdir(folder_path)

# Is here to get argumants from UI
parser = argparse.ArgumentParser()
parser.add_argument("--saved_model_path", type=str, help='Specify path for chosen model')
args = parser.parse_args()

app = Flask(__name__)


def load_model(model_path):
    model = UNET(in_channels=3, out_channels=1)
    model.load_state_dict(torch.load(model_path, map_location=torch.device(device))['state_dict'])
    model.to(device)
    model.eval()
    return model


model = load_model(args.saved_model_path if args.saved_model_path else "models/UNET_checkpoints/my_checkpoint.pth.tar")


transform = A.Compose([
        A.Resize(height=240, width=160),
        A.Normalize(
            mean=[0.0, 0.0, 0.0],
            std=[1.0, 1.0, 1.0],
            max_pixel_value=255.0,
        ),
        ToTensorV2()
    ])


# Merges the mask with the image
def add_mask(img: np.array, mask: np.array):
    mask = mask.astype(np.uint8)
    mask_yellow = np.concatenate([mask * 255, mask * 255, mask * 0], axis=2)
    mask_person = cv2.bitwise_and(img, img, mask=mask)
    mask_background = cv2.bitwise_and(img, img, mask=cv2.threshold(cv2.bitwise_not(mask), 0, 255, cv2.THRESH_OTSU)[1])
    dst = cv2.addWeighted(mask_person, 0.6, mask_yellow, 0.4, 0.0)
    return cv2.add(dst, mask_background)


# Here image reshaped, passed to a nn, then merged with output (mask)
@app.route('/process_image', methods=['POST'])
def process_image():
    file = request.files['file']
    image_bytes = file.read()
    image = np.array(Image.open(io.BytesIO(image_bytes)).convert("RGB"))
    image_1 = image.copy()
    image = transform(image=image)['image'].to(device)
    image_shape = image.shape
    image_1_shape = image_1.shape
    image_1 = cv2.resize(image_1, (image_shape[2], image_shape[1]))
    predicted = torch.sigmoid(model(image.unsqueeze(0))) > 0.5
    predicted = torch.permute(predicted[0], (1, 2, 0))
    predicted = predicted.cpu().detach().numpy().astype(np.uint8)
    result = add_mask(image_1, predicted)
    result = cv2.resize(result, (image_1_shape[1], image_1_shape[0]))
    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    cv2.imwrite(f'results/{file.name}{datetime.datetime.now()}.jpeg', np.array(result))
    return jsonify({'prediction': result.tolist()})


# Video processed the same way as image is
@app.route('/process_video', methods=['POST'])
def process_video():
    video = request.files['file']
    video.save(video.filename)
    cap = cv2.VideoCapture(video.filename)
    fourcc = cv2.VideoWriter_fourcc('V','P','8','0')
    out = cv2.VideoWriter('output.webm', fourcc, 24, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    # Loading Video as a sequence of images
    while True:
        ret, image = cap.read()
        if not ret:
            break
        image_1 = image.copy()
        image = transform(image=image)['image'].to(device)
        image_shape = image.shape
        image_1_shape = image_1.shape
        image_1 = cv2.resize(image_1, (image_shape[2], image_shape[1]))
        predicted = torch.sigmoid(model(image.unsqueeze(0)))
        predicted = predicted > 0.5
        predicted = torch.permute(predicted.squeeze(0), (1, 2, 0))
        predicted = predicted.cpu().detach().numpy().astype(np.uint8)
        result = add_mask(image_1, predicted)
        result = cv2.resize(result, (image_1_shape[1], image_1_shape[0]))
        out.write(result)  # Merging images with masks back to video
    cap.release()
    out.release()


    with open('output.webm', 'rb') as f:
        result = f.read()
    with open(f'results/{video.filename}{datetime.datetime.now()}.webm', 'wb') as f:
        f.write(result)
    return result




logging.basicConfig(level=logging.INFO)
serve(app, host='0.0.0.0', port=5000)