import logging
import boto3
from botocore.exceptions import ClientError
import requests
import os
from github import Github

EMAILS = ['alex-m-howard@pm.me']
BUCKET_NAME = 'prod-site-example'
REGION_NAME = 'us-east-1'
REPO_NAME = 'Production-Hub'

def upload_file(file, filename):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # Upload the file
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.environ.get(
                                 'AWS_ACCESS_KEY'),
                             aws_secret_access_key=os.environ.get(
                                 'AWS_SECRET_KEY'),
                             region_name=REGION_NAME)

    try:
        s3_client.put_object(
            Body=file,
            Bucket=BUCKET_NAME, 
            Key=filename 
            )  
    except ClientError as e:
        logging.error(e)
        return False
    return True 


def list_all_objects_version(prefix_name):
    
    session = boto3.session.Session()
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.environ.get(
                                 'AWS_ACCESS_KEY'),
                             aws_secret_access_key=os.environ.get(
                                 'AWS_SECRET_KEY'),
                             region_name=REGION_NAME)
    
    try:
        result = s3_client.list_object_versions(Bucket=BUCKET_NAME, Prefix=prefix_name)
    
    except ClientError as e:
        raise Exception("boto3 client error in list_all_objects_version function: " + e.__str__())
    except Exception as e:
        raise Exception("Unexpected error in list_all_objects_version function of s3 helper: " + e.__str__())

    return result


def create_presigned_url(object_name, version_id, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3',
                             aws_access_key_id=os.environ.get(
                                 'AWS_ACCESS_KEY'),
                             aws_secret_access_key=os.environ.get(
                                 'AWS_SECRET_KEY'),
                             region_name=REGION_NAME)
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': BUCKET_NAME,
                                                            'Key': object_name,
                                                            'VersionId': version_id},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def email(data):
    url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"
    
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": f"{os.environ.get('API_KEY')}",
        "X-RapidAPI-Host": "rapidprod-sendgrid-v1.p.rapidapi.com"
    }
        
    payload = {
            "personalizations": [{"subject": f"AUTOMATED REQUEST: {data['request_type']} Requested by {data['requested_by']}"}],
            "from": {"email": "alex-m-howard@pm.me"}
        }
    
    
    payload["personalizations"][0]["to"] = []
    
    for each in EMAILS:
        payload["personalizations"][0]["to"].append({"email": each})

           
    payload["content"] = [
            {
                "type": "text/html",
                "value": f"""
                <div class="box" style="display:flex; align-items:center; justify-content: center;">
                    <h3>Programming Request</h2>
                </div>
                <hr>
                <h5>Part/Program: {data["to_change"]}</h5>
                <br>
                <h5>Description: {data["description"]}</h5>
                
                """
            }
        ]
    
    response = requests.request("POST", url, json=payload, headers=headers)

    return(response.text)


def send_temp_email(email, code):
    url = "https://rapidprod-sendgrid-v1.p.rapidapi.com/mail/send"

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": f"{os.environ.get('API_KEY')}",
        "X-RapidAPI-Host": "rapidprod-sendgrid-v1.p.rapidapi.com"
    }

    payload = {
        "personalizations": [{"subject": "One Time Passcode", "to": [{"email": email}]}],
        "from": {"email": "alex-m-howard@pm.me"},
        "content" : [
        {
            "type": "text/html",
            "value": f"""
                <div class="box" style="display:flex; align-items:center; justify-content: center;">
                    <h3>Your temporary verification code</h2>
                </div>
                <hr>
                <h3>{code}</h3>
                <br>
                <br>
                <br>
                <br>
                <br>
                <br>
                <br>
                <br>
                <br>
                <p>If you have any issues, please contact <a href='mailto:alex-m-howard@pm.me'>Alex Howard</a></p>
                """
        }
    ]}

    response = requests.request("POST", url, json=payload, headers=headers)

    return (response.text)


def get_issues():
    g = Github(os.environ.get('GITHUB_TOKEN'))
    
    repo = g.get_user().get_repo(REPO_NAME)
    issues = repo.get_issues(state='all')
    
    return issues
    
    
def post_issue(data):    
    g = Github(os.environ.get('GITHUB_TOKEN'))
    
    repo = g.get_user().get_repo(REPO_NAME)
    return repo.create_issue(title=data["title"], body=data["body"])


def upload_file(file, filename, project_id, part_id, uploaded_by, notes=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
            region_name=REGION_NAME)

        s3_client.put_object(
            Body=file,
            Bucket=BUCKET_NAME,
            Key=filename
        )

    except ClientError as e:
        logging.error(e)
        return False
    return True


def get_s3_data():
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
        region_name=REGION_NAME)

    paginator = s3_client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=BUCKET_NAME)

    files = []

    for bucket in page_iterator:
        try:
            for item in bucket['Contents']:

                try:
                    metadata = s3_client.head_object(
                        Bucket=BUCKET_NAME, Key=item['Key'])

                    metadata['key'] = item['Key']
                    files.append(metadata)
                except:
                    print("Failed {}".format(item['Key']))
        except Exception as e:
            print(e)
    return files


def get_s3_object(filename, version_id):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
        region_name=REGION_NAME)
    obj = s3_client.get_object(
        Bucket=BUCKET_NAME, Key=filename, VersionId=version_id)

    return obj


def delete_s3_object(filename, version_id):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
        region_name=REGION_NAME)
    response = s3_client.delete_object(
        Bucket=BUCKET_NAME, Key=filename, VersionId=version_id)

    return response


def get_obj(filename):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'),
        region_name=REGION_NAME)

    obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=filename)
    return obj
