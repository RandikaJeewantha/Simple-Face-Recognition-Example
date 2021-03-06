import cv2
import numpy as np
import face_recognition
import os

path = '../Images of Faces'
images = []
classNames = []
myList = os.listdir(path)
print('Image List: ',myList)

for c1 in myList:
    curImg = cv2.imread(f'{path}/{c1}')
    images.append(curImg)
    classNames.append(os.path.splitext(c1)[0])
    
print('Name List: ', classNames)

def findEncodings(images):
    encodeList = []
    
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    
    return encodeList

encodeListKnown = findEncodings(images)

print('Encoding Complete')

capture = cv2.VideoCapture(0)

def checkIsAcceptable(value):
            
    if value <= 0.4:
        return True
                
    else:
        return False

while True:

    success, img = capture.read()
    imgs = cv2.resize(img, (0,0), None, 0.25,0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)
   
    facesCurFrame = face_recognition.face_locations(imgs)
    encodesCurFrame = face_recognition.face_encodings(imgs, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        
        print('Face Difference: ', faceDis)
        
        matchIndex = np.argmin(faceDis)
        
        minValue = np.amin(faceDis) 
        
        isAcceptable = checkIsAcceptable(minValue)
        
        print('Min Value: ', minValue)
        print('Is It In Acceptable Level (<0.4): ', isAcceptable)
        
        if isAcceptable:
            name = classNames[matchIndex].upper()
            
        else:
            name = 'UnKnown'
        
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            
    cv2.imshow('Webcam', img)
    cv2.waitKey(1)