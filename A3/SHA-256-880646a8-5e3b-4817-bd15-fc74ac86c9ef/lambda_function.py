import hashlib
import json
import urllib3

def lambda_handler(event, context):
    print(event)
    print("hello")
    print(event.get('course_uri'))
    input_string = event
    print("input_string", input_string)
   
    
    value = input_string.get('value')
    
    if not value:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing value'})
        }
        
    hash_str = hashlib.sha256(value.encode('utf-8')).hexdigest()
    
    
    
    
    payload = {
        'banner': 'B00982225',
        'result': hash_str,
        'arn': 'arn:aws:lambda:us-east-1:970200206506:function:SHA-256',
        'action': 'sha256',
        'value': value
    }
    
    print("Payload",payload)
    
    url = input_string.get('course_uri')
    if url:
        http = urllib3.PoolManager()
        response = http.request('POST', url, body=json.dumps(payload), headers={'Content-Type': 'application/json'})
        
        return {
            'statusCode': response.status,
            'body': response.data.decode('utf-8')
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid course_uri'})
        }
