import pickle
import json
import argparse
from tqdm import tqdm
from copy import deepcopy

import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor

if torch.cuda.is_available():
    DEVICE = 'cuda'
else:
    DEVICE = 'cpu'
class CostModel(object):
    def __init__(self) -> None:
        # Load Whisper model and processor
        self.__processor = WhisperProcessor.from_pretrained("openai/whisper-small.en")
        self.__model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small.en").to(DEVICE)
        self.__audio_inputs = None

    def set_audio(self, audio, sampling_rate):
        self.__audio_inputs = self.__processor(
            audio, sampling_rate=sampling_rate, return_tensors="pt"
        ).input_features.to(DEVICE)

    def get_loss(self, text):
        # Prepare the target text input IDs
        target = self.__processor(
            text=text, return_tensors="pt", padding=True
        ).input_ids.to(DEVICE)

        # Make sure to set the decoder input IDs
        with torch.no_grad():
            outputs = self.__model(input_features=self.__audio_inputs, labels=target)

        return outputs.loss.item()


class Environment(object):
    def __init__(self, init_state, cost_function, phoneme_table) -> None:
        self.init_state = init_state
        self.phoneme_table = deepcopy(phoneme_table)
        self.__cost_function = cost_function

    def compute_cost(self, text):
        try:
            cost = self.__cost_function(text)
        except:
            cost = 1e6
        return cost

correct=[]
incorrect=[]
evaluated=[]
with open("data.pkl", 'rb') as fp:
    data = pickle.load(fp)
with open("phoneme_table.json", 'r') as fp:
    phoneme_table = json.load(fp)
cost_model = CostModel()
i=0
with open("outputs.json", 'r') as file:
    output_text = json.load(file)
for sample in tqdm(data):
    audio = sample['audio']['array']
    sr = sample['audio']['sampling_rate']
    gold = sample['gold']
    text=sample['text']
    environment = Environment(text, cost_model.get_loss, phoneme_table)
    cost_model.set_audio(audio, sr)
    cost=environment.compute_cost(gold)
    correct.append((gold,cost))
    cost=environment.compute_cost(text)
    incorrect.append((text,cost))
    output=output_text[i]
    cost=environment.compute_cost(output)
    evaluated.append((output,cost))
    i+=1
score=0
for i in range(len(correct)):
    gold_sentence,gold_cost=correct[i]
    output_sentence,output_cost=evaluated[i]
    input_sentence,input_cost=incorrect[i]
    if(gold_sentence==output_sentence):
        score+=1
    else:
        print("Input sentence: "+input_sentence+" "+str(input_cost))
        print("You evaluated: "+output_sentence+" "+str(output_cost))
        print("Correct sentence: "+gold_sentence+" "+str(gold_cost))
        print()
accuracy=(score*100)/len(correct)
print("Accuracy is: "+str(accuracy)+"%")
