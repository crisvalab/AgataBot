import os
import gc
import tensorflow as tf
from os.path import isfile, join
import gpt_2_simple as gpt2

class AgataBot():

    def __init__(self, prepare_chat):
        self.RAW_DATASETS_FOLDER = './datasets/raw/'
        self.ENCODED_DATASETS_FOLDER = './datasets/encoded/'
        self.MODEL_NAME = '355M'
        self.RUN_NAME = 'run1'
        self.sess = gpt2.start_tf_sess()
        self.requests = 0
        if prepare_chat:
            self.prepare_chat()

    def download_model(self):
        print(f'Downloading {self.MODEL_NAME} model...')
        gpt2.download_gpt2(model_name=self.MODEL_NAME)
        print(f'Model {self.MODEL_NAME} download correctly!')

    def encode_datasets(self):
        datasets = [f for f in os.listdir(self.RAW_DATASETS_FOLDER) if isfile(join(self.RAW_DATASETS_FOLDER, f))]
        for dataset in datasets:
            print(f'Preparing to encode {dataset} dataset...')
            dataset_path = f'{self.RAW_DATASETS_FOLDER}{dataset}'
            output_path = f'{self.ENCODED_DATASETS_FOLDER}{dataset.replace(".txt", ".npz")}'
            gpt2.encode_dataset(file_path=dataset_path, out_path=output_path, model_name=self.MODEL_NAME)
            print(f'Dataset {dataset} encoded to {output_path}!')
        print('Finished encoding all datasets!\n')

    def start_training(self):
        compressed_datasets = [f for f in os.listdir(self.ENCODED_DATASETS_FOLDER) if isfile(join(self.ENCODED_DATASETS_FOLDER, f))]
        compressed_datasets.sort()
        for compressed_dataset in compressed_datasets:
            dataset_path = f'{self.ENCODED_DATASETS_FOLDER}{compressed_dataset}'
            gpt2.finetune(self.sess, dataset=dataset_path, model_name=self.MODEL_NAME, steps=1000, multi_gpu=True, overwrite=True, run_name=self.RUN_NAME)
            self.sess = gpt2.reset_session(self.sess)
        print(f'Finished training {self.MODEL_NAME} model!')

    def prepare_chat(self):
        gpt2.load_gpt2(self.sess, run_name=self.RUN_NAME)
        _ = gpt2.generate(self.sess, run_name=self.RUN_NAME, temperature=0.7,
                        prefix='My name is Agata.', nsamples=1, batch_size=1, return_as_list=True, 
                        length=25, include_prefix=False, top_p=0.9, top_k=40)[0]
        self.chat_prepared = True

    def generate_answer(self, question, context):
        def get_acurated_answer(question, generated):
            generated = generated.split('\n')
            for i in range(len(generated)):
                if generated[i] == question:
                    return generated[i+1].strip().rstrip()
        if not self.chat_prepared:
            self.prepare_chat()

        generated = gpt2.generate(self.sess, run_name=self.RUN_NAME, temperature=0.7,
                        prefix=context, nsamples=1, batch_size=1, return_as_list=True, 
                        length=200, include_prefix=False, top_p=0.9, top_k=40)[0] #0.9 y 40

        self.requests += 1
        if self.requests == 8:
            tf.reset_default_graph()
            self.sess.close()
            self.sess = gpt2.start_tf_sess(threads=8)
            gpt2.load_gpt2(self.sess)
            self.requests = 0
        gc.collect()

        return get_acurated_answer(question, generated)