import re

class Tokenizer:
    def __init__(self):
        pass

    def get_grams_from_source(self, comments):
        grams = list()
        for comment in comments:
            # remove whitespace (2 more)
            comment = re.sub(r'\s\s+', ' ', comment)
            words = comment.split(' ') 
            grams.extend(list(zip(words, words[1:])))
        return grams

    def get_grams_from_license(self, comments):
        grams = list()    
        grams.extend(list(zip(comments, comments[1:])))
        
        return grams