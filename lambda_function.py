import base64
import boto3
import hashlib
import datetime
import os

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    bucket = os.getenv("BUCKET", None)
    if bucket is None: exit(1)

    try:
        contenttype = event['headers']['Content-Type']
        remoteip = event['headers']['X-Forwarded-For']
        if contenttype == 'image/png':
            img = base64.b64decode(event['body'])
            key = hashlib.md5((remoteip + datetime.datetime.now().strftime('%s')).encode('utf-8')).hexdigest() + '.png'
            obj = s3.Object(bucket, key)
            obj.put(Body=img, ContentType=contenttype)
            return {
                'statusCode': 200,
                'body': 'http://' + bucket + '/' + key,
            }
        else:
            raise ValueError(contenttype)

    except ValueError as e:
        print(e)
        return {
            'statusCode': 500,
            'body': 'Content Type Error',
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': 'Internal Server Error',
        }

