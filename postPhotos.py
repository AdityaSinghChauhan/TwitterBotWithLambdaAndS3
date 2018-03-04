# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 20:11:37 2018

@author: adityas.chauhan
"""

import boto3
from random import *
def postPhotos(event,context):
    import tweepy as tp
    import time
    import requests
    import os
    
    
    # credentials to login to twitter api
    consumer_key = ''
    consumer_secret = ''
    access_token = ''
    access_secret = ''
    
    # login to twitter account api
    auth = tp.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tp.API(auth)
    
    #Generate a random file name such that it matches the pattern of the files you have saved in your bucket
    key = 'astronomy-'+str(randint(1, 15))+'.jpg'
    
    #See if the file exists in your S3 Bucket.
    if list(get_matching_s3_keys(bucket='bucketName', prefix='', suffix='.jpg')).count(key) == 1:
        print(key)
        clientMy = boto3.client('s3')
        response = clientMy.get_object(Bucket='bucketName', Key=key)
        data = response.get('Body').read()
        url = 'https://s3.amazonaws.com/bucketName/'+key;
        filename = '/tmp/temp.jpg'
        request = requests.get(url, stream=True)
        if request.status_code == 200:
            with open(filename, 'wb') as image:
                for chunk in request:
                    image.write(chunk)
        api.update_with_media(filename, status="Hey There... #ILoveAstronomy")
        os.remove(filename)
    
"""
This function returns all the objects matching the prefix and suffix consition in a S3 Bucket.
"""
def get_matching_s3_keys(bucket, prefix='', suffix=''):
    """
    Generate the keys in an S3 bucket.

    :param bucket: Name of the S3 bucket.
    :param prefix: Only fetch keys that start with this prefix (optional).
    :param suffix: Only fetch keys that end with this suffix (optional).
    """
    s3 = boto3.client('s3')
    kwargs = {'Bucket': bucket}

    # If the prefix is a single string (not a tuple of strings), we can
    # do the filtering directly in the S3 API.
    if isinstance(prefix, str):
        kwargs['Prefix'] = prefix

    while True:

        # The S3 API response is a large blob of metadata.
        # 'Contents' contains information about the listed objects.
        resp = s3.list_objects_v2(**kwargs)
        for obj in resp['Contents']:
            key = obj['Key']
            if key.startswith(prefix) and key.endswith(suffix):
                yield key

        # The S3 API is paginated, returning up to 1000 keys at a time.
        # Pass the continuation token into the next response, until we
        # reach the final page (when this field is missing).
        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break
