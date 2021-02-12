import ast




class info_read:
    def __init__(self):
        self.path_file='card_path_info.txt'
        self.eval_path=self.evaluate(self.path_file)
        self.main_dir=self.eval_path['card_storage']['directory_name']
        self.sub_dirs=self.eval_path['card_storage']['directories']
        
        
        self.card_files=self.eval_path['card_storage']['file_names']
        self.name_file=self.main_dir+'\\'+self.eval_path['card_storage']['extra'][0]
        
        
    def get_card_paths(self):
        pths=[]
        for i in self.card_files:
            base_path=self.main_dir+'\\'+i
            for j in self.card_files[i]:
                npath=base_path+'\\'+j
                pths.append(npath)
        return pths
    
    def evaluate(self,path):
        # try:
        file=open(path,'r')
        info=ast.literal_eval(file.read())
        file.close()
        return info
        # except:
        #     print('file: '+path+' could no tbe evaluated')
    
    def read_file(self,path):
        
        file=open(self.name_file,'r')
        info=file.read()
        file.close()
        return info
    
    def get_card_names(self):
        info=self.read_file(self.name_file)
        names=info.split(',')
        for i in names:
            print(i)
        
        
        
        

class card_retriever(info_read):
    
    def __init__(self):
        info_read.__init__(self)
        
    def get_card(self, card_name):
        p=self.get_card_paths()
        
        for i in p:
            file=open(i,'r',encoding='utf-8')
            info=file.read()
            file.close()
            info=info[0:len(info)-1]
            
            flist=ast.literal_eval('['+info+']')
            for monster in flist:
                name=monster['name']
                if name.lower() == card_name.lower():
                    return monster
    
    def display_cards(self,cards,ctypes):
        tmax=50
        start=0
        end=tmax
        tcount=0
        
        fin_cards=[]
        
        for i in cards:
            
            if 'main_monsters' in ctypes:
                if 'extra_type' not in i and 'monster_type' in i:
                    fin_cards.append(i)
            
            if 'extra_monsters' in ctypes:
                if 'extra_type' in i:
                    fin_cards.append(i)
                    
            if 'spells' in ctypes:
                if 'spell_type' in i:
                    fin_cards.append(i)
            
            if 'traps' in ctypes:
                if 'trap_type' in i:
                    fin_cards.append(i)
        
        for i in fin_cards:
            print('+'*50)
            for k in i:
                if k!='card_text':
                    print(k,'-',i[k])
                else:
                    print('------------')
                    print('card_text')
                    print('------------')
                    text=i[k]
                    while(tcount<len(text)):
                        sect=text[start:end]
                        print(sect)
                        tcount+=tmax
                
                        start+=tmax
                
                        if end+tmax<len(text):
                            end+=tmax
                        else:
                            end=len(text)
                            
            start=0
            end=tmax
            tcount=0
            print('+'*50)
        
        
        
    def find_words_in_card(self,words,card_type=None):
        
        cards_found=[]
        
        for i in self.card_files:
            base_path=self.main_dir+'\\'+i
            for j in self.card_files[i]:
                npath=base_path+'\\'+j
        
                file=open(npath,'r',encoding='utf-8')
                info=file.read()
                file.close()
        
                if len(info)==0:
                    pass
                else:
                    info=info[0:len(info)-1]
                    ev=ast.literal_eval('['+info+']')
                    
                    filt1=[]
                    
                    for k in ev:
                        text=k['card_text'].lower()
                        
                        if len(words['wanted'])>0:
                            for word in words['wanted']:
                                if word.lower() in text or word.lower() in k['name']:
                                        filt1.append(k)
                                        
                    if len(words['excluded'])>0:
                        for k in filt1:
                            text=k['card_text'].lower()
                            
                            for word in words['excluded']:
                                if (word.lower() not in text) and (word.lower() not in k['name']):
                                    cards_found.append(k)
                    else:
                        for mon in filt1:
                            cards_found.append(mon)
                                

                        
        return cards_found
            

words={'wanted':[],'excluded':[]}

words['wanted']=['backrow']
words['excluded']=[]



cr=card_retriever()
cards=cr.find_words_in_card(words)
c1=[]
# cr.display_cards(cards,['spells'])
# c=cr.get_card('spell power grasp')
for i in cards:
    print(i['name'])

        





























