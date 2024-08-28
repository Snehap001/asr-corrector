import pickle
import json
from tqdm import tqdm
correct=[]
incorrect=[]
with open("data.pkl", 'rb') as fp:
    data = pickle.load(fp)
for sample in tqdm(data):
    gold = sample['gold']
    text=sample['text']
    correct.append(gold)
    incorrect.append(text)
with open("outputs.json", 'r') as file:
    output_text = json.load(file)
score=0
for i in range(len(correct)):
    gold_sentence=correct[i]
    output_sentence=output_text[i]
    input_sentence=incorrect[i]
    if(gold_sentence==output_sentence):
        score+=1
    else:
        print("Input sentence: "+input_sentence)
        print("You evaluated: "+output_sentence)
        print("Correct sentence: "+gold_sentence)
        print()
accuracy=(score*100)/len(correct)
print("Accuracy is: "+str(accuracy)+"%")
