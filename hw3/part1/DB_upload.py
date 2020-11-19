import json
import boto3
import string
import time
from random import *

AWS_REGION = 'us-west-2'

def RandomPassword():
    characters = string.ascii_letters+string.digits
    password = "".join(choice(characters) for x in range(randint(12, 16)))
    return password

def WriteDB1(dynamodb=None):

    with open("DB1_sample.json") as json_file:
        DB1_datas = json.load(json_file)
        
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)

    table = dynamodb.Table('passcodes')
    
    for DB1_data in DB1_datas:
        DB1_data['TAC'] = RandomPassword()
        DB1_data['TTL'] = int(time.time())+300
        print(DB1_data)
        table.put_item(Item=DB1_data)
        

def WriteDB2(dynamodb=None):

    with open("DB2_sample.json") as json_file:
        DB2_datas = json.load(json_file)
        
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
        
    table = dynamodb.Table('visitors')
    
    for DB2_data in DB2_datas:
        print(DB2_data)
        table.put_item(Item=DB2_data)

if __name__ == '__main__':
    WriteDB1()
    WriteDB2()


