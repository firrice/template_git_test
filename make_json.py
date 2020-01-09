#coding:utf-8
import json
import base64
from PIL import Image
import io
import os
import cv2
import numpy as np

def generate_json(file_dir, file_name):
    str_json = {}
    shapes = []
    # 读取坐标
    fr = open(os.path.join(file_dir, file_name))
    for line in fr.readlines():  # 逐行读取，滤除空格等
        lineArr = line.strip().split(' ')
        points = []
        points.append([float(int(lineArr[0])), float(int(lineArr[1]))])
        points.append([float(int(lineArr[2])), float(int(lineArr[3]))])
        points.append([float(int(lineArr[4])), float(int(lineArr[5]))])
        points.append([float(int(lineArr[6])), float(int(lineArr[7]))])
        print(points)
        shape = {}
        shape["label"] = "plate_1"
        shape["points"] = points
        shape["line_color"] = []
        shape["fill_color"] = []
        shape["flags"] = {}
        shapes.append(shape)
    str_json["version"] = "3.14.1"
    str_json["flags"] = {}
    str_json["shapes"] = shapes
    str_json["lineColor"] = [0, 255, 0, 128]
    str_json["fillColor"] = [255, 0, 0, 128]
    picture_basename = file_name.replace('.txt', '.jpg')
    str_json["imagePath"] = picture_basename
    img = cv2.imread(os.path.join(file_dir, picture_basename))
    str_json["imageHeight"] = img.shape[0]
    str_json["imageWidth"] = img.shape[1]
    str_json["imageData"] = base64encode_img(os.path.join(file_dir, picture_basename))
    return str_json


def base64encode_img(image_path):
    src_image = Image.open(image_path)
    output_buffer = io.BytesIO()
    src_image.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data).decode('utf-8')
    return base64_str


file_dir = "./result_roialign_refinement/"
txt_name = './result_roialign_refinement.txt'
txt = open(txt_name, 'r')
lines = txt.readlines()
#利用总的txt为每个图片单独生成txt
for line in lines:
    line = line.strip('\n')
    old_content = line.split(' ')
    new_content = []
    img_name = old_content[0]
    #new_content.append(img_name)
    new_son_txt_name = img_name.replace('.jpg', '.txt')
    new_son_txt = open(file_dir + new_son_txt_name, 'a')
    for i in range(int(((len(old_content) - 1) / 4))):
        new_son_txt.write(old_content[i * 4 + 1] + ' ') #lt_x
        new_son_txt.write(old_content[i * 4 + 2] + ' ') #lt_y
        new_son_txt.write(old_content[i * 4 + 3] + ' ') #rt_x
        new_son_txt.write(old_content[i * 4 + 2] + ' ') #rt_y
        new_son_txt.write(old_content[i * 4 + 3] + ' ') #rb_x
        new_son_txt.write(old_content[i * 4 + 4] + ' ') #rb_y
        new_son_txt.write(old_content[i * 4 + 1] + ' ') #lb_x
        new_son_txt.write(old_content[i * 4 + 4] + ' ') #lb_y
        new_son_txt.write('\n')
    new_son_txt.close()
txt.close()
#
file_name_list = [file_name for file_name in os.listdir(file_dir) \
						  if file_name.lower().endswith('txt')]
for file_name in file_name_list:
    str_json = generate_json(file_dir,file_name)
    json_data = json.dumps(str_json)
    jsonfile_name = file_name.replace(".txt",".json")
    f = open(os.path.join(file_dir, jsonfile_name), 'w')
    f.write(json_data)
    f.close()