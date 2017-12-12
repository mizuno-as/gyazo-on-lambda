import base64
import boto3
import hashlib
import datetime

s3 = boto3.resource('s3')
bucket = 's3_bucket_name'

def lambda_handler(event, context):
    try:
        contenttype = event['headers']['Content-Type']
        subtype = contenttype.split('/')
        remoteip = event['headers']['X-Forwarded-For']
        if subtype[0] == 'image':
            img = base64.b64decode(event['body'])
            key = hashlib.md5((remoteip + datetime.datetime.now().strftime('%s')).encode('utf-8')).hexdigest() + '.' + subtype[1]
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

