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

    decoded_info = decode(image)

    print(decoded_info)


def detect_and_crop_img(image_path):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path = 'best.pt', force_reload = True)

    results = model(image_path)
    print(results.xyxy)
    bbox = results.xyxy[0][0]
    print(bbox)
    xmin = int(bbox[0])
    ymin = int(bbox[1])
    xmax = int(bbox[2])
    ymax = int(bbox[3])

    image = cv2.imread(image_path)

    cropped_image = image[ymin:ymax, xmin:xmax]
    gray_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    bright_img = cv2.adaptiveThreshold(gray_image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,181,15)
    cv2.imshow("bright image" , bright_img)
    cv2.waitKey(0)
    return barcode_decoder(cropped_image)


# barcode_decoder('output.jpg')

img = detect_and_crop_img('trial2.jpg')

print(img)