# -*- coding: utf-8 -*-
"""Ecommecre_data_using_LR.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FcXMAGbfl5jbm23nklxG0mLN0R13d0tg

# Eccomerce Data Analysis  Project using Linear Regression 
An ecommerce company based in New York City that sells clothing online but they also have in-store style and clothing advice sessions. Customers come in to the store, have sessions/meetings with a personal stylist, then they can go home and order either on a mobile app or website for the clothes they want. The company is trying to decide whether to focus their efforts on their mobile app experience or their website.

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

"""We need to download the data first"""

from google.colab import files
files.upload()

!wget https://raw.githubusercontent.com/gmashik/Machine_learning_projects/master/E_commerce_project/data/Ecommerce%20Customers

"""Need to read the data from Ecommerce Customers csv file as a Pandas DataFrame"""

ecomdata=pd.read_csv("Ecommerce Customers")

"""# Now exproe the data info"""

ecomdata.head()

ecomdata.info()

ecomdata.describe()

"""**Let's explore the data visually to get an idea how the featers are **"""

sns.set_palette("GnBu_d")
sns.set_style('whitegrid')

sns.jointplot(x='Time on App',y='Yearly Amount Spent',data=ecomdata)

sns.jointplot(x='Time on Website',y='Yearly Amount Spent',data=ecomdata)

"""`Time sepnt on App and yearly spending seems to have some linear relationship`

A Hex and kde plot are shown below
"""

sns.jointplot(x='Time on App',y='Yearly Amount Spent',kind='kde',data=ecomdata)

sns.jointplot(x='Time on App',y='Yearly Amount Spent',kind='hex',data=ecomdata)

"""To get an overview of the features we aregoing to use pairplot"""

sns.pairplot(ecomdata,palette="BuGn_r")

"""**Based on this pairplot we can see that the length of the membership is linearly related to the customers yearly spending. However the app time spending is also an important feature. Lets explore this using the linear model plot **"""

sns.lmplot(x='Length of Membership',y='Yearly Amount Spent',data=ecomdata)

"""# **Analysis using Linear Regression**

So, the company needs a strong reason wheather they spend their budget in the App developement or Website developement. 
For this decesion we are going to make an analysis that how Yearly Spent Amount of customers going to be affected if any of our features such as Time spent on App, Length of Membership changes. 
We are going to make a linear model.  Set the target variable  is** "Yearly Amount Spent"** and the features are **'Avg. Session Length', 'Time on App','Time on Website', 'Length of Membership'**.
So basically the model is 
**$y=W_1x_1+W_2x_2+W_3x_3+W_4x_4$** 

Where $W_1$,$W_2$,$W_3$,$W_4$ are the weights of the variable
"""

y=ecomdata['Yearly Amount Spent']
x=ecomdata[['Avg. Session Length','Time on App','Time on Website','Length of Membership']]

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)

"""**Now we are going to train the model**"""

from sklearn.linear_model import LinearRegression

linm=LinearRegression(fit_intercept=False,normalize=False)#instansiate model

"""**Train the model using fit**"""

linm.fit(x_train,y_train,sample_weight=None)

"""Predict the test data for the model accuracy"""

p_test=linm.predict(x_test)

from sklearn import  metrics

"""# **Model Evaluation**"""

print('Mean absolute error:', metrics.mean_absolute_error(y_test, p_test))
print('Mear Squared error:', metrics.mean_squared_error(y_test, p_test))
print('Root Mear Squared error:', np.sqrt(metrics.mean_squared_error(y_test,p_test)))

"""Form this error analysis it can be said that the model is not so bad.

**The distribution of residul**
"""

sns.distplot((y_test-p_test),bins=50)

"""### **Weights of the model**"""

print('Weights: \n', linm.coef_)

"""Tabular form"""

weight=pd.DataFrame(linm.coef_,x.columns)
weight.columns=['Weight']
weight

"""Comments on the weights analysis:

- If we keep all other features fixed, a 1 unit increase in **Avg. Session Length** is associated with an **increase of 25.940704 total dollars spent**.
- If we keep all other features fixed, a 1 unit increase in **Time on App** is associated with an **increase of 38.932224 total dollars spent**.
- If we keep all other features fixed, a 1 unit increase in **Time on Website** is associated with an **increase of 0.709183 total dollars spent**.
- If we keep all other features fixed, a 1 unit increase in **Length of Membership** is associated with an **increase of 61.674205 total dollars spent**.

# **Conclusion on "should focus more on their mobile app or on their website?"**

We can think about this in two ways: 
 Develop the Website to catch up to the performance of the mobile app, or develop the app more since that is what is working better. This sort of answer really depends on the other factors going on at the company,So we need to explore the relationship between Length of Membership and the App or the Website before coming to a conclusion. We can see that both app vs membership length and website vs membership length has similar relationship pattern. So, my suggestion is to spend more on the App develoement.
"""