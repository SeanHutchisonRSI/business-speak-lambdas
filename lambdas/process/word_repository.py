import boto3
from collections import defaultdict

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('business_speech_words')

item_refs = table.scan(
    ProjectionExpression='word_id',
    Limit=500)
item_map = defaultdict(list)
for ref in item_refs:
    item_map[ref['word_type']] = ref
    


def test():
    return item_refs