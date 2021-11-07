import whois
import datetime
import pandas as pd
from os.path import splitext
import tldextract
from urllib.parse import urlparse
import numpy as np
from flask import Flask,render_template,request
import pickle
import os
import flask


def perform_whois(url):
    try:
        whois_result = whois.whois(url)
        return whois_result
    except Exception:
        return False

#function to fetch the website age in days using URL created_date
def get_registered_date_in_days(whois_result):
    if(whois_result!=False):
        created_date = whois_result.creation_date
        if((created_date is not None) and (type(created_date)!=str)):
            if(type(created_date)==list):
                created_date=created_date[0]
            today_date=datetime.datetime.now()
            days = (today_date-created_date).days
            return days
        else:
            return -1
    else:
        return -1

#function to fetch the website expiry date in days using URL expiration_date
def get_expiration_date_in_days(whois_result):
    if(whois_result!=False):
        expiration_date = whois_result.expiration_date
        if((expiration_date is not None) and (type(expiration_date)!=str)):
            if(type(expiration_date)==list):
                expiration_date = expiration_date[0]
            today_date=datetime.datetime.now()
            days = (expiration_date-today_date).days
            return days
        else:
            return -1
    else:
        return -1

#function to fetch the website's last updated date in days using URL updated_date
def get_updated_date_in_days(whois_result):
    if(whois_result!=False):
        updated_date = whois_result.updated_date
        if((updated_date is not None) and (type(updated_date)!=str)):
            if(type(updated_date)==list):
                updated_date = updated_date[0]
            today_date=datetime.datetime.now()
            days = (today_date-updated_date).days
            return days
        else:
            return -1
    else:
        return -1
"""def perform_dnsresolver(url):
    result = dns.resolver.query(url, 'A')
    print(type(result))
    for ipval in result:
        print('IP', ipval.to_text())"""

"""perform_dnsresolver('google.com')"""

def get_dot_count(url):
    return url.count('.')

def get_url_length(url):
    return len(url)

def get_digit_count(url):
    return sum(c.isdigit() for c in url)

def get_special_char_count(url):
    count = 0
    special_characters = [';','+=','_','?','=','&','[',']']
    for each_letter in url:
        if each_letter in special_characters:
            count = count + 1
    return count

def get_hyphen_count(url):
    return url.count('-')

def get_double_slash(url):
    return url.count('//')

def get_single_slash(url):
    return url.count('/')

def get_protocol_count(url):
    http_count = url.count('http')
    https_count = url.count('https')
    http_count = http_count - https_count #correcting the miscount of https as http
    return (http_count + https_count)

expiration_date_in_days = []
updated_date_in_days = []
dotCount = []
urlLength = []
digitCount = []
specialCharCount = []
hyphenCount = []
doubleSlashCount = []
singleSlashCount = []
protocolCount = []
registered_date_in_days = []

def extract_all_features(url1):
    counter = 0
#    for url in dataset['url']:
 #       counter = counter + 1
    print(counter)
    whois_result = perform_whois(url1)
    #Extracting whois features from URLs
    registered_date_in_days.append(get_registered_date_in_days(whois_result))
    expiration_date_in_days.append(get_expiration_date_in_days(whois_result))
    updated_date_in_days.append(get_updated_date_in_days(whois_result))
    #Extracting lexical features from URLs
    dotCount.append(get_dot_count(url1))
    urlLength.append(get_url_length(url1))
    digitCount.append(get_digit_count(url1))
    specialCharCount.append(get_special_char_count(url1))
    hyphenCount.append(get_hyphen_count(url1))
    doubleSlashCount.append(get_double_slash(url1))
    singleSlashCount.append(get_single_slash(url1))
    protocolCount.append(get_protocol_count(url1))

features_df = pd.DataFrame()
features_df['whois_regDate'] = registered_date_in_days
features_df['whois_expDate'] = expiration_date_in_days
features_df['whois_updatedDate'] = updated_date_in_days
features_df["dot_count"] = dotCount
features_df["url_len"] = urlLength
features_df["digit_count"] = digitCount
features_df["special_count"] = specialCharCount
features_df["hyphen_count"] = hyphenCount
features_df["double_slash"] = doubleSlashCount
features_df["single_slash"] = singleSlashCount
features_df["protocol_count"] = protocolCount
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__) #Initialize the flask App
model = pickle.load(open('model.pkl', 'rb')) # loading the trained model

@app.route('/') # Homepage
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])

def predict():
    if request.method == 'POST':
        usr_input = str(request.form.get('usr'))
        usr_input = extract_all_features(usr_input)
        
        features_df = pd.DataFrame()
        features_df['whois_regDate'] = registered_date_in_days
        features_df['whois_expDate'] = expiration_date_in_days
        features_df['whois_updatedDate'] = updated_date_in_days
        features_df["dot_count"] = dotCount
        features_df["url_len"] = urlLength
        features_df["digit_count"] = digitCount
        features_df["special_count"] = specialCharCount
        features_df["hyphen_count"] = hyphenCount
        features_df["double_slash"] = doubleSlashCount
        features_df["single_slash"] = singleSlashCount
        features_df["protocol_count"] = protocolCount
        
      #1: 'phishing' ,0: 'benign'
        my_url_f = features_df.iloc[:,[0,1,2,3,4,5,6,7,8,9,10] ].values
      #my_url_f
        
        url_label = model.predict(my_url_f)
     
        if (url_label == 0):
            label = 'benign'
        else:
            label = 'phishing'
        
        return render_template('index.html',val=label)
    return render_template('index.html')

 
if __name__ == "__main__":
    app.run(debug=True)
    