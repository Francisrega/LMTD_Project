import requests
import json
import boto3
from botocore.exceptions import ClientError
import sqlite3
from aws import AWSmanager


class Prepare:
    def __init__(self):
        # Assign URL to variable: url
        self.url = 'https://www.themealdb.com/api/json/v1/1/random.php/?apikey=1'
        self.sqliteConnection = sqlite3.connect('newProject/db.sqlite3')
        self.cursor = self.sqliteConnection.cursor()
        self.cursor.execute("select email from FoodieBlog_student")
        self.emails_json = self.cursor.fetchall()
        self.email_list = []
        # Package the request, send the request and catch the response: r
        
        self.r = requests.get(self.url).json()
        self.r2 = {}
        self.r3 = {}

        with open('emails.json', 'w') as w:
            json.dump(self.emails_json, w, sort_keys=True, indent=4)
        with open('emails.json', 'r') as r:
            self.email_list = json.load(r)
        
        with open('savedata.json', 'w') as sd:
            
            json.dump(self.r, sd, sort_keys=True, indent=4) 
        
        with open('savedata.json', 'r') as psd:
            self.r2 = json.load(psd)
        self.r3 = self.r2["meals"]
        self.r4 = self.r3[0]
        

    
        
        
        

        
        
        self.sendRecipe()

    def sendRecipe(self):   
        recipe_sec1 = f"""
        
            YOUR RECIPE OF THE DAY:
            Meal: {self.r4["strMeal"]}\n
            Category: {self.r4["strCategory"]}\n
            Culture of Origin: {self.r4["strArea"]}\n
            Ingredients you will need:\n"""
        
        for i in range(1, 20):
            add = f'{self.r4[f"strMeasure{i}"]} {self.r4[f"strIngredient{i}"]}\n'
            recipe_sec1 = recipe_sec1 + add
        
        recipe_sec2 = f"""Instructions:
            {self.r4["strInstructions"]}"""
        
        recipe = recipe_sec1 + recipe_sec2

        Sender(recipe, self.email_list)

class Sender:
    def __init__(self, recipe, email_list):
        self.recipe = recipe
        self.email_list = email_list
        self.sender = "dev.martinez86@gmail.com"
        self.recipient = "dev.martinez86@gmail.com"
        self.aws_region = "us-east-1"
        self.subject = "Your New Recipe suggestion"
        self.body_text = (f"{recipe}")
        self.body_html = f"""<html>
            <head></head>
            <body>
            <h1>Your New Recipe Suggestion</h1>
            <p>{recipe}</p>
            </body>
            </html>
            """    
        self.charset = "UTF-8"      
        self.client = boto3.client('ses',region_name=self.aws_region)
        self.sendRecipe()
    
    def sendRecipe(self):
        for i in range(len(self.email_list)):
            recipient = self.email_list[i]
            self.recipient = recipient[0]
            try:
                #Provide the contents of the email.
                response = self.client.send_email(
                    Destination={
                        'ToAddresses': [
                            self.recipient,
                        ],
                    },
                    Message={
                        'Body': {
                            'Html': {
                                'Charset': self.charset,
                                'Data': self.body_html,
                            },
                            'Text': {
                                'Charset':self.charset,
                                'Data': self.body_text,
                            },
                        },
                        'Subject': {
                            'Charset': self.charset,
                            'Data': self.subject,
                        },
                    },
                    Source=self.sender,
                    # If you are not using a configuration set, comment or delete the
                    # following line
                    #ConfigurationSetName=CONFIGURATION_SET,
                )
            # Display an error if something goes wrong.	
            except ClientError as e:
                print(e.response['Error']['Message'])
            else:
                print("Email sent! Message ID:"),
                print(response['MessageId'])
        json_uploader = AWSmanager()
        json_uploader.save_to_s3()
        json_uploader.listBucketFile("lmtd-team-delta")


   
                
    



