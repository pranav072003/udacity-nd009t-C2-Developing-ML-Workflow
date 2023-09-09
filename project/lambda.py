#lambda-function-1
import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    # Get the s3 address from the Step Function event input
    key = event['s3_key'] ## TODO: fill in
    bucket = event['s3_bucket'] ## TODO: fill in
    
    # Download the data from s3 to /tmp/image.png
    ## TODO: fill in
    s3 = boto3.client('s3')
    s3.download_file(bucket, key, '/tmp/image.png')
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }
    
#lambda-function-2
import json
import sagemaker
import boto3
import base64
from sagemaker.serializers import IdentitySerializer

# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2023-09-09-09-09-06-186" ## TODO: fill in

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event["body"]["image_data"]) ## TODO: fill in)

    # Instantiate a Predictor
    predictor = sagemaker.predictor.Predictor(
    ENDPOINT,
    sagemaker_session=sagemaker.Session(),
    ) ## TODO: fill in

    # For this model the IdentitySerializer needs to be "image/png"
    predictor.serializer = IdentitySerializer("image/png")
    
    key = event['body']['s3_key'] ## TODO: fill in
    bucket = event['body']['s3_bucket'] ## TODO: fill in
    s3 = boto3.client('s3')
    s3.download_file(bucket, key, '/tmp/image.png')
    
    with open("/tmp/image.png", "rb") as f:
        payload = f.read()
    
    # Make a prediction:
    inferences = predictor.predict(payload) ## TODO: fill in
    
    # We return the data back to the Step Function    
    event["body"]["inferences"] = inferences.decode('utf-8')
    return {
        'statusCode': 200,
        'body': event["body"]
    }


#lambda-function-3
import json


THRESHOLD = .83


def lambda_handler(event, context):
    
    # Grab the inferences from the event
    inferences = json.loads(event["body"]["inferences"]) ## TODO: fill in
    
    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = [float(i) > THRESHOLD for i in inferences] ## TODO: fill in
    
    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    # if meets_threshold != [False, False]:
    #     pass
    # else:
    #     raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': event["body"]
    }


