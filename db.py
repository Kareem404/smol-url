import boto3
from utils import generate_url
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv
import os


class DB():
    def __init__(self, access_key, secret_access_key):
        self.access_key = access_key
        self.secret_access_key = secret_access_key

        dynamodb = boto3.resource(
            'dynamodb', 
            aws_access_key_id=self.access_key, 
            aws_secret_access_key=self.secret_access_key, 
            region_name = 'us-east-1'
        )

        self.table = dynamodb.Table('short-URLs')

    def add_long_url(self, long_url):
        """
        Function that adds a short URL in the database
        args:-
            - long_url(str): The actual URL that we will redirect to
        returns:-
            - short_url(str): The unique generated short_url 
        """
        not_unique_key = True
        while not_unique_key:
            try:
                short_url = generate_url() # get base62 URL
                
                self.table.put_item(
                    Item = {
                        'short_url': short_url, 
                        'long_url': long_url,
                        'num_clicks': 0
                    }, 
                    ConditionExpression="attribute_not_exists(short_url)" # to make sure we do not overwrite (returns an exception if key exists)
                )
                # stops if no exception is caught
                print(f"Added {long_url} successfully")
                return short_url # returns short url
            except Exception as e:
                print(e)
                print("key may already exist")


    def update_clicks(self, short_url):
        try:
            response = self.table.update_item(
                Key = {"short_url": short_url}, 
                UpdateExpression = "set num_clicks = num_clicks + :one", 
                ExpressionAttributeValues={":one": 1},
            )
        except Exception as err:
            print(err)
        print(f"Updated {short_url} clicks successfully")

    def get_long_url(self, short_url):
        try:
            response = self.table.query(KeyConditionExpression=Key('short_url').eq(short_url))
            entry = response['Items']
            if entry == []:
                return 404
            else:
                self.update_clicks(short_url=short_url)
                return entry[0]['long_url']
        except Exception as e:
            print(e)