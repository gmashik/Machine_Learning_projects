# -*- coding: utf-8 -*-
"""Airbnb_Project(1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_zqgsE4M3M7xjlDgkoPYiRNBXg4OT4rV

#**Airbnb Project(1)**

<table align="center">
  
  <td align="center"><a target="_blank" href="https://colab.research.google.com/drive/1_zqgsE4M3M7xjlDgkoPYiRNBXg4OT4rV?authuser=2#scrollTo=spJCE-HI8CNk">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTR7EtP27gljpJg91k2DVoRgkB84hkMl78bOA&usqp=CAU""  style="padding-bottom:5px;" />
        
  Run this project in Google Colab</a></td>
  
</table>
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import sklearn
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso

"""# **Getting data**"""

# Commented out IPython magic to ensure Python compatibility.
# %ls

#upload the files from the directory
from google.colab import files
files.upload()

"""**!!This can be safely skipped and start from the "Start with cleaned data section"!!**"""

df=pd.read_csv("airbnb-listings.csv")

"""Check data table"""

df.info()

df.head(3)

"""How many records in this dataframe?How many columns in this dataframe? Let's explore that"""

print("number of samples in the data are",df.shape[0])
print("number of columns/features in the data are",df.shape[1])

c=1
for i in df.columns:
  print("Columns/Feature ",c," is",i)
  c+=1

"""# **Data cleaning**

**Lets explore the columns**
"""

df.info()

"""We dont need all the columns for our analysis. We are going to use some of them so we can create new data frame with the selected columns."""

selected_columns = [
  'host_is_superhost',
  'cancellation_policy',
  'instant_bookable',
  'host_total_listings_count',
  'neighbourhood_cleansed',
  'zipcode',
  'latitude',
  'longitude',
  'property_type',
  'room_type',
  'accommodates',
  'bathrooms',
  'bedrooms',
  'beds',
  'bed_type',
  'minimum_nights',
  'number_of_reviews',
  'review_scores_rating',
  'review_scores_accuracy',
  'review_scores_cleanliness',
  'review_scores_checkin',
  'review_scores_communication',
  'review_scores_location',
  'review_scores_value',
  'price']

newdf = df[selected_columns]
print("Number of columns in our new dataframe is ",newdf.shape[1])
print("We selected ",newdf.shape[1]," columns out of ",df.shape[1]," columns for our analysis")
newdf.head()

"""Check the data types of the features"""

newdf.dtypes

"""If we select price as our target we can see that the data type of
the price column is not numeric so the first step is to convert them into numeric column a with proper cleaning
"""

newdf['price'].head(4)

"""noticed that there is also an "$" sign. So we must take care of this care fully"""

newdf.replace({'price': r'[\$]'}, {'price': ''}, regex=True,inplace=True)
newdf.replace({'price': r'[\,]'}, {'price': ''}, regex=True,inplace=True)

newdf['price'].head(4)

"""It is cleaned but still the datatype is not numeric"""

newdf['price']=newdf['price'].astype('float64')

newdf['price'].head(4)

newdf.describe(include='all')

"""As we have different count results for the different columns, that means we have null values records for some columns. 
There are a few nulls in the categorical feature `zipcode`. Let's get rid of those rows where any of that column is null, so this is the simplest approach for the time being.
"""

#help(newdf.dropna)

newdf.dropna(axis=0,subset=['zipcode'],inplace=True)

newdf.describe(include='all')

"""Some rows are dropped, but still there are some columns with differnet numbers of records

Now let's try imputation for numerical features. We want to fill the nulls in some numerical features with the median of that column.
"""

cols = [
  "bedrooms",
  "bathrooms",
  "beds",
  "review_scores_rating",
  "review_scores_accuracy",
  "review_scores_cleanliness",
  "review_scores_checkin",
  "review_scores_communication",
  "review_scores_location",
  "review_scores_value"
]

newdf.fillna(newdf.median()[cols],inplace=True)

newdf.info()

plt.figure(figsize=(12,5),)
sns.distplot((newdf.price),bins=100,kde=True)

"""Seems not normal. Is it log normal? lets see."""

sns.distplot(np.log(newdf['price']),bins=100)

newdf.describe(include='all')

"""So, We have same amount of data for all the columns. NOw we are going to deal with the extreme values"""

#Just checking all the prices are nonnegative or not
if newdf.query('price>=0').price.count() ==newdf.price.count():
  print("We all all the nonnegative values")
print("")
if newdf.query('price==0').price.count()>=1:
  print("We have ",newdf.query('price==0').price.count()," 0 value in price column")

#help(newdf.query)
#We are getting rid of the 0 price row
newdf.query('price>0',inplace=True)

newdf['minimum_nights'].describe(include='all')
#newdf.minimum_nights.value_counts()
print("Numebr of entry where minimum nights are greater than 365 days are: ",newdf.query('minimum_nights>365').minimum_nights.count())

"""Minimum Nights max value is too high. Let's get rid of some extreme value"""

newdf.query('minimum_nights<=365',inplace=True)

newdf.describe(include='all')

#put this cleaned data into a new file
newdf.to_csv('cleandata')

"""# **Start with cleaned data**"""

