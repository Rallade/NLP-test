import neuralcoref
"""
git clone https://github.com/huggingface/neuralcoref.git
cd neuralcoref
pip install -r requirements.txt
pip install -e .
cd ../

PIP VERSION DOES NOT WORK, must be built from source, use commands above
"""
import spacy
import re

nlp = spacy.load("en_core_web_sm") #install spacy, python(3) -m spacy download en_core_web_sm
neuralcoref.add_to_pipe(nlp, greedyness = 0.55) #greedyness somewhat arbitrary, preformed best for the examples
queries = [
    "Though <its> primary duty is to automate Stark’s Malibu estate",
    "the lifelike program fulfills many other needs for Stark, like being an information source for <him>, a diagnostic tool",
    "During the Ultron Offensive, JARVIS was destroyed by Ultron, although <his> remaining programming codes unknowingly continued ",
    "<It> can connect to Stark Industries central database and Stark’s personal server and can access outside computers and radio signals."
]


def resolve(doc, parsed_query):
    """
    doc: spacy language object for entire document
    parsed_query: spacy language object for formatted target query
    """
    token = doc[0]
    match = False
    for i in range(len(doc)):
        j = 0
        #looking for query 
        while(doc[i+j].text == parsed_query[j].text):
            if(j == len(parsed_query) - 1):
                match = True
                break
            j += 1
        if match and doc[i].text == word:
            token = doc[i]
    coreference = token._.coref_clusters[0].main
    return coreference

with open('test_text','r') as text_file:
    text = text_file.read()
    doc = nlp(text.replace('\n', ' '))
    for query in queries:
        match = re.search(r"\<..*>", query)
        word = match.group(0)[1:-1]
        parsed_query = query[:match.start()] + query[match.start() + 1 : match.end() - 1] + query[match.end():]
        parsed_query = nlp(parsed_query)
        coreference = resolve(doc, parsed_query)
        print("INPUT:", query)
        print("Output:", coreference)
        print("The <{0:s}> in the input refers to <{1:s}> entity".format(word, coreference.text))
    


    