# -*- coding: utf-8 -*-
"""
Created on Wed April 14 16:45:09 2024

@author: laberroutra
"""

# Import the library
#import asana
#from asana.rest import ApiException
import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime

#Print how long it takes
start = time.time()

# Replace YOUR_ASANA_API_KEY with your actual Asana API key
ASANA_API_KEY = '2/1202965984506774/1206605108431587:44ba029e336d6aa0a14cacf77915bbb1'
ASANA_API_URL = 'https://app.asana.com/api/1.0'

# Get only the taks for certain projects
# Get all the columns values for all the tasks
# How to not send duplicates to Sydney

my_projects = ['1205040094572451']   # Just the general project

# my_projects = ['1206467477449323','1206467477951384','1206467477951399',
#                 '1206467477951403','1206467477951407','1206467477951411',
#                 '1206489231672871','1206489231672875','1206489231672879',
#                 '1206489231672883','1206489231672891','1206586806152830',
#                 '1206586806152833','1206603374650357','1206603374650364',
#                 '1206603374650371','1206603374650375','1206603374650379',
#                 '1205040094572451']

# Header to the data
headers = ['Project ID', 
            'Project Name',
            'Task ID',
            'First Name',
            'Last Name',
            'Email',
            'UTEP ID',
            'Address',
            'Address 2',
            'Phone Number',
            'City',
            'State',
            'Other State',
            'ZIP Code',
            'Country',
            'Relationship with UTEP',
            'Class of',
            'Designation 1',
            'Display Donation',
            'Amount of Donation 1',
            'Channel',
            'UTEP email',
            'Receive Confirmation',
            'Other Address',
            'Designation 2',
            'Amount 2',
            'Designation 3',
            'Amount 3',
            'Designation 4',
            'Amount 4',
            'Designation 5',
            'Amount 5',
            'COEDU Funds',
            'COEDU Funds 2',
            'COEDU Funds 3',
            'COEDU Funds 4',
            'COEDU Funds 5',
            'COEG',
            'COEG 2',
            'COEG 3',
            'COEG 4',
            'COEG 5',
            'COHS',
            'COHS 2',
            'COHS 3',
            'COHS 4',
            'COHS 5',
            'COLA',
            'COLA 2',
            'COLA 3',
            'COLA 4',
            'COLA 5',
            'CONUR',
            'CONUR 2',
            'CONUR 3',
            'CONUR 4',
            'CONUR 5',
            'COS',
            'COS 2',
            'COS 3',
            'COS 4',
            'COS 5',
            'SPHARM',
            'SPHARM 2',
            'SPHARM 3',
            'SPHARM 4',
            'SPHARM 5',
            'Athletics',
            'Athletics 2',
            'Athletics 3',
            'Athletics 4',
            'Athletics 5',
            'Academic Affairs',
            'Academic Affairs 2',
            'Academic Affairs 3',
            'Academic Affairs 4',
            'Academic Affairs 5',
            'Student Affairs',
            'Student Affairs 2',
            'Student Affairs 3',
            'Student Affairs 4',
            'Student Affairs 5',
            'Other fund',
            'Other fund 2',
            'Other fund 3',
            'Other fund 4',
            'Other fund 5',
            'Name Honor 1',
            'Name Honor 2',
            'Name Honor 3',
            'Mailing address Honor 1',
            'Mailing Address 2',
            'Mailing Address Honor 3',
            'Honor or Memory 1',
            'Honor or Memory 2',
            'Honor or Memory of 3',
            'Preferred First Name',
            'Gift Confirmed',
            'Amount12', 
            'Amount34', 
            'Amount1234', 
            'Total Amount',
            'RYPI'
            ]

appeal_id = 'AF RYP PO FY24'

# Function to get all projects
def get_all_projects():
    endpoint = f'{ASANA_API_URL}/projects'
    headers = {'Authorization': f'Bearer {ASANA_API_KEY}'}
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        projects = response.json()['data']
        return projects
    else:
        print(f'Error: {response.status_code}')
        return None

# Get all projects
projects = get_all_projects()
num_projects = len(my_projects)
num_custom_fields = 100 # Total number of fields (columns)
fields = []
all_data = []

# Add an extra parameter to the get_tasks_in_project function
def get_tasks_in_project(project_id, include_custom_fields=True):
    endpoint = f'{ASANA_API_URL}/projects/{project_id}/tasks'
    headers = {'Authorization': f'Bearer {ASANA_API_KEY}'}
    
    # Add 'opt_fields=custom_fields' to the query parameters if requested
    query_params = {}
    if include_custom_fields:
        query_params['opt_fields'] = 'custom_fields'
    
    response = requests.get(endpoint, headers=headers, params=query_params)

    if response.status_code == 200:
        tasks = response.json()['data']
        return tasks
    else:
        print(f'Error: {response.status_code}')
        return None

