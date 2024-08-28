
import random
import math
import json
class Agent(object):
    def __init__(self, phoneme_table, vocabulary) -> None:
        """
        Your agent initialization goes here. You can also add code but don't remove the existing code.
        """
        reversed_table={}
        for key, value in phoneme_table.items():
            for v in value:
                if(v in reversed_table):
                    reversed_table[v].append(key)
                else:
                    reversed_table[v]=[key]
        self.phoneme_table = reversed_table
        self.vocabulary = vocabulary
        self.best_state = None
    def sound_similar(self,init_sentence,environment):       
        init_sentence=init_sentence.upper()
        orig_sentence=init_sentence
        init_cost=1e9  
        length=len(orig_sentence)
        substr_len=1
        for i in range (0,length):
            phoneme=orig_sentence[i:i+substr_len]
            key=phoneme
            if(key in self.phoneme_table):
                values=self.phoneme_table[key]
                for v in values:
                    new_sentence=orig_sentence[:i]+v+orig_sentence[(i+substr_len):]
                    cost=environment.compute_cost(new_sentence)
                    if(cost<init_cost):
                        init_cost=cost
                        init_sentence=new_sentence
        substr_len=2  
        for i in range (0,length-1):
            phoneme=orig_sentence[i:i+substr_len]
            key=phoneme
            if(key in self.phoneme_table):
                values=self.phoneme_table[key]
                for v in values:
                    new_sentence=orig_sentence[:i]+v+orig_sentence[(i+substr_len):]
                    cost=environment.compute_cost(new_sentence)
                    if(cost<init_cost):
                        init_cost=cost
                        init_sentence=new_sentence                          
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
        cost = 1e9
        changed_sentence=self.best_state
        new_cost=0
        max_iterations=9
        while(max_iterations>0):
            new_cost,changed_sentence=self.sound_similar(changed_sentence,environment)
            if new_cost<cost :
                print(changed_sentence)
                print(new_cost)
                print(10-max_iterations)
                cost=new_cost
                self.best_state=changed_sentence
                environment.best_state=changed_sentence
            max_iterations-=1
        new_cost=0 
        changed_sentence=self.best_state
        new_cost,changed_sentence=self.vocab(changed_sentence,environment)
        if(new_cost<cost):
            self.best_state=changed_sentence
            environment.best_state=changed_sentence

    
