import spacy
#from spacy import displacy
#import entityLinker as el

def get_chuncks_keywords(question,language='de'):
    
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
    #ents = [ent[0] for ent in entities]
    #ents_annotated = [(token,entity['URI']) for entity in recognized_entites for token in ents if token == entity['surfaceForm']] 
    #missing_entities = [(ent,'') for ent in ents if ent not in [x[0] for x in ents_annotated]]
    #tokens = ents_annotated + missing_entities + [(tag[0],'') for tag in pos if tag[1] == u'VERB']
    tokens = entities + [(tag[0],'') for tag in pos if tag[1] == u'VERB']
    
    return entities, pos, dep, nouns, categories, tokens

if __name__ == '__main__':
    
    question = u'Wann sind Barack Obama und Michelle Obama in die Vereinigten Staaten ausgewandert?'
    #question = 'Did you read Game of thrones today?'
    #recognized_entites = el.get_linked_entity(question)
    #recognized_entites=[]
    entities, pos, dep, nouns, cats, tokens = get_chuncks_keywords(question)
    
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
