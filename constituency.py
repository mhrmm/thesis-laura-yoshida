from hierplane import HierplaneNode, HierplaneWindow

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


CONSTITUENCY_STYLES = {"other": ["color0"],
                          "event": ["color1", "strong"],
                          "entity": ["color2"],
                          "detail": ["color3"],
                          "sequence": ["seq"],
                          "reference": ["placeholder"]}
            
LINK_TO_POSITION = dict()  


class NltkTreeWrapper:
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
        if root.label() in PTB_STYLE_MAP:
            node_type = PTB_STYLE_MAP[root.label()]        
        else:
            node_type = "other"    
        span = self.get_span(root_pos)
        if len(self.get_children(root_pos)) > 0:
            span = None
            label = root.label()
        else:
            label = ' '.join(root.leaves())
        node = HierplaneNode(label, children, 
                             span, root.label(),
                             node_type)
        return node
    
    def to_hierplane(self):
        node = self.to_hierplane_node(())
        return HierplaneWindow(node, ' '.join(self.subtrees[()].leaves()),
                               CONSTITUENCY_STYLES, LINK_TO_POSITION)
        
