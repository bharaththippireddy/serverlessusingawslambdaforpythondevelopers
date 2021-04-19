def lambda_handler(event, context):
    for each_record in event['Records']:
        print(each_record['body'])
