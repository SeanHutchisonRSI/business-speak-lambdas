import sys
import json
import uuid
from random import randint
# import boto3

def write(s):
    sys.stdout.write(s)

def read_file(filename):
    # with open("words/" + filename) as f:
    with open("lambdas/import/words/" + filename) as f:
        return f.readlines()

def print_random_words(times, words):
    for _ in range(0, times):
        endIndex = len(words) - 1
        index = randint(0, endIndex)
        word = words[index]
        sys.stdout.write(word)

def print_items(items):
    for word in items:
        sys.stdout.write(word)

def word_to_json(word, word_type):
    d = {}
    d["word"] = word.strip()
    d["word_id"] = uuid.uuid4().urn[9:]
    d["active"] = True
    d["word_type"] = word_type
    return d
    
def words_to_json(words, word_type):
    return list(map(lambda word: word_to_json(word, word_type), words))

def print_dictionary(dictionary):
    sys.stdout.write(json.dumps(dictionary, sort_keys=True, indent=4))


def lambda_handler(event, context):
    adverbs = words_to_json(read_file("adverbs.txt"), "adverb")
    adjectives = words_to_json(read_file("adjectives.txt"), "adjective")
    nouns = words_to_json(read_file("nouns.txt"), "noun")
    verbs = words_to_json(read_file("verbs.txt"), "verb")
    past_verbs = words_to_json(read_file("verbs_past.txt"), "verb")
    
    items = adverbs + adjectives + nouns + verbs + past_verbs
    write("Adverbs: " + str(len(adverbs)) + "\n")
    write("Adjectives: " + str(len(adjectives)) + "\n")
    write("Nouns: " + str(len(nouns)) + "\n")
    write("Verbs: " + str(len(verbs)) + "\n")
    write("Past Verbs: " + str(len(past_verbs)) + "\n")
    write("Total: " + str(len(items)) + "\n")
    
    for item in items:
        write(item["word"] + "\n")

    # dynamodb = boto3.resource('dynamodb')
    # table = dynamodb.Table('business_speech_words')
    # with table.batch_writer() as batch:
    # for item in items:
    #     print_dictionary(item)
        # batch.put_item(Item=item)

lambda_handler(None, None)
            

