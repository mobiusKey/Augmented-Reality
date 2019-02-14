import cv2
from cv2 import aruco
import numpy as np
import glob

with np.load('pose_webcam_calibration_output.npz') as X:
	mtx, dist, _, _= [X[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]
	
image_size = (1920, 1080)
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_1000)

markerLength = 1

arucoParams = aruco.DetectorParameters_create()

imgDir = "images"

for fname in glob.glob("images/W*.jpg"):
	img = cv2.imread(fname)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=arucoParams)
	if ids != None:
		rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, markerLength, mtx, dist)
		imgAruco = aruco.drawDetectedMarkers(img, corners, ids, (0,255,0))
		imgAruco = aruco.drawAxis(imgAruco, mtx, dist, rvec, tvec, 1)
	else:
		print("marker not detected")
		imgAruco = img
	cv2.imshow("aruco", img)
	
	if cv2.waitKey(0) & 0xFF == ord('q'):
		break
