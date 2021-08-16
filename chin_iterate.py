#from matplotlib import image
from utils import *
import os
import numpy as np
from tqdm import tqdm
import pandas as p
import nibabel as nib

dataset = pd.read_csv("ukb45494.csv")
for idx in tqdm(os.listdir("data")):
	
	data_dir = os.path.join("data",idx)
	image_path_ED = f"{data_dir}/sa_ED.nii.gz"
	image_path_ES = f"{data_dir}/sa_ES.nii.gz"
	seg_image_path_ED = f"{data_dir}/seg_sa_ED.nii.gz"
	seg_image_path_ES = f"{data_dir}/seg_sa_ES.nii.gz"

	if os.path.exists(image_path_ED) and os.path.exists(seg_image_path_ED) and os.path.exists(image_path_ES) and os.path.exists(seg_image_path_ES):
		try:
			image_ED = nib.load(image_path_ED).get_fdata()
			image_ES = nib.load(image_path_ES).get_fdata()
			seg_ED  = nib.load(seg_image_path_ED).get_fdata()
			seg_ES = nib.load(seg_image_path_ES).get_fdata()
			#BSA = get_body_surface_area(dataset,int(idx))
			chin_ED_list = []
			chin_ES_list = []
			c_list = []

			for i in range(2,image_ED.shape[2]-1):
				chin_ED,comp_ED = get_chin(image_ED[:,:,i],seg_ED[:,:,i])
				chin_ES,comp_ES= get_chin(image_ES[:,:,i],seg_ES[:,:,i])
				compaction = comp_ED/comp_ES
				chin_ED_list.append(chin_ED)
				chin_ES_list.append(chin_ES)
				c_list.append(compaction)

			# slice 5=3 bc we skipped the first two slices
			chin_ED_list = np.array(chin_ED_list)
			median_chin_ED = np.median(chin_ED_list)
			max_chin_ED = np.max(chin_ED_list)
			slice5_chin_ED = chin_ED_list[3]	

			chin_ES_list = np.array(chin_ES_list)
			median_chin_ES = np.median(chin_ES_list)
			max_chin_ES = np.max(chin_ES_list)
			slice5_chin_ES = chin_ES_list[3]	

			c_list = np.array(c_list)
			median_comp = np.median(c_list)
			max_comp = np.max(c_list)
			slice5_comp = c_list[3]	

			with open("chin_traits.csv",'a') as f:
				f.write(f"{idx},{median_chin_ED},{max_chin_ED},{slice5_chin_ED},{median_chin_ES},{max_chin_ES},{slice5_chin_ES},{median_comp},{max_comp},{slice5_comp}\n")
		except ValueError as err:
			print(err.args)
		except:
			print(f"File corrupted")