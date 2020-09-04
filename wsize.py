import cv2
from math import sqrt
import numpy as np
from parser import get

def pose_parse(file_path):
    MODE = "COCO"
    protoFile = "./pose_deploy_linevec.prototxt"
    weightsFile = "./pose_iter_440000.caffemodel"
    nPoints = 18
    POSE_PAIRS = [ [1,0],[1,2],[1,5],[2,3],[3,4],[5,6],[6,7],[1,8],[8,9],[9,10],[1,11],[11,12],[12,13],[0,14],[0,15],[14,16],[15,17]]

    frame = cv2.imread(file_path)
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    frameCopy = np.copy(frame) #................................
    threshold = 0.1 #...........................................
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

    points = []            #.......................................

    for i in range(nPoints):   
         # confidence map of corresponding body's part.
        probMap = output[0, i, :, :]

         # Find global maxima of the probMap.
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

        # Scale the point to fit on the original image
        x = (frameWidth * point[0]) / W
        y = (frameHeight * point[1]) / H
        a.append(x);
        a.append(y);
        #a.append(prob)


    # # ================================cropping Image till Torso=======
    # frame = frame[0: int((a[17]+a[23])/2)+17 , int(a[16]-33): int(a[22]+35) ]
    # frame = cv2.resize(frame, (192, 256))  
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  

    return a

# ================================Pose Keypoints diagram=============================== 
   
    #     cv2.circle(frameCopy, (int(x), int(y)), 8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
    #     cv2.putText(frameCopy, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, lineType=cv2.LINE_AA)

    #     # Add the point to the list if the probability is greater than the threshold
    #     points.append((int(x), int(y)))
 

    # # Draw Skeleton
    # for pair in POSE_PAIRS:
    #     partA = pair[0]
    #     partB = pair[1]

    #     if points[partA] and points[partB]:
    #         cv2.line(frame, points[partA], points[partB], (0, 255, 255), 2)
    #         cv2.circle(frame, points[partA], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)


    # # cv2.imwrite('Output-Keypoints-fro.jpg', frameCopy)
    # # cv2.imwrite('Output-Skeleton-fro.jpg', frame)

    # return a



