#### WE WILL EXTRACT ALL POSSIBLE FROM LONG AXIS####
import numpy as np
import os
from utils import *
from tqdm import tqdm


for idx in tqdm(os.listdir("data/")):
	try:
		image_path = f"data/{idx}/la_4ch.nii.gz"
		seg_image_path=f"data/{idx}/seg4_la_4ch.nii.gz"
		orig_image, masked_image,shape_properties = segment_right_ventricle(image_path,seg_image_path)
#		figs,dists = segment_mitral_valve(image_path, seg_image_path)
		height = shape_properties[0,:,1]
		width = shape_properties[0,:,0]
		angle = shape_properties[0,:,2]
		height = (np.max(height)-np.min(height))/np.max(height)
		width = (np.max(width)-np.min(width))/np.max(width)
		angle = np.max(angle)-np.min(angle)
#		mitral = (np.max(dists)-np.min(dists))/np.max(dists)
		with open("LA_RV_traits.csv",'a') as f:
			f.write(f"{idx},{height},{width},{angle},{mitral}\n")
	except:
		print("FILE CORRUPTEd")
# height max-min

# widht max-min

# angle we'll do max-min

# distace we'll do max-min
