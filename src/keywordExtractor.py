import spacy
from spacy import displacy
import entityLinker as el

def get_chuncks_keywords(question,recognized_entites,language='de'):
    
    # Load tokenizer, tagger, parser, NER and word vectors
    nlp = spacy.load(language)
    doc = nlp(question)
    
    # Find named entities
    entities = [(entity.text, entity.label_) for entity in doc.ents]
    
    # Find POS Tags
    pos = [(token, token.pos_) for token in doc]
    
    # Find Dependencies
    dep = [(token, token.dep_) for token in doc]
    
    # Find Noun chunks
    nouns = [noun_chunk for noun_chunk in doc.noun_chunks]
    
    # Find Categories
    categories = [cat for cat in doc.cats]
    
    # Collect Tokens
    ents = list(set([ent[0] for ent in entities]).union([ent['surfaceForm'] for ent in recognized_entites]))
    tokens = ents + [tag[0] for tag in pos if tag[1] == u'VERB']
    
    return entities, pos, dep, nouns, categories, tokens

if __name__ == '__main__':
    
    question = u'Wann sind Barack Obama und Michelle Obama in die Vereinigten Staaten von Amerika ausgewandert?'
    recognized_entites = el.get_linked_entity(question)
    #print(recognized_entites)
    entities, pos, dep, nouns, cats, tokens = get_chuncks_keywords(question,recognized_entites)
    
    print('====== Entities ======')
    
    print(entities)
        
    print('====== POS ======')
        
    print(pos)
        
    print('====== DP ======')
    
    print(dep)
        
    print('====== Nouns ======')
    
    print(nouns)
        
    print('====== Categories ======')
    
    print(cats)
    
    print('====== Tokens ======')
    
    print(tokens)
        
    
    #displacy.parse_deps(text)
        
    #displacy.serve(text)
    #displacy.serve(text,style='ent')
