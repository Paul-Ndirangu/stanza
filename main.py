from fastapi import FastAPI
import stanza
from nltk.tree import Tree
import re

app = FastAPI()

stanza.download('en')
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


# we need to get tuples from above string..
# we just use stack
def parse_tree_fn(tree_string):
    stack = []
    current = []
    tokens = re.findall(r'\w+|\(|\)', tree_string)

    for token in tokens:
        if token == '(':
            stack.append(current)
            current = []
        elif token == ')':
            if current:
                stack[-1].append(tuple(current))
                current = stack.pop()
        else:
            current.append(token)

    return tuple(current)


def get_branches(tree):
    all_res = []
    def traverse(node, branch):
        if not isinstance(node, tuple):
            temp_br = branch.copy()
            temp_br.append(node)
            all_res.append(temp_br)
            #print(branch, node)
        else:
            label, *children = node
            branch.append(label)
            for child in children:
                traverse(child, branch)
            branch.pop()
    traverse(tree, [])
    return  all_res


def get_return_results(presure_idx, array_vals):
    consecutive_values = []

    # last val of curr sublist
    curr_values = [array_vals[0][-1]]
    for sublist in array_vals[1:]:
        if sublist[:presure_idx] == array_vals[array_vals.index(sublist) - 1][:presure_idx]:
            curr_values.append(sublist[-1])
        else:
            if len(curr_values) > 1:
                consecutive_values.append(curr_values)
            else:
                consecutive_values.append(curr_values[0])
            curr_values = [sublist[-1]]

    # get what is the end of the current sublist
    if len(curr_values) > 1:
        consecutive_values.append(curr_values)
    else:
        consecutive_values.append(curr_values[0])

    return [" ".join(x)  if isinstance(x, list) else x for x in consecutive_values]


@app.post('/constituency-parser')
async def parse_constituency_parser(text_input: str, pressure_index: int):
    global parsed_cons_tree
    
    parsed_cons_tree = nlp(text_input).sentences[0].constituency
    # const_parse_tree = constituency_parser(parsed_cons_tree)
    
    parse_tree_str = str(parsed_cons_tree).replace(" ", ",")
    tree_parsed = parse_tree_fn(parse_tree_str)
    
    all_branches = get_branches(tree_parsed[-1])
    res = get_return_results(pressure_index, all_branches)
    
    return {
        "result": res
    }

