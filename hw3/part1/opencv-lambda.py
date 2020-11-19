import json
import boto3
from datetime import datetime, date, time, timedelta
import cv2
import os

# hls_stream_ARN and STREAM_NAME should be changed to your stream arn!!!!!!!!!!!!!!!!!!!!!!!!!!!!
hls_stream_ARN = "arn:aws:kinesisvideo:us-west-2:105234542199:stream/LiveRekognitionVideoAnalysisBlog/1604980612135"

STREAM_NAME = "LiveRekognitionVideoAnalysisBlog"
kvs = boto3.client("kinesisvideo")

print("Attempting to get an HLS streaming URL from AWS GetDataEndpoint API...")

# Grab the endpoint fVeryFirstrom GetDataEndpoint
endpoint = kvs.get_data_endpoint(
    APIName="GET_MEDIA_FOR_FRAGMENT_LIST",
    StreamARN=hls_stream_ARN
)['DataEndpoint']
# Grab the HLS Stream URL from the endpoint
kvam = boto3.client("kinesis-video-archived-media", endpoint_url=endpoint)
response = kvam.list_fragments(
    StreamName=STREAM_NAME,
    MaxResults=1000,
    # NextToken='string',
    FragmentSelector={
        'FragmentSelectorType': 'SERVER_TIMESTAMP',
        'TimestampRange': {
            'StartTimestamp': datetime.now() - timedelta(minutes=1),
            'EndTimestamp': datetime.now()
        }
    }
)

fraglist = []
for data in response['Fragments']:
    fraglist.append(data['FragmentNumber'])

response = kvam.get_media_for_fragment_list(
    StreamName='LiveRekognitionVideoAnalysisBlog',
    Fragments= fraglist[max(0,len(fraglist)-10):]
    )

fname = '/tmp/test.webm'
with open(fname, 'wb+') as f:
    chunk = response['Payload'].read(1024*8)
    while chunk:
        f.write(chunk)
        chunk = response['Payload'].read(1024*8)

cam = cv2.VideoCapture('/tmp/test.webm')
currentframe = 0
s3 = boto3.client('s3')

#bucket name should be changed!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
bucket = 'kyvideo'
while(currentframe < 10):
    ret,frame = cam.read()
    if ret:
        name = "testimage" + str(currentframe) + ".jpg"
        cv2.imwrite("/tmp/"+name,frame)
        response = s3.list_objects_v2(Bucket=bucket, Prefix = name)
        if response:
            s3.delete_object(Bucket=bucket, Key = name)
        s3.upload_file("/tmp/"+name, bucket, name)
        currentframe += 1
    else:
        break

cam.release()
cv2.destroyAllWindows()

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'frame' : currentframe
    }