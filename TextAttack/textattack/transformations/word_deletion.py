"""
word deletion Transformation
============================================

"""

from .transformation import Transformation
from gramformer import Gramformer
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
  
        if len(current_text.words) > 1:
            for i in indices_to_modify:
                transformed_texts.append(current_text.delete_word_at_index(i))
                new_sentence = str(current_text.delete_word_at_index(i))[16:-5] + "."
                grammar_sentence =list( gf.correct(new_sentence, max_candidates=1))[0]
                # if  new_sentence == grammar_sentence:
                #     grammar_texts.append(grammar_sentence.lower())
                # else:
                #     grammar_texts.append('')
                grammar_texts.append(grammar_sentence.lower())
            answer = [] 
            for index, item in enumerate(grammar_texts):
                entities = get_entities(item)
                check_subject, check_verb = False, False
                for idx, entity in enumerate(entities):
                    if entity[1] in ['NNP', 'NE', 'PRP', 'NNS', 'NN', 'NP', 'JJ']:
                        check_subject = True
                   
                    if check_subject == True and entity[1] in ['VBP', 'VB', 'VBD', 'PRP', 'VBZ']:
                         check_verb = True
                    
                if check_subject and check_verb:
                    # print(transformed_texts[index])
                    answer.append(transformed_texts[index])
        print("answer", answer)
        return answer
    