#use this when use google colab
#this is the cleaned version of data
#!wget https://raw.githubusercontent.com/gmashik/Machine_learning_projects/master/Airbnb_project/Data/airbnb-cleaned.csv

#cdf=pd.read_csv('airbnb-cleaned.csv')

cdf=pd.read_csv('cleandata')

print("Number of samle in cleaded version is : ",cdf.shape[0])
print("Number of feature in cleaded version is : ",cdf.shape[1])

cdf.info()

"""**We can see that some of our data is not numerical. They are categorical. So we are going to get dummy variables using one-hot encoding.**

First get the categorical columns
"""

categoricalColumns=cdf.select_dtypes(include='object').columns
c=1
for i in categoricalColumns:
  print(" Categorical column number ",c," is ",i)
  c+=1

cdf=pd.get_dummies(cdf,columns=categoricalColumns)
cdf.head()

cdf.shape

X=cdf.drop(['price'],axis=1)
y=cdf['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=33)

scaler=StandardScaler()
X_train=scaler.fit_transform(X_train)
X_test=scaler.transform(X_test)

#Define Linear Regression
def linear_regrassion(x,y,cross_val):
  lrmodel=LinearRegression()
  parameters = {'fit_intercept':[True,False], 'normalize':[True,False], 'copy_X':[True, False]}
  lrmodel_grids=GridSearchCV(estimator=lrmodel,param_grid=parameters,
                           scoring='neg_mean_squared_error',
                           cv=cross_val,verbose=0,n_jobs=1)
  lrmodel_grids.fit(x,y)
  lrbest_param=lrmodel_grids.best_params_
  print("Best parameters for Linear Regression is :",lrbest_param)

"""# **Linear regression model result**"""

linear_regrassion(X_train,y_train,5)

from sklearn import metrics 
lrmodel=LinearRegression(copy_X=True,fit_intercept=False,normalize=True)
lrmodel.fit(X_train,y_train)
p_test=lrmodel.predict(X_test)
print('Model r2/variance:', lrmodel.score(X_test,y_test))
print('Mean absolute error:', metrics.mean_absolute_error(y_test, p_test))
print('Mean Squared error:', metrics.mean_squared_error(y_test, p_test))
print('Root Mear Squared error:', np.sqrt(metrics.mean_squared_error(y_test,p_test)))

"""# **Ridge Regression Model result**"""

#Ridge Regression
def ridge_regression(x,y,cross_val):
  ridge_model=Ridge()
  alphas = np.array([1.0,0.01,0.001,0.0001,0.005,0.02,0])
  norm_var= ([True,False])
  parameters={'alpha':alphas,'normalize':norm_var}
  ridgemodel_grid=GridSearchCV(ridge_model,param_grid=parameters,
                               scoring='neg_mean_squared_error',
                               n_jobs=1,
                               cv=cross_val)
  ridgemodel_grid.fit(x,y)
  ridgemodelbest_param=ridgemodel_grid.best_params_
  print("Best parameters for Linear Regression is :",ridgemodelbest_param)

ridge_regression(X_train,y_train,4)

ridgemodel=Ridge(alpha=1.0,normalize=False)
ridgemodel.fit(X_train,y_train)
p2_test=lrmodel.predict(X_test)
print('Model r2/variance:', ridgemodel.score(X_test,y_test))
print('Mean absolute error:', metrics.mean_absolute_error(y_test, p2_test))
print('Mean Squared error:', metrics.mean_squared_error(y_test, p2_test))
print('Root Mear Squared error:', np.sqrt(metrics.mean_squared_error(y_test,p2_test)))

"""**The error is pretty high we will move to the deep neural network approch now**

# **Neural Network approach**
"""

import tensorflow as tf
class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self,epoch,logs={}):
    if(logs.get('loss')<60.0):
      print("\nEarly stopping using callback.....")
      self.model.stop_training=True

import tensorflow as tf
callback=myCallback()
model=tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(96,)),
    tf.keras.layers.Dense(128,activation='relu',kernel_regularizer=tf.keras.regularizers.L2(0.02)),
    tf.keras.layers.Dropout(.5),
    tf.keras.layers.Dense(256,activation='relu',kernel_regularizer=tf.keras.regularizers.L2(0.02)),
    tf.keras.layers.Dropout(.5),
    tf.keras.layers.Dense(1)
])
model.compile(optimizer='rmsprop',loss='mae',metrics=['mse','mae'])

r=model.fit(X_train,y_train,epochs=200,validation_data=(X_test,y_test),
callbacks=[callback])

print("Train Score = ",model.evaluate(X_train,y_train))
print("Test Score = ",model.evaluate(X_test,y_test))

plt.plot(r.history['loss'],label='loss')
plt.plot(r.history['val_loss'],label='val_loss')
plt.legend()

plt.plot(r.history['mse'],label='mse')
plt.plot(r.history['val_mse'],label='val_mse')
plt.legend()

"""# **Conclusion**

**Still not a great approximation but great than the previous approximations. In this project I cleaned some raw data and explore them a little. I build several simple model for the price prediction. We need a lot more feature engineering or probably try to include more non-linearity to imrove the results**
"""

