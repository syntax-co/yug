import requests,ast,string,os,io
from bs4 import BeautifulSoup as bs

lc=string.ascii_lowercase
uc=string.ascii_uppercase

type_list=['Aqua','Beast','Beast-Warrior','Cyberse','Dinosaur','Divine=Beast','Dragon',
           'Fairy','Fiend','Fish','Insect','Machine','Plant','Psychic','Pyro','Reptile',
           'Rock','Sea Serpent','Spellcaster','Thunder','Warrior','Winged Beast','Wyrm','Zombie']

abilities=['Toon','Spirit','Union','Gemini','Flip','Fusion','Xyz','Synchro','Ritual','Link']
effect_type=['Normal','Effect','Pendulum','Tuner', 'Special Summon']

break_options=['\n','\r','\t']

skip_file='name_skips.txt'
pre_url='https://www.db.yugioh-card.com'
page='https://www.db.yugioh-card.com/yugiohdb/card_list.action'



header=agent={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'}
moster_dic={}
tick=0



def start_scrape():
    global tick
    
    skips=get_skip_names()
    
    html=requests.get(page).content
    soup=bs(html,'lxml')

    found=soup.findAll(class_='pack pack_en') #gets all links to page containg cards and information

    
    for i in found: #goes through each link that is found
        name=i.find('strong').text # references the name of the card release
        link=i.find('input').get('value') #gets the link for current card release 
        if name not in skips:
            
            html2=requests.get(pre_url+link).content
            soup2=bs(html2,'lxml')
            
            found2=soup2.findAll('dl') #gets all the section of the website that contain card info
            
            for i in found2:
                #name of the card
                name=i.find('dt',{'class':'box_card_name'}).find('span',{'class':'card_status'}).find('strong').text
                #attribute type of the card
                attribute=i.find('dd',{'class':'box_card_spec'}).find('span',{'class':'box_card_attribute'}).find('span').text
                
                if attribute != 'TRAP' and attribute !='SPELL':
                    #this section is for monsters and excludes traps and spells

                
                    try: #first tries to get the normal level of the monster
                        level=i.find('dd',{'class':'box_card_spec'}).find('span',{'class':'box_card_level_rank level'}).find('span').text
                    except:
                        try: #then tries to get the rank of the monster if it is a ranked monster
                            level=i.find('dd',{'class':'box_card_spec'}).find('span',{'class':'box_card_level_rank rank'}).find('span').text
                        except: # lastly tries to get the link marker if the moster ended up being a link monster
                            level=i.find('dd',{'class':'box_card_spec'}).find('span',{'class':'box_card_linkmarker'}).find('span').text
                    #gets the section of the page that holds card type information
                    retype=i.find('dd',{'class':'box_card_spec'}).find('span',{'class':'card_info_species_and_other_item'}).text
                    attack=i.find('dd',{'class':'box_card_spec'}).find('span',{'class':'atk_power'}).text #gets the attack
                    defense=i.find('dd',{'class':'box_card_spec'}).find('span',{'class':'def_power'}).text #gets the defense
                    
                    words=[]
                    a_count=0

                    #filters throught retype to find the type of the moster the effect-type of the moster and its abilities
                    mtype=[]
                    abil=[]
                    ef_type=[]
                    
                    for k in type_list:
                        if k in retype:
                            words.append(k)
                            mtype.append(k)
                        
                            
                    for k in abilities:
                        if k in retype:
                            words.append(k)
                            a_count+=1
                            abil.append(k)
                            
                    for k in effect_type:
                        if k in retype:
                            words.append(k)
                            ef_type.append(k)
                    
                    
                    if 'Effect' in words: #goes through the information if the monster is an effect monster
                        '''if the monster is a ritual monster or if it a regular effect monster the
                           card text is seperated'''
                        if a_count==0 or 'Ritual' in words: 
                            te=str(i.find('dd',{'class':'box_card_text'})).split('<dd class="box_card_text">\r\n\t\t\r\n\t\t\t\t\t\t\t\t\t\t')
                            effect=te[1].split('\r\n\t\t\r\n\t\t\t\t\t\t\t\t\t</dd>')[0]
                            
                            this={'name':name,'attribute':attribute,'level':level,'type':mtype,'attack':attack,'defense':defense,'ability':abil,'effect type':ef_type,'effect':effect}
                            write_card_info(this)
                        
                        
                        elif 'Fusion' in words or 'Xyz' in words or 'Synchro' in words or 'Link' in words:
                            
                            '''if the monster is a fusion; xyz; synchro or a link moster then it
                               then the card text seperation is divided into two parts. the first part
                               is the requirements for the summoning of the monster and then the card text'''
                            
                            te=list(str(i.find('dd',{'class':'box_card_text'})))
                            conv=list(te)
                            
                            def get_card_req_eff():
                                '''this function is used as for the
                                   seperation of the card'''
                                for l in break_options:
                                    if l in conv:
                                        ammount=conv.count(l)
                                        
                                        for k in range(ammount):

                                            conv.remove(l)
                                sw1=0
                                piece=[]
                                pieces=[]
                                for l in conv:
                                    if l=='<':
                                        sw1=1
                                        piece.append(l)
                                        
                                    elif l=='>':
                                        sw1=0
                                        piece.append(l)
                                        pieces.append(''.join(piece))
                                        
                                        piece=[]
                                    else:
                                        if sw1==1:
                                            piece.append(l)
                                            
                                        
                                beginning=pieces[0]
                                end=pieces[len(pieces)-1]
                                breaker=pieces[1]
                                
                                new_conv=''.join(conv)

                                beg_rem=new_conv.split(beginning)[1]
                                end_rem=beg_rem.split(end)[0]
                                inner=end_rem.split(breaker,1)

                                masked=['Masked HERO Goka','Masked HERO Vapor','Masked HERO Acid',
                                        'Masked HERO Dian','Masked HERO Blast','Time Magic Hammer',
                                        'Doom Virus Dragon','Tyrant Burst Dragon','Mirror Force Dragon',
                                        'Rocket Hermos Cannon','Goddess Bow','Red-Eyes Black Dragon Sword',
                                        'Elemental HERO Divine Neos','Masked HERO Koga','Masked HERO Divine Wind',
                                        'Masked HERO Dark Law','Masked HERO Anki','Destruction Dragon']
                                secondary=['Neo-Spacian Marine Dolphin']
                                '''the lists "masked" and "secondary hold card names that
                                   cannot be filltered with normal methods due to the requirements for the summoning
                                   of these cards being combined with the rest of the effect and will need future
                                   seperation"'''
                                try:
                                    
                                    if name not in masked and name not in secondary:
                                        requirement=inner[0]
                                        effect=inner[1]
                                    elif name in secondary:
                                        
                                        ripped=inner[0].split('.',2)
                                        requirement=ripped[1]+'.'
                                        effect=ripped[0]+'.'+ripped[2]
                                    
                                    else:
                                        ripped=inner[0].split('.',1)
                                        requirement=ripped[0]+'.'
                                        effect=ripped[1]
                                        
                                except:
                                    print(name) #prints name of the card in case of error and as a reference to find the problem within the website html
                                    
                            
                                
                                return requirement,effect
                            
                            req1=get_card_req_eff()
                            this={'name':name,'attribute':attribute,'level':level,'type':mtype,'attack':attack,'defense':defense,'ability':abil,'effect type':ef_type,'requirement':req1[0],'effect':req1[1]}
                            write_card_info(this)
                            
                        else:
                            '''this section is for any card that had passed the if statement
                               and this is used as a filler for potential future code'''
                            te=str(i.find('dd',{'class':'box_card_text'})).split('<dd class="box_card_text">\r\n\t\t\r\n\t\t\t\t\t\t\t\t\t\t')
                            effect=te[1].split('\r\n\t\t\r\n\t\t\t\t\t\t\t\t\t</dd>')[0]
                            this={'name':name,'attribute':attribute,'level':level,'type':mtype,'attack':attack,'defense':defense,'ability':abil,'effect type':ef_type,'effect':effect}
                            write_card_info(this)
                    else:
                        '''this is where the normal monsters with no effect go
                               seperation is not necessary but I chose to inlcude it just as a
                               filler for later code'''
                        te=str(i.find('dd',{'class':'box_card_text'})).split('<dd class="box_card_text">\r\n\t\t\r\n\t\t\t\t\t\t\t\t\t\t')
                        text=te[1].split('\r\n\t\t\r\n\t\t\t\t\t\t\t\t\t</dd>')[0]
                        
                        this={'name':name,'attribute':attribute,'level':level,'type':mtype,'attack':attack,'defense':defense,'ability':abil,'effect type':ef_type}
                        write_card_info(this)

                        
                    
                else:
                    '''if the card is a spell or a trap the codes skips
                       to this section'''
                    
                    level='None'
                    type_='None'
                    attack='None'
                    defense='none'
                    if attribute == 'TRAP' or attribute =='SPELL':
                        try:
                            spell_type=i.find('dd',{'class':'box_card_spec'}).find('span',{'class':'box_card_effect'}).find('span').text
                        except:
                            spell_type='Normal'
                    else:
                        spell_type='None'

                    
                    te=str(i.find('dd',{'class':'box_card_text'})).split('<dd class="box_card_text">\r\n\t\t\r\n\t\t\t\t\t\t\t\t\t\t')
                    effect=te[1].split('\r\n\t\t\r\n\t\t\t\t\t\t\t\t\t</dd>')[0]
                    
                    this={'name':name,'attribute':attribute,'level':level,'type':type_,'attack':attack,'defense':defense,'spell type':spell_type,'effect':effect}
                    write_card_info(this)
                        
                
    
                    
                    

mode='list-mode'

conspells=[]
eqpspells=[]
fldspells=[]
norspells=[]
quispells=[]
ritspells=[]

contraps=[]
countraps=[]
nortraps=[]

effmonsters=[]
fusmonsters=[]
linmonsters=[]
normonsters=[]
ritmonsters=[]
synmonsters=[]
xyzmonsters=[]

con_spells='Cards/Spells/conitous_spells.txt'
eqp_spells='Cards/Spells/equip_spells.txt'
fld_spells='Cards/Spells/field_spells.txt'
nor_spells='Cards/Spells/normal_spells.txt'
qui_spells='Cards/Spells/quick-play_spells.txt'
rit_spells='Cards/Spells/ritual_spells.txt'

con_traps='Cards/Traps/continous_traps.txt'
coun_traps='Cards/Traps/counter_traps.txt'
nor_traps='Cards/Traps/normal_traps.txt'

eff_monsters='Cards/Monsters/effect_monsters.txt'
fus_monsters='Cards/Monsters/fusion_mosters.txt'
lin_monsters='Cards/Monsters/link_mosters.txt'
nor_monsters='Cards/Monsters/normal_monsters.txt'
rit_monsters='Cards/Monsters/ritual_mosters.txt'
syn_monsters='Cards/Monsters/synchro_mosters.txt'
xyz_monsters='Cards/Monsters/xyz_mosters.txt'


def path_write(path,item):

    paths=[con_spells,eqp_spells,fld_spells,
    nor_spells,qui_spells,rit_spells,con_traps,coun_traps,
    nor_traps,eff_monsters,fus_monsters,lin_monsters,
    nor_monsters,rit_monsters,syn_monsters,xyz_monsters]
    
    content=[conspells,eqpspells,fldspells,
    norspells,quispells,ritspells,contraps,countraps,
    nortraps,effmonsters,fusmonsters,linmonsters,
    normonsters,ritmonsters,synmonsters,xyzmonsters]
    

    
    
    
    
    if mode=='list-mode':
        for i in content:
            file=open(paths[content.index(i)],'w',encoding="utf-8")
            file.write(str(i))
            file.close()
        
    elif mode=='file-mode':
        
        file=open(path,'r')
        g=ast.literal_eval(file.read())
        file.close()
        g.append(item)
        
        file=open(path,'w',encoding="utf-8")
        
        for i in str(g):
            file.write(i)
    
        file.close()
    
def write_card_info(info):
    '''this function will be used in the future to write all the seperated
       card information into files that are seperated into the respective card types'''
    global cont
    

    
    
    

        
    


        

    
    att=info['attribute']
    

    if  att == 'SPELL':
        st=info['spell type']
        
        if st == 'Continuous':
            
            if mode=='file-mode':
                path_write(con_spells,info)
            elif mode=='list-mode':
                if info not in conspells:
                    conspells.append(info)
            
        elif st == 'Equip':
            if mode=='file-mode':
                path_write(eqp_spells,info)
            elif mode=='list-mode':
                if info not in eqpspells:
                    eqpspells.append(info)
        elif st == 'Field':
            if mode=='file-mode':
                path_write(fld_spells,info)
            elif mode=='list-mode':
                if info not in fldspells:
                    fldspells.append(info)
            
        elif st == 'Normal':
            if mode=='file-mode':
                path_write(nor_spells,info)
            elif mode=='list-mode':
                if info not in norspells:
                    norspells.append(info)
            
        elif st == 'Quick-Play':
            if mode=='file-mode':
                path_write(qui_spells,info)
            elif mode=='list-mode':
                if info not in quispells:
                    quispells.append(info)
            
        elif st == 'Ritual':
            if mode=='file-mode':
                path_write(rit_spells,info)
            elif mode=='list-mode':
                if info not in ritspells:
                    ritspells.append(info)
            
        else:
            print("error: write -> spell type error")
        
    elif att == 'TRAP':
        st=info['spell type']
        if st == 'Continuous':
            if mode=='file-mode':
                path_write(con_traps,info)
            elif mode=='list-mode':
                if info not in contraps:
                    contraps.append(info)
            
        elif st == 'Counter':
            if mode=='file-mode':
                path_write(coun_traps,info)
            elif mode=='list-mode':
                if info not in countraps:
                    countraps.append(info)
            
        elif st == 'Normal':
            if mode=='file-mode':
                path_write(nor_traps,info)
            elif mode=='list-mode':
                if info not in nortraps:
                    nortraps.append(info)
            
        else:
            print("error: write -> trap type error")
    else:
        ab=info['effect type']
        abil=info['ability']
        
        
        
        if 'Effect' in ab:
            if 'Xyz' in abil:
                if mode=='file-mode':
                    path_write(xyz_monsters,info)
                elif mode=='list-mode':
                    if info not in xyzmonsters:
                        xyzmonsters.append(info)
            elif 'Fusion' in abil:
                if mode=='file-mode':
                    path_write(fus_monsters,info)
                elif mode=='list-mode':
                    if info not in fusmonsters:
                        fusmonsters.append(info)
            elif 'Synchro' in abil:
                if mode=='file-mode':
                    path_write(syn_monsters,info)
                elif mode=='list-mode':
                    if info not in synmonsters:
                        synmonsters.append(info)
            elif 'Ritual' in abil:
                if mode=='file-mode':
                    path_write(rit_monsters,info)
                elif mode=='list-mode':
                    if info not in ritmonsters:
                        ritmonsters.append(info)
            elif 'Link' in abil:
                if mode=='file-mode':
                    path_write(lin_monsters,info)
                elif mode=='list-mode':
                    if info not in linmonsters:
                        linmonsters.append(info)
            else:
                if mode=='file-mode':
                    path_write(eff_monsters,info)
                elif mode=='list-mode':
                    if info not in effmonsters:
                        effmonsters.append(info)

        
        elif 'Normal' in ab:
            if 'Xyz' in abil:
                if mode=='file-mode':
                    path_write(xyz_monsters,info)
                elif mode=='list-mode':
                    if info not in xyzmonsters:
                        xyzmonsters.append(info)
            elif 'Fusion' in abil:
                if mode=='file-mode':
                    path_write(fus_monsters,info)
                elif mode=='list-mode':
                    if info not in fusmonsters:
                        fusmonsters.append(info)
            elif 'Synchro' in abil:
                if mode=='file-mode':
                    path_write(syn_monsters,info)
                elif mode=='list-mode':
                    if info not in synmonsters:
                        synmonsters.append(info)
            elif 'Ritual' in abil:
                if mode=='file-mode':
                    path_write(rit_monsters,info)
                elif mode=='list-mode':
                    if info not in ritmonsters:
                        ritmonsters.append(info)
            elif 'Link' in abil:
                if mode=='file-mode':
                    path_write(lin_monsters,info)
                elif mode=='list-mode':
                    if info not in linmonsters:
                        linmonsters.append(info)
            else:
                if mode=='file-mode':
                    path_write(nor_monsters,info)
                elif mode=='list-mode':
                    if info not in normonsters:
                        normonsters.append(info)
        

        
        
            
                    
    
    

    
#--------------------------------------------#
'''these functions are used to add, remove, and get the names
   that are within the skip file for the card pack releases'''
def add_name_to_skip(name):
    file=open(skip_file,'r')
    info=ast.literal_eval(file.read())
    file.close()
    
    for i in name:
        if i not in info:
            info.append(i)
    
    
    file=open(skip_file,'w')
    for i in str(info):
        file.write(i)
    file.close()

def remove_name_to_skip(name):
    file=open(skip_file,'r')
    info=ast.literal_eval(file.read())
    file.close()
    
    for i in name:
        if i in info:
            info.remove(name)

    file=open(skip_file,'w')
    for i in str(info):
        file.write(i)
    file.close()

def get_skip_names():
    file=open(skip_file,'r')
    info=ast.literal_eval(file.read())
    file.close()
    return info
#--------------------------------------------#
def clear_all_card_files():
    for root, dirs, files in os.walk('Cards'):
        for f in files:
            loc=os.path.join(root, f)
            file=open(loc,'w')
            file.write('[]')
            file.close()

def clean_up():
    paths=[]
    
    for root,dire,files in os.walk('Cards'):
        for i in files:
            paths.append(os.path.join(root,i))

            
    for i in paths:
        file=open(i,'r',encoding='utf-8')
        info=ast.literal_eval(file.read())
        file.close()

        for k in info:
            num=info.count(k)
            if num>1:
                name=k['name']
                for l in info:
                    if l['name']==name:
                        dex=info.index(l)
                        info.pop(dex)

    
    
    

    




def start():
    clear_all_card_files()
    start_scrape()
    if mode=='list-mode':
        path_write(' ',' ')
    clean_up()