# Modify the loop to iterate through tasks and fetch custom fields
if projects:
    for project in projects:
        project_id = project['gid']
        project_name = project['name']
        
        if project_id in my_projects:
            
            # Get tasks with custom fields included
            tasks = get_tasks_in_project(project_id, include_custom_fields=True)
            
            if tasks:
                #print(f'Tasks in project "{project_name}":')
                #print('Project id',project_id)
                for task in tasks:
                    task_id = task['gid']
                    #print(f'- {task_id}')
                    fields = []
                    
                    # Access custom fields dictionary
                    custom_fields = task.get('custom_fields', None)
                    if custom_fields:
                        # Iterate through each custom field
                        fields.append(project_id)
                        fields.append(project_name)
                        fields.append(task_id)
                        
                        for field in custom_fields:
                            field_name = field['name']
                            field_value = field.get('display_value', None)
                           
                            # Add to the fields array
                            fields.append(field_value)
                            
                            
                    else:
                        print('No custom fields found for this task')
                    all_data.append(fields)
            else:
                print(f'No tasks found in project "{project_name}"')
            
else:
    print('No projects found.')
   

# Convert list to dataframe
df = pd.DataFrame(all_data)
df.columns = headers

# print(df)

# Save the clean and complete file to the Scalefunder template
df.to_csv('Asana_data.csv', index=False)

# print(df.columns)


# ******************** Convert Asana's data to the Scale ********************
# Get the funds ids table
df_funds = pd.read_csv('Import Asana files/Funds_IDs.csv')
#df_temp = pd.read_csv('Import Asana files/Giving_Day_Temp.csv')  #<<--- PLACEHOLDER WHILE ASANA IS DOWN
df_temp = df.copy()

# for col in df_temp.columns:
#     print(col)


# *************** Get only the "Confirmed" tasks ***************
df_temp = df_temp.drop(df_temp[df_temp['Gift Confirmed'] != 'Confirmed'].index)

# ******************** Get the Tasks ID already work on ********************
df_id_upl = pd.read_csv('Import Asana files/Already_Uploaded.csv')
print(df_id_upl)

# *************** Remove the ones already work on ***************
# Create a boolean mask indicating whether the value in 'column_to_check' appears in 'df2'
mask = df_temp['RYPI'].isin(df_id_upl['AID'])

# Invert the mask to get rows where the value does not appear in 'df2'
filtered_df1 = df_temp[~mask]

filtered_df1.to_csv('TEMP.csv')

# *************** Clean the data ***************
# Proper First and Last Name
df_temp['First Name'] = df_temp['First Name'].str.upper().str.title()
df_temp['Last Name'] = df_temp['Last Name'].str.upper().str.title()

# Proper Address
df_temp['Address'] = df_temp['Address'].str.upper().str.title()
df_temp['Address 2'] = df_temp['Address 2'].astype(str)
df_temp['Address 2'] = df_temp['Address 2'].str.upper().str.title()
df_temp['Address 2'].replace('Nan', '', inplace=True)

# Proper Email
df_temp['Email'] = df_temp['Email'].str.lower()
df_temp['UTEP email'] = df_temp['UTEP email'].str.lower()


# Phone - just numbers
df_temp['Phone Number'] = df_temp['Phone Number'].astype(str)  # Change to text
df_temp['Phone Number'] = df_temp['Phone Number'].str.replace('-', '')
df_temp['Phone Number'] = df_temp['Phone Number'].str.replace('(', '')
df_temp['Phone Number'] = df_temp['Phone Number'].str.replace(')', '')

# Proper City
df_temp['City']= df_temp['City'].str.upper().str.title()

# State = Other State, when selected "Other State"
df_temp['State']= [x.replace('Other', str(y)) for x, y in df_temp[['State','Other State']].to_numpy()]

# Drop the Other State column
df_temp.drop(df_temp.columns[[12]], axis=1, inplace=True)

# for col in df_temp.columns:
#     print(col)

# Proper Country
df_temp['Country'].replace('US', 'United States', inplace=True)
df_temp['Country'].replace('usa', 'United States', inplace=True)
df_temp['Country'].replace('USA', 'United States', inplace=True)
df_temp['Country'].replace('MX', 'Mexico', inplace=True)
df_temp['Country'].replace('México', 'Mexico', inplace=True)
df_temp['Country']= df_temp['Country'].str.upper().str.title()

