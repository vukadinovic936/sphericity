import pandas as pd
import numpy as np
import math
from datetime import date
id_dict = {"131338-0.0":"cardiomyopathy",
        "131350-0.0":"atrial_fibrillation",
        "131354-0.0":"heart_failure_date",
        "131346-0.0":"cardiac_arrest"}

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
    pheno = pd.read_csv("hwpheno.csv")
    df2 = pd.read_csv("hw_ukb45494.csv")

    ## get important dates
    first_visit_date = np.array(df2['53-0.0'])
    second_visit_date = np.array(df2['53-1.0'])
    third_visit_date = np.array(df2['53-2.0'])
    fourth_visit_date = np.array(df2['53-3.0'])

    last_visit = []
    for i in range(len(second_visit_date)):
        if fourth_visit_date[i] == fourth_visit_date[i]:
            last_visit.append(fourth_visit_date[i])
        elif third_visit_date[i] == third_visit_date[i]:
            last_visit.append(third_visit_date[i])
        else:
            last_visit.append(second_visit_date[i])

    last_visit_date = np.array(last_visit)
    df3 = pd.read_csv("hw_ukb47615.csv")
    event_date = df3[incident_id]
    event_date = np.array(event_date)
    
    days_without_incident = []
    status = []
    ## 2 event happened
    ## 1 event didn't happen
    for i in range(len(pheno)):
        if ( not isnan(event_date[i])) and ( comes_after(event_date[i], first_visit_date[i])):
            days_without_incident.append(diff_in_days(event_date[i], first_visit_date[i]))
            status.append(2)
        else:
            days_without_incident.append(diff_in_days(last_visit_date[i], first_visit_date[i]))
            status.append(1)
    pheno['days_without_incident'] = days_without_incident
    pheno['status'] = status
    ## now include age, sex and BSA
    age = np.array(df2['21003-0.0'])
    sex = np.array(df2['31-0.0'])
    BSA = np.array(df2['22427-2.0'])
    pheno['age'] = age
    pheno['sex'] = sex
    pheno['BSA'] = BSA
    pheno.to_csv(f"{ id_dict[incident_id]}.csv")


    
   






