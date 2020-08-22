import requests
import json

import boto3
from botocore.exceptions import ClientError

class Prepare:
    def __init__(self):
        # Assign URL to variable: url
        self.url = 'https://www.themealdb.com/api/json/v1/1/random.php/?apikey=1'

        # Package the request, send the request and catch the response: r
        #self.r = requests.get(self.url)
        self.r = requests.get(self.url).json()
        #print(self.r)
        self.r2 = {}
        self.r3 = {}

        # Print the text of the response
        #print(self.r.text)
        with open('savedata.json', 'w') as sd:
            #data = json.dumps(self.r, default=lambda o: o.__dict__, sort_keys=True, indent=4)
            json.dump(self.r, sd, sort_keys=True, indent=4) 
        
        with open('savedata.json', 'r') as psd:
            self.r2 = json.load(psd)
        self.r3 = self.r2["meals"]
        self.r4 = self.r3[0]
        

    
        
        
        

        
        
        self.sendRecipe()

    def sendRecipe(self):   
        recipe = f"""
        
            YOUR RECIPE OF THE DAY:
            Meal: {self.r4["strMeal"]}
            Category: {self.r4["strCategory"]}
            Culture of Origin: {self.r4["strArea"]}
            Ingredients you will need:
            {self.r4["strMeasure1"]} {self.r4["strIngredient1"]}
            {self.r4["strMeasure2"]} {self.r4["strIngredient2"]}
            {self.r4["strMeasure3"]} {self.r4["strIngredient3"]}
            {self.r4["strMeasure4"]} {self.r4["strIngredient4"]}
            {self.r4["strMeasure5"]} {self.r4["strIngredient5"]}
            {self.r4["strMeasure6"]} {self.r4["strIngredient6"]}
            {self.r4["strMeasure7"]} {self.r4["strIngredient7"]}
            {self.r4["strMeasure8"]} {self.r4["strIngredient8"]}
            {self.r4["strMeasure9"]} {self.r4["strIngredient9"]}
            {self.r4["strMeasure10"]} {self.r4["strIngredient10"]}
            {self.r4["strMeasure11"]} {self.r4["strIngredient11"]}
            {self.r4["strMeasure12"]} {self.r4["strIngredient12"]}
            {self.r4["strMeasure13"]} {self.r4["strIngredient13"]}
            {self.r4["strMeasure14"]} {self.r4["strIngredient14"]}
            {self.r4["strMeasure15"]} {self.r4["strIngredient15"]}
            {self.r4["strMeasure16"]} {self.r4["strIngredient16"]}
            {self.r4["strMeasure17"]} {self.r4["strIngredient17"]}
            {self.r4["strMeasure18"]} {self.r4["strIngredient18"]}
            {self.r4["strMeasure19"]} {self.r4["strIngredient19"]}
            {self.r4["strMeasure20"]} {self.r4["strIngredient20"]}
            Instructions:
            {self.r4["strInstructions"]}"""
        Sender(recipe)

class Sender:
    def __init__(self, recipe):
        self.recipe = recipe
        self.sender = "dev.martinez86@gmail.com"
        self.recipient = "sababrocks@gmail.com"
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
        
                
    



