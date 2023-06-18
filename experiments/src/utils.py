import re
#def extract_quadruplet(label_sequence, orig_sequence, postprocessor):
# def extract_quadruplet(label_sequence, orig_sequence, postprocessor):
#     extractions = []
#     # find all matching quadruplet with (); pattern
#     quadruplets = re.findall("\(.*?\)", label_sequence)
#     for quadruplet in quadruplets:
#         # Remove the in the start "("  and at the end ")".
#         quadruplet = quadruplet[1:-1]
#         try:
#             aspect_term, opinion_term, sentiment, aspect_category = quadruplet.split(',')
#             #aspect_term, opinion_term, sentiment, aspect_category = postprocessor.post_process(aspect_term, opinion_term, sentiment, aspect_category, orig_sequence)
#         except ValueError:
#             aspect_term, opinion_term, sentiment, aspect_category = '', '', '', ''
#         aspect_term = aspect_term.strip().lower()
#         opinion_term = opinion_term.strip().lower()
#         sentiment = sentiment.strip().lower()
#         aspect_category = aspect_category.strip().lower()
#         extractions.append((aspect_term, opinion_term, sentiment, aspect_category)) 
#     return extractions

def extract_quadruplet(sequence):
    extractions = []
    # find all matching quadruplet with (); pattern
    quadruplets = re.findall("\(.*?\)", sequence)
    for quadruplet in quadruplets:
        # Remove the in the start "("  and at the end ")".
        quadruplet = quadruplet[1:-1]
        try:
            aspect_term, opinion_term, sentiment, aspect_category = quadruplet.split(',')
        except ValueError:
            aspect_term, opinion_term, sentiment, aspect_category = '', '', '', ''
        aspect_term = aspect_term.strip().lower()
        opinion_term = opinion_term.strip().lower()
        sentiment = sentiment.strip().lower()
        aspect_category = aspect_category.strip().lower()
        extractions.append((aspect_term, opinion_term, sentiment, aspect_category)) 
    return extractions

def extract_triplet(sequence):
    extractions = []
    # find all matching quadruplet with (); pattern
    triplets = re.findall("\(.*?\)", sequence)
    for triplet in triplets:
        # Remove the in the start "("  and at the end ")".
        triplet = triplet[1:-1]
        try:
            aspect_term, opinion_term, sentiment = triplet.split(',')
        except ValueError:
            aspect_term, opinion_term, sentiment = '', '', ''
        aspect_term = aspect_term.strip().lower()
        opinion_term = opinion_term.strip().lower()
        sentiment = sentiment.strip().lower()
        extractions.append((aspect_term, opinion_term, sentiment)) 
    return extractions