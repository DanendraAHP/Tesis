from Levenshtein import distance
import re

class PostProcessor:
    def __init__(self, use_postprocess):
        self.use_postprocess = use_postprocess
        self.aspect_categories = ['price', 'produk', 'payment', 'website&apps', 'delivery', 'customerservice', 'user']
        self.sentiments = ['negative', 'positive', 'neutral']
    def edit_word(self, pred_word:str, true_sentence: list[str]):
        min_dist = 9999
        for true_word in true_sentence:
            dist = distance(pred_word, true_word)
            if dist<min_dist:
                min_dist=dist
                corrected_word = true_word
        return corrected_word
    def edit_words(self, pred_word:str, true_sentence: list[str])->str:
        pred_word = pred_word.split()
        corrected_words = [self.edit_word(word, true_sentence) for word in pred_word]
        return " ".join(corrected_words)
    def post_process(self, entity:str, aspect_term:str, opinion_term:str, sentiment:str, aspect_category:str, orig_sentence:str)->str:
        aspect_category = self.edit_word(aspect_category, self.aspect_categories)
        sentiment = self.edit_word(sentiment, self.sentiments)
        orig_sentence = re.sub(r'[^\w\s]', ' ', orig_sentence)
        orig_sentence = orig_sentence.strip()
        orig_sentence = orig_sentence.split()
        orig_sentence = [sen for sen in orig_sentence if sen!='' or sen!=' ']
        if self.use_postprocess:
            #to avoid postprocessing implisit aspect
            if aspect_term!='_':
                aspect_term = self.edit_words(aspect_term, orig_sentence)
                #aspect_term = re.sub(r'[^\w\s]', '', aspect_term)
            if entity!='_':
                entity = self.edit_words(entity, orig_sentence)
                #entity = re.sub(r'[^\w\s]', '', entity)
            opinion_term = self.edit_words(opinion_term, orig_sentence)
            opinion_term = re.sub(r'[^\w\s]', '', opinion_term)
        return entity, aspect_term, opinion_term, sentiment, aspect_category