# -*- coding: utf-8 -*-
"""Recommender_system_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZffQoyhC2n_bTyUBwow8CDbAj0u1fGW2

# **Recommender syetem project(1)**

<table align="center">
  
  <td align="center"><a target="_blank" href="https://colab.research.google.com/drive/1ZffQoyhC2n_bTyUBwow8CDbAj0u1fGW2?authuser=2#scrollTo=MzzwGixxnkj9">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTR7EtP27gljpJg91k2DVoRgkB84hkMl78bOA&usqp=CAU""  style="padding-bottom:5px;" />
        
  Run this project in Google Colab</a></td>
  
</table>

**In this project we are going to build a very simple recommender system based on the user rating and the correlation between movies. In the end we can take input of a simple movie name and can recommend 5 similar movies to that.**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

!wget https://raw.githubusercontent.com/gmashik/Machine_learning_projects/master/Recommender_system/Data/u1.data

!wget https://raw.githubusercontent.com/gmashik/Machine_learning_projects/master/Recommender_system/Data/Movie_Id_Titles

column_names = ['user_id', 'item_id', 'rating', 'timestamp']
data = pd.read_csv('u1.data', sep='\t', names=column_names)

data.head()

"""It will be much more meaningful with the use of movie title instead of item id only. lets get the movie title"""

title = pd.read_csv('Movie_Id_Titles')

title.head()

"""Lets merge this"""

data=pd.merge(data,title,on='item_id')
data.head()

"""# Lets Explore the data"""

tr=pd.DataFrame(data.groupby('title')['rating'].mean())
tr.head()

tr['num_of_rating']=data.groupby('title')['rating'].count()
tr.head()

sns.distplot(tr['rating'],bins=30,kde=False)

sns.jointplot('rating','num_of_rating',data=tr,kind='scatter')

"""**Except one or two outliers we can see a trend of high number of rating movies have high number of ratings**

# **Create recommendation for differenet movies**

So, we need to create a matrix that has the user ids on one axis and the movie title on another axis. Each cell will then consist of the rating the user gave to that movie. We will get a lot of NaN values, because most people have not seen most of the movies.
"""

mmatrix=data.pivot_table(index='user_id',columns='title',values='rating')
mmatrix.head()

mmatrix.shape

corrmat=pd.DataFrame()

c=0
for i in mmatrix.columns:
  corrmat[mmatrix.columns[c]]=mmatrix.corrwith(mmatrix[mmatrix.columns[c]])
  c=c+1
  if(c%100==0): 
    print(c)

corrmat['num_of_rating']=tr['num_of_rating']
corrmat.head()

"""Below code will generate 10 random movies of a movie from the data

# **Final movie recommender system**

Give a movie name in the form below then it will recommend you some similar movie. If the Name of the movie field is blank then it will pick recommendation for a random movie
"""

#@title Enter a movie name or it will choose a random movie and suggest similar movie to that
Name_of_the_movie = "Star Wars (1977)" #@param {type:"string"}
i=0
x=100000
for c in corrmat.columns:
  if corrmat.columns[i]==Name_of_the_movie:
    x=i
    break
  i=i+1
if x==100000:
  x=np.random.choice(range(1,1664))
  print("Didn't find the exact match. So suggesting you a random movie and simimar movies")
temp1=corrmat[corrmat.columns[x]].sort_values(ascending=False)
temp2=pd.DataFrame(temp1)
#temp2['num_of_ratings']=corrmat['num_of_rating']
temp2=temp2.join(corrmat['num_of_rating'])
temp2=temp2.join(tr['rating'])
temp2.dropna(inplace=True)
print("Movie name:",mmatrix.columns[x])
print("5 related movies with ratings are: \n")
temp3=temp2[temp2['num_of_rating']>100]

if temp3.shape[0]==0:
  print("There is no similar movies found in the datadase")
else:
  print(temp3['rating'].head(5))
