import boto3
import zipfile
from datetime import *
from io import BytesIO
import json
import re


def unzip_file(source,destination,zip_file,bucket):
    
    dev_client = boto3.client('s3')

    dev_resource = boto3.resource('s3')

    S3_ZIP_FOLDER = source

    S3_UNZIPPED_FOLDER = destination

    S3_BUCKET = bucket

    ZIP_FILE = zip_file

    bucket_dev = dev_resource.Bucket(S3_BUCKET)
    print(bucket_dev)
    zip_obj = dev_resource.Object(bucket_name=S3_BUCKET, key=f"{S3_ZIP_FOLDER}/{ZIP_FILE}")

    print("zip_obj=", zip_obj)

    buffer = BytesIO(zip_obj.get()["Body"].read())

    z = zipfile.ZipFile(buffer)

    #
    # for each file within the zip

    for filename in z.namelist():
        file_info = z.getinfo(filename)

        # Now copy the files to the 'unzipped' S3 folder

        print(f"Copying file {filename} to {S3_BUCKET}/{S3_UNZIPPED_FOLDER}{filename}")

        response = dev_client.put_object(

            Body=z.open(filename).read(),

            # might need to replace above line with the one
            # below for windows files
            #
            # Body=z.open(filename).read().decode("iso-8859-1").encode(encoding='UTF-8'),

            Bucket=S3_BUCKET,

            Key=f'{S3_UNZIPPED_FOLDER}/{filename}'

        )

    print(f"Done Unzipping {ZIP_FILE}")



def lambda_handler(event, context):
    print(event)
    print("-----------------")
    print(context)
    unzip_file(event['source'],event['destination'],event['file'],event['bucket'])
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('done zipping file')
    }
