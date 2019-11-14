import hmac, hashlib
import os

SLACK_SIGNING_SECRET  = os.environ['slackSigningSecret']
SLACK_SECRET_VERSION = os.environ['slackSigningVersion']

def validate(event):
    # todo(skh): Validate that request took place in the last five minutes
    timestamp = event['headers']['X-Slack-Request-Timestamp']
    body = event['body']
    sig_basestring = SLACK_SECRET_VERSION + ':' + timestamp + ':' + body
    m = hmac.new(SLACK_SIGNING_SECRET, digestmod=hashlib.sha256)
    m.update(sig_basestring)
    digest = 'v0=' + m.hexdigest()
    incoming_signature = event['multiValueHeaders']['X-Slack-Signature'][0]
    return digest != incoming_signature