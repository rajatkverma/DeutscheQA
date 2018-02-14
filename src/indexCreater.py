#
#	Need to add SPARQLWrapper to requirments
#	Need to have the index json file to read from
#

import json
import io
import csv
from SPARQLWrapper import SPARQLWrapper, JSON

def get_DBPedia_DE_label(uri):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    select distinct ?label where { <"""
    + uri +"""> 
    <http://www.w3.org/2000/01/rdf-schema#label> ?label FILTER (lang(?label) = 'de') }
    """)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(10000)
    results = sparql.query().convert()
    labels = []
    for result in results['results']['bindings']:
        labels.append(result['label']['value'])
    return labels

def get_WikiData_Id(uri):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    SELECT DISTINCT ?wiki
    WHERE {
            <"""+uri+"""> <http://www.w3.org/2002/07/owl#sameAs> ?wiki.
            FILTER regex(?wiki,'wikidata.org')
    }
    """)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(10000)
    results = sparql.query().convert()
    try:
        wid = results["results"]["bindings"][0]['wiki']['value']
        return wid[wid.rfind('/')+1:]
    except IndexError:
        return ''

def get_WikiData_DE_label(wikiId):
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery("""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    SELECT DISTINCT ?label 
    WHERE 
    { 
      {wd:"""+wikiId+""" skos:altLabel ?label.} 
      UNION
      {wd:"""+wikiId+""" rdfs:label ?label.} 
      UNION
      {wd:"""+wikiId+""" dbo:alias ?label.}
      FILTER (lang(?label) = 'de')
    } """)
    sparql.setReturnFormat(JSON)
    sparql.setTimeout(10000)
    results = sparql.query().convert()
    labels = []
    for result in results['results']['bindings']:
        labels.append(result['label']['value'])
    return labels

if __name__ == '__main__':
    with open("labels.csv", "a+") as out:
        writer = csv.writer(out)
        with io.open('./dbentityindex9.json', mode="r", encoding="utf-8") as f:
            for cnt, line in enumerate(f):
                if cnt < 0:#30716:
                    obj = json.loads(line)
                    url = obj['_source']['uri']
                    #url = 'http://dbpedia.org/resource/Cologne'
                    print(cnt,url)
                    DBlabels = get_DBPedia_DE_label(url)
                    wikiId = get_WikiData_Id(url)
                    WDlabels = []
                    if len(wikiId):
                        WDlabels = get_WikiData_DE_label(wikiId)
                    labels = list(set(DBlabels).union(WDlabels))
                    for label in labels:
                        writer.writerow([url.encode('utf-8'),label.encode('utf-8')])