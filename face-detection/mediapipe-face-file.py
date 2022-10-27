# find face and crop

import cv2
import mediapipe as mp
import sys
from time import sleep
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
font = cv2.FONT_HERSHEY_SIMPLEX

IMAGE_FILES = [sys.argv[1]]
with mp_face_detection.FaceDetection(
    model_selection=0, min_detection_confidence=0.7) as face_detection:        
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    annotated_image = image
    results = face_detection.process(image)
    if results.detections:
      i = 0
      for detection in results.detections:
        annotated_image = image
        y,x,k = image.shape
        bounding_box = detection.location_data.relative_bounding_box;
        cropped_img = image[int(bounding_box.ymin*y)-50:int(bounding_box.height*y)+int(bounding_box.ymin*y)+50, int(bounding_box.xmin*x)-25:int(bounding_box.width*x)+int(bounding_box.xmin*x)+50]
        cv2.imwrite("show" + str(i) + ".png", cropped_img)
        i = i + 1
    # if results.detections:
        #   y,x,k = image.shape
    #   bounding_box = results.detections[1].location_data.relative_bounding_box;
    #   cropped_img = image[int(bounding_box.ymin*y)-50:int(bounding_box.height*y)+int(bounding_box.ymin*y)+50, int(bounding_box.xmin*x)-50:int(bounding_box.width*x)+int(bounding_box.xmin*x)+50]
    #   cv2.imshow("cropped", cv2.resize(image, (128,128), interpolation = cv2.INTER_AREA))
      #cv2.imwrite("cropped" + str(idx) + '.png', cropped_img)