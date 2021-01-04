# Smart Door Authentication System

Build a distributed system that authenticate people using Kinesis Video Streams and Amazon Rekognition, and provide them access to a virtual door.

# Workflow

1. Process streaming video and perform stream analysis to identify faces.
2. Check if visitor's face is matched with the face data in the database.
3. If so, send a OTP which is only valid for 5 minutes.
4. If not, send a visitor's face image and description to system manager.
5. If system manager allows him/her to enter, the system store the visitor's face data into the database and send them a OTP.

# Architecture
