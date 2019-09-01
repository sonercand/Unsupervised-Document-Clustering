#!/usr/bin/env python
# coding: utf-8

# ##### Read and Merge
# 
#      list parquet files in the directory
#      file_df = read.parquet(files[0])
#      for file in files[1:]:
#          file_df_temp = read.parquet(file)
#          file_df = file_df.join(file_df_temp)
#      save file_df as parquet
#      return file_df

# In[4]:


from os import listdir
from os.path import isfile, join
#list search files
path = '..\data'
files = [f for f in listdir(path) if isfile(join(path, f))]


# In[15]:


# Merge all the search files
import pandas as pd
df_list = []
for file in files:
    df_list.append(pd.read_parquet(path+'\\'+file))
df = pd.concat(df_list,sort=True)
print(df.shape)


# In[17]:


# Drop duplicate search pages
df_1 = df.drop_duplicates()
print('Number of adds found for the search term data scientist is {}'.format(df_1.shape[0]))


# In[18]:


# Save File
df_1.to_parquet(path+'\\data_scientist_merged_01_09_2019.parquet')

