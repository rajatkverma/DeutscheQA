import spotlight




def get_linked_entity(text,confidence=0.5):
    annotations = spotlight.annotate('http://api.dbpedia-spotlight.org:2226/rest/annotate',
                                  text,
                                confidence, support=20,spotter='Default')
    return annotations




if __name__== "__main__":
    
    text='Wann wurde Frau Angela Merkel geboren ?'
    annotations=get_linked_entity(text)

