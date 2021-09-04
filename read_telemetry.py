# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 17:17:09 2021

@author: NGurel

Script for reading continuous time telemetry from pig models

METADATA: Telemetry_METADATA

The corresponding times are:
Baseline - 06-06-2020 to 06-07-2020
Week 2 - 06-22-2020 to 06-23-2020
Week 2.5 - 06-25-2020 to 06-26-2020
Week 3 - 07-03-2020 to 07-04-2020
Week 4 - 07-09-2020 to 07-10-2020

plotted vars: HR, PR, Pdur, QRS
"""
# In[ ]:
import pandas as pd
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt

# In[ ]: BASELINE FILE: P175607_1087460_ECG_06052020_06082020.x00
#need to save as SCV file because binary excel screws up the datetime..
# BASELINE FILE: P175607_1087460_ECG_06052020_06082020.x00
filepath = 'C:/Users/ngurel/Documents/Telemetry/175607 - Files and Initial Analysis-selected/P175607_1087460_ECG_06052020_06082020.x00.csv'
filename = filepath.split('.csv')[0].split('selected/')[1]
baseline_label = 'Baseline'
baseline_dates = ['6-Jun-20','7-Jun-20']

df = pd.read_csv(filepath)


# In[ ]: WEEK 2 AND 2.5 FILE: P175607_1087460_ECG_06222020_06272020.x00
filepath = 'C:/Users/ngurel/Documents/Telemetry/175607 - Files and Initial Analysis-selected/P175607_1087460_ECG_06222020_06272020.x00.csv'
filename = filepath.split('.csv')[0].split('selected/')[1]
week2_label = 'Week2'
week2_dates = ['22-Jun-20','23-Jun-20']

week2p5_label = 'Week2.5'
week2p5_dates = ['25-Jun-20','26-Jun-20']

df = pd.read_csv(filepath)

# In[ ]:  # WEEK 3 AND 4 FILE: P175607_1087460_ECG_07032020_07102020.x00
filepath = 'C:/Users/ngurel/Documents/Telemetry/175607 - Files and Initial Analysis-selected/P175607_1087460_ECG_07032020_07102020.x00.csv'
filename = filepath.split('.csv')[0].split('selected/')[1]
week3_label = 'Week3'
week3_dates = ['3-Jul-20','4-Jul-20']

week4_label = 'Week4'
week4_dates = ['9-Jul-20','10-Jul-20']

df = pd.read_csv(filepath)

# In[ ]: things to look for & add
      
steps_section = 'steps section' 
steps_section_first_colname = 'cpu-date'   
steps_section_last_colname = 'QRS__aver' 
cpu_date_colnum = 3 #first col in this section
QRS_aver_colnum = 25 #last col in this section

beats_section = 'beats section' 
beats_section_first_colname = 'cpu-date'   
beats_section_last_colname = 'QRS'   
cpu_date_colnum = 3 #first col in this section
QRS_colnum = 21

data_end_section = 'invalidated beats section'

# In[ ]:  ############################################# STEPS SECTION ####################################################

steps_section_loc = list(zip(*np.where(df.values == steps_section))) #[(233, 1)]
beats_section_loc = list(zip(*np.where(df.values == beats_section))) #[(8883, 1)]

steps_section_loc = np.asarray(steps_section_loc)
steps_section_row = steps_section_loc[0][0]    #233
steps_section_col= steps_section_loc[0][1]    

beats_section_loc = np.asarray(beats_section_loc)
beats_section_row = beats_section_loc[0][0]    #8883
beats_section_col= beats_section_loc[0][1] 

#data steps_section is between row 233 and 8883 if we drop nans and excessive stuff
df_steps_section = df[steps_section_row:beats_section_row]

#now search for cpu-date
steps_section_fcolname_loc = list(zip(*np.where(df_steps_section.values == steps_section_first_colname))) #[(7, 2)]
steps_section_fcolname_loc = np.asarray(steps_section_fcolname_loc)
steps_section_fcolname_row = steps_section_fcolname_loc[0][0]  #7th row  
steps_section_fcolname_col= steps_section_fcolname_loc[0][1] #2nd col

#now search for QRS__aver
steps_section_lcolname_loc = list(zip(*np.where(df_steps_section.values == steps_section_last_colname))) 
steps_section_lcolname_loc = np.asarray(steps_section_lcolname_loc)
steps_section_lcolname_row = steps_section_lcolname_loc[0][0]    #7th row
steps_section_lcolname_col= steps_section_lcolname_loc[0][1]  #26th col

##search for rows 
rows_steps_section_loc = list(zip(*np.where(df_steps_section.values == steps_section_first_colname))) #[(7, 0)]truncate everything before 7th
rows_steps_section_loc = np.asarray(rows_steps_section_loc)
rows_steps_section_loc = rows_steps_section_loc[0][0]

#now take the actual data between columns 2 and 26
df_steps_section_actual = df_steps_section.iloc[(rows_steps_section_loc):, (steps_section_fcolname_col):(steps_section_lcolname_col+1)] 
df_steps_section_actual = df_steps_section_actual.reset_index(drop = True)

#set first row as column names
headers = df_steps_section_actual.iloc[0]
df_steps_section_actual = df_steps_section_actual.rename(columns=headers)
df_steps_section_actual = df_steps_section_actual[1:]

####################################CHANGE LABEL FOR DIFFERENT FILES AND DATES###################################################
## baseline: 
# current_label = baseline_label
# current_dates = baseline_dates

# #week 2 & week 2.5 (in same file)
# #make first label as is and leave others as no_label
# current_label = week2_label
# current_dates = week2_dates
# df_steps_section_actual['experiment_label'] = np.where(df_steps_section_actual['cpu-date'].isin(current_dates), current_label, 'no_label')

# #without changing above label, add the second label
# current_label = week2p5_label
# current_dates = week2p5_dates
# df_steps_section_actual['experiment_label'] = np.where(df_steps_section_actual['cpu-date'].isin(current_dates), current_label, df_steps_section_actual['experiment_label'])

#week 3 & week 4
#make first label as is and leave others as no_label
current_label = week3_label
current_dates = week3_dates
df_steps_section_actual['experiment_label'] = np.where(df_steps_section_actual['cpu-date'].isin(current_dates), current_label, 'no_label')

#without changing above label, add the second label
current_label = week4_label
current_dates = week4_dates
df_steps_section_actual['experiment_label'] = np.where(df_steps_section_actual['cpu-date'].isin(current_dates), current_label, df_steps_section_actual['experiment_label'])

#save for the records
fname_steps_section = filename + '_steps_section.csv'
df_steps_section_actual.to_csv(fname_steps_section, index = False)

# drop rows with ['experiment_label']=='no_label'
df_steps_section_actual = df_steps_section_actual.drop(df_steps_section_actual[df_steps_section_actual['experiment_label'] == 'no_label'].index)

#save for the records
# fname_steps_section = filename + '_steps_section_' + current_label +'.csv'
# fname_steps_section = filename + '_steps_section_' +'week2_week2p5' +'.csv'
fname_steps_section = filename + '_steps_section_' +'week3_week4' +'.csv'
df_steps_section_actual.to_csv(fname_steps_section, index = False)

# In[ ]: ############################################## BEATS SECTION ####################################################

beats_section_loc_start = list(zip(*np.where(df.values == beats_section))) #[(8883, 1)]
beats_section_loc_end = list(zip(*np.where(df.values == data_end_section))) #[(58693, 1)]

beats_section_loc_start = np.asarray(beats_section_loc_start)
beats_section_row_start = beats_section_loc_start[0][0]    #8883
beats_section_col_start = beats_section_loc_start[0][1]    #1

beats_section_loc_end = np.asarray(beats_section_loc_end)
beats_section_row_end = beats_section_loc_end[0][0]    #58693
beats_section_col_end = beats_section_loc_end[0][1]    #1

df_beats_section = df[beats_section_row_start:beats_section_row_end]

#now search for cpu-date
beats_section_fcolname_loc = list(zip(*np.where(df_beats_section.values == beats_section_first_colname))) #
beats_section_fcolname_loc = np.asarray(beats_section_fcolname_loc)
beats_section_fcolname_row = beats_section_fcolname_loc[0][0]  #  14
beats_section_fcolname_col= beats_section_fcolname_loc[0][1] #2

#now search for QRS__aver
beats_section_lcolname_loc = list(zip(*np.where(df_beats_section.values == beats_section_last_colname))) 
beats_section_lcolname_loc = np.asarray(beats_section_lcolname_loc)
beats_section_lcolname_row = beats_section_lcolname_loc[0][0]    #14
beats_section_lcolname_col= beats_section_lcolname_loc[0][1]  #22

##search for rows 
rows_beats_section_loc = list(zip(*np.where(df_beats_section.values == beats_section_first_colname))) # truncate everything before this
rows_beats_section_loc = np.asarray(rows_beats_section_loc)
rows_beats_section_loc = rows_beats_section_loc[0][0]

#now take the actual data between those cols
df_beats_section_actual = df_beats_section.iloc[(rows_beats_section_loc):, (beats_section_fcolname_col):(beats_section_lcolname_col+1)] 
df_beats_section_actual = df_beats_section_actual.reset_index(drop = True)

#set first row as column names
headers = df_beats_section_actual.iloc[0]
df_beats_section_actual = df_beats_section_actual.rename(columns=headers)
df_beats_section_actual = df_beats_section_actual[1:]

####################################CHANGE LABEL FOR DIFFERENT FILES AND DATES###################################################
## baseline: 
# current_label = baseline_label
# current_dates = baseline_dates
#week 2 & week 2.5 (in same file)

# #make first label as is and leave others as no_label
# current_label = week2_label
# current_dates = week2_dates
# df_beats_section_actual['experiment_label'] = np.where(df_beats_section_actual['cpu-date'].isin(current_dates), current_label, 'no_label')

# #without changing above label, add the second label
# current_label = week2p5_label
# current_dates = week2p5_dates
# df_beats_section_actual['experiment_label'] = np.where(df_beats_section_actual['cpu-date'].isin(current_dates), current_label, df_beats_section_actual['experiment_label'])

#week 3 & week 4
#make first label as is and leave others as no_label
current_label = week3_label
current_dates = week3_dates
df_beats_section_actual['experiment_label'] = np.where(df_beats_section_actual['cpu-date'].isin(current_dates), current_label, 'no_label')

#without changing above label, add the second label
current_label = week4_label
current_dates = week4_dates
df_beats_section_actual['experiment_label'] = np.where(df_beats_section_actual['cpu-date'].isin(current_dates), current_label, df_beats_section_actual['experiment_label'])


#save for the records
fname_beats_section = filename + '_beats_section.csv'
df_beats_section_actual.to_csv(fname_beats_section, index = False)

# drop rows with ['experiment_label']=='no_label'
df_beats_section_actual = df_beats_section_actual.drop(df_beats_section_actual[df_beats_section_actual['experiment_label'] == 'no_label'].index)

#save for the records
# fname_beats_section = filename + '_beats_section_' + current_label +'.csv'
# fname_beats_section = filename + '_beats_section_' + 'week2_week2p5' +'.csv'
fname_beats_section = filename + '_beats_section_' + 'week3_week4' +'.csv'

df_beats_section_actual.to_csv(fname_beats_section, index = False)


# In[ ]: now merge the csvs you saved in a single df and plot violins


filepath_steps_baseline = 'C:/Users/ngurel/Documents/Telemetry/175607 - Files and Initial Analysis-selected/P175607_1087460_ECG_06052020_06082020.x00_steps_section_Baseline.csv'
filepath_steps_week2_week2p5 = 'C:/Users/ngurel/Documents/Telemetry/175607 - Files and Initial Analysis-selected/P175607_1087460_ECG_06222020_06272020.x00_steps_section_week2_week2p5.csv'
filepath_steps_week3_week4 = 'C:/Users/ngurel/Documents/Telemetry/175607 - Files and Initial Analysis-selected/P175607_1087460_ECG_07032020_07102020.x00_steps_section_week3_week4.csv'

filepath_beats_baseline = 'C:/Users/ngurel/Documents/Telemetry/175607 - Files and Initial Analysis-selected/P175607_1087460_ECG_06052020_06082020.x00_beats_section_Baseline.csv'
filepath_beats_week2_week2p5 = 'C:/Users/ngurel/Documents/Telemetry/175607 - Files and Initial Analysis-selected/P175607_1087460_ECG_06222020_06272020.x00_beats_section_week2_week2p5.csv'
filepath_beats_week3_week4 = 'C:/Users/ngurel/Documents/Telemetry/175607 - Files and Initial Analysis-selected/P175607_1087460_ECG_07032020_07102020.x00_beats_section_week3_week4.csv'

animal_details = filepath_steps_baseline.split("selected/")[1].split("_ECG_")[0]
#concat all steps
df_steps_baseline = pd.read_csv(filepath_steps_baseline)
df_steps_week2_week2p5 = pd.read_csv(filepath_steps_week2_week2p5)
df_steps_week3_week4 = pd.read_csv(filepath_steps_week3_week4)
df_steps = pd.concat([df_steps_baseline, df_steps_week2_week2p5,df_steps_week3_week4 ], ignore_index=True)
steps_fname = animal_details + '_allprotocol_steps_data.csv'
df_steps.to_csv(steps_fname, index = False)

#concat all beats
df_beats_baseline = pd.read_csv(filepath_beats_baseline)
df_beats_week2_week2p5 = pd.read_csv(filepath_beats_week2_week2p5)
df_beats_week3_week4 = pd.read_csv(filepath_beats_week3_week4)
df_beats = pd.concat([df_beats_baseline, df_beats_week2_week2p5,df_beats_week3_week4 ], ignore_index=True)
beats_fname = animal_details + '_allprotocol_beats_data.csv'
df_beats.to_csv(beats_fname, index = False)


#beats violinplots

ax = sns.violinplot(x="experiment_label", y="HR", data=df_beats)
plt.savefig('beats_HR.pdf')

ax = sns.violinplot(x="experiment_label", y="RR", data=df_beats)
plt.savefig('beats_RR.pdf')

ax = sns.violinplot(x="experiment_label", y="PR", data=df_beats)
plt.savefig('beats_PR.pdf')

ax = sns.violinplot(x="experiment_label", y="Pdur", data=df_beats)
plt.savefig('beats_Pdur.pdf')

ax = sns.violinplot(x="experiment_label", y="QRS", data=df_beats)
plt.savefig('beats_QRS.pdf')

#steps violinplots

ax = sns.violinplot(x="experiment_label", y="RR__aver", data=df_steps)
plt.savefig('steps_RR__aver.pdf')

ax = sns.violinplot(x="experiment_label", y="HR__aver", data=df_steps)
plt.savefig('steps_HR__aver.pdf')

ax = sns.violinplot(x="experiment_label", y="PR__aver", data=df_steps)
plt.savefig('steps_PR__aver.pdf')

ax = sns.violinplot(x="experiment_label", y="Pdur__aver", data=df_steps)
plt.savefig('steps_Pdur__aver.pdf')

ax = sns.violinplot(x="experiment_label", y="QRS__aver", data=df_steps)
plt.savefig('steps_QRS__aver.pdf')














    
