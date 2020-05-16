# Installing Parsers

To install the Berkeley parser, do the following in the Terminal:

    pip install benepar

Then open python and download the Berkeley parser model for English:

    > import benepar
    > benepar.download('benepar_en2')

# Hierplane Visualization

To visualize the Berkeley parser using Hierplane:

    > parser = benepar.Parser("benepar_en2")
    > parse = parser.parse("Colorless green ideas sleep furiously.")
    > from hierplane import *    
    > window = HierplaneWindow.from_nltk_tree(parse)
    > window.save_as_html('foo.html')
    
Then open ```foo.html``` in your preferred browser.


# Attachment Schema

In a Python interpreter, do the following:

    > from berkeley import BerkeleyParser
    > from evaluate import AttachmentSchema
    > schemas = AttachmentSchema.from_plaintext_file('data/pp1.asc')
    > evaluate(schemas, BerkeleyParser())        


    