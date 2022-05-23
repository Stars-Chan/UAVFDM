import cv2
import numpy as np
import argparse
from utils import *

def run(imgpath):
    image = cv2.imread(imgpath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray, (3, 3))
    ret, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    kernel = np.ones((5, 5), np.uint8)
    erode = cv2.erode(th, kernel, iterations=1)
    canny = cv2.Canny(erode,50,200)
    lines = cv2.HoughLinesP(canny,1,np.pi/180,30,minLineLength=100,maxLineGap=10)
    lines1 = lines[:,0,:]
    linesArr = []
    for x1,y1,x2,y2 in lines1[:]:
        linesArr.append((x1,y1))
        linesArr.append((x2,y2))
    # 划分直线上点的集合
    linesArr_X = []
    linesArr_Y = []
    linesArr_P = []
    Ymax = Ymin = 0
    # 中线点
    for i in linesArr :
        if(Ymin == 0):
            Ymin = i[1]
        if(i[1] > Ymax):
            Ymax = i[1]
        if(i[1] < Ymin):
            Ymin = i[1]
    Ymid = (Ymin+Ymax)/2
    for i in linesArr :
        if(i[1] > Ymid):
            linesArr_P.append(i)
        else:
            linesArr_X.append(i[0])
            linesArr_Y.append(i[1])
    # 拟合直线
    b,k = linear_regression(linesArr_X, linesArr_Y)
    _X = [250,900]
    _Y = [b + k * x for x in _X]
    cv2.line(image,(_X[0],int(_Y[0])),(_X[1],int(_Y[1])),(0,0,255),2)
    # 计算杆径
    Ds = []
    for i in linesArr_P:
        Ds.append(get_distance_from_point_to_line(i, (_X[0],_Y[0]), (_X[1],_Y[1]))) 
    d = sum(Ds)/len(Ds)
    cv2.line(image,(_X[0],int(_Y[0]+d)),(_X[1],int(_Y[1]+d)),(0,255,0),3)
    #在图片上添加文字信息
    str_result = "result: " + str(d/39.231)
    cv2.putText(image,str_result, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(255,0,0), 1, cv2.LINE_AA)
    show_image(image)
    cv2.imwrite('./results/rod_diameter/BO00000003.bmp', image)

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--imgpath', type=str, default= './images/BO00000003.bmp', help='image path')
    opt = parser.parse_args()
    return opt

def main(opt):
    run(**vars(opt))

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)