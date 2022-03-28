import re

class Tokenizer:
    def __init__(self):
        pass

    def get_grams_from_source(self, comments):
        grams = list() # plain text (splited by whitespace)
        words = list() # 2-gram tuple
        for comment in comments:
            # remove whitespace (2 more)
            comment = re.sub(r'\s\s+', ' ', comment)
            word = comment.split(' ') 
            words.extend(word)
            grams.extend(list(zip(word, word[1:])))
        return grams, words, comments

    def get_grams_from_license(self, comments):
        grams = list()    
        grams.extend(list(zip(comments, comments[1:])))

        return grams
