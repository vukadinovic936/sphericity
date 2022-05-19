import pandas as pd
import numpy as np
import math
from datetime import date
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
    df = pd.merge( pd.merge( pd.merge(df2[['eid','53-0.0','40000-0.0', '21003-0.0', '31-0.0', '22427-2.0' ]],
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


    
   






