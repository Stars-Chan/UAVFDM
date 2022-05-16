import cv2
import argparse
from utils import *

def run(imgpath):
    image = cv2.imread(imgpath)
    h, w, _=image.shape
    corArr = []
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (11, 11))
    corners = cv2.goodFeaturesToTrack(blur,46,0.01,10)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    spCorners = cv2.cornerSubPix(blur,corners,(11,11),(-1,-1),criteria)
    image = cv2.drawChessboardCorners(image, (7,6), spCorners,False)
    # 去掉图像两侧角点
    trim = 20
    for index in range(len(spCorners)) :
        i = spCorners[index][0]
        if(i[0] > trim and i[0] < (w-trim)):
            corArr.append(i)
    # 划分角点集合
    corArr_X = []
    corArr_Y = []
    corArr_P = []
    Ymax = Ymin = 0
    # 中线点
    for i in corArr :
        if(Ymin == 0):
            Ymin = i[1]
        if(i[1] > Ymax):
            Ymax = i[1]
        if(i[1] < Ymin):
            Ymin = i[1]
    # 划分直线、点集
    bias = 10
    for i in corArr :
        if(i[1] + bias > Ymax):
            corArr_P.append(i)
        elif(i[1]-bias < Ymin ):
            corArr_X.append(i[0])
            corArr_Y.append(i[1])
    # 拟合直线
    b,k = linear_regression(corArr_X, corArr_Y)
    _X = [0,600]
    _Y = [b + k * x for x in _X]
    # 计算大径
    MDs = []
    for i in corArr_P:
        MDs.append(get_distance_from_point_to_line(i, (_X[0],_Y[0]), (_X[1],_Y[1]))) 
    md = sum(MDs)/len(MDs)
    print("外螺纹大径测量结果（pixel）：",md)
    show_image(image)

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--imgpath', type=str, default= './image/SC00000001.bmp', help='image path')
    opt = parser.parse_args()
    return opt

def main(opt):
    run(**vars(opt))

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)