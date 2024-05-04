from flask import Flask, render_template

import boto3
from cvzone.HandTrackingModule import HandDetector
import cv2
import time

app = Flask(__name__)

# Function to launch EC2 instance
def launchOS():
    instances = ec2.run_instances(
        ImageId = "ami-0d3f444bc76de0a79",
        KeyName = "aws_key_ssh",
        SecurityGroupIds= ["sg-0ad8c158a053db21b"] ,
        InstanceType="t2.micro",
        MinCount=1,
        MaxCount=1
    )
    launchedID = instances["Instances"][0]["InstanceId"]
    allOS.append(launchedID)
    print("1 instance Launched!")
    print("Total Instances: ", len(allOS))
    print(instances["Instances"][0]["KeyName"]+".pem")
    
    while True:
     response = ec2.describe_instances(InstanceIds=[launchedID])
     state = response['Reservations'][0]['Instances'][0]['State']['Name']
     if state == 'running':
         break
     sleep(5)

    response = ec2.describe_instances(InstanceIds=[launchedID])
    public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
    print(" ")
    print("Use following command to connect:")
    print("ssh -i "+instances["Instances"][0]["KeyName"]+".pem"+" ec2-user@"+public_ip)

# Function to terminate EC2 instance
def terminateOS():
    deli = allOS.pop()
    deleteOS.append(deli)
    ec2.terminate_instances(InstanceIds=(deleteOS))
    print("1 instance Terminated!")
    print("Instances remaining: ", len(allOS))
    deleteOS.clear()

# Function to start the hand gesture recognition
def startGestureRecognition():
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

# Route to render index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Route to launch EC2 instance
@app.route('/launch')
def launch_instance():
    launchOS()
    return 'EC2 instance launched successfully!'

# Route to terminate EC2 instance
@app.route('/terminate')
def terminate_instance():
    terminateOS()
    return 'EC2 instance terminated successfully!'

# Route to start gesture recognition
@app.route('/start-gesture-recognition')
def start_gesture():
    startGestureRecognition()
    return 'Gesture recognition started!'

if __name__ == '__main__':
    app.run(debug=True)
