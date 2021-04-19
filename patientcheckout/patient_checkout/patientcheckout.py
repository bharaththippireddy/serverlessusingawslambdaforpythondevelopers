import boto3
import json
import os
import logging


s3 = boto3.client('s3')
sns_client = boto3.client('sns')
logger = logging.getLogger('patientcheckout')
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    topic = os.environ.get('PATIENT_CHECKOUT_TOPIC')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    logger.info('Reading {} from {}'.format(file_key, bucket_name))
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    file_content = obj['Body'].read().decode('utf-8')
    checkout_events = json.loads(file_content)
    for each_event in checkout_events:
        logger.info('Messaging being published')
        logger.info(each_event)
        sns_client.publish(
            TopicArn=topic,
            Message=json.dumps({'default': json.dumps(each_event)}),
            MessageStructure='json'
        )
