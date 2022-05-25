from re import I
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
from scipy import signal
from matplotlib import animation, rc
import pandas as pd

id_dict = {"131338-0.0":"cardiomyopathy",
        "131350-0.0":"atrial_fibrillation",
        "131354-0.0":"heart_failure_date",
        "131346-0.0":"cardiac_arrest",
        "131286-0.0": "hypertension"}

def isnan(ob):
    """ Check if the object is NaN
        Nans are not equal to iteself
    """
    return ob!=ob

def comes_after(date1,date2):
    """
    Arguments:
        date1 : str
            date in a format YYYY:MM:DD
        date 2 : str
            date in a format YYYY:MM:DD

        Checks if a date1 comes after date2
    """
    if(date.fromisoformat(date1) - date.fromisoformat(date2)).days > 0:
        return True
    else:
        return False

def diff_in_days(date1,date2):
        return (date.fromisoformat(date1) - date.fromisoformat(date2)).days    

def prepare_for_cox(incident_id):
    """
    Arguments:
        incident_id : str
            id of the incident that you want to measure days to
    Return:
        incident.csv : csv file
            csv file with all necessary info to make Cox Model in R
    """
    pheno = pd.read_csv("C:/Users/VukadinoviM/Documents/Beyond_Size/phenotypes/sphericity_index.tsv",sep='\t')
    pheno['eid'] = pheno['idx']
    df2 = pd.read_csv("C:/Users/VukadinoviM/Documents/Beyond_Size/small_datasets/si_ukb45494.csv")
    df3 = pd.read_csv("C:/Users/VukadinoviM/Documents/Beyond_Size/small_datasets/si_ukb47615.csv")
    df4 = pd.read_csv("C:/Users/VukadinoviM/Documents/Beyond_Size/small_datasets/BMI.csv")
    # merge df2 and df3 to get all the data
    df = pd.merge( pd.merge( pd.merge(df2[['eid','53-0.0','40000-0.0', '21003-0.0', '31-0.0', '22427-2.0', 'length', 'width' ]],
                            df3[['eid',incident_id, '131286-0.0','102-0.0']],on='eid'),
                            pheno[['eid','pheno']],on='eid' ), df4[['eid','21001-0.0']], on='eid' )

    # rename columns appropriately
    df = df.rename(columns={'53-0.0': 'first_visit_date',
                            '40000-0.0': 'death_date',
                            '21003-0.0':"age",
                            "31-0.0": "sex",
                            "22427-2.0": "BSA",
                            incident_id: 'event_date',
                            "131286-0.0": 'hypertension',
                            "102-0.0": "pulse_rate",
                            "21001-0.0": "BMI"
                            })

    # hypertension field checks if a person was diagnosed before the MRI date
    # 1 - diagnosed before MRI
    # 0 - not diagnosed or diagnosed after MRI
    df['hypertension'] = df['hypertension'].fillna("2021-03-31")
    new_hyper = []
    for i in range(len(df)):
        new_hyper.append(comes_after(df['first_visit_date'][i],df['hypertension'][i])) 
    df['hypertension'] = np.array(new_hyper, dtype='uint8')

    # add last const date
    df['CONST_DATE']="2021-03-31"

    ## get important dates
    #first_visit_date = np.array(df['53-0.0'])
    #second_visit_date = np.array(df['53-1.0'])
    #third_visit_date = np.array(df['53-2.0'])
    #fourth_visit_date = np.array(df['53-3.0'])
    #death_date = np.array(df['40000-0.0'])
    ## 2 event happened
    ## 1 event didn't happen
    days_without_incident = []
    status = []
    for index,row in df.iterrows():
        if (not isnan(row['event_date'])) and (comes_after(row['event_date'], row['first_visit_date'])):
            days_without_incident.append(diff_in_days(row['event_date'],row['first_visit_date']))
            status.append(1)
        elif isnan(row['event_date']):
            status.append(0)
            if (not isnan(row['death_date'])):
                days_without_incident.append(diff_in_days(row['death_date'],row['first_visit_date']))
            else:
                days_without_incident.append(diff_in_days(row['CONST_DATE'], row['first_visit_date']))
        else:
            status.append(0)
            days_without_incident.append(-1)

    df['days_without_incident'] = days_without_incident
    df['status'] = status
#    df = df[df.days_without_incident != -1]
    df.to_csv(f"{ id_dict[incident_id]}.csv")

def length_papillary(image_path, seg_image_path, thres = 0.35, label=1):
    """
    - Calculates length of papillary muscle 
    - Run on end-diastolic and end-systolic images individually 
    to calculate strain later
    - Returns image, mask, dimension, and length 
    TO-DO: Think about QC if end-diastolic and -systolic images are not clear
    """
    nim = nib.load(image_path)
    image = nim.get_fdata()
    seg_nim = nib.load(seg_image_path)
    seg_image = seg_nim.get_fdata()
    length=[]
    cnt=0
    masked_image = np.zeros_like(image)
    frame = image
    seg_frame = seg_image
    img,top,left,right,down = focus( (frame) * (seg_frame==label))
    img=img / np.max(img)
    thresh_img = np.copy(img)
    thresh_img[thresh_img<thres]=0
    imgray = (255*thresh_img).astype(np.uint8)
    
    # Create hull and calculate length
    contours, hierarchy = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = Reverse(sorted(contours, key = len))
    cont=contours[0]
    hull = cv2.convexHull(cont, returnPoints=True)
    hull = np.int0(hull)
    length = cv2.arcLength(hull,False)
    
    # Create segmentation 
    blank1 = np.zeros((img.shape[0],img.shape[1]))
    blank2 = np.zeros((img.shape[0],img.shape[1]))
    cv2.drawContours(blank1,[hull],-1,(147,0,255),thickness=1) 
    cv2.drawContours(blank2,[hull],-1,(147,0,255),thickness=cv2.FILLED) 
    mask = np.copy(img)
    mask[(blank2-blank1)==0] =0
    mask[img>thres]=0
    mask[mask>0]=1
    whole_mask = np.zeros_like(frame)
    whole_mask[top[0]:down[0],left[1]:right[1]] = mask
    masked_image = whole_mask
    
    # Get dimensions 
    nim = nib.load(image_path)
    pixdim = nim.header['pixdim'][1:4]
    print(nim.header.get_zooms()[-1])
    return image,masked_image,pixdim, length
   
def strain_papillary(l_0,l_1):
    return (l_1-l_0)/

    
   






