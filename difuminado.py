from PIL import Image as imageMain
from PIL.Image import Image
import cv2
import numpy
import os

def convertir(path,cont):
    imagePath = path
    imagePil = imageMain.open(imagePath)
    imageCv = cv2.cvtColor(numpy.array(imagePil), cv2.COLOR_RGB2BGR)
    #cv2.imshow('Original Image', imageCv)

    gray = cv2.cvtColor(imageCv, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('Gray Scaled', gray)

    bilateral = cv2.bilateralFilter(gray, 11, 17, 17)
    #cv2.imshow('After Bilateral Filter', bilateral)

    blur = cv2.GaussianBlur(bilateral, (5, 5), 0)
    #cv2.imshow('After Gausian Blur', blur)

    edged = cv2.Canny(blur, 170, 200)
    #cv2.imshow('After Canny Edge', edged)

    contours, hierarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:30]
    tempContours1 = cv2.drawContours(imageCv.copy(), contours, -1, (255, 0, 0), 2)
    #cv2.imshow('Detected Contours', tempContours1)

    rectangleContours = [None]
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approximationAccuracy = 0.02 * perimeter
        approximation = cv2.approxPolyDP(contour, approximationAccuracy, True)
        if len(approximation) == 4:
            rectangleContours.append(contour)
            rectangleContours.pop(0)
    if rectangleContours[0] is None:
        imagen = imageCv
        print('Not proccesing image ', cont , ' :c' )
    else:        
        plateContour = rectangleContours[0]
        tempContours2 = cv2.drawContours(imageCv.copy(), [plateContour], -1, (255, 0, 0), 2)
        #cv2.imshow('Detected Plate Contour', tempContours2)

        x,y,w,h = cv2.boundingRect(plateContour)
        plateImage = imageCv[y:y+h, x:x+w]
        #cv2.imshow('Plate Original', plateImage)

        plateImageBlur = cv2.GaussianBlur(plateImage, (25, 25), 0)
        #cv2.imshow('Plate Blurred', plateImageBlur)

        def findMostOccurringColor(cvImage) -> (int, int, int):
            width, height, channels = cvImage.shape
            colorCount = {}
            for y in range(0, height):
                for x in range(0, width):
                    BGR = (int(cvImage[x, y, 0]), int(cvImage[x, y, 1]), int(cvImage[x, y, 2]))
                    if BGR in colorCount:
                        colorCount[BGR] += 1
                    else:
                        colorCount[BGR] = 1

            maxCount = 0
            maxBGR = (0, 0, 0)
            for BGR in colorCount:
                count = colorCount[BGR]
                if count > maxCount:
                    maxCount = count
                    maxBGR = BGR

            return maxBGR

        plateBackgroundColor = findMostOccurringColor(plateImageBlur)
        tempContours3 = cv2.drawContours(imageCv.copy(), [plateContour], -1, plateBackgroundColor, -1)
        imagen = tempContours3
        #cv2.imshow('Original Image', imageCv)
        #cv2.imshow('Result', tempContours3)

        #cv2.waitKey(0)

    cv2.destroyAllWindows()
    return imagen