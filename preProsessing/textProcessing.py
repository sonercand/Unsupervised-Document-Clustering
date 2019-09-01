#!/usr/bin/env python
# coding: utf-8

# #####  Text Preprocessing
# 
#      Load merged job search results
#      load word to vector model (downloaded from https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit)
#      remove stop words from description field
#      for each word in a given description fetch word vector size of 300
#      add a new column to the dataframe to keep word vectors
#      save pickles
#      

# #####  libraries

# In[79]:


import gensim
from gensim.models import Word2Vec
import numpy as np
import nltk
import itertools
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
import scipy
from scipy import spatial
from nltk.tokenize.toktok import ToktokTokenizer
import re
import numpy as np
import pandas as pd
tokenizer = ToktokTokenizer()
nltk.download('stopwords')
nltk.download('punkt')
stopword_list = nltk.corpus.stopwords.words('english')


# ##### load data set

# In[7]:


path = '..\data'
df = pd.read_parquet(path+'\\data_scientist_merged_01_09_2019.parquet')


# In[9]:


df.head(1)


# > Note: Only Job Description field will be processed in this notebook

# In[10]:


df_sub = df[['id','description']]


# ######  word2vec model

# In[14]:


model = gensim.models.KeyedVectors.load_word2vec_format(path+'\\GoogleNews-vectors-negative300.bin.gz', binary=True)


# In[80]:


def remove_stopwords(text, is_lower_case=False):
    pattern = r'[^a-zA-z0-9\s]'
    text = re.sub(pattern, ", ",text)
    tokens = tokenizer.tokenize(text)
    tokens = [token.strip() for token in tokens]
    if is_lower_case:
        filtered_tokens = [token for token in tokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in tokens if token.lower() not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text
# Function to get the embedding vector for n dimension, we have used "300"
def get_embedding(word):
    if word in model.wv.vocab:
        return model[word]
    else:
        return np.zeros(300)

def remove_embed(text):
    filt_text = remove_stopwords(text)
    return np.array([get_embedding(word) for word in filt_text])
    


# In[81]:


df_sub['word_vec'] = df_sub.apply(lambda x: remove_embed(x['description']),axis=1)


# In[82]:


df_sub['word_vec'].iloc[0].shape


# In[101]:


df_sub.shape


# In[111]:



m=0
l=100
while m<len(df_sub):
    print(m,l)
    df_sub.iloc[m:l].to_pickle(path+'\\word_encoding\\'+str(l)+'encoded_description.pkl',protocol=2)
    m=m+101
    l=l+101

