import cv2 as cv
import numpy as np

#Initializing
print("OpenCV ver. " + cv.__version__)

#파일 읽기
imageFolder = 'Data/Images/'
imageName = 'One'
imageType = '.jpg'
image = cv.imread(imageFolder + imageName + imageType, cv.IMREAD_COLOR)

#이미지 처리
binaryRaw = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
ret, binary = cv.threshold(binaryRaw, 127, 255, cv.THRESH_BINARY)
binary2 = cv.adaptiveThreshold(binaryRaw, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 15, 2)

mat = binary.copy()

print(mat)
np.savetxt(imageFolder + imageName + ".txt", mat, fmt='%i', delimiter=',')


#결과 출력
cv.namedWindow('bin 01', cv.WINDOW_NORMAL)
cv.imshow('bin 01', binary)
cv.namedWindow('bin 02', cv.WINDOW_NORMAL)
cv.imshow('bin 02', binary2)
while cv.getWindowProperty('bin 01', 0) >= 0 and cv.getWindowProperty('bin 02', 0) >= 0 :
    cv.waitKey(1)
cv.destroyAllWindows()


