'''
This function handles a Slack slash command and echoes the details back to the user.

Follow these steps to configure the slash command in Slack:

  1. Navigate to https://<your-team-domain>.slack.com/services/new

  2. Search for and select "Slash Commands".

  3. Enter a name for your command and click "Add Slash Command Integration".

  4. Copy the token string from the integration settings and use it in the next section.

  5. After you complete this blueprint, enter the provided API endpoint URL in the URL field.


To encrypt your secrets use the following steps:

  1. Create or use an existing KMS Key - http://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html

  2. Click the "Enable Encryption Helpers" checkbox

  3. Paste <COMMAND_TOKEN> into the kmsEncryptedToken environment variable and click encrypt


Follow these steps to complete the configuration of your command API endpoint

  1. When completing the blueprint configuration select "Open" for security
     on the "Configure triggers" page.

  2. Enter a name for your execution role in the "Role name" field.
     Your function's execution role needs kms:Decrypt permissions. We have
     pre-selected the "KMS decryption permissions" policy template that will
     automatically add these permissions.

  3. Update the URL for your Slack slash command with the invocation URL for the
     created API resource in the prod stage.
'''

import boto3
import json
import logging
import os
import sys
import hmac, hashlib

from base64 import b64decode
from urlparse import parse_qs


SLACK_SIGNING_SECRET  = os.environ['slackSigningSecret']
SLACK_SECRET_VERSION = os.environ['slackSigningVersion']

kms = boto3.client('kms')
# To Remove

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def validate(event, context):
    headers = event['headers']
    # todo(skh): Validate that request took place in the last five minutes
    timestamp = event['headers']['X-Slack-Request-Timestamp']
    body = event['body']
    sig_basestring = SLACK_SECRET_VERSION + ':' + timestamp + ':' + body
    m = hmac.new(SLACK_SIGNING_SECRET, digestmod=hashlib.sha256)
    m.update(sig_basestring)
    digest = 'v0=' + m.hexdigest()
    incoming_signature = event['multiValueHeaders']['X-Slack-Signature']
    
    if digest != incoming_signature:
        logger.error("Digest (%s) does not match expected", digest)
        return respond(Exception('Invalid request signature'))


def lambda_handler(event, context):
    validate(event, context)
    
    params = parse_qs(event['body'])
    token = params['token'][0]
    

    user = params['user_name'][0]
    command = params['command'][0]
    channel = params['channel_name'][0]
    if 'text' in params:
        command_text = params['text'][0]
    else:
        command_text = ''

    return respond(None, "%s invoked %s in %s with the following text: %s" % (user, command, channel, command_text))
