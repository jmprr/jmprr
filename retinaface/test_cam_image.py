import cv2
import numpy as np
import os
from retinaface import RetinaFace
import os

thresh = 0.8
scales = [1024, 1980]

gpuid = 0

detector = RetinaFace('./model/R50',0,'net3')

cap = cv2.VideoCapture(0)
for i in range(1):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2.imwrite('./storage/face.png', frame)
del(cap)

img = cv2.imread('./storage/face.png')
print(img.shape)
im_shape = img.shape
target_size = scales[0]
max_size = scales[1]
im_size_min = np.min(im_shape[0:2])
im_size_max = np.max(im_shape[0:2])
#im_scale = 1.0
#if im_size_min>target_size or im_size_max>max_size:
im_scale = float(target_size) / float(im_size_min)
# prevent bigger axis from being more than max_size:
if np.round(im_scale * im_size_max) > max_size:
    im_scale = float(max_size) / float(im_size_max)

print('im_scale', im_scale)

scales = [im_scale]
flip = False

faces, landmarks = detector.detect(img,
                                    thresh,
                                    scales=scales,
                                    do_flip=flip)
print(faces.shape, landmarks.shape)

if faces is not None:
    print('find', faces.shape[0], 'faces')
    for i in range(faces.shape[0]):
        #print('score', faces[i][4])
        box = faces[i].astype(np.int64)
        #color = (255,0,0)
        color = (0, 0, 255)
        cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color, 2)
        img_crop = img[box[1]:box[3], box[0]:box[2]]
        """ if landmarks is not None:
            landmark5 = landmarks[i].astype(np.int64)
            #print(landmark.shape)
            for l in range(landmark5.shape[0]):
                color = (0, 0, 255)
                if l == 0 or l == 3:
                    color = (0, 255, 0)
                cv2.circle(img, (landmark5[l][0], landmark5[l][1]), 1, color, 2) """
                #crop_img = img[box[1]:box[3], box[0]:box[2]] # img[y_min:y_max, x_min:x_max]
                
    """ filename = './detector_test.jpg'
    print('writing', filename)
    cv2.imwrite(filename, img) """
    
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    os.remove('./storage/face.png')
    