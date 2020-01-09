#coding:utf-8
#可视化jason文件
import cv2
import os
import json

def main():
    root_folder_path = "./origin_data/"
    save_root_folder_path = "./result/"
    if not os.path.exists(save_root_folder_path):
        os.mkdir(save_root_folder_path)
    folder_list = os.listdir(root_folder_path)
    label = dict()
    for folder_name in folder_list:
        save_son_folder_path = save_root_folder_path + folder_name
        if not os.path.exists(save_son_folder_path):
            os.mkdir(save_son_folder_path)
        object_list = os.listdir(root_folder_path + folder_name)
        for object_name in object_list:
            if(object_name.endswith("jpg")):
                img = cv2.imread(root_folder_path + folder_name + '/' + object_name , -1)
                for object_name_1 in object_list:
                    if(object_name.split('.')[0] == object_name_1.split('.')[0] and object_name_1.endswith("json")):
                        file = open(root_folder_path + folder_name + '/' + object_name_1 , "rb")
                        json_file = json.load(file)
                        for i in range(len(json_file["shapes"])):
                            points = json_file["shapes"][i]["points"]
                            if "label" in json_file["shapes"][i]:
                                label[json_file["shapes"][i]["label"]] = 1
                            lt = (points[0][0], points[0][1])
                            rb = (points[2][0], points[2][1])
                            cv2.rectangle(img, lt, rb, (0, 0, 255), 3)
                            cv2.putText(img , json_file["shapes"][i]["label"] , lt , cv2.FONT_HERSHEY_COMPLEX , 5 , (0 , 255 , 0) , 3)
                        print("img : {} is ok!".format(object_name))
                        cv2.imwrite(save_son_folder_path + '/' + object_name , img)
                        break
    print(label)
    print("OK!")

if __name__ == "__main__":
    main()