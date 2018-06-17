from SPARQLWrapper import SPARQLWrapper, JSON, CSV
import pandas as pd
import webbrowser

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
prefix rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
prefix dbo: <http://dbpedia.org/ontology/>
prefix dbp: <http://dbpedia.org/property/>
prefix foaf: <http://xmlns.com/foaf/0.1/>
select distinct ?name ?description ?producer ?comment ?homepage where {
?film       rdf:type dbo:Film;
            rdfs:label ?name;
            dbo:abstract ?description;            
            dbp:producer ?producer;            
            rdfs:comment ?comment;
            foaf:homepage ?homepage.
FILTER((lang(?name)="en")&&(lang(?description)="en")&&(lang(?comment)="en"))

OPTIONAL{?film  dbo:thumbnail ?thumbnail.}
}limit 50
""")
sparql.setReturnFormat(JSON)
result = sparql.query().convert()

table = []
head = result["head"]["vars"]
# print(result)
print("count of result:" + str(len(result["results"]["bindings"])))

for item in result["results"]["bindings"]:

    _item = []

    name = item["name"]["value"]
    _item.append(name)

    # language = item["name"]["xml:lang"]
    # _item.append(language)

    description = item["description"]["value"]
    _item.append(description)

    producer = item["producer"]["value"]
    _item.append(producer)

    comment= item["comment"]["value"]
    _item.append(comment)

    homepage = item["homepage"]["value"]
    _item.append(homepage)

    table.append(_item)

_table = pd.DataFrame(table, columns=(head[0], head[1], head[2], head[3], head[4]))
#print(_table)

h = _table.to_html()
with open("film.html", 'w', encoding='utf-8') as f:
    f.write(h)
webbrowser.open('film.html')