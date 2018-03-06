# TwitterBotWithLambdaAndS3
This piece of code helps one getting started with Bots and AWS Services ( Lambda and S3)

This application would:

1. Scrap images from web and store them in an Amazon S3 Bucket.
   :: fetchPhotosFromWeb.py :: We scrap images from https://www.pexels.com/search/astronomy/ and save in a S3 bucket. 

2. Fetch images from the S3 bucket and tweet in a fixed interval.
