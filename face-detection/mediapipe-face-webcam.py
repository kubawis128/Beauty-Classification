# find face and crop

import base64
import json
import socket
import cv2
import mediapipe as mp
import predict as pt
import freenect

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
font = cv2.FONT_HERSHEY_SIMPLEX

def get_video():
    array,_ = freenect.sync_get_video()
    #array = cv2.cvtColor(array,cv2.COLOR_BGR2RGB)
    return array

#cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.4) as hands:
        
  with mp_face_detection.FaceDetection(
      model_selection=2, min_detection_confidence=0.4) as face_detection:
          
    while True:
      image = get_video()

      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

      annotated_image = image
      results_hands = hands.process(image)
      results = face_detection.process(image)
      image.flags.writeable = True
      #image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      #cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))
      
      if results.detections:
        for detection in results.detections:
          annotated_image = image.copy()
          mp_drawing.draw_detection(annotated_image, detection)
      ok = False
      if results_hands.multi_hand_landmarks:
          for hand_landmarks in results_hands.multi_hand_landmarks:
            mp_drawing.draw_landmarks(annotated_image,hand_landmarks,mp_hands.HAND_CONNECTIONS,mp_drawing_styles.get_default_hand_landmarks_style(),mp_drawing_styles.get_default_hand_connections_style())
            thumb_x, thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * 640, hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * 480
            index_x, index_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * 640, hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * 480
            if ((abs(thumb_y-index_y) + abs(thumb_x-index_x))/2) < 15:
                  cv2.putText(annotated_image, 'Ok!', (10,450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
                  ok = True
            else:
              ok = False
      #cv2.imshow('MediaPipe Face Detection', annotated_image)
      annotated_image = cv2.resize(annotated_image, (480,480),interpolation = cv2.INTER_AREA)


      _, im_arr = cv2.imencode('.png', annotated_image)
      im_bytes = str(base64.b64encode(im_arr.tobytes()))
      base64_string = im_bytes[2:(len(im_bytes)-1)]
      
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.connect(("127.0.0.1",2138))
      sock.send(bytes(base64_string, "utf-8"))
      sock.close()
      
      k = cv2.waitKey(1)
      if k == ord('a') or ok:
        if results.detections:
          index = 0
          prediction_results = []
          for detection in results.detections:
            index += 1
            y,x,k = image.shape
            bounding_box = detection.location_data.relative_bounding_box;
            if int(bounding_box.ymin*y)-50 < 0 or int(bounding_box.xmin*x)-50 < 0:
              continue

            cropped_img = image[int(bounding_box.ymin*y)-50:int(bounding_box.height*y)+int(bounding_box.ymin*y)+50, int(bounding_box.xmin*x)-50:int(bounding_box.width*x)+int(bounding_box.xmin*x)+50]
            score = pt.predict(image, cv2.resize(cropped_img, (128,128), interpolation = cv2.INTER_AREA),index)

            _, im_arr = cv2.imencode('.png', cropped_img)
            im_bytes = str(base64.b64encode(im_arr.tobytes()))
            base64_string = im_bytes[2:(len(im_bytes)-1)]
            prediction_results.append(dict(score=score,image=base64_string))

          sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          sock.connect(("127.0.0.1",2137))
          res = json.dumps(prediction_results)
          sock.send(bytes(res, "utf-8"))
          sock.close()
      if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()
