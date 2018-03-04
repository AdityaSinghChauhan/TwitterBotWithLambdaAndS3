def lambda_handler(event, context):
    import requests
    from bs4 import BeautifulSoup as bs
    import os
    import boto3
    
    # website with astro images
    url = 'https://www.pexels.com/search/astronomy/'
    
    # download page for parsing
    page = requests.get(url)
    soup = bs(page.text, 'html.parser')
    
    # locate all elements with image tag
    image_tags = soup.findAll('img')
    
    #image file identifier
    x = 0
    
    # writing images
    for image in image_tags:
        try:
            url = image['src']
            response = requests.get(url)
            if response.status_code == 200:
                s3_client = boto3.client('s3')
                object = requests.get(url).content
                s3_client.put_object(Body=object, Bucket='bucketname', Key='astronomy-' + str(x) + '.jpg', ContentType='image/jpg', ContentEncoding='utf-8', StorageClass='STANDARD', ACL='public-read')
            x += 1
        except Exception as e:
            print(e)
            pass
    return 'Web Scrapping completed'
