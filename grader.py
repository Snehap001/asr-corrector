import pickle
import json
from tqdm import tqdm
correct=[]
with open("data.pkl", 'rb') as fp:
    data = pickle.load(fp)
for sample in tqdm(data):
    gold = sample['gold']
    correct.append(gold)
with open("outputs.json", 'r') as file:
    output_text = json.load(file)
score=0
for i in range(len(correct)):
    gold_sentence=correct[i]
    output_sentence=output_text[i]
    if(gold_sentence==output_sentence):
        score+=1
    else:
        print("You evaluated: "+output_sentence)
        print("Correct sentence: "+gold_sentence)
accuracy=(score*100)/len(correct)
print("Accuracy is: "+str(accuracy)+"%")
