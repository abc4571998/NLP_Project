"""
word deletion Transformation
============================================

"""

from .transformation import Transformation
from gramformer import Gramformer
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from textattack.shared import AttackedText
import nltk
import functools

@functools.lru_cache(maxsize=2**14)
def get_entities(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    entities = nltk.chunk.ne_chunk(tagged, binary=True)
    return entities.leaves()
    
class WordDeletion(Transformation):
    def _get_transformations(self, current_text, indices_to_modify):
        transformed_texts = []
        gf = Gramformer(models=1)
        grammar_texts = []
        answer = []
        print(current_text)
        grammar_texts.append(str(current_text)[15:-3])
        if len(current_text.words) > 1: 
            for i in indices_to_modify: #문장에서 한 단어씩 빼보기 
                # transformed_texts.append(current_text.delete_word_at_index(i)) #단어 뺐을 때 문장을 저장하기
                new_sentence = str(current_text.delete_word_at_index(i))[15:-3] #+ "." 
                grammar_sentence =list( gf.correct(new_sentence, max_candidates=1))[0] #그래머 체크, 결과 하나만 나오게 
                if grammar_sentence not in grammar_texts:
                    grammar_texts.append(grammar_sentence.lower()) #오류를 수정한 문장
            # print(grammar_texts)
            answer = [] 
            for index, item in enumerate(grammar_texts):
                tokenized_sentence = word_tokenize(item)
                pos = pos_tag(tokenized_sentence)

                for token in pos:
                    if token[0] == "n't" or token[0] == "not":
                        del tokenized_sentence[tokenized_sentence.index(token[0])]
                        continue
                    
                    elif token[1] == "JJ" or token[1] == "RB" or token[1] == "DT" or token[1] == "CC":
                        del tokenized_sentence[tokenized_sentence.index(token[0])]
                        continue
                new = ' '.join(s for s in tokenized_sentence)
                # print("token sentence", tokenized_sentence)
                new_grammmar =list( gf.correct(new, max_candidates=1))[0]
                # print("new grammar", new_grammmar)
                answer.append(AttackedText(new_grammmar))
                
        # print(answer)
        return answer