# Department = Designation ????     <<<---------- CHECK WITH SYDNEY
df_temp['Department'] = df_temp['Designation 1'] 

# Sort the dataframe
df_temp.sort_values(by=['Task ID'], ascending=True, inplace=True)
#print(df_temp)


# *************** Duplicate Constituent Info for each selected fund  ***************
df_asana_clean = df_temp.copy()

# All funds in 1 column
def create_df (df_new_name):      

    # Create new column
    df_new_name['Fund'] = ''
    
    # All funds in 1 column
    df_new_name['Fund'] = df_new_name.apply( lambda x: x[22:33].str.cat(sep='_'), axis=1 )

    # Delete the columns
    df_new_name.drop(df_new_name.columns[[22,23,24,25,26,27,28,29,30,31,32]], axis=1, inplace=True)

# *** Designation 1 ***

cols1 = ['Task ID', 'First Name', 'Last Name', 'Email', 'UTEP ID', 'Address', 
          'Address 2', 'Phone Number', 'City', 'State', 'ZIP Code', 'Country', 
          'Relationship with UTEP', 'Class of', 'Department', 'Designation 1', 
          'Display Donation', 'Amount of Donation 1', 'Channel', 'UTEP email', 
          'Receive Confirmation', 'Other Address', 'COEDU Funds', 'COEG', 
          'COHS', 'COLA', 'CONUR', 'COS', 'SPHARM', 'Athletics', 
          'Academic Affairs', 'Student Affairs', 'Other fund','Name Honor 1', 
          'Mailing address Honor 1', 'Honor or Memory 1', 
          'Preferred First Name', 'RYPI']

df1 = df_asana_clean[cols1]

# Define a function to add a label to another column if the column field is not empty
def add_label(row, label):
  if pd.isnull(row['Designation']) or row['Designation'] is None:
      if row[label] is not None:
          return 'Other Area at UTEP'
      else:
          return ''
  else:
      return row['Designation']

# Change the column name 
df1 = df1.rename(columns={'Designation 1': 'Designation', 
                                'Amount of Donation 1': 'Amount',
                                'Name Honor 1': 'Name Honor',
                                'Mailing address Honor 1': 'Mailing Address Honor',
                                'Honor or Memory 1': 'Honor or Memory'})

df1['Designation'] = df1.apply(lambda row: add_label(row,'Other fund'), axis=1)
create_df (df1)


# *** Designation 2 ***
cols2 = ['Task ID', 'First Name', 'Last Name', 'Email',  'UTEP ID', 'Address', 
          'Address 2', 'Phone Number', 'City', 'State', 'ZIP Code', 'Country', 
          'Relationship with UTEP', 'Class of', 'Department', 'Designation 2',
          'Display Donation', 'Amount 2', 'Channel', 'UTEP email',
          'Receive Confirmation', 'Other Address', 'COEDU Funds 2', 'COEG 2', 
          'COHS 2', 'COLA 2', 'CONUR 2', 'COS 2', 'SPHARM 2', 'Athletics 2',
          'Academic Affairs 2', 'Student Affairs 2', 'Other fund 2', 'Name Honor 2', 
          'Mailing Address 2', 'Honor or Memory 2', 'Preferred First Name', 'RYPI']

df2 = df_asana_clean[cols2]

# Change the column name 
# Change the column name 
df2 = df2.rename(columns={'Designation 2': 'Designation', 
                                'Amount 2': 'Amount',
                                'Name Honor 2': 'Name Honor',
                                'Mailing Address 2': 'Mailing Address Honor',
                                'Honor or Memory 2': 'Honor or Memory'})

df2['Designation'] = df2.apply(lambda row: add_label(row, 'Other fund 2'), axis=1)
create_df (df2)


# *** Designation 3 ***
cols3 = ['Task ID', 'First Name', 
          'Last Name', 'Email', 'UTEP ID', 'Address', 
          'Address 2', 'Phone Number', 'City', 'State', 
          'ZIP Code', 'Country', 'Relationship with UTEP', 'Class of', 
          'Department', 'Designation 3', 'Display Donation', 'Amount 3', 'Channel', 'UTEP email', 
          'Receive Confirmation', 'Other Address', 'COEDU Funds 3', 'COEG 3', 
          'COHS 3', 'COLA 3', 'CONUR 3', 'COS 3', 'SPHARM 3', 'Athletics 3',
          'Academic Affairs 3', 'Student Affairs 3', 'Other fund 3', 'Name Honor 3', 
          'Mailing Address Honor 3', 'Honor or Memory of 3', 'Preferred First Name', 'RYPI']

