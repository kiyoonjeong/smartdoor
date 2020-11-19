import boto3

AWS_REGION = 'us-west-2'

def CreateB1(s3=None):
    if not s3:
        s3 = boto3.resource('s3', region_name=AWS_REGION)
    if AWS_REGION != 'us-west-2':
        print('aaa')
        response = s3.create_bucket(
            ACL='private',
            Bucket='cs9223c-as2-s3b1',
            CreateBucketConfiguration={
                'LocationConstraint': AWS_REGION
            },
            ObjectLockEnabledForBucket=True
        )
    else:
        response = s3.create_bucket(
            ACL='private',
            Bucket='cs9223c-as2-s3b1',
            ObjectLockEnabledForBucket=True
        )
    return response

if __name__ == '__main__':
    response = CreateB1()
