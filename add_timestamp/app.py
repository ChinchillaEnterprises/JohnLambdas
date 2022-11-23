import json
import boto3
from datetime import datetime
import io
import csv
from io import StringIO

# import requests

s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    print(event)
    #get bucket name from event
    #get key from event
    #to be able to get bucket and key from event, google
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    # bucket = 'john-drop'
    # key = 'customers/Customers.csv'
    print(bucket, key)
    obj = s3_resource.Object(bucket, key)
    timestamp = obj.last_modified
    
    obj = s3_client.get_object(Bucket=bucket, Key=key)
    data = obj['Body'].read().decode('utf-8')
   
    writer_buffer = io.StringIO()

    print("now reading/writing")
    writer = csv.writer(writer_buffer, lineterminator='\n')
    reader = csv.reader(io.StringIO(data))

    all = []
    row = next(reader)
    row.append('timestamp')
    all.append(row)

    for row in reader:
        row.append(timestamp)
        all.append(row)

    writer.writerows(all)
    
    buffer_to_upload = io.BytesIO(writer_buffer.getvalue().encode())
    print("now putting to s3")
    s3_client.put_object(Body=buffer_to_upload, Bucket='abel-drop', Key='Customers.csv')
    print("done")
    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
