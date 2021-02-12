import requests,ast,string,os,time
import re
import CICA
from bs4 import BeautifulSoup as bs



# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# info_retriever is responsible for going through each link that is provied in
# 'card_path_info.txt'. this class inherits from CICA to give it the ability to
# store the infomation that it has recieved.

class info_retriever(CICA.CICA):
    #===========================================================================
    #===========================================================================
    #===========================================================================
    def __init__(self):
        CICA.CICA.__init__(self) #Initializes inherited class
        
        # the variables below contain information of the different informaton that
        # each card could have and could be used for the seperation of the card information
        # or for cross referenceing while parsing through the data
        self.attributes=['Dark','Light','Divine','Earth','Wind','Fire','Water']
        self.spell_types=['Normal','Quick-Play','Continuous','Field','Equip','Ritual']
        self.trap_types=['Normal','Continuous','Counter']
        
        self.type_list=['Aqua','Beast','Beast-Warrior','Cyberse','Dinosaur','Divine-Beast','Dragon',
                   'Fairy','Fiend','Fish','Insect','Machine','Plant','Psychic','Pyro','Reptile',
                   'Rock','Sea Serpent','Spellcaster','Thunder','Warrior','Winged Beast','Wyrm','Zombie']

        self.extra_deck=['Fusion','Xyz','Synchro','Link']
        self.abilities=['Toon','Spirit','Union','Gemini','Flip','Ritual']
        self.effect_types=['Normal','Effect','Pendulum','Tuner', 'Special Summon']
    #===========================================================================
    #===========================================================================
    #===========================================================================
    
    #===========================================================================
    #===========================================================================
    #===========================================================================
    # removes possible sequences that are used in html for formatting reasons.
    # returns string without the specied sequences within 'seqs'
    def sequence_remover(self, item):
        seqs=['\n','\r','\t']
        buf=item
        
        for i in seqs:
            seped=buf.split(i) #splits at all occurences of sequence
            buf=''.join(seped) #joins it back together into a string
            
        # sep=buf.split(' ')
            
        return buf  
    #===========================================================================
    #===========================================================================
    #===========================================================================  
    
    #===========================================================================
    #===========================================================================
    #===========================================================================
    # returns a list of all links that are found within the 
    # evaluated version of 'card_path_info.txt'
    def get_card_links(self):
        holder=self.paths['card_links']
        links=[]
        
        for i in holder:
            for k in holder[i]:
                links.append(k)
        
        
        return links
    #===========================================================================
    #===========================================================================
    #===========================================================================
    
    #===========================================================================
    #===========================================================================
    #===========================================================================
    # checks to see if there is bad html format and returns boolean. not useful
    # anymore becuase the conditional used within it is no longer constant among
    # all links but does returns true and still attempts to fix the issue if still
    # present using regex
    def check_for_bad_parse(self,soup_bowl):
        irows=soup_bowl.find('tbody').find_all('tr')
        bad_flag=False
        for i in irows:
            if len(i)!=10: #10 was the normal amount of columns within each row of the page for yugiohcardguide.com
                bad_flag=True
        return bad_flag
    #===========================================================================
    #===========================================================================
    #===========================================================================
    
    #===========================================================================
    #===========================================================================
    #===========================================================================
    # this function takes the link passed to is and gets html content from that
    # page.    
    def get_card_info_from_link(self, link):
        
        new_link=link
        html=requests.get(new_link).text#.content
        soup=bs(html,'lxml')
        soup_check=self.check_for_bad_parse(soup)
        
        if soup_check: #fixes missing </tr> tags if soup_check is True
            fixed = re.sub(r'</a>\s+<tr valign="top"', '</a></td></tr><tr valign="top"', html)
            soup=bs(fixed,'lxml')
            
        info_rows=soup.find('tbody').find_all('tr') #finds all the rows for each card and its information
        found_cards=[]
        
        for i in info_rows: # iterates through each card row and collects all information for each 
                            # card row
            
            info=i.find_all('td') #find each section containing the card info
            info_list=[] #used to hold card info for the current card
            
            for k in info: #add all info found found for the current card and appends it to info_list
                item=self.sequence_remover(k.text) #removes sequences if any
                info_list.append(item)
            
            # the section below is nessecary for the current links being used to collect
            # the card info because each link leaves certain information out that is needed
            # to be stored
            if 'attribute' in new_link: #inserts the atrribute for the current card into info_list
                for j in self.attributes:
                    if j.lower() in new_link:
                        info_list.insert(2,self.sequence_remover(j))
                        
            elif 'spells' in new_link: #inserts card type that is missing within the link ('Spell') and inserts type of spell card
                for j in self.spell_types:
                    if j.lower() in new_link:
                        info_list.insert(1,'Spell')
                        info_list.insert(2,self.sequence_remover(j))
                
                        
            elif 'traps' in new_link: # same thing as above but with traps instead
                for j in self.trap_types:
                    if j.lower() in new_link:
                        info_list.insert(1,'Trap')
                        info_list.insert(2,self.sequence_remover(j))
                
            #appends the list containing all the card info for the current card and 
            #removes the last element of the list becasue it is an empty string
            #that is within the column for card purchase sites
            found_cards.append(info_list[0:len(info_list)-1])
        return found_cards
    #===========================================================================
    #===========================================================================
    #===========================================================================
    
    #===========================================================================
    #===========================================================================
    #===========================================================================
    #organizes the list of card gotten from each list into its respective list
    #within the 'sep_cards' dictionary
    def card_info_organizer(self,card_list):
        work=card_list
        sep_cards={'mdeck':[],'edeck':[],'spell':[],'trap':[]}
        
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #sort the cards into 'sep_cards' dictionary
        def sort_card_types():
            for i in work:
                
                ex_flag=False
                
                # i=i[0:len(i)-1]
            
                if 'Spell' not in i and 'Trap' not in i: #makes sure it is not a trap or spell
                    for e in self.extra_deck: #checks to see if the current monster is an extra deck monster
                        if e in i[1]:
                            ex_flag=True
                    if ex_flag:
                        sep_cards['edeck'].append(i)
                        ex_flag=False
                    else:
                        sep_cards['mdeck'].append(i)
                elif 'Spell' in i:
                    sep_cards['spell'].append(i)
                elif 'Trap' in i:
                    sep_cards['trap'].append(i)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
            
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #extracts all the information within the list given and creates a dictionary of
        #the information 
        def main_deck_mon_extract(mlist): 
            org_cards=[]
            
            def ability_check(monster): # used to check if the monster has an ability withing the self.abilities list
                abs=[]
                eff_sect=monster[1] #index of ability section
                for i in self.abilities:
                    if i in eff_sect:
                        abs.append(i)
                if len(abs)>0:
                    return abs
                else:
                    return None
                
            def effect_check(monster): #checks to see if the monster has any effect within self effect_types
                efs=[]
                eff_sect=monster[1] #index of effect section
                for i in self.effect_types:
                    if i in eff_sect:
                        efs.append(i)
                if len(efs)>0:
                    return efs
                else:
                    return None
                
                        
            for i in mlist: #iterates through the list of cards
                org_info={}
                
                # set variables containg the info within certain indexs 
                name=i[0]
                ability=ability_check(i)
                eff_type=effect_check(i)
                attribute=i[2]
                mon_type=i[3]
                level=i[4]
                atk=i[5]
                defen=i[6]
                card_text=i[7]
                
                textb=''
                if name=='Gladiator Beast Darius':
                    for character in card_text:
                        try:
                            textb+=character
                        except:
                            nchar=character.encode('utf-8')
                            if nchar  == '\xc2\x93':
                                textb+='"'
                
                
                
                #assigns all dictionary keys and values needed
                org_info['name']=name
                org_info['ability']=ability
                org_info['effect_type']=eff_type
                org_info['attribute']=attribute
                org_info['monster_type']=mon_type
                org_info['level']=level
                org_info['attack']=atk
                org_info['defense']=defen
                org_info['card_text']=card_text
                
                org_cards.append(org_info) # appends card info dic to a list
            return org_cards # returns the list of cards gotten
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++   
        # does similar action to 'main_deck_mon_extract' 
        def extra_deck_extract(elist):
            org_cards=[]
            
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
            def ex_type_sep(line):#function to extract extra deck type from a passed string
                found=None
                seped=line
                
                #sometimes the string given could have a slash in them
                #if so the line is split and then iterates through the seperated
                #line and checks to see if it the item is within self.extra_deck
                if '/' in line: 
                    seped=line.split('/')
                    for i in seped:
                        if i in self.extra_deck:
                            found=i
                            return found
                else:
                    t=line
                    
                    for i in self.extra_deck:
                        if i in t:
                            found=i
                            return found
                    
                
                return found
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
        
            
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            #does the same thing as the function in 'main_deck_mon_extract'
            #just a bit to lazy and does not make that much of a difference
            #to me at this time
            def eff_check(monster):
                efs=[]
                eff_sect=monster[1]
                for i in self.effect_types:
                    if i in eff_sect:
                        efs.append(i)
                        
                if len(efs)>0:
                    return efs
                else:
                    return None
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
            #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                
                
            for i in elist:#iterates through the list of monsters provided
                org_info={}
                
                #information wanted to store in dictionary
                name=i[0]
                extra_type=ex_type_sep(i[1])
                eff_type=eff_check(i)
                attribute=i[2]
                mon_type=i[3]
                atk=i[5]
                card_text=i[7]
                
                    
                #checks to see the type of extra deck monster it is
                #and seperates accordingly
                if extra_type =='Link':
                    rating=i[6]
                    org_info['link_rating']=rating
                elif extra_type=='Xyz':
                    rank=i[4]
                    org_info['rank']=rank
                elif extra_type=='Synchro' or extra_type=='Fusion':
                    level=i[4]
                    org_info['level']=level
                
                #assigns info wanted to dictionary
                org_info['name']=name
                org_info['extra_type']=extra_type
                org_info['effect_type']=eff_type
                org_info['attribute']=attribute
                org_info['monster_type']=mon_type
                org_info['attack']=atk
                org_info['card_text']=card_text
                
                #appends dictionary to final list that will be returned
                org_cards.append(org_info)
                
            return org_cards #returns the list of cards
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
            
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  
        #extracts all trap info needed  
        def trap_extract(tlist):
            org_cards=[]
            for i in tlist:#iterates through given list of info
                org_info={}
                
                #assigns value to variables
                name=i[0]
                card_type=i[1]
                trap_type=i[2]
                card_text=i[len(i)-1]
                
                #add info wanted to dictionary
                org_info['name']=name
                org_info['card_type']=card_type
                org_info['trap_type']=trap_type
                org_info['card_text']=card_text
                
                org_cards.append(org_info)# appends info dictionary to final list returned
            return org_cards
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++            
            
            
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #extracts spell card info from list given
        def spell_extract(slist):
            org_cards=[]
            for i in slist:#iterates through given list
                org_info={}
                
                name=i[0]
                card_type=i[1]
                spell_type=i[2]
                card_text=i[len(i)-1]
                
                org_info['name']=name
                org_info['card_type']=card_type
                org_info['spell_type']=spell_type
                org_info['card_text']=card_text
                
                org_cards.append(org_info)
            return org_cards
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        
        sort_card_types()
        if len(sep_cards['mdeck'])>0:
            main_deck=main_deck_mon_extract(sep_cards['mdeck'])
            sep_cards['mdeck']=main_deck
            
        if len(sep_cards['edeck'])>0:
            extra_deck=extra_deck_extract(sep_cards['edeck'])
            sep_cards['edeck']=extra_deck
            
        if len(sep_cards['trap'])>0:
            traps=trap_extract(sep_cards['trap'])
            sep_cards['trap']=traps
            
        if len(sep_cards['spell']):
            spells=spell_extract(sep_cards['spell'])
            sep_cards['spell']=spells
        

        
        return sep_cards
    #===========================================================================
    #===========================================================================
    #===========================================================================
        
                
            
                
    
    #===========================================================================
    #===========================================================================
    #===========================================================================
    def start_scrape(self):
        count=0
        links=self.get_card_links()
        self.clear_card_files()
        self.info_file_check()
        max_size=len(links)
        for i in links:
            if count<=max_size:
        
                cards_gotten=self.get_card_info_from_link(i)
                organized=self.card_info_organizer(cards_gotten)
                self.store_card_info(organized)
                count+=1
    #===========================================================================
    #===========================================================================
    #===========================================================================    
                
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////        
























