from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Translator():
    
    def __init__(self):
        self.tokenizer_to_en = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-es-en")
        self.model_to_en = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-es-en")
        self.tokenizer_to_es = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-es")
        self.model_to_es = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-es")

    def translate_to_english(self, text):
        text = self.model_to_en.generate(**self.tokenizer_to_en(text, return_tensors="pt", padding=True))
        text = [self.tokenizer_to_en.decode(t, skip_special_tokens=True) for t in text][0]
        return text

    def translate_to_spanish(self, text):
        text = self.model_to_es.generate(**self.tokenizer_to_es(text, return_tensors="pt", padding=True))
        text = [self.tokenizer_to_es.decode(t, skip_special_tokens=True) for t in text][0]
        return text