import boto3
import json
import logging
import sys
from urlparse import parse_qs

# Custom Modules
import word_repository
from slack_validation import validate
from generator import get_basic, get_scrum, add_suggestion

logger = logging.getLogger()
logger.setLevel(logging.INFO)

word_types = ['adverb', 'verb', 'adjective', 'noun']

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):
    if not validate(event):
        logger.error("Digest does not match expected signature")
        return respond(Exception('Invalid request signature'))
    
    params = parse_qs(event['body'])
    
    if 'text' not in params:
        return respond(None, get_basic(event, 'present'))
    
    text = params['text'][0].split()    
    if text[0] == 'scrum':
        response = get_scrum(event)
    elif text[0] == 'suggest':
        if text[1] in word_types: 
            response = add_suggestion(text[1], text[2])
        else:
            response = 'Choose a valid word type: [' + ', '.join(word_types) + ']'
    else:
        response = get_basic(event, 'present')
    
        
    return respond(None, response)
