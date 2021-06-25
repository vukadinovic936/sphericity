from matplotlib import image
from utils import *
import os
import numpy as np
from tqdm import tqdm

for d in tqdm(os.listdir("data")):
    data_dir = os.path.join("data",d)
    image_path = f"{data_dir}/sa.nii.gz"
    seg_image_path = f"{data_dir}/seg_sa.nii.gz"
    if os.path.exists(image_path) and os.path.exists(seg_image_path):
        with open("MeanPapillaryMass.csv",'a') as f:
            f.write(f"{d},{np.mean(get_papillary_mass(image_path,seg_image_path))}\n")

# cat MeanPapillaryMass.csv


