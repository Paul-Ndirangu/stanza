from fastapi import FastAPI
import stanza
from nltk.tree import Tree
import re

stanza.download('en')
app = FastAPI()
nlp = stanza.Pipeline(
    lang='en', 
    processors='tokenize,pos,constituency', 
    download=None
    )


def constituency_parser(parse_tree):
    """
    Create constituency parsers using spacy module.
    It uses stanza module parse the sentence and create tree then nltk is used to draw a graph.

    :params :
        sentence which is a string to be analysed
    Model returns "" if not parsed successfully else Tree
    """
    # Convert it to a tree object and display
    tree = "" if not parsed_cons_tree else Tree.fromstring(parsed_cons_tree.pretty_print())
    return tree


@app.post('/constituency-parser')
async def parse_constituency_parser():
    global parsed_cons_tree
    text_input = "The quick brown fox jumped over the hedge"
    parsed_cons_tree = nlp(text_input).sentences[0].constituency
    const_parse_tree = constituency_parser(parsed_cons_tree)
    # print(f"\nConst Parse tree: {const_parse_tree}")
    return {
        "const_parse_tree": const_parse_tree
    }

