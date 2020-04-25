import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
import requests
from bs4 import BeautifulSoup
import html
from sklearn.metrics.pairwise import linear_kernel
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import time


# Now that we scraped the sites and save the csv file, lets open it and fill any NA values with an empty string
elec_df = pd.read_csv('elective_data_courses_final.csv',encoding='unicode_escape')
elec_df = elec_df[['Course Department','Course Code','Course Title','Pillar','Prof','Description']]
elec_df = elec_df.fillna('')
results_df = elec_df.copy()


# clean the df
for col in elec_df.columns:
    elec_df[col] = elec_df[col].apply(lambda x: html.unescape(x).lower())
    
elec_df['Description'] = elec_df['Course Title'] + ' ' + elec_df['Pillar']+' '+elec_df['Description']


# Clean description
def clean_col(rowval):
    end_string = ' '
    cleanregex = re.compile(r'[a-zA-Z0-9]+') # select only alphanumeric characters
    all_words = cleanregex.findall(rowval)
    rowval = end_string.join(all_words)
    
    # stem words
    ps = PorterStemmer()
    words_stem = [ps.stem(word) for word in rowval.split()]
    rowval = ' '.join(words_stem)
    
    # lemmatize words - I did not get as accurate as stemming so I stick to stemming
    # words_lemmatize = [lemmatizer.lemmatize(word) for word in rowval.split()]
    # rowval = ' '.join(words_lemmatize)
    
    return rowval
elec_df['Initial Description'] = elec_df['Description']
elec_df['Description'] = elec_df['Description'].apply(clean_col)
elec_df['Description'] = elec_df['Description'].apply(clean_col)


tfidf = TfidfVectorizer(stop_words = 'english')
tfidf_matrix = tfidf.fit_transform(elec_df['Description'])
indices = pd.Series(elec_df['Course Title']) # define the indices that id the course 

# Find the similarity matrix between the courses
similarity = linear_kernel(tfidf_matrix,tfidf_matrix)

def plot_heatmap(similarity,figsize = (10,10),title = 'Similarity between Courses',courses = False):
    plt.figure(figsize = figsize)
    if courses == True:
        ax = sns.heatmap(similarity,xticklabels=elec_df['Course Title'],yticklabels=elec_df['Course Title'],cmap = 'Blues')
    else:
        ax = sns.heatmap(similarity,xticklabels=['Input'],yticklabels=elec_df['Course Title'],cmap = 'Blues')
    ax.set_title(title)

def recommender(user_input, num_suggestions, electives_taken):
    """
    This function generates 5 top electives similar to the text input given
    
    input: user_input, a course from the electives ie. financial engineering
           cos_sim, similarity matrix of all the courses 
           
    output: top 5 recommended electives
    """
    ps = PorterStemmer()
    rec_elec = [] # course recommendations will be stored here
    rec_descr = []
    electives_taken = [elective.lower() for elective in electives_taken]
    
    user_input = ' '.join(user_input)
    word_stem = [ps.stem(word.lower()) for word in user_input.split(' ')]
    uinput = ' '.join(word_stem) # convert list of strings to one string
    uinput = tfidf.transform([uinput]) # apply tfidf onto the string
    
    
    # create similarity matrix for courses and specified input
    similarity = cosine_similarity(tfidf_matrix,uinput)
    sim = similarity.flatten()
    
    # find the course vector that relates the input string to the rest of the courses in descending orders
    sim_score = pd.Series(sim,index = indices.index).sort_values(ascending = False) # rank and sort the classes
    
    # choose the top 5 classes that relate to the interests the most
    # Checks if number of suggestions required exceeds number of electives available
    if sim_score.shape[0] < num_suggestions:
        return 'Not enough electives', None
    
    # Find indices of all classes from best to worst
    top_classes = list(sim_score.index) # put indexes in a list
    for index in top_classes: # for each index in the list
        # if course with that index is not found in electives taken - RECOMMEND IT
        if elec_df['Course Title'][index] not in electives_taken: 
            elective_full = results_df['Course Department'][index]+ ' '+\
            results_df['Course Code'][index]+': '+\
            results_df['Course Title'][index]
            rec_elec.append(elective_full)
            rec_descr.append(results_df['Description'][index])
        if len(rec_elec) >= num_suggestions: # only recommend as much as asked.
            break
            
    plot_heatmap(similarity, title = 'Similarity between Input and Courses')
    image_path = './static/images/'
    image_name = 'plot{}.png'.format(str(round(time.time())))
    plt.savefig(image_path + image_name, bbox_inches='tight')
    
    return rec_elec, similarity, image_name