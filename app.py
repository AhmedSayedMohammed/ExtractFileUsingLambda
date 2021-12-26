from flask import Flask
import boto3

app = Flask(__name__)
payload = b'{"destination": "zipped","source": "zipped","file": "zippedfile.zip","bucket": "almentor"}'


def extract_file():
    session = boto3.Session(profile_name='s3access')
    dev_client = session.client('lambda')

    response = dev_client.invoke(
        FunctionName='arn:aws:lambda:us-east-2:900777405078:function:ExtractS3',
        InvocationType='Event',
        Payload=payload,
    )
    return response


@app.route('/')
def hello_world():  # put application's code here
    extract_file()
    return 'true'


if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000)
