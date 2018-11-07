#This code calculates the yield power law and power law rheology constants 
#Mostly applied on drilling and hydraulic fracturing - polymer based fluids

#Author: Sercan Gul

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
#------------------------------------------------------------------------------
#csv file should have columns named 600,300,200,100,6 and 3
df = pd.read_csv('viscometerdata.csv')
print ("Reading CSV")
#Rheology calculations from dial reading data
def YPLfunction(y, tauy, K, m):
    return tauy + K*y**m

def PLfunction(y, K, m):
    return  K*y**m

def NEWTfunction(y, K):
    return  K*y

#The shear rate for 600,300,200,100,6 and 3 RPM Viscometer
y = [1021.98,510.99,341.66,170.33,10.22,5.11]

tauy =[]
K = []
m = []
#------------------------------------------------------------------------------
print ("Calculations of rheology properties from dial readings")
for index, row in df.iterrows():
    x =[row['600'], row['300'],row['200'], row['100'],row['6'], row['3']]
    shearstress = np.asarray(x) * 1.066 * 0.4788 #unit conversion 

    popt, pcov = curve_fit(YPLfunction,y,shearstress)
    A = popt[0]
    B = popt[1]
    C = popt[2]
    
    if A < 0:  #if curve fit gives negative values for yield stress
        popt2, pcov2 = curve_fit(PLfunction, y, shearstress)
        A = 0
        B = popt2[0]
        C = popt2[1]
        
    if C>0.92: #if the model gives very high K numbers (close to a newtonian fluid)
        popt, pcov = curve_fit(NEWTfunction,y,shearstress)
        A = 0
        B = popt[0]
        C = 1
        
    tauy.append(A)
    K.append(B)
    m.append(C)
    
df["tauy"] = tauy
df["K"] = K
df["m"] = m