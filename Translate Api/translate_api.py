# =============================================================
# Load in library
# =============================================================

import pandas as pd
import numpy as np
import glob
from mtranslate import translate
from os import path
from PIL import Image
import matplotlib.pyplot as plt
import os, requests, uuid, json
import concurrent.futures
import time

review_raw = pd.read_csv("Datasets/all_raw_data.csv", error_bad_lines=False)
print(review_raw.shape)

# Check if all foreign languages have translation

review = review_raw.copy()

nan_body_rows = review[review['Body'].isnull()]

nan_sub_rows = review[review['Subject'].isnull()]

# Fill nan body with subject

review['Body'] = review['Body'].fillna(review['Subject'])
len(review[review['Body'].isnull()])
print(len(review[review['Translated Body'].isnull()]))
print(len(review['Body']))

# Remove rows with both nan body and nan subject
review = review[~review['Body'].isnull()]

# combine English subject & body with translated subject & body
review['Subject_combined'] = review['Translated Subject'].fillna('')
review['Body_combined'] = review['Translated Body'].fillna(review['Body'])
# review['Subject_combined'].to_csv('Subject_combined.csv',index = False)
# review['Body_combined'].to_csv('Body_combined.csv',index = False)

review['Review_Text'] = review['Body_combined'] + ' ' + review['Subject_combined']

# =================================================
# Translate
# =================================================

### threading

out = []
out_dict = {}
CONNECTIONS = 50
TIMEOUT = 10
time1 = None
time2 = None

### Select the propotion of dataset that you need to translate
review_test = review[100000:200000]
body_translate=[]
count = 0
start = time.time()


for index, row in review_test.iterrows():
    try:
        eng_text = translate(row['Review_Text'],'en')
        #time.sleep(10)
        body_translate.append(eng_text)
    except:
        body_translate.append('Translation Error')
    count += 1
    print(count)


#df = pd.DataFrame(body_translate, columns=["Text"])

review_test['Review_Text_translation'] = body_translate

review_final = review_test[['App Name', 'App Store', 'App ID', 'Review ID',
       'Country', 'Version', 'Rating', 'Date', 'Author', 'Emotion', 'Device', 'Review_Text', 'Review_Text_translation']]

### Please change the output name everytime
review_final.to_csv('review_final_100001_200000.csv', index=False)

print("--- %s seconds ---" % (time.time() - start))


