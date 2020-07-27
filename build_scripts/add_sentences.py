import re
import sys
import os
from pymongo import MongoClient


if __name__ == '__main__':

    if len(sys.argv) != 4:
        print("Usage: update_locs <DB> <Collection> <Insert Collection>")
        sys.exit()
    else:
        db, col, insert_col = sys.argv[1], sys.argv[2], sys.argv[3]

    try:
        db = MongoClient(os.environ['URI'])[db]
        collection = db[col]
        insert_collection = db[insert_col]
    except Exception as e:
        print('Error while connecting: ', e)
        sys.exit()

    docs_without_sentences = collection.find({'sentences': None})
    for doc in docs_without_sentences:
        text = doc['text']
        to_insert = {}
        # added to split sentences
        to_insert['sentences'] = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
        insert_collection.update_one({'_id': doc['_id']}, {'$set': to_insert})

    docs_without_sentences.close()


