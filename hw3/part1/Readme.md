#### createDB.py
Creating DB1 with ttl=TTL and with partition key "visitor" (string) and DB2 with partition key "faceId" by:
$python3 createDB.py

CreateDB1(dynamodb): 
use: create DB1

CreateDB2(dynamodb):
use: create DB2

SetTTL(table_name{Required}, dynamodb):
use: set TTL attribute to table_name

#### createS3.py
Creating B1 'cs9223c-as2-s3-b1' by:
$pyhton3 createS3.py

CreateB1(s3):
use: create B1

#### DB_upload.py
Uploading data in DB1_sample.json and DB2_sample.json to dynamodb by:
$python3 DB_upload.py

RandomPassword():
use: return a random combination of letters and digits between 12 to 16 long

WriteDB1():
use: upload data in "DB1_sample.json" to DB1
notice: we will set temporary password and TTL in this function. If we want to set in another place, please delete line 25 (for temprary access code) and line 26 (for TTL)

WriteDB2():
use: upload data in "DB1_sample.json" to DB2

#### usingDB1.py
Some useable function for DB1

Access_Temporary_Password(visitor,dynamodb):
use: request a temporary code and upload this code on dynamoDB
input: visitor
output: password

Is_Temporary_Password(visitor,password,dynamodb):
use: check whether password is eligible
input: visitor, password
output: boolean (False: no this visitor in DB1, wrong password, TTL expired)
