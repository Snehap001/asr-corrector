
import random
import math
import json
def load_dictionary(file_path):
    with open(file_path, 'r') as file:
        valid_words = set(word.strip().upper() for word in file)
    return valid_words

def is_spelled_correctly(word, valid_words):
    return word.upper() in valid_words

# Load dictionary once

class Agent(object):
    def __init__(self, phoneme_table, vocabulary) -> None:
        """
        Your agent initialization goes here. You can also add code but don't remove the existing code.
        """
        self.phoneme_table = phoneme_table
        self.vocabulary = vocabulary
        self.best_state = None
        self.valid_words = load_dictionary('words.txt')
   

    def sound_similar(self,init_sentence,environment):
        
        init_sentence=init_sentence.upper()
        words_list=init_sentence.split()
        init_cost=1e9
        
        for i in range(0,len(words_list)):
            w=words_list[i]
            print(w)
            for key,value in self.phoneme_table.items():
                

                for v in value:
                    orig=w
                    lower_v=v.upper()
                    lower_key=key.upper()
                    
                    new_string = orig.replace(lower_v,lower_key )
                 
                    if(new_string!=orig ):
                        new_list=words_list
                        new_list[i]=new_string
                       
                        new_sentence=' '.join(new_list)
                        cost=environment.compute_cost(new_sentence)
                        
                        if(cost<init_cost):
                            init_sentence=new_sentence
                            init_cost=cost
                        new_list[i]=orig

        return init_cost,init_sentence
                            

    def vocab(self,init_sentence,environment):
        init_sentence=init_sentence.upper()
        orig_sentence=init_sentence
        words_list=init_sentence.split()
        init_cost=1e9
        vis_front=0
        vis_back=0

        for v in self.vocabulary:
            if not(vis_front):
                words_list=orig_sentence.split()
                new_list=[v]
                new_list=new_list+words_list
                new_sentence=' '.join(new_list)
                cost=environment.compute_cost(new_sentence)
                if cost<init_cost:
                    init_sentence=new_sentence
                    init_cost=cost
                    vis_front=1
            elif not(vis_back):
                words_list=orig_sentence.split()
                new_list=words_list
                new_list.append(v)
                new_sentence=' '.join(new_list)
                cost=environment.compute_cost(new_sentence)
                if cost<init_cost:
                    init_sentence=new_sentence
                    init_cost=cost
                    vis_back=1
        vis_front=0
        vis_back=0
        for v in self.vocabulary:
            if not(vis_front):
                words_list=orig_sentence.split()
                new_list=[v]
                new_list=new_list+words_list
                new_sentence=' '.join(new_list)
                cost=environment.compute_cost(new_sentence)
                if cost<init_cost:
                    init_sentence=new_sentence
                    init_cost=cost
                    vis_front=1
        vis_front=0
        vis_back=0
        for v in self.vocabulary:
            
            if not(vis_back):
                words_list=orig_sentence.split()
                new_list=words_list
                new_list.append(v)
                new_sentence=' '.join(new_list)
                cost=environment.compute_cost(new_sentence)
                if cost<init_cost:
                    init_sentence=new_sentence
                    init_cost=cost
                    vis_back=1
        

        return init_cost,init_sentence


    

    def asr_corrector(self, environment):
        """
        Your ASR corrector agent goes here. Environment object has following important members.
        - environment.init_state: Initial state of the environment. This is the text that needs to be corrected.
        - environment.compute_cost: A cost function that takes a text and returns a cost. E.g., environment.compute_cost("hello") -> 0.5

        Your agent must update environment.best_state with the corrected text discovered so far.
        """
 

        self.best_state = environment.init_state
        prev_sentence=" "
        cost = 1e9
        i=10
        changed_sentence=self.best_state
        print(self.best_state)
        
        print(cost)
        new_cost=0
        temperature=1000
        cooling_rate=0.8
        max_iterations=10
        while(max_iterations>0):
            # prev_sentence=self.best_state

            new_cost,changed_sentence=self.sound_similar(changed_sentence,environment)
            print(changed_sentence,new_cost)
            delta_value=new_cost-cost
            if new_cost<cost or random.uniform(0, 1) < math.exp(-delta_value / temperature):
                cost=new_cost
                self.best_state=changed_sentence
                environment.best_state=changed_sentence
            temperature*=cooling_rate
            max_iterations-=1
        new_cost=0
       
        changed_sentence=self.best_state
       
        
        new_cost,changed_sentence=self.vocab(changed_sentence,environment)
        # print(new_cost," ",changed_sentence)
        if(new_cost<cost):
            self.best_state=changed_sentence
            environment.best_state=changed_sentence

        print(self.best_state)

        print(cost)

    