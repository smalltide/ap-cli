import boto3

s3 = boto3.client('s3')

bucket = 'privateapcomputeenvironment-aps3bucket-16arlqbgeklw9'
key = '{{ name }}'

try:
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    print("CONTENT: " + content)
except Exception as e:
    print(e)
    print(
        'Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.
        format(key, bucket))
    raise e
