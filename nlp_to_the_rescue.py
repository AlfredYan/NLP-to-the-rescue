# =============================================================
# Load in library
# =============================================================

import pandas as pd
import numpy as np
import glob
import enchant
from googletrans import Translator
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import os, requests, uuid, json
import concurrent.futures
import time
#from microsofttranslator import Translator

# from textblob import TextBlob
# from langdetect import detect
# from langdetect.lang_detect_exception import LangDetectException

# ==============================================================
# EDA
# ==============================================================

# Read in data
# TODO: File 17 & 18 have issues and cannot be read in hence I put them into bad files folder will deal with them later.

# all_files = glob.glob("Datasets/*.csv")
#
# li = []
#
# for file in all_files:
#     print(file)
#     df = pd.read_csv(file, error_bad_lines=False, encoding='utf8')
#     li.append(df)
#
# review_raw = pd.concat((pd.read_csv(file, error_bad_lines=False, encoding='utf8')
#                         for file in all_files))


review_raw = pd.read_csv("/Users/yuluo/Desktop/depaul_capstone/NLP-to-the-rescue/Datasets/all_raw_data.csv",
                         error_bad_lines=False)


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

# Detect language

# d = enchant.Dict("en_US")
#
# def lang_detect(value):
#     try:
#         return d.check(value)
#     except:
#         return('error')
#
# review['language_id'] = review['Body'].apply(lambda x: lang_detect(x))
#
# len(review[~review['Translated Body'].isnull()])
# len(review[~review['language_id']])
#
# non_eng_review = review[~review['language_id']]

# CLD-2 is pretty good and extremely fast
# lang-detect is a tiny bit better, but much slower
# langid is good, but CLD-2 and lang-detect are much better
# NLTK's Textcat is neither efficient nor effective.


# combine English subject & body with translated subject & body
review['Subject_combined'] = review['Translated Subject'].fillna(review['Subject'])
review['Body_combined'] = review['Translated Body'].fillna(review['Body'])

review['Body_combined_char_count'] = review['Body_combined'].str.len()
print(sum(review['Body_combined_char_count']))

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


translator = Translator()
translation = translator.translate("早上好")
print(print(translation.origin, ' -> ', translation.text))


def lang_translate(value):
    try:
        return translator.translate(value).text
    except:
        return('Translation Error')



#body_combined = review['Body_combined']

review_test = review[0:200]

body_translate=[]

count=0
start = time.time()

for index, row in review_test.iterrows():
    count+=1
    print(count)
    translator = Translator()
    try:
        eng_text = translator.translate(row['Body_combined']).text
        print(eng_text)
        #time.sleep(10)
        body_translate.append(eng_text)
    except:
        body_translate.append('Translation Error')

review_test['Body_combined_translation'] = body_translate

print("--- %s seconds ---" % (time.time() - start))

#review_test['Body_eng'] = review_test['Body_combined'].apply(translator.translate, dest='en').apply(getattr, args=('text', ))


# with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
#     text_to_translate = {executor.submit(lang_translate, comment, TIMEOUT): comment for comment in body_combined[0:220]}
#     for future in concurrent.futures.as_completed(text_to_translate):
#         try:
#             data = future.result()
#         except Exception as exc:
#             data = str(type(exc))
#         finally:
#             out.append(data)
#             print(str(len(out)), end="\r")
#
#             if time1 == None:
#                 time1 = time.time()
#             if len(out)/len(out)>=1 and time2==None:
#                 time2 = time.time()
#
# print('Took {:.2f} s'.format((time2-time1)))


# Checks to see if the Translator Text subscription key is available
# as an environment variable. If you are setting your subscription key as a
# string, then comment these lines out.
# if 'TRANSLATOR_TEXT_KEY' in os.environ:
#     subscriptionKey = os.environ['TRANSLATOR_TEXT_KEY']
# else:
#     print('Environment variable for TRANSLATOR_TEXT_KEY is not set.')
#     exit()
# If you want to set your subscription key as a string, uncomment the line
# below and add your subscription key.
# subscriptionKey = 'bfa4d8b786b54ff5b9dd62bb4ce28436'
#
# base_url = 'https://api.cognitive.microsofttranslator.com'
# path = '/translate?api-version=3.0'
# params = '&to=de&to=it'
# constructed_url = base_url + path + params
#
# headers = {
#     'Ocp-Apim-Subscription-Key': subscriptionKey,
#     'Content-type': 'application/json',
#     'X-ClientTraceId': str(uuid.uuid4())
# }
#
# body = [{
#     'text' : 'Hello World!'
# }]

# request = requests.post(constructed_url, headers=headers, json=body)
# response = request.json()
# print(json.dumps(response, sort_keys=True, indent=4, ensure_ascii=False, separators=(',', ': ')))

review_set2 = review[['App Name', 'App Store', 'App', 'Store', 'App ID', 'Review ID',
       'Country', 'Version', 'Rating', 'Date', 'Author', 'Emotion', 'Device', 'Subject_combined', 'Body_combined']]

percent_missing = review_set2.isnull().sum()/len(review_set2)
missing_value_df = pd.DataFrame({'column_name': review_set2.columns,
                                 'percent_missing': percent_missing})

missing_value_df = missing_value_df.sort_values(by='percent_missing', ascending=False)

missing_value_df['percent_missing'] = pd.Series(["{0:.2f}%".format(val * 100) for val in missing_value_df['percent_missing']],
                                                index = missing_value_df.index)

missing_value_df.to_csv('/Users/yuluo/Desktop/depaul_capstone/NLP-to-the-rescue/missing_value_check.csv')

print(review_set2.shape)

review_set2.to_csv('/Users/yuluo/Desktop/depaul_capstone/NLP-to-the-rescue/Datasets/review_processed.csv')


# ===========================================
# Create Word Cloud
# ===========================================

