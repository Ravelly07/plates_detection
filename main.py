from difuminado import convertir
import cv2

capture = cv2.VideoCapture('./Videos/cholula_puebla_street_cloudy_afternoon_27082021_1757.mp4')
cont = 0
path = 'Videos/out/Temp_'
outputPath = ''
Path_ = 'Videos/outPut/' 
outputPath_ = ''

while (capture.isOpened()):
    ret, frame = capture.read()
    if (ret == True):
        outputPath = path + 'IMG_%04d.jpg' % cont
        outputPath_ = Path_ + 'IMG_%04d.jpg' % cont
        cv2.imwrite(outputPath, frame)    
        
        img = convertir(outputPath,cont)
        cv2.imwrite(outputPath_,img)

        cont += 1
        if (cv2.waitKey(1) == ord('s')):
            break
    else:
        break

capture.release()
cv2.destroyAllWindows()