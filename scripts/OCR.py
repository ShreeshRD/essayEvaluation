import pytesseract
from PIL import Image

import cv2
from matplotlib import pyplot as plt

#image_file = "ocr_python_textbook/data/page_01.jpg"
#img = cv2.imread(image_file)
#rot = "ocr_python_textbook/data/page_01_rotated.JPG"

#C:\Users\Shreesh\AppData\Local\Tesseract-OCR
'''
1. Install tesseract OCR and add it to PATH
2. pip install pytesseract
3. Change path below
'''
pytesseract.pytesseract.tesseract_cmd = 'D:/program files/Tesseract-OCR/tesseract.exe'

def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)

    height, width  = im_data.shape[:2]
    
    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)

    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])

    # Hide spines, ticks, etc.
    ax.axis('off')

    # Display the image.
    ax.imshow(im_data, cmap='gray')

    plt.show()

def noise_removal(image):
    import numpy as np
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return (image)


def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#https://becominghuman.ai/how-to-automatically-deskew-straighten-a-text-image-using-opencv-a0c30aed83df
import numpy as np

def getSkewAngle(cvImage) -> float:
    # Prep image, copy, convert to gray scale, blur, and threshold
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Apply dilate to merge text into meaningful lines/paragraphs.
    # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
    # But use smaller kernel on Y axis to separate between different blocks of text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    # Find all contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

    # Find largest contour and surround in min area box
    largestContour = contours[0]
    #print (len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    cv2.imwrite("temp/boxes.jpg", newImage)
    # Determine the angle. Convert it to the value that was originally used to obtain skewed image
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle
# Rotate the image around its center

def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

# Deskew image
def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)
def threshold(gimg):
    thresh, im_bw = cv2.threshold(gimg, 210, 230, cv2.THRESH_BINARY)
    return im_bw

def getText(file_path):
    rot = file_path
    img = cv2.imread(rot)
    #inverted_image = cv2.bitwise_not(img)
    fix = deskew(img)

    gray_image = grayscale(fix)
    #thresh, im_bw = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
    thresh = threshold(gray_image)

    no_noise = noise_removal(thresh)

    #print(pytesseract.image_to_osd(Image.open(image_file)))
    #print(pytesseract.image_to_osd(no_noise))
    cv2.imwrite("ocr_python_textbook/temp/rotated_fixed.jpg", no_noise)

    #cv2.imwrite("temp/no_noise.jpg", no_noise)
    #no_noise = "temp/no_noise.jpg"
    #img = Image.open(no_noise)

    ocr_result = pytesseract.image_to_string(fix)
    return (ocr_result)
    #display("ocr_python_textbook/temp/rotated_fixed.jpg")
#display(rot)
if __name__ == "__main__":
    text = getText("test.png")
    print(text)