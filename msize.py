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
    return a
   
# ==============================================================================
def men_size_predict(file_path, input_height, unit):
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
    if unit=='inch':
        input_height = input_height*2.54

    calculated_height = abs((yc[11]+yc[14])/2 - yc[0])
    sf = input_height / calculated_height 
 
    #=============================Men Size Chart=============================

    s = sqrt((xc[5] - xc[2])**2 + (yc[5] - yc[2])**2)
    w = sqrt((xc[11] - xc[8])**2 + (yc[11] - yc[8])**2)
    
    neck = round(s/2 * sf, 1)
    chest = round(s*1.4 * sf, 1)
    sleeve = round((sqrt((xc[1] - xc[5])**2 + (yc[5] - yc[1])**2) + sqrt((xc[6] - xc[5])**2 + (yc[6] - yc[5])**2) + sqrt((xc[7] - xc[6])**2 + (yc[7] - yc[6])**2))/2 * sf,1)
    waist = round(w*1.6 * sf,1)
    hip = round(w*2 * sf , 1)
    inseam = round((sqrt((xc[11] - xc[12])**2 + (yc[12] - yc[12])**2) + sqrt((xc[12] - xc[13])**2 + (yc[12] - yc[13])**2)) * 0.91 *sf , 1)
    
    
    dims = [neck, chest, sleeve, waist, hip, inseam]
    # print(neck) 
    # print(chest) 
    # print(sleeve)
    # print(waist) 
    # print(hip) 
    # print(inseam) 
 
  # ================================ Classification on basis of size chart ===============   
    
    sample_size=[]
    if neck <= 39:
        sample_size.append(1)
    elif neck > 39 and neck <= 42:
        sample_size.append(2)
    elif neck > 42 and neck <= 44:
        sample_size.append(3)
    else:
        sample_size.append(4)
    
    
    
    if chest <= 98:
        sample_size.append(1)
    elif chest > 98 and chest <= 106:
        sample_size.append(2)
    elif chest > 106 and chest <= 113:
        sample_size.append(3)
    else:
        sample_size.append(4)
    
    
    if sleeve <= 86.5:
        sample_size.append(1)
    elif sleeve > 86.5 and sleeve <= 89:
        sample_size.append(2)
    elif sleeve > 89 and sleeve <= 91.5:
        sample_size.append(3)
    else:
        sample_size.append(4)
    
    
    if waist <= 86.5:
        sample_size.append(1)
    elif waist > 86.5 and waist <= 89:
        sample_size.append(2)
    elif waist > 89 and waist <= 91.5:
        sample_size.append(3)
    else:
        sample_size.append(4)
    
    if hip <= 102:
        sample_size.append(1)
    elif hip > 102 and hip <= 108:
        sample_size.append(2)
    elif hip > 108 and hip <= 116.5:
        sample_size.append(3)
    else:
        sample_size.append(4)
    
    
    if inseam <= 77.5:
        sample_size.append(1)
    elif inseam > 79 and inseam <= 81:
        sample_size.append(2)
    elif inseam > 81 and inseam <= 82.5:
        sample_size.append(3)
    else:
        sample_size.append(4)
    
    
    def most_frequent(List): 
        return max(set(List), key = List.count) 
      
    
    f = (most_frequent(sample_size)) 
    
    if f == 1:
        ans = 'S'
    elif f == 2:
        ans = 'M'
    elif f == 3:
        ans = 'L'
    else:
        ans = 'XL'
    
    
    # print( sample_size )
    # print( ans)
    return ans
#=======================================================================




#=============================Key Point Labels===========================
# {0,  "Nose"},
# {1,  "Neck"},
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