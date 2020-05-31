# -*- coding: utf-8 -*-

from collections import defaultdict
from hierplane import HierplaneNode, HierplaneWindow

PTB_ENTITY_TAGS = ['NP','NX','NN','NNS','NNP','NNPS','PRP','PRP$','NOUN','PRON','PROPN']
PTB_EVENT_TAGS = ['S','SBAR','SBARQ','SINV','SQ','VP','VB','VBD',
                  'VBG','VBN','VBP','VBZ', 'VERB']
PTB_DETAIL_TAGS = ['ADJP','ADVP','PP','JJ','JJR','JJS','RB','RBR','RBS','RP','IN','ADP','ADJ']
PTB_STYLE_MAP = dict([(tag, 'entity') for tag in PTB_ENTITY_TAGS]
                     + [(tag, 'event') for tag in PTB_EVENT_TAGS]
                     + [(tag, 'detail') for tag in PTB_DETAIL_TAGS])
PTB_STYLE_MAP['COREF'] = "reference"

LINK_TO_POSITION = {
  "nsubj": "left",
  "dobj": "right",
  "pobj": "right"
}

DEPENDENCY_STYLES = {"other": ["color0"],
                          "event": ["color1", "strong"],
                          "entity": ["color2"],
                          "detail": ["color3"],
                          "sequence": ["seq"],
                          "reference": ["placeholder"]}
 

class Tree:
    def __init__(self, label, children, span, text, dependency, tag):
        self.label = label
        self.children = children
        self.span = span
        self.text = text
        self.dependency = dependency
        self.tag = tag

def treeify(dparse):
    def treeify_h(root, offset):
        label = dparse.words[root]
        dependency = dparse.deps[root]
        tag = dparse.tags[root]
        child_trees = []
        initial = offset
        if root in children:
            left_children = [child for child in children[root] if child < root]
            for child in left_children:
                child_tree, offset = treeify_h(child, offset)
                offset += 1
                child_trees.append(child_tree)        
        start = offset
        offset += len(label)
        stop = offset
        if root in children:
            right_children = [child for child in children[root] if child > root]
            for child in right_children:                
                offset += 1
                child_tree, offset = treeify_h(child, offset)                
                child_trees.append(child_tree)                
        return Tree(label, child_trees, (start, stop), text[initial:offset], dependency, tag), offset
    
    text = ' '.join(dparse.words)
    heads = dparse.heads
    children = defaultdict(list)
    for (i, head) in enumerate(heads):
        children[head].append(i)
    children = dict(children)
    assert len(children[-1]) == 1
    root = children[-1][0]
    result, _ = treeify_h(root, 0)
    return result

    
class DependencyParse:
    def __init__(self, words, heads, deps, tags):
        self.words = words
        self.heads = heads
        self.deps = deps
        self.tags = tags
        self.tree = treeify(self)
        
    def get_span(self, position):
        return self.spans[position]
    
    def get_tree(self, position):
        return self.subtrees[position]
        
    def get_children(self, position):
        child_positions = sorted([pos2 for pos2 in self.treepositions 
                                  if pos2[:-1] == position])
        return child_positions
        
    def to_hierplane_node(self, root):
        children = []
        for child in root.children:
            children.append(self.to_hierplane_node(child))
        label = root.label
        if root.tag.startswith("COREF:"):
            label = root.tag[len("COREF:"):]
            root.tag = "COREF"
        node_type = "other"  
        if root.tag in PTB_STYLE_MAP:
            node_type = PTB_STYLE_MAP[root.tag]        
        node = HierplaneNode(label, children, root.span, 
                             root.dependency, node_type)
        return node
    
    def to_hierplane(self):
        node = self.to_hierplane_node(self.tree)
        return HierplaneWindow(node, self.tree.text, DEPENDENCY_STYLES, LINK_TO_POSITION)