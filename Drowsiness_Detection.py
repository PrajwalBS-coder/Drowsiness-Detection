from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
from pygame import mixer
import smtplib
from twilio.rest import Client
mixer.init()
sound = mixer.Sound('alarm.wav')
sound.play()
def eye_aspect_ratio(eye):
	A = distance.euclidean(eye[1], eye[5])
	B = distance.euclidean(eye[2], eye[4])
	C = distance.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear
	
thresh = 0.25
frame_check = 30
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")# Dat file is the crux of the code

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
cap=cv2.VideoCapture(0)
flag=0
while True:
	ret, frame=cap.read()
	frame = imutils.resize(frame, width=450) 
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	subjects = detect(gray, 0)
	for subject in subjects:
		shape = predict(gray, subject)
		shape = face_utils.shape_to_np(shape)#converting to NumPy Array
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)
		ear = (leftEAR + rightEAR) / 2.0
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
		
		if ear < thresh:
			flag += 1
			print (flag)
			if(flag<=20):
				if(flag>10):
					cv2.putText(frame, "Feeling Sleepy", 
					(40, 60),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			if flag >= frame_check:
				sound.play()
				server = smtplib.SMTP_SSL("smtp.gmail.com",465)
				server.login("legendamin008@gmail.com","runxxybmnstsqplq")
				server.sendmail("legendamin008@gmail.com","prajwaljhon@gmail.com","The Driver Has Gone To Sleep Please Do Take The Car To your Control As soon As Possible")
				server.quit()
				
				
				
				
				
				
				
				
				
				
				client=Client('AC3910f6aa598e061e2aeb58a74e9d4aec','bb63e348fa55db62750cce8359bd9069')
				message=client.messages.create(
					body="The Driver Has Gone To Sleep Please Reach Out The Driver",
					from_='+18036744197',
					to='+917349682310'

		      
				)
				message=client.messages.create(
					body="The Driver Has Gone To Sleep Please Reach Out The Driver",
					from_='whatsapp:+14155238886',
					to='whatsapp:+917349682310'
				)





			
				cv2.putText(frame, "ALERT!", (40, 60),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
				cv2.putText(frame, "Alerting Nearer Vehicle", (15,325),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

				#print ("Drowsy")
		else:
			flag = 0
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
cv2.destroyAllWindows()
cap.release() 
