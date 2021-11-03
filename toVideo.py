import os
import cv2

path = r"./Videos/outPut/"
archivos = sorted(os.listdir(path))
print(archivos)
img_array = []

for x in range(0, len(archivos)):
	nomArchivo = archivos[x]
	dirArchivo = path + "/" + str(nomArchivo)
	print(dirArchivo)
	img = cv2.imread(dirArchivo)
	img_array.append(img)

height, width = img.shape[:2]
video = cv2.VideoWriter('./Videos/video/output_cholula_puebla_street_cloudy_afternoon_27082021_1757.avi', cv2.VideoWriter_fourcc(*'DIVX'), 10, (width, height))

for i in range(0, len(archivos)):
	video.write(img_array[i])

video.release()