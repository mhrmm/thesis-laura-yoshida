from allennlp.predictors.predictor import Predictor
from nltk.tree import Tree
from dependency import DependencyParse
    

def head_to_tree(heads):
    # takes a list of dependency heads and returns each head's children as a dictionary
    children = {}
    for i in range(0,len(heads)+1):
        children[i] = []
    for j in range(0,len(heads)):
        children[heads[j]].append(j+1)
    return children
            
def descendents(tree,i):
    # takes a dictionary and an index i and returns all descendents of the key at i
    if tree[i] == []:
        return [i]
    else:
        desc = [i]
        for c in tree[i]:
            desc+=(descendents(tree,c))
        return desc
    
def get_spans(tree):
    # takes a dictionary and returns a list of lists representing
    # constituents
    spans = []
    for i in tree:
        desc = descendents(tree,i)
        # we ignore one-word constituents
        if len(desc) > 1 and len(desc) < len(tree):
            spans.append([min(desc)-1,max(desc)])
    return spans
  
from collections import defaultdict        

class BiaffineParser:
    def __init__(self):
        self.parser = Predictor.from_path(
                "https://s3-us-west-2.amazonaws.com/allennlp/models/" + 
                "biaffine-dependency-parser-ptb-2018.08.23.tar.gz")


    def __call__(self, sent):
        return self.get_spans(sent)
        
    
    def get_spans(self, sent):
        json_parse = self.parser.predict(sentence=sent)
        heads = json_parse['predicted_heads']
        return heads # This gives the head word of each token.
        # TODO: convert these heads into a list of the constituent spans.
        # see test_biaffine.py to look at an example input/output.

    def parse(self, sent):
        json_parse = self.parser.predict(sentence=sent)
        tags = json_parse['pos']
        deps = json_parse['predicted_dependencies']
        heads = [i-1 for i in json_parse['predicted_heads']]
        words = json_parse['words']
        return DependencyParse(words, heads, deps, tags)
    

    def parse_to_nltk(self, sent):
        def parse_to_nltk_h(root):
            label = words[root]
            child_trees = []
            if root in children:
                for child in children[root]:
                    child_trees.append(parse_to_nltk_h(child))
            return Tree(label, child_trees)
        json_parse = self.parser.predict(sentence=sent)
        tags = json_parse['pos']
        deps = json_parse['predicted_dependencies']
        heads = json_parse['predicted_heads']
        words = json_parse['words']
        
        children = defaultdict(list)
        for (i, head) in enumerate(heads):
            children[head-1].append(i)
        children = dict(children)
        assert len(children[-1]) == 1
        root = children[-1][0]
        return parse_to_nltk_h(root)
                       

    def parse_to_hierplane(self, sent):
        dparse = self.parse(sent)        
        return dparse.to_hierplane().to_json()
        #tree = self.parse_to_nltk(sent)
        #nltk_tree = NltkTreeWrapper(tree)
        #print(nltk_tree.tree)
        #return nltk_tree.to_hierplane().to_json()
        
