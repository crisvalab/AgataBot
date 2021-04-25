from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

class SentimentAnalysis():

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("sagorsarker/codeswitch-spaeng-sentiment-analysis-lince")
        self.model = AutoModelForSequenceClassification.from_pretrained("sagorsarker/codeswitch-spaeng-sentiment-analysis-lince")
        self.nlp = pipeline('sentiment-analysis', model=self.model, tokenizer=self.tokenizer)

    def analize(self, sentence):
        return self.nlp(sentence)[0]

if __name__ == '__main__':
    an = SentimentAnalysis()
    print(an.analize("I don't like pizza."))