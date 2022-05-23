import cv2
import numpy as np
import argparse
from utils import show_image

def run(imgpath):
    image = cv2.imread(imgpath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 滤波去噪
    blur = cv2.blur(gray, (7, 7))
    # 二值化
    ret, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    canny = cv2.Canny(th,25,200)
    # 霍夫找圆,minDist表示两个圆之间圆心的最小距离;param1表示传递给canny边缘检测算子的高阈值，而低阈值为高阈值的一半;param2检测圆的阈值，越大，圆形越完美；
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, minDist=50, param1=100, param2=40, minRadius=50, maxRadius=1000)
    circles = circles[0, :, :]
    circles = np.uint16(np.around(circles))
    for i in circles[:]:
        # 绘制外圈圆（红色）
        cv2.circle(image, (i[0], i[1]), i[2], (0, 0, 255), 3)
        # 绘制圆心（绿色）
        cv2.circle(image, (i[0], i[1]), 2, (0, 255,0), 3)
        # print("孔径测量结果（pixel）：",i[2]*2)
        str_result = "result: " + str(i[2]*2/39.231)
        #在图片上添加文字信息
        cv2.putText(image,str_result, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(255,0,0), 1, cv2.LINE_AA)
    show_image(image)
    cv2.imwrite('./results/aperture/GA00000010.bmp', image)

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--imgpath', type=str, default= './images/GA00000010.bmp', help='image path')
    opt = parser.parse_args()
    return opt

def main(opt):
    run(**vars(opt))

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)
