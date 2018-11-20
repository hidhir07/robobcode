# Cam libs
from picamera import PiCamera
from time import sleep


# QR libs
from pyzbar import pyzbar
import argparse
import opencv as cv2

# Construct the argumenr parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add.argument("-i","--image", required=True,
                help="/home/pi/Desktop/qr/0,0.png")
args = vars(ap.parse_args())

# Load the input image
image = cv2.imread.args["image"]

# Find the barcodes in the iamge and decode each of the barcodes
barcodes = pyzbar.decode(image)

# Loop over the detected barcodes
for barcode in barcodes:
    # Extract the bounding box location of the barcode and draw the
    # bounding box surrounding te barcode on the image
    (x, y, w, h) = barcode.rect
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # The barcode data is a bytes objects so if we want to draw it on
    # our output image we need to convert itto a string first
    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type

    # Draw the barcode data and barcode type on the image
    text = "{} ({})".format(barcodeData, barcodeType)
    cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 0, 255), 2)

    # Print the barcode type and data to the terminal
    print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

# Show the output image
cv2.imshow("Image", image)
cv2.waitkey(0)

'''
camera = PiCamera()

camera.start_preview()
sleep(20)
camera.stop_preview()
'''
