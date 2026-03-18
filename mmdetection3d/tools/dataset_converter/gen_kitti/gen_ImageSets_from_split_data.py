import os
import random
from utils import read_json, mkdir_p, write_txt


def gen_ImageSet_from_split_data(ImageSets_path, split_data_path, sensor_view="vehicle"):
    # 读取split数据
    # split_data = read_json(split_data_path)
    # test_file = ""
    # train_file = ""
    # val_file = ""

    # if "vehicle_split" in split_data.keys():
    #     sensor_view = sensor_view + "_split"
    #     split_data = split_data[sensor_view]
    # # 获取train数据
    # train_data = split_data.get("train", [])
    
    # # 随机选择十分之一的数据作为验证集（val）
    # num_val = len(train_data) // 10  # 十分之一
    # val_data = random.sample(train_data, num_val)  # 随机抽取十分之一

    # # 从train中移除val数据
    # train_data = [item for item in train_data if item not in val_data]

    # # 更新split_data中的train和val
    # split_data["train"] = train_data
    # split_data["val"] = val_data

    # # 写入更新后的数据文件
    # train_file = "\n".join(split_data["train"]) + "\n"
    # val_file = "\n".join(split_data["val"]) + "\n"

    # # The test part of the dataset has not been released
    # test_file = ""

    # # 将数据保存到对应的txt文件中
    # mkdir_p(ImageSets_path)
    # write_txt(os.path.join(ImageSets_path, "test.txt"), test_file)
    # write_txt(os.path.join(ImageSets_path, "trainval.txt"), train_file + val_file)
    # write_txt(os.path.join(ImageSets_path, "train.txt"), train_file)
    # write_txt(os.path.join(ImageSets_path, "val.txt"), val_file)

    split_data = read_json(split_data_path)
    test_file = ""
    train_file = ""
    val_file = ""

    if "vehicle_split" in split_data.keys():
        sensor_view = sensor_view + "_split"
        split_data = split_data[sensor_view]
    for i in range(len(split_data["train"])):
        name = split_data["train"][i]
        train_file = train_file + name + "\n"

    for i in range(len(split_data["val"])):
        name = split_data["val"][i]
        val_file = val_file + name + "\n"

    # The test part of the dataset has not been released
    # for i in range(len(split_data["val"])):
    #     name = split_data["val"][i]
    #     test_file = test_file + name + "\n"

    trainval_file = train_file + val_file

    mkdir_p(ImageSets_path)
    write_txt(os.path.join(ImageSets_path, "test.txt"), test_file)
    write_txt(os.path.join(ImageSets_path, "trainval.txt"), trainval_file)
    write_txt(os.path.join(ImageSets_path, "train.txt"), train_file)
    write_txt(os.path.join(ImageSets_path, "val.txt"), val_file)

def gen_ImageSet_from_split_data_seq(ImageSets_path, json_root, sensor_view="vehicle"):
    # 读取split数据
    split_data = {}
    test_file = ""
    train_file = ""
    val_file = ""

    # 获取json_root目录下所有json文件的文件名（不带扩展名）
    json_files = [f for f in os.listdir(json_root) if f.endswith('.json')]
    
    # 提取文件名（去掉.json后缀）
    all_files = [os.path.splitext(f)[0] for f in json_files]
    
    # 整个数据集作为训练集（后续从中划分验证集）
    train_data = all_files

    # 计算2/7的数据作为验证集（val）
    total_samples = len(train_data)

    raw_val_size = int(total_samples * (2.0/7.0))  # 原始验证集大小
    
    # 确保验证集大小能被4整除
    adjusted_val_size = raw_val_size - (raw_val_size % 4)
    
    # 随机选择2/7的数据作为验证集（val）
    # num_val = int(len(train_data) * 0.4)
    val_data = random.sample(train_data, adjusted_val_size)  # 随机抽取40%

    # 从train中移除val数据
    train_data = [item for item in train_data if item not in val_data]

    # 对划分后的数据进行排序（从小到大）
    train_data = sorted(train_data, key=lambda x: int(x))
    val_data = sorted(val_data, key=lambda x: int(x))

    # 更新split_data中的train和val
    split_data["train"] = train_data
    split_data["val"] = val_data

    # 写入更新后的数据文件
    train_file = "\n".join(split_data["train"]) + "\n"
    val_file = "\n".join(split_data["val"]) + "\n"

    # The test part of the dataset has not been released
    test_file = ""

    # 将数据保存到对应的txt文件中
    mkdir_p(ImageSets_path)
    write_txt(os.path.join(ImageSets_path, "test.txt"), test_file)
    write_txt(os.path.join(ImageSets_path, "trainval.txt"), train_file + val_file)
    write_txt(os.path.join(ImageSets_path, "train.txt"), train_file)
    write_txt(os.path.join(ImageSets_path, "val.txt"), val_file)