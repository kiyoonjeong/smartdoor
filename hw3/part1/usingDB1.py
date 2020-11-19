import boto3
import string
import time

from random import *

AWS_REGION = 'us-west-2'

def RandomPassword():
    characters = string.ascii_letters+string.digits
    password = "".join(choice(characters) for x in range(randint(12, 16)))
    return password
    
def Access_Temporary_Password(visitor,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    table = dynamodb.Table('passcodes')
    
    password = RandomPassword()
    
    new_access={}
    new_access['visitor'] = visitor
    new_access['TAC'] = password
    new_access['TTL'] = int(time.time())+300
    table.put_item(Item=new_access)
    return password

def Is_Temporary_Password(visitor,password,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('passcodes')
    data = table.get_item(Key = {"visitor": visitor})
    if 'Item' not in data:
        return False
    item = data['Item']
    if password == item['TAC'] and int(time.time())<item['TTL']:
        return True
    else:
        return False
        
if __name__ == '__main__':
    visitor = '999'
    password = ''
    password = Access_Temporary_Password(visitor)
    print(Is_Temporary_Password(visitor,password))
