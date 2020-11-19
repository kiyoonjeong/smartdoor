import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    AWS_REGION = 'us-west-2'
        
    otp = event['body']
    # strip the first 4 characters
    otp = otp[4:]
    
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    table = dynamodb.Table('passcodes')
    response = table.get_item(Key = {
        'TAC' : otp,
    })

    print("response : " , response)
    
    if response.get("Item"):
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": { },
            "body": json.dumps("passed")
        }
    else:
        return {
            "isBase64Encoded": False,
            "statusCode": 200,
            "headers": { },
            "body": json.dumps("failed")
        }