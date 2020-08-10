from kafka import KafkaConsumer
import json
from json import loads
import boto3
from botocore.client import Config

ACCESS_KEY_ID = ''
ACCESS_SECRET_KEY = ''
BUCKET_NAME = 'bucket';


s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4'))


def consumeAndUploadToS3():
    con, bucket = getConnection()
    print('Making connection.')
    consumer = KafkaConsumer(
        'my-first-topic',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group-1',
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers='localhost:9092')

    print('Starting to consume messages...')
    for message in consumer:
        print("OFFSET: " + str(message[0])+ "\t MSG: " + str(message))
        with open('message.json', 'w') as f:  # writing JSON object
            json.dump(message, f)
        data = open("message.json", 'rb')
        con.Bucket(bucket).put_object(Key="message.json", Body=data, ACL='public-read')
        print("Done-uploading")


if __name__ == '__main__':
    consumeAndUploadToS3()
