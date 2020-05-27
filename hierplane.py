import json

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


    
class HierplaneNode:
    def __init__(self, label, children,
                 span, relationship_to_parent, style):
        self.label = label
        self.children = children
        self.span = span
        self.relationship_to_parent = relationship_to_parent
        self.style = style
        
    def to_json(self):
        node_type = self.style
        children = [child.to_json() for child in self.children]
        #if len(children) == 0:
        word = self.label
        #else:
        #    word = self.relationship_to_parent        
        result = {'nodeType': node_type,
                  'word': word,
                  'link': self.relationship_to_parent}
        if len(children) > 0:
            result['children'] = children
        #else:
        if self.span is not None:
            result['spans'] = [{'start': self.span[0], 'end': self.span[1]}]         
        return result

class HierplaneWindow:
    
    def __init__(self, root_node, text, style_map, link_to_pos):
        self.root_node = root_node
        self.text = text
        self.style_map = style_map
        self.link_to_pos = link_to_pos


    def to_json(self):
        pre_json = {'linkToPosition': self.link_to_pos,
                    'nodeTypeToStyle': self.style_map,
                    'text': self.text,
                    'root': self.root_node.to_json()}
        return pre_json
        
    def to_html(self):
        pre_json = {'linkToPosition': self.link_to_pos,
                    'nodeTypeToStyle': self.style_map,
                    'text': self.text,
                    'root': self.root_node.to_json()}
        output = (PROLOGUE 
                  + json.dumps(pre_json, indent=4) 
                  + EPILOGUE)
        return output
        
    def save_as_html(self, filename):
        with open(filename, 'w') as writer:
            writer.write(self.to_html())
    
    