df3 = df_asana_clean[cols3]

# Change the column name 
df3 = df3.rename(columns={'Designation 3': 'Designation', 
                                'Amount 3': 'Amount',
                                'Name Honor 3': 'Name Honor',
                                'Mailing Address Honor 3': 'Mailing Address Honor',
                                'Honor or Memory of 3': 'Honor or Memory'})

df3['Designation'] = df3.apply(lambda row: add_label(row,'Other fund 3'), axis=1)
create_df (df3)

# *** Designation 4 ***
cols4 = ['Task ID', 'First Name', 'Last Name', 'Email', 'UTEP ID', 'Address', 
          'Address 2', 'Phone Number', 'City', 'State', 'ZIP Code', 'Country', 
          'Relationship with UTEP', 'Class of', 'Department', 'Designation 4', 
          'Display Donation', 'Amount 4', 'Channel',  'UTEP email', 
          'Receive Confirmation', 'Other Address', 'COEDU Funds 4', 'COEG 4', 
          'COHS 4', 'COLA 4', 'CONUR 4', 'COS 4', 'SPHARM 4', 'Athletics 4',
          'Academic Affairs 4', 'Student Affairs 4', 'Other fund 4', 'Preferred First Name', 'RYPI']

df4 = df_asana_clean[cols4]

# Change the column name 
df4 = df4.rename(columns={'Designation 4': 'Designation', 
                                'Amount 4': 'Amount'})

df4['Designation'] = df4.apply(lambda row: add_label(row,'Other fund 4'), axis=1)
create_df (df4)

# *** Designation 5 ***
cols5 = ['Task ID', 'First Name', 'Last Name', 'Email', 'UTEP ID', 'Address', 
          'Address 2', 'Phone Number', 'City', 'State', 'ZIP Code', 'Country', 
          'Relationship with UTEP', 'Class of', 'Department', 'Designation 5', 
          'Display Donation', 'Amount 5', 'Channel', 'UTEP email', 
          'Receive Confirmation', 'Other Address', 'COEDU Funds 5', 'COEG 5', 
          'COHS 5', 'COLA 5', 'CONUR 5', 'COS 5', 'SPHARM 5', 'Athletics 5',
          'Academic Affairs 5', 'Student Affairs 5', 'Other fund 5', 'Preferred First Name', 'RYPI']
 
df5 = df_asana_clean[cols5]

# Change the column name 
df5 = df5.rename(columns={'Designation 5': 'Designation', 
                                'Amount 5': 'Amount'})

df5['Designation'] = df5.apply(lambda row: add_label(row,'Other fund 5'), axis=1)
create_df (df5)

df_join = pd.concat([df1, df2, df3, df4, df5], ignore_index=True)
df_join.sort_values(by=['Task ID'], ascending=True, inplace=True)

df_join['Designation'].replace('Other','Other Area at UTEP', inplace = True)

# *************** Add the funds for the Deps with 1 fund ***************
d = {'Designation': ['Hunt College of Business',
                    'Library',
                    'Alumni Association',
                    'Womans Auxiliary of UTEP',
                    'Graduate School',
                    'UTEP Endowed Scholarship Fund',
                    'Osher Lifelong Learning Institute',
                    'The Diana Natalicio Institute for Hispanic Student Success Gift Fund'], 
      'Fund': ['Hunt College of Business Student Travel and Conference Attendance Fund',
              'Library Enhancement Fund',
              'Alumni Association of UTEP Endowed Scholarship Fund',
              "Woman's Auxiliary Centennial Endowed Scholarship",
              'Graduate School Student Support Endowment',
              'UTEP Endowed Scholarship Fund',
              'Osher Lifelong Learning Institute Gift Fund',
              'The Diana Natalicio Institute for Hispanic Student Success Gift Fund']}

other_fund_id = 306
other_group = 'Other Area at UTEP'
other_fund = 'Select "Other" and Designate Below'

df_1funds = pd.DataFrame(data=d)

# Assign fund to the units with only one fund
df_join = pd.merge(df_join, df_1funds, on ='Designation', how ='left') 

# Concatenate the two funds columns
df_join['Fund'] = df_join.apply( lambda x: x['Fund_x':'Fund_y'].str.cat(sep=''), axis=1 )

# Delete the rows without funds
df_join['Fund'].replace('', np.nan, inplace=True)
df_join.dropna(subset=['Fund'], inplace=True)

# Delete the columns
df_join.drop(df_join.columns[[27,28]], axis=1, inplace=True)


