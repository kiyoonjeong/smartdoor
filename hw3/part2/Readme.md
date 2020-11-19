* I recommend to use python3.6 for lambda functions. When you build a layer later, python 3.8 might be a problem. Also, I recommend to build all this services in west-2 area.


#### rekognitionvideo.js
If you successfully follow all the steps in the link, this lambda function would already be built. You need to fix some part of the code.

(I'm not familiar with javascript, so if you find anything weird or any errors, please let me know. ) 

* Known Face : face.MatchedFaces contains faceId. Send this info to 'dbupload' lambda function.
* Unknown Face : Invoke 'opencv-lambda' function. Send the s3 url of images to Admin.

* Permission policy added : CloudWatch, LambdaExecute
* Special permission needed to connect with other lambda functions. I created policy called 'InvokeOtherLambdaPolicy'. 
JSON
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction",
                "lambda:InvokeAsync"
            ],
            "Resource": "arn:aws:lambda:us-west-2:105234542199:function:opencv-lambda2"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction",
                "lambda:InvokeAsync"
            ],
            "Resource": "arn:aws:lambda:us-west-2:105234542199:function:dbupload"
        }
    ]
}

#### dbupload.py
1. Get user's phone number, username from 'visitors' table by using 'faceId'.
2. Put opt data into 'passcodes' table.
3. Send SNS to user

* permission added : dynamodb, SNS

#### opencv-lambda.py
1. Stream ARN and name should be replaced to yours.
2. kvam.list_fragments -> get list of video frames
3. kvam.get_media_for_fragment_list -> get the most recent video frame
4. Write/Read video file and capture image via cv2 library.
5. Upload images into s3 bucket.

* permission added : S3, Kinesis, KinesisVideoStreams, LambdaExecute, KinesisAnalytics
* Library cv2 is not built in lambda, so you need to create a layer.
  * https://www.youtube.com/watch?v=cz8QjmgfGHc
  * https://www.youtube.com/watch?v=FQBT8vVRkAg
  * I recommend you to use python3.6. (Python 3.8 doesn't work.) Also, you need to specify the version of the opencv-python, unless you would get an error. ("opencv-python==4.0.0.21")


#### visitorupload.py
This should work with the apigateway. I assumed that lambda get following data from the website.
{
  "faceId": "d4cb9f60-ba8f-4fa2-b89b-298734f772e6",
  "name": "kiyoonjeong",
  "phone": "+16468807282",
  "filename": "kiyoon.jpg"
}
1. Put item into 'visitors' table.
2. Put item into 'passcodes' table.
3. Send password to 'sns'.

* permission added : dynamodb, sns

#### S3
S3 : kyvideo

I allowed it to be opened to all. Anyone who has the url can access to file.