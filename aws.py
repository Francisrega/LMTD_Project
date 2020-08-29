import boto3
import json



class AWSmanager:
    def __init__(self):
        self.s3 = boto3.resource('s3')

#   #define connections to boto3 and save file to s3
    def save_to_s3(self):  
        s3 = boto3.client('s3') 
        boto3.client('s3').upload_file('emails.json', 'lmtd-team-delta', 'email-test.json')
   
    def listBucketFile(self, bucketName):
        bucket = self.s3.Bucket(bucketName)
        files = bucket.objects.all()
        for file in files:
            print(file.key)



