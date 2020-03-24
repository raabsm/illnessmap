import pandas as pd
import sys

if len(sys.argv) != 2:
    print("Usage: get_sick_reviews <path_to_file>")
    sys.exit()

file = sys.argv[1]

all_reviews = pd.read_json(file, lines=True)


def hsan_total_score(x):
    if x is None:
        return None
    else:
        try:
            return x['total_score']
        except TypeError as e:
            return x


def dict_to_flt(x):
    if isinstance(x, float):
        return x
    return x['total_score']


all_reviews['reg_total_score'] = all_reviews['classification'].apply(dict_to_flt)
all_reviews['hsan_total_score'] = all_reviews['classification_hsan'].apply(hsan_total_score)
sick_df = all_reviews[(all_reviews['reg_total_score'] > 0.1) | ((all_reviews['hsan_total_score'] != None) & (all_reviews['hsan_total_score'] > 0.1))]

sick_df.to_json('sick_reviews.json', orient='records')