# *************** Add the fund_id and the Appeail_id columns ***************
# Add appeal_id
df_join['Appeal_id'] = appeal_id

# Add fund_id
# Assign fund to the units with only one fund
df_join = pd.merge(df_join, df_funds, on ='Fund', how ='left') 

# Fix the OTHER funds Department and Fund id
df_join['Department_y'] = df_join['Department_y'].astype(str)
df_join['Fund ID'] = df_join['Fund ID'].astype(str)

df_join['Department_y'].replace('nan', 'Other Area at UTEP', inplace=True)
df_join['Fund ID'].replace('nan', '306', inplace=True)

# Fix the Asana ID for later
df_join['RYPI'] = df_join['RYPI'] + "@asana.com"   #<<-- honoree_email ADDED THE FUND ID

df_join.to_csv('join.csv', index = False)

# *************** Change to the ScaleFunder template ***************
# Get just the needed data for Scalefunder

df_sf = df_join[['First Name', 'Last Name', 'Email', 'Amount', 'Address', 
                  'Address 2', 'City', 'State', 'ZIP Code', 'Country', 
                  'Phone Number', 'Department_y', 'Fund', 'Fund ID', 
                  'Appeal_id', 'Channel', 'Display Donation', 
                  'Preferred First Name', 'Relationship with UTEP', 'Class of', 
                  'Name Honor', 'Mailing Address Honor', 'Honor or Memory', 
                  'UTEP email', 'UTEP ID', 'RYPI']]
                 



# Change column header to lower case
df_sf.columns = df_sf.columns.str.lower()

# Change the column name 
df_sf = df_sf.rename(columns={'first name': 'first_name', 'last name': 'last_name', 
                              'address 2' : 'address2', 'zip code' : 'zipcode', 
                              'phone number' : 'phone', 'fund id' : 'fund_id', 
                              'relationship with utep' : 'Affinity', 
                              'class of' : 'Class Yr V2', 
                              'department_y': 'department', 
                              'preferred first name': 'Preferred First',
                              'display donation':'donor_display',
                              'utep email' : 'UTEP Email',
                              'mailing address honor' : 'honoree mail',
                              'rypi' : 'honoree_email'})

# Donor display for Scalefunder
df_sf['donor_display'] = df_sf['donor_display'].replace({'Display name and gift amount' :'display',
                                                          'Display name only' : 'hide_amount',
                                                          'Display gift amount only' : 'hide_name',
                                                          'Do not display my name and gift amount' : 'hide_all'})

df_sf['wall_label1'] = df_sf['first_name']
df_sf['wall_label2'] = df_sf['honor or memory'] + " " + df_sf['name honor'].str.upper().str.title()

# Drop Name honor and Honor/Memory columns
df_sf = df_sf.drop(columns = {'name honor', 'honor or memory'})

# Reorder the columns
df_sf = df_sf.loc[:, ['first_name', 'last_name', 'email', 'amount', 'address', 
                      'address2', 'city', 'state', 'zipcode', 'country', 
                      'phone', 'department', 'fund', 'fund_id', 'appeal_id', 
                      'channel', 'donor_display', 'Preferred First', 
                      'Affinity', 'Class Yr V2', 'wall_label1', 'wall_label2', 
                      'UTEP Email', 'honoree mail', 'honoree_email']]


# *************** Save in a csv file ***************
#date = date.today()
date_time = datetime.now()
# format specification
#format = '%Y-%m-%d %H-%M-%S'
format = '%H-%M'

# applying strftime() to format the datetime
string = date_time.strftime(format)

#df_sf.to_csv('asana_data_clean_' + string + '.csv', index=False)
df_sf.to_csv('asana_data_clean.csv', index=False)


# *************** Save only the Task IDs work on  ***************
df_task_ids = df_join[['RYPI','First Name', 'Last Name', 'Email', 'Fund', 'Amount']].copy() 

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
time_simple = now.strftime("%H-%M-%S")
#df_task_ids['Time'] = current_time

df_task_ids['enumerated'] = [i for i, _ in enumerate(df_task_ids['RYPI'])]

df_task_ids['RYPI'] = df_task_ids['RYPI'].str.split('@').str[0]

#df_task_ids.to_csv('Already_Uploaded_to_ScaleFunder.csv')
#df_task_ids.to_csv('tasks_ids_' + time_simple + '.csv', index=False)
df_task_ids.to_csv('tasks_ids_.csv', index=False)


# *************** DONE ***************
print("*** Done ***")
end = time.time()
#print("Time lapsed:", end - start)
print("--- %s seconds ---" % (end - start))