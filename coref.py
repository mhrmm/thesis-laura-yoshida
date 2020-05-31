from allennlp.predictors.predictor import Predictor
from biaffine import BiaffineParser
from dependency import DependencyParse
import allennlp_models.coref


class AllenCoref:
    def __init__(self):
        self.predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/coref-spanbert-large-2020.02.27.tar.gz")
        self.parser = BiaffineParser()

    def __call__(self, sent):
        return self.predictor.predict(sent)
    
        
 
    def parse_to_hierplane(self, sent):
        coref_results = self(sent)
        document = ' '.join(coref_results['document'])
        dparse = self.parser.parse(document)
        words, heads, deps, tags = dparse.words, dparse.heads, dparse.deps, dparse.tags
        assert(len(words) == len(coref_results['document']))
        for cluster in coref_results['clusters']:
            sorted_cluster = sorted([tuple(x) for x in cluster])
            assert(len(sorted_cluster) >= 1)
            ante_start, ante_stop = sorted_cluster[0]
            antecedent_text = ' '.join(words[ante_start:ante_stop+1])
            for (a, b) in sorted_cluster[1:]:
                for x in range(a, b+1):
                    tags[x] = 'COREF:{}'.format(antecedent_text)        
        dparse2 = DependencyParse(words, heads, deps, tags)
        return dparse2.to_hierplane().to_json()
                
        