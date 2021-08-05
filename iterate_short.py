#from matplotlib import image
from utils import *
import os
import numpy as np
from tqdm import tqdm
import pandas as pd
from ukbb_cardiac.common.cardiac_utils import *
# TODO: CREATE A QUALITY CHECK, SOMETIMES A BOX APPEARS IN A DIFFERENT LOCATION

dataset = pd.read_csv("ukb45494.csv")

for idx in tqdm(os.listdir("data")):
    data_dir = os.path.join("data",idx)

    image_path = f"{data_dir}/sa.nii.gz"
    seg_image_path = f"{data_dir}/seg_sa.nii.gz"
    if os.path.exists(image_path) and os.path.exists(seg_image_path):
        try:

            BSA = get_body_surface_area(dataset,int(idx))
            mass_per_frame = get_papillary_mass(image_path,seg_image_path)/BSA
            pap_mass_mean = np.mean(mass_per_frame) # mass in g

            wt = np.array(evaluate_wall_thickness_per_frame(seg_image_path,return_max=False))/BSA
            max_wt = np.array(evaluate_wall_thickness_per_frame(seg_image_path,return_max=True))/BSA
            mean_thickness = np.mean(wt)
            max_thickness = np.mean(max_wt)
            biggest_change = np.max(FirstDeriv(wt))
            smallest_change = np.min(FirstDeriv(wt)) # in mm

            with open("SA_traits.csv",'a') as f:
                f.write(f"{idx},{pap_mass_mean},{mean_thickness},{max_thickness},{biggest_change},{smallest_change}\n")
        except ValueError as err:
            print(err.args)
        except:
            print(f"File corrupted")