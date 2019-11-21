from allennlp.predictors.predictor import Predictor


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
        print(heads) # This gives the head word of each token.
        # TODO: convert these heads into a list of the constituent spans.
        # see test_biaffine.py to look at an example input/output.
        