var AWS = require('aws-sdk');
var sns = new AWS.SNS();

var SNSTopic = process.env.sns;
var lambda = new AWS.Lambda();
exports.handler = (event, context, callback) => {
        var unmatchedFace = 0;
        let shouldSkip = false;
        
        event.Records.forEach((record) => {
            
            // Kinesis data is base64 encoded so decode here
            const load = new Buffer(record.kinesis.data, 'base64').toString('ascii');
            const payload = JSON.parse(load);
            //console.log('Data: ', payload);
            var framenum;
            
           if(payload.FaceSearchResponse != null)
           {
               
               //Let's consider only one face (first detect face only)  
               payload.FaceSearchResponse.forEach((face) =>  {
                   if (shouldSkip){
                       return;
                   }
                   // known face
                   if(face.MatchedFaces != null && 
                         Object.keys(face.MatchedFaces).length > 0)
                   {
                        
                        console.log('Test1: ', JSON.stringify(face.DetectedFace));
                        console.log('Test2: ', JSON.stringify(face.MatchedFaces));
                        console.log('Test3: ', JSON.stringify(face.MatchedFaces[0]));
                        var facevar = face.MatchedFaces[0];
                        const facedata = {faceId : facevar.Face.FaceId};
                        var params = {
                          FunctionName : 'dbupload',
                          InvocationType : 'RequestResponse',
                          LogType: 'None',
                          Payload: JSON.stringify(facedata)
                        };
                        lambda.invoke(params, function(error, data) {
                          if (error) {
                              console.log('error: ', error);
                              context.fail(error);
                            // context.done('error', error);
                          } else{
                              console.log('data: ', data);
                              context.succeed('picture said' + data.Payload);
                          }
                        });
                        
                        shouldSkip = true;
                        
                   }
                   
                   else
                   {
                        if (unmatchedFace < 1){
                            unmatchedFace++;
                            return;
                        }
                        console.log('Test1: ', JSON.stringify(face.DetectedFace));
                        console.log('Test2: ', JSON.stringify(face.MatchedFaces));
                        var params = {
                           FunctionName : 'opencv-lambda2',
                           InvocationType : 'RequestResponse',
                           LogType: 'None',
                           Payload: '{"name" : "Alex"}'
                        };
                        lambda.invoke(params, function(error, data) {
                          if (error) {
                              console.log('error: ', error);
                              context.fail(error);
                            // context.done('error', error);
                          } else{
                                console.log('data: ', data);
                                context.succeed('picture said' + data.Payload);
                                framenum = 10;
                                var message = '';
                                var i;
                                for (i = 0; i < framenum; i++){
                                    message += `<a href = "https://kyvideo.s3-us-west-2.amazonaws.com/testimage${i}.jpg">link</a> ,`;
                                }
                                console.log('message: ', message);
                                var params = {
                                  Message: message,
                                  TopicArn: SNSTopic
                                };
                                sns.publish(params, function(err, data) {
                                  if (err){
                                    console.log(err, err.stack); // an error occurred
                                    callback(err);
                                  } 
                                  else{
                                    console.log(data);           // successful response
                                    callback(null, `Successfully processed ${event.Records.length} records.`);
                                  }     
                                });
                          }

                        });
                        shouldSkip = true;
                   }
               });
           }
        });
};