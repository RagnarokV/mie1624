import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import numpy as np
import nltk
import nltk
import os
import csv
nltk.download('punkt')
nltk.download('stopwords')
from nltk import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
#from hcluster import pdist, linkage, dendrogram
from nltk.tokenize import RegexpTokenizer
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram
from sklearn.metrics import pairwise_distances

import scipy.cluster.hierarchy as sch

job_list = pd.read_csv('./ZipRecruiter.csv')
recommended_courses = pd.read_csv('./recommended_courses.csv')
skillset = ['deep learning', 'machine learning', 'ai' ,'artificial intelligence', 'ml','data science', 'cost analysis','prediction','code','coding','data architecture','programming','machine learning','ai','statistics','mathematic','communication','critical thinking','visualization','master','professional','bachelor','business decisions','operationalizing','infrastructure','prototype','workflows','modeling','statistical','cloud','jupyter','rstudio','pycharm','atom','matlab','visual studio','spyder','vim','notepad','sublime','google colab','google','google cloud','notebook','ai platform','datalab','binder','ibm watson','ibm watson studio','ocean','python','r','sql','c','c++','java','javascript','typescript','bash','ggplot','matplotlib','plotly','d3','shiny','seaborn','geoplotlib','leaflet','cpu','gpu','tpu','linear','logistic','regression','forest','gradient','bayesian','neural networks','neural','dense','convolutional','transformer','ml','augmentation','automated','feature engineering','selection','architecture','pipelines','image','video','pil','cv2','skimage','u-net','mask r-cnn','image segmentation','object detection  ','yolov3','retinanet','image classification','vgg','inception','resnet','gan','vae','computer vision','generative networks','word embeddings','vectors','glove','fasttext','word2ve','encoder','decorder seq2seq','vanilla','contextualized embeddings','elmo','cove','gpt-2','bert','xlnet','scikit-learn','tensorflow','keras','randomforest','xgboost','pyTorch','caret','lightgbm','spark mlib','fast.ai','amazon','azure','salesforce','alibaba','aws']
#list of skills]


jobs=job_list.iloc[:,1:6]
columns_titles = ["company","job_title",'location','salary','link']
jobs=jobs.reindex(columns=columns_titles)
jobs= jobs[0:7]
#job_list

recommended_courses['score']=0

def recommender_system (t, recommended_courses):
    recommended_courses['score']=0
    
    for i in range(len(recommended_courses)):
        for sk in skillset:
            #print (sk)
            if recommended_courses[sk][i]>0 and job_list[sk][t]>0:
                recommended_courses['score'][i]+=1
                
            else:        
                pass
    columns_titles = ["course_title","program_title",'avg_rating', 'course_link']
    recommended_courses = recommended_courses.sort_values(by='score', ascending=False)
    recommended_courses=recommended_courses.reindex(columns=columns_titles)
    recommendation = recommended_courses.iloc[0:3,0:5]

    titles = recommendation['program_title'].tolist()
    companies = recommendation['course_title'].tolist()
    links = recommendation['course_link'].tolist()
    return list(zip(titles, companies, links))
    
