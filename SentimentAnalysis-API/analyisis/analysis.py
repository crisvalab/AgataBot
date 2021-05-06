from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

class SentimentAnalysis():

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("sagorsarker/codeswitch-spaeng-sentiment-analysis-lince")
        self.model = AutoModelForSequenceClassification.from_pretrained("sagorsarker/codeswitch-spaeng-sentiment-analysis-lince")
        self.nlp = pipeline('sentiment-analysis', model=self.model, tokenizer=self.tokenizer)

    def analize(self, sentence):
        return self.nlp(sentence)[0]