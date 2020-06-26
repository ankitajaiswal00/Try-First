import cv2
import numpy as np

def pose_parse(person_name):
    MODE = "COCO"
    protoFile = "./pose_deploy_linevec.prototxt"
    weightsFile = "./pose_iter_440000.caffemodel"
    nPoints = 18
    POSE_PAIRS = [ [1,0],[1,2],[1,5],[2,3],[3,4],[5,6],[6,7],[1,8],[8,9],[9,10],[1,11],[11,12],[12,13],[0,14],[0,15],[14,16],[15,17]]

    frame = cv2.imread("./Database/val/person/"+person_name+".jpg")
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
    inWidth = 192
    inHeight = 256
    inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight),
                            (0, 0, 0), swapRB=False, crop=False)
    net.setInput(inpBlob)
    output = net.forward()
    H = output.shape[2]
    W = output.shape[3]
    a = []
    for i in range(nPoints):
        probMap = output[0, i, :, :]
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
        x = (frameWidth * point[0]) / W
        y = (frameHeight * point[1]) / H
        a.append(x);
        a.append(y);
        a.append(prob)
    dicti = {"pose_keypoints":a}
    people = []
    people.append(dicti)
    dicti = {"people":people}
    import json     
    with open("./Database/val/pose/"+person_name+"_keypoints.json", "w") as outfile:  
        json.dump(dicti, outfile)