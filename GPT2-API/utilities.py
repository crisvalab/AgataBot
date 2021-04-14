import argparse
from conversation import Conversation
from bot import AgataBot
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer_to_en = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-es-en")
model_to_en = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-es-en")
tokenizer_to_es = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-es")
model_to_es = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-es")

parser = argparse.ArgumentParser(description='Interact with GPT-2 functionality.')
parser.add_argument('--download_model', help=f'Starts downloading the model.', action='store_true')
parser.add_argument('--encode', help='Starts encoding all datasets.', action='store_true')
parser.add_argument('--train', help='Starts training the model.', action='store_true')
parser.add_argument('--dialogue', help='Starts talking with the model.', action='store_true')
args = parser.parse_args()

if __name__ == '__main__':
    bot = AgataBot(prepare_chat=True)

    if args.download_model:
        print(f'Preparing to download the {bot.MODEL_NAME} model...')
        bot.download_model()
    elif args.encode:
        print('Preparing to encode all datasets...')
        bot.encode_datasets()
    elif args.train:
        print('Preparing to train the model...')
        bot.start_training()
    elif args.dialogue:
        print('Preparing to dialogue with the model...')
        convers = Conversation()
        while True:
            text = input("Humano: ")
            if text != '':
                text = model_to_en.generate(**tokenizer_to_en(text, return_tensors="pt", padding=True))
                text = [tokenizer_to_en.decode(t, skip_special_tokens=True) for t in text][0]
                convers.append_context(text)
                response = bot.generate_answer(question=text, context=convers.context)
                convers.append_context(response)
                response = model_to_es.generate(**tokenizer_to_es(response, return_tensors="pt", padding=True))
                response = [tokenizer_to_es.decode(t, skip_special_tokens=True) for t in response][0]
                print(f'Agata: {response}')
