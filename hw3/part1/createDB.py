import boto3

AWS_REGION = 'us-west-2'

def CreateDB1(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
        
    table = dynamodb.create_table(
        TableName='passcodes',
        KeySchema=[
            {
                'AttributeName': 'TAC',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'TAC',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    table.wait_until_exists()
    print("Create Passcodes Table Successfully")
    return table
def CreateDB2(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
        
    table = dynamodb.create_table(
        TableName='visitors',
        KeySchema=[
            {
                'AttributeName': 'faceId',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'faceId',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    table.wait_until_exists()
    print("Create Visitors Table Successfully")
    return table

def SetTTL(table_name,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.client('dynamodb', region_name=AWS_REGION)
        
    ttl = dynamodb.describe_time_to_live(TableName=table_name)
    response = dynamodb.update_time_to_live(
        TableName=table_name,
        TimeToLiveSpecification={
            'Enabled': True,
            'AttributeName': 'TTL'
        }
    )
    print("Set TTL to Passcodes Table Successfully")
    return ttl , response

if __name__ == '__main__':
    passcode_table = CreateDB1()
    visitor_table = CreateDB2()
    ttl , response = SetTTL('passcodes')

