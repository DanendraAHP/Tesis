from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import preprocessor as p
from src.slang_word import SLANG_WORDS

p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.HASHTAG, p.OPT.RESERVED, p.OPT.EMOJI, p.OPT.SMILEY)
class Preprocessor:
    """
    Untuk preprocess sebelum masuk ke fine tuner
    input :
        preprocess_type : p0/p1/p2/p3
        tokenizer : huggingface tokenizer
        tokenizer_max_length : max length hasil tokenizer nantinya
        text_col : kolom text raw yang ingin dibersihkan
        label_col : kolom label yang ingin diprediksi
    out : 
        tokenized_inputs : huggingface dataset hasil pembersihan dan tokenizer
    """
    def __init__(self, 
                 preprocess_type:str , 
                 tokenizer, 
                 tokenizer_max_length:int, 
                 text_col:str,
                 label_col:str
        ):
        self.prepocess_type = preprocess_type
        self.tokenizer = tokenizer
        self.tokenizer_max_length = tokenizer_max_length
        self.text_col = text_col
        self.label_col = label_col
        if self.prepocess_type=='p01' or self.prepocess_type=='p03':
            #create stopword remover
            self.stop_factory = StopWordRemoverFactory()
            self.stopword_remover = self.stop_factory.create_stop_word_remover()
        if self.prepocess_type=='p02' or self.prepocess_type=='p03':
            # create stemmer
            self.factory = StemmerFactory()
            self.stemmer = self.factory.create_stemmer()
        
    def clean_repetitive(self, word):
        prev_char = None
        char_count=-1
        clean_word=''
        for c in word:
            if prev_char!=c:
                prev_char=c
                char_count=0
            else:
                char_count+=1
            if char_count<1:
                clean_word+=c
        #remove word if only 1 char left
        return clean_word if len(clean_word)>1 else ''
    def clean_text(self, text):
        #lower case
        text = text.lower()
        #clean text with tweet-preprocessor
        text = p.clean(text)
        #clean repetitive word
        #text = " ".join([self.clean_repetitive(word) for word in text.split()])
        #convert slang word into dictionary
        text = " ".join([SLANG_WORDS[word] if word in SLANG_WORDS else word for word in text.split()])
        return text
    def stem(self, text):
        return self.stemmer.stem(text)
    def stopword_removal(self, text):
        return self.stopword_remover.remove(text)
    def preprocess_dataset(self, examples):
        inputs = examples[self.text_col]
        inputs = [self.clean_text(input) for input in inputs]
        if self.prepocess_type=='p01' or self.prepocess_type=='p03':
            inputs = [self.stopword_removal(input) for input in inputs]
        if self.prepocess_type=='p02' or self.prepocess_type=='p03':
            inputs = [self.stem(input) for input in inputs]
        targets =examples[self.label_col] 
        tokenized_inputs = self.tokenizer(
            inputs, max_length=self.tokenizer_max_length, truncation=True, padding=True
        )
        labels = self.tokenizer(
            targets, padding=True
        )
        tokenized_inputs['labels'] = labels['input_ids']
        return tokenized_inputs
    