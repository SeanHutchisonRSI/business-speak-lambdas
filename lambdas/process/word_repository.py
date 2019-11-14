import boto3
from collections import defaultdict
from random import randint
from boto3.dynamodb.conditions import Key

TABLE_NAME = 'business_speech_words'

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)
ref_map = defaultdict(list)

item_refs = table.scan(
    ProjectionExpression='word_id, word_type',
    Limit=500)
for ref in item_refs['Items']:
    word_type = ref['word_type']
    ref_map[word_type].append(ref)

def getRandomWord(word_type):
    refs = ref_map[word_type]
    word_id = refs[randint(0, len(refs)-1)]['word_id']
    item = table.get_item(TableName=TABLE_NAME, Key={'word_id':word_id})['Item']
    return item['word']
