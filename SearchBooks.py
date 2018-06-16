from SPARQLWrapper import SPARQLWrapper, JSON, CSV
import pandas as pd
import webbrowser

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix dbo: <http://dbpedia.org/ontology/>
prefix dc: <http://purl.org/dc/elements/1.1/>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
select distinct ?name ?subject ?book ?sameAs ?description  where
{
    ?book  rdf:type  dbo:Book;
           
           dct:subject ?subject;
           rdfs:label ?name;
           owl:sameAs ?sameAs;
           dbo:abstract ?description.
}limit 40
""")

sparql.setReturnFormat(JSON)
result = sparql.query().convert()
# ?name ?subject ?book ?sameAs ?description
table = []
head = result["head"]["vars"]

print("count of result:" + str(len(result["results"]["bindings"])))

for item in result["results"]["bindings"]:

    _item = []
    name = item["name"]["value"]
    _item.append(name)

    subject = item["subject"]["value"]
    _item.append(subject)

    book = item["book"]["value"]
    _item.append(book)

    sameAs = item["sameAs"]["value"]
    _item.append(sameAs)

    description = item["description"]["value"]
    _item.append(description)

    table.append(_item)

_table = pd.DataFrame(table, columns=(head[0], head[1], head[2], head[3], head[4]))
# print(_table)
#
h = _table.to_html()

with open("books.html", 'w', encoding='utf-8') as f:
# with open(a, 'w', encoding='utf-8') as f:
    f.write(h)
webbrowser.open('books.html')