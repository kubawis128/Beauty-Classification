# find face and crop

import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
font = cv2.FONT_HERSHEY_SIMPLEX

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:
        
  with mp_face_detection.FaceDetection(
      model_selection=0, min_detection_confidence=0.7) as face_detection:
          
    while cap.isOpened():
      success, image = cap.read()
      if not success:
        print("Ignoring empty camera frame.")
        continue

      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

      annotated_image = image
      results_hands = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
      results = face_detection.process(image)
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))
      
      if results.detections:
        for detection in results.detections:
          annotated_image = image
          mp_drawing.draw_detection(annotated_image, detection)

      if results_hands.multi_hand_landmarks:
          for hand_landmarks in results_hands.multi_hand_landmarks:
            mp_drawing.draw_landmarks(annotated_image,hand_landmarks,mp_hands.HAND_CONNECTIONS,mp_drawing_styles.get_default_hand_landmarks_style(),mp_drawing_styles.get_default_hand_connections_style())
            thumb_x, thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * 640, hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * 480
            index_x, index_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * 640, hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * 480
            if ((abs(thumb_y-index_y) + abs(thumb_x-index_x))/2) < 15:
                  cv2.putText(annotated_image, 'Ok!', (10,450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
      cv2.imshow('MediaPipe Face Detection', annotated_image)
      annotated_image = cv2.resize(annotated_image, (128,128),interpolation = cv2.INTER_AREA)
      k = cv2.waitKey(1)
      if k == ord('a'):
        if results.detections:
          y,x,k = image.shape
          bounding_box = results.detections[0].location_data.relative_bounding_box;
          cropped_img = image[int(bounding_box.ymin*y)-50:int(bounding_box.height*y)+int(bounding_box.ymin*y)+50, int(bounding_box.xmin*x)-50:int(bounding_box.width*x)+int(bounding_box.xmin*x)+50]
          cv2.imshow("cropped", cv2.resize(cropped_img, (128,128), interpolation = cv2.INTER_AREA))
      if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()