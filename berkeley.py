import benepar

PROLOGUE = r"""<!DOCTYPE html><html>
  <head>
    <title>Hierplane!</title>
    <link rel="stylesheet" type="text/css" href="http://unpkg.com/hierplane/dist/static/hierplane.min.css">
  </head>
  <body>
    <script src="http://unpkg.com/hierplane/dist/static/hierplane.min.js"></script>
    <script>
    const tree ="""
    
EPILOGUE = r""";
      hierplane.renderTree(tree);
    </script>
  </body>
</html>
"""

class BerkeleyParser:
    def __init__(self, model = "benepar_en2"):
        self.parser = benepar.Parser(model)

    def __call__(self, sent):
        return self.get_spans(sent)
        
    def get_spans(self, sent):
        def get_spans_helper(treepositions, start_index):
            children = sorted([position for position in treepositions 
                               if len(position) == 1])
            if len(children) == 0:
                return [(start_index, start_index+1)]
            result = []
            orig_start_index = start_index
            for child in children:
                descendants = [position[1:] for position in treepositions 
                               if len(position) > 0 and position[0] == child[0]]
                child_spans = get_spans_helper(descendants, start_index)
                result += child_spans
                start_index = child_spans[0][1]
            result = [(orig_start_index, start_index)] + result
            return result
        tree = self.parser.parse(sent)
        return set(get_spans_helper(tree.treepositions(), 0))
    

class BerkeleyTreeWrapper:
    def __init__(self, tree):
        self.tree = tree
        nonleaves = [pos for pos in tree.treepositions() 
                         if pos + (0,) in tree.treepositions()]
        self.subtrees = dict(zip(nonleaves, list(tree.subtrees())))
        self.treepositions = [pos for pos in nonleaves if pos != ()]
        self.spans = dict()
        def compute_spans(position, offset):
            child_positions = self.get_children(position)
            revised_offset = offset
            for child_pos in child_positions:
                revised_offset = compute_spans(child_pos, revised_offset)
                revised_offset += 1
            right_bound =  offset + len(' '.join(self.subtrees[position].leaves()))
            self.spans[position] = (offset, right_bound)
            return right_bound
        compute_spans((), 0)
    
    def get_span(self, position):
        return self.spans[position]
    
    def get_tree(self, position):
        return self.subtrees[position]
        
    def get_children(self, position):
        child_positions = sorted([pos2 for pos2 in self.treepositions 
                                  if pos2[:-1] == position])
        return child_positions
        
    def to_hierplane_node(self, root_pos):
        root = self.get_tree(root_pos)
        children = []
        for child_pos in self.get_children(root_pos):
            children.append(self.to_hierplane_node(child_pos))
        node = HierplaneNode(' '.join(root.leaves()), children, 
                             self.get_span(root_pos), root.label())
        return node
    
    def to_hierplane(self):
        node = self.to_hierplane_node(())
        return HierplaneWindow(node, ' '.join(self.subtrees[()].leaves()))
        
        
import json

PTB_CLAUSE_TAGS = ['S', 'SBAR', 'SBARQ', 'SINV', 'SQ']
PTB_PHRASE_TAGS = ['ADJP', 'ADVP', 'CONJP', 'FRAG', 'INTJ', 'LST',
                   'NAC', 'NP', 'NX', 'PP', 'PRN', 'PRT', 'QP',
                   'RRC', 'UCP', 'VP', 'WHADJP', 'WHAVP', 'WHNP',
                   'WHPP', 'X']
PTB_WORD_TAGS = ['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS',
                 'LS','MD','NN','NNS','NNP','NNPS','PDT','POS',
                 'PRP','PRP$','RB','RBR','RBS','RP','SYM',
                 'TO','UH','VB','VBD','VBG','VBN','VBP','VBZ',
                 'WDT','WP','WP$','WRB']
PTB_ENTITY_TAGS = ['NP','NX','NN','NNS','NNP','NNPS','PRP','PRP$']
PTB_EVENT_TAGS = ['S','SBAR','SBARQ','SINV','SQ','VP','VB','VBD',
                  'VBG','VBN','VBP','VBZ']
PTB_DETAIL_TAGS = ['ADJP','ADVP','PP','JJ','JJR','JJS','RB','RBR','RBS','RP']
PTB_STYLE_MAP = dict([(tag, 'entity') for tag in PTB_ENTITY_TAGS]
                     + [(tag, 'event') for tag in PTB_EVENT_TAGS]
                     + [(tag, 'detail') for tag in PTB_DETAIL_TAGS])
    
class HierplaneNode:
    def __init__(self, label, children,
                 span, relationship_to_parent):
        self.label = label
        self.children = children
        self.span = span
        self.relationship_to_parent = relationship_to_parent
        
    def to_json(self):
        if self.relationship_to_parent in PTB_STYLE_MAP:
            node_type = PTB_STYLE_MAP[self.relationship_to_parent]        
        else:
            node_type = "other"
        word = self.label
        children = [child.to_json() for child in self.children]
        result = {'nodeType': node_type,
                  'word': word,
                  'link': self.relationship_to_parent}
        if len(children) > 0:
            result['children'] = children
        else:
            result['spans'] = [{'start': self.span[0], 'end': self.span[1]}]         
        return result

class HierplaneWindow:
    
    def __init__(self, root_node, text):
        self.root_node = root_node
        self.text = text
        
    def to_html(self):
        pre_json = {'nodeTypeToStyle': {
                          "other": ["color0"],
                          "event": ["color1", "strong"],
                          "entity": ["color2"],
                          "detail": ["color3"],
                          "sequence": ["seq"],
                          "reference": ["placeholder"]
                        },
                    'text': self.text,
                    'root': self.root_node.to_json()}
        output = (PROLOGUE 
                  + json.dumps(pre_json, indent=4) 
                  + EPILOGUE)
        return output
        

