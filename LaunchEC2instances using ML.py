#!/usr/bin/env python
# coding: utf-8

# In[1]:


#pip install boto3

import boto3

ec2 = boto3.client('ec2',
                   'ap-south-1',
                   aws_access_key_id='...',
                   aws_secret_access_key='...')


# In[2]:


allOS = []


# In[3]:


def launchOS():
    instances = ec2.run_instances(
        ImageId = "ami-0a2acf24c0d86e927",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        SecurityGroupIds=["sg-08df27de4d97d801f"]
    )
    launchedID = instances["Instances"][0]["InstanceId"]
    allOS.append(launchedID)
    print("1 instance Launched!")
    print("Total Instances: ", len(allOS))


# In[4]:


def terminateOS():
    deleteOS = allOS.pop()
    ec2.terminate_instances(InstanceIds=(allOS))
    print("1 instance Terminated!")
    print("Instances remaining: ", len(allOS))


# In[5]:


#pip install opencv-python
#pip install cvzone
#pip install mediapipe

from cvzone.HandTrackingModule import HandDetector
import cv2
import time


# In[6]:


def start():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)
    while True:
        # Get image frame
        success, img = cap.read()
        # Find the hand and its landmarks
        hands = detector.findHands(img, draw=False) 
    
        if hands:
            lmlist = hands[0]
            totalFinger = detector.fingersUp(lmlist)
            if totalFinger == [0, 1, 1, 0, 0]:
                launchOS()
                cv2.imshow("Image", img)
                time.sleep(3)
            elif totalFinger == [0, 1, 0, 0, 0]:
                terminateOS()
                cv2.imshow("Image", img)
                time.sleep(3)

        # Display
        cv2.imshow("Image", img)
        if cv2.waitKey(100) == 13:
            break
    cap.release()
    cv2.destroyAllWindows()


# In[8]:
start()


