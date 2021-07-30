#from matplotlib import image
from utils import *
import os
import numpy as np
from tqdm import tqdm
import pandas as pd

# TODO: CREATE A QUALITY CHECK, SOMETIMES A BOX APPEARS IN A DIFFERENT LOCATION

dataset = pd.read_csv("ukb45494.csv")

for idx in tqdm(os.listdir("data")):
    data_dir = os.path.join("data",idx)

    image_path = f"{data_dir}/la_4ch.nii.gz"
    seg_image_path = f"{data_dir}/seg4_la_4ch.nii.gz"
    if os.path.exists(image_path) and os.path.exists(seg_image_path):
        try:
            orig_image, masked_image,shape_properties  = segment_right_ventricle(image_path,seg_image_path)
            
            BSA = get_body_surface_area(dataset,int(idx))
            mean_height = np.mean(np.array(shape_properties)[0,:,0])/BSA
            mean_width = np.mean(np.array(shape_properties)[0,:,1])/BSA
            mean_angle = np.mean(np.array(shape_properties)[0,:,2])/BSA

            max_height = np.max(np.array(shape_properties)[0,:,0])/BSA
            max_width = np.max(np.array(shape_properties)[0,:,1])/BSA
            max_angle = np.max(np.array(shape_properties)[0,:,2])/BSA

            min_height = np.min(np.array(shape_properties)[0,:,0])/BSA
            min_width = np.min(np.array(shape_properties)[0,:,1])/BSA
            min_angle = np.min(np.array(shape_properties)[0,:,2])/BSA
        
            with open("LA_RV_traits.csv",'a') as f:
                f.write(f"{idx},{mean_height},{max_height},{min_height},{mean_width},{max_width},{min_width},{mean_angle},{max_angle},{min_angle}\n")
        except ValueError as err:
            print(err.args)
        except:
            print(f"File corrupted")


# name = "1002625"
# img_path = f"data/{name}/la_4ch.nii.gz"
# seg_img_path = f"data/{name}/seg4_la_4ch.nii.gz"
#
#
# image,masked_image,shape_props = segment_left_ventricle(img_path,seg_img_path)
# create_video_lv(image,masked_image,shape_props)
#
# figs,dists = segment_mitral_valve(img_path,seg_img_path)
# create_video_mitral_valve(figs,dists)
#
# image,masked_image,shape_props = segment_right_ventricle(img_path,seg_img_path)
# create_video_lv(image,masked_image,shape_props)
#
