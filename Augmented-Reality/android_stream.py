import numpy as np
import cv2
from cv2 import aruco
from webcam import Webcam

print("starting...")

#start webcam
webcam = Webcam()
webcam.start()

# load camera matrix and distortion coefficients
with np.load('pose_webcam_calibration_output.npz') as X:
	mtx, dist, _, _= [X[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]
	
image_size = (1920, 1080)
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_1000)

markerLength = 0.07

arucoParams = aruco.DetectorParameters_create()


#stream = cv2.VideoCapture('http://104.38.59.31:8080/video')

# Use the next line if your camera has a username and password
# stream = cv2.VideoCapture('protocol://username:password@IP:port/1')  

while True:
	img = webcam.get_current_frame()
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=arucoParams)
	print("type {} value: {}".format(type(ids), id))
	if type(ids) is np.ndarray:
		if ids.any() != None:
			rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, markerLength, mtx, dist)
			imgAruco = aruco.drawDetectedMarkers(img, corners, ids, (0,255,0))
			imgAruco = aruco.drawAxis(imgAruco, mtx, dist, rvec, tvec, 0.07)
	else:
		# print("marker not detected")
		
		imgAruco = img
	cv2.imshow("aruco", img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		webcam.stop()
		break
		
