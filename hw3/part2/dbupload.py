import json
import boto3
import string
import time
from random import *

def lambda_handler(event, context):
    print(event)
    AWS_REGION = 'us-west-2'
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    table1 = dynamodb.Table('visitors')
    dbdata = table1.get_item(Key = {
        'faceId' : event["faceId"]
    })
    dbdata = dbdata["Item"]
    phone = dbdata['phoneNumber']
    username = dbdata["name"]
    characters = string.ascii_letters+string.digits
    password = "".join(choice(characters) for x in range(randint(12, 16)))
    
    table2 = dynamodb.Table('passcodes')
    item ={
        'visitor' : username,
        'TAC' : password,
        'TTL' : int(time.time())+300
    }
    table2.put_item(Item=item)
    
    client = boto3.client("sns")
    response = client.publish(
        PhoneNumber = phone,
        Message = password
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