def women_size_predict(file_path,input_height, unit):
    #=============================saving co-ordinates for various paths=====================================
    pt = pose_parse(file_path)
    
    xc = []
    yc = []
    for i in range(18):
        # print(pt[2*i], pt[2*i+1])
        xc.append(pt[2*i])
        yc.append(pt[2*i+1])
    
    xc = np.array(xc)
    yc = np.array(yc)
    
    #=============================scaling_factor===============================
    input_height = float(input_height)
    if unit=='cm':
        input_height = input_height/2.54
    calculated_height = abs((yc[11]+yc[14])/2 - yc[0])
    sf = input_height / calculated_height 
 
    #=============================Women Size Chart=============================
    
    s = sqrt((xc[5] - xc[2])**2 + (yc[5] - yc[2])**2)
    w = sqrt((xc[11] - xc[8])**2 + (yc[11] - yc[8])**2)
    
    shoulders= s * sf
    bust = s*1.4 * sf
    sleeve = (sqrt((xc[1] - xc[5])**2 + (yc[5] - yc[1])**2) + sqrt((xc[6] - xc[5])**2 + (yc[6] - yc[5])**2) + sqrt((xc[7] - xc[6])**2 + (yc[7] - yc[6])**2))/2 * sf
    waist = w*1.6 * sf
    hip = w*2 * sf
    inseam = (sqrt((xc[11] - xc[12])**2 + (yc[12] - yc[12])**2) + sqrt((xc[12] - xc[13])**2 + (yc[12] - yc[13])**2)) * 0.91 * sf
    
    # =============================== Conversion to inches =====================
    
    shoulders = round(shoulders/2.54,1)
    bust = round(bust/2.54,1) 
    sleeve = round(sleeve/2.54,1)
    waist = round(waist/2.54,1)
    hip = round(hip/2.54) 
    inseam = round(inseam/2.54,1)
    
    # ==================================Printing the dimnesions ====================
    
    dims = [shoulders,  bust, sleeve, waist, hip, inseam]
    # print(shoulders) 
    # print(bust) 
    # print(sleeve)
    # print(waist) 
    # print(hip) 
    # print(inseam) 
    
    
    # ================================ Classification on basis of size chart ===============
    
    sample_size=[]
    if shoulders <= 23:
        sample_size.append(1)
    elif shoulders > 23 and shoulders <= 24:
        sample_size.append(2)
    elif shoulders > 24 and shoulders <= 25:
        sample_size.append(3)
    elif shoulders > 25 and shoulders <= 26:
        sample_size.append(4)
    elif shoulders > 26 and shoulders <= 27:
        sample_size.append(5)
    elif shoulders > 27 and shoulders <= 28:
        sample_size.append(6)
    else:
        sample_size.append(7)
    
    
    
    if bust <= 34:
        sample_size.append(1)
    elif bust > 34 and bust <= 36:
        sample_size.append(2)
    elif bust > 36 and bust <= 38:
        sample_size.append(3)
    elif bust > 38 and bust <= 40:
        sample_size.append(4)
    elif bust > 40 and bust <= 42:
        sample_size.append(5)
    elif bust > 42 and bust <= 44:
        sample_size.append(6)
    else:
        sample_size.append(7)
    
    
    if sleeve <= 23:
        sample_size.append(1)
    elif sleeve > 23 and sleeve <= 24:
        sample_size.append(2)
    elif sleeve > 24 and sleeve <= 26:
        sample_size.append(3)
    elif sleeve > 26 and sleeve <= 27:
        sample_size.append(4)
    elif sleeve > 27 and sleeve <= 28:
        sample_size.append(5)
    elif sleeve > 28 and sleeve <= 29:
        sample_size.append(6)
    else:
        sample_size.append(7)
    
    
    if waist <= 16:
        sample_size.append(1)
    elif waist > 16 and waist <= 20:
        sample_size.append(2)
    elif waist > 20 and waist <= 25:
        sample_size.append(3)
    elif waist > 25 and waist <= 28:
        sample_size.append(4)
    elif waist > 28 and waist <= 31:
        sample_size.append(5) 
    elif waist > 31 and waist <= 33:
        sample_size.append(6) 
    else:
        sample_size.append(7)
    
    if hip <= 20:
        sample_size.append(1)
    elif hip > 20 and hip <= 24:
        sample_size.append(2)
    elif hip > 24 and hip <= 31:
        sample_size.append(3)
    elif hip > 30 and hip <= 33:
        sample_size.append(4)
    elif hip > 33 and hip <= 37:
        sample_size.append(5)
    elif hip > 37 and hip <= 40:
        sample_size.append(6)
    else:
        sample_size.append(7)
    
    
    
    def most_frequent(List): 
        return max(set(List), key = List.count) 
      
    
    f = (most_frequent(sample_size)) 
    
    if f == 1:
        ans = 'XS'
    elif f == 2:
        ans = 'S'
    elif f == 3:
        ans = 'M'
    elif f == 4:
        ans = 'L'
    elif f == 5:
        ans = 'XL'
    elif f == 6:
        ans = 'XLL'
    else:
        ans = 'XLLL'
    
    # print( calculated_height )
    # print( sample_size )
    return ans 

#=======================================================================




#=============================Key Point Labels===========================
# {0,  "Nose"},
# {1,  "shoulders"},
# {2,  "RShoulder"},
# {3,  "RElbow"},
# {4,  "RWrist"},
# {5,  "LShoulder"},
# {6,  "LElbow"},
# {7,  "LWrist"},
# {8,  "MidHip"},
# {9,  "RHip"},
# {10, "RKnee"},
# {11, "RAnkle"},
# {12, "LHip"},
# {13, "LKnee"},
# {14, "LAnkle"},
# {15, "REye"},
# {16, "LEye"},
# {17, "REar"},
# {18, "LEar"}

#========================================================================








    # dicti = {"pose_keypoints":a}
    # people = []
    # people.append(dicti)
    # dicti = {"people":people}
    # import json  
    # get()   
    # with open("./static/Database/val/pose/"+person_name+"_keypoints.json", "w") as outfile:  
    #     json.dump(dicti, outfile)