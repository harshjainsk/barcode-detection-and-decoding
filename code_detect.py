from pyzbar.pyzbar import decode
import barcode
from barcode import Code128
from barcode.writer import ImageWriter
import cv2
import torch
from PIL import Image



def create_barcode():

    bar_code = barcode.get_barcode_class('code128')

    barcode_data = bar_code('vihave-ai', writer = ImageWriter())

    fullname = barcode_data.save('trial')

    print(fullname)


def barcode_decoder(image):

    # image comes in numpy array and then decoded    
    decoded_info = decode(image)
    return decoded_info


def detect_and_crop_img(image_path):

    # loading model and detecting barcode
    model = torch.hub.load('ultralytics/yolov5', 'custom', path = 'best.pt', force_reload = True)
    results = model(image_path)

    # print(results.xyxy)

    # extracting bounding box coordinates
    bbox = results.xyxy[0][0]
    # print(bbox)
    xmin = int(bbox[0])
    ymin = int(bbox[1])
    xmax = int(bbox[2])
    ymax = int(bbox[3])

    # reading image and cropping
    image = cv2.imread(image_path)

    cropped_image = image[ymin:ymax, xmin:xmax]

    # converting the RGB output image to BGR image
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR)

    return barcode_decoder(gray_image)



decoded_info = detect_and_crop_img('images\\trial2.jpg')

print(decoded_info)