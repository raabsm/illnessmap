import re


def add_sentences_to_reviews(collection_from, collection_to):
    docs_without_sentences = collection_from.find({'sentences': None})
    for doc in docs_without_sentences:
        text = doc['text']
        to_insert = {}
        # added to split sentences
        to_insert['sentences'] = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
        collection_to.update_one({'_id': doc['_id']}, {'$set': to_insert})

    docs_without_sentences.close()




