# -*- coding: utf-8 -*-
"""DesertData.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Igelpg8JHkbxeqRADm9mdwQ-IPB9u6sJ
"""

# Commented out IPython magic to ensure Python compatibility.
#Allows chart to appear in the notebook
# %matplotlib inline

#Libraries for analysis
import pandas as pd
import numpy as np
from osgeo import gdal
import rasterio
from sklearn import svm
from osgeo import gdal_array
from affine import Affine
import gdal
from pyproj import Proj, transform

#Libraries for Visualizing data
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(font_scale = 1.2)

rasterArray = gdal_array.LoadFile(r"NewDataDesert\desert_som_output.gri")
rA = gdal.Open(r"NewDataDesert\desert_som_output.gri")
rA.GetMetadata().values()

type(rasterArray)
c_names=["x", "y"]+list(rA.GetMetadata().values())
c_names

(n_rasters, max_x, max_y) = rasterArray.shape
big_matrix = np.zeros((max_x*max_y, 8))
big_matrix.shape
cell=0
for i in range(max_x):
    for j in range(max_y):
        big_matrix[cell, 0]=i
        big_matrix[cell, 1]=j
        for r in range(n_rasters):
            big_matrix[cell,2+r]=rasterArray[r,i,j]
        cell=cell+1

df=pd.DataFrame(big_matrix, columns=c_names)
df.head()

df.dropna(inplace =  True)       
df.isnull().sum().sum() #removes the nan data

#drop the coloumns x, y, Subsidence, Uplift
df=df.drop(['x', 'y', 'Subsidence', 'Uplift'], axis = 'columns')

def my_function(n,df,tr_size,kr,C_value):
  per_n=n/100
  tr_size=tr_size/100
    
  #df20=df.sample(frac=0.2,random_state=0)
  df_new=df.sample(frac=per_n,random_state=0) #random_state = 0, to test differnt percentages, kernals, C values, gammas and features
    
  X_train, X_test, y_train, y_test = train_test_split(df_new.drop('Geothermal', axis='columns'), df_new.Geothermal, train_size=tr_size)
  model = SVC(kernel= kr, C=C_value)
  model.fit(X_train, y_train)
  y_pred = model.predict(X_test)
  y_truth=y_test
  acc= metrics.accuracy_score(y_truth, y_pred)
  print('Accuracy = ', acc)
  y_score = (y_truth==y_pred)
  #y_truth[0]=1, y_pred[0]=1
  #y_truth[1]=1, y_pred[1]=0
  sum(y_score)/len(y_pred)

my_function(20,df,5,"linear",1)

my_function(20,df,10,"linear",1)

my_function(20,df,10,"poly",1)

from sklearn import svm
from sklearn.svm import SVC  # "Support vector classifier"
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt


X_train, X_test, y_train, y_test = train_test_split(df.drop('Geothermal', axis='columns'), df.Geothermal, train_size=0.05)
model = ExtraTreesClassifier()
model.fit(X_train, y_train)
X = pd.DataFrame(X_train)
print(model.feature_importances_) #use inbuilt class feature_importances of tree based classifiers
#plot graph of feature importances for better visualization
feat_importances = pd.Series(model.feature_importances_, index=X.columns)
feat_importances.plot(kind='barh')
plt.show()

my_function(20,df,5,"linear",10000)
features_names = ['Minerals','Temperature','Faults'] #column names of the dataset
svm = svm.SVC(kernel='linear')
X_train, X_test, y_train, y_test = train_test_split(df.drop('Geothermal', axis='columns'), df.Geothermal, train_size=0.05)
svm.fit(X_train, y_train)

my_function(20,df,10,"poly",10000)
