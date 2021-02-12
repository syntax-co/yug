import ast,os
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# CICA Class has functions to check for the existence of the Directories and Files used
# for storing card information, clear all the data within those files and a function
# to store card information to the respective files    
class CICA: #Card Information Check Arranger
    #===========================================================================
    #===========================================================================
    #===========================================================================
    # all paths that are needed to store the card information and the file name 
    # that contains all the paths, and file names for card information storage
    def __init__(self):
        self.path_file='card_path_info.txt' # file name for the paths
        self.paths=self.evaluate(self.path_file) # evaluates the paths files
        
        self.base_path=self.paths['location_path'] # used to direct the location of card storage
        self.card_paths=self.paths['card_storage'] # contains a dic of directory names and file names
        self.card_dir=self.base_path+self.card_paths['directory_name'] # main directory name
        self.info_dirs=self.card_paths['directories'] # sub directories for main directory
        self.file_names=self.card_paths['file_names'] # dict of names of file names for card storage
        
        self.all_names_file=self.card_dir+'\\'+self.card_paths['extra'][0] # path for file that contains all card names 
        self.mon_dir=self.card_dir+'\\'+self.info_dirs[0] # monster directory
        self.spell_dir=self.card_dir+'\\'+self.info_dirs[1] # spell directory
        self.trap_dir=self.card_dir+'\\'+self.info_dirs[2] # trap directory
    #===========================================================================
    #===========================================================================
    #===========================================================================
    
    
    #===========================================================================
    #===========================================================================
    #===========================================================================
    # evaluates and return file that is passed
    # for now is only used during __init__ to evaluate path file
    def evaluate(self,fname):
        file=open(fname,'r')
        info=ast.literal_eval(file.read())
        file.close()
        return info
    #===========================================================================
    #===========================================================================
    #===========================================================================
    
    #===========================================================================
    #===========================================================================
    #===========================================================================
    # clears all data within the card files
    def clear_card_files(self):
        structure='' #format in which the file is rewritten in case of  needed evaluation to a dictionary or a list
        
        for i in self.file_names['Monsters']: # goes through all monster files
            npath=self.mon_dir+'\\'+i
            file=open(npath,'w')
            file.write(structure)
            file.close()
            
        for i in self.file_names['Spells']: # goes through all spell files
            npath=self.spell_dir+'\\'+i
            file=open(npath,'w')
            file.write(structure)
            file.close()
        
        for i in self.file_names['Traps']: # goes through all trap files
            npath=self.trap_dir+'\\'+i
            file=open(npath,'w') 
            file.write(structure)
            file.close()
            
        file=open(self.all_names_file,'w') # rewrites all names file
        file.write(structure)
        file.close()
    #===========================================================================
    #===========================================================================
    #===========================================================================
    
    #===========================================================================
    #===========================================================================
    #===========================================================================
    # checks files and directories and if it does not exists in the specified
    # paths it is then created 
    def info_file_check(self):
        struct=''#'[]'
        
        if not os.path.isdir(self.card_dir): # checks for existence of main directory
            os.mkdir(self.card_dir)
            
        if not os.path.isfile(self.all_names_file): # checks for existence of file with all the card names
            file=open(self.all_names_file,'w')
            file.write(struct)
            file.close()
            
            
        for i in self.info_dirs: # checks for existence of sub directories
            ipath=self.card_dir+'\\'+i
            if not os.path.isdir(ipath):
                os.mkdir(ipath)
            
            for k in self.file_names[i]: # check for existence of files within each sub directory
                info_path=ipath+'\\'+k
                if not os.path.isfile(info_path):
                    file=open(info_path,'w')
                    file.write(struct)
                    file.close()
    #===========================================================================
    #===========================================================================
    #===========================================================================
        
    #===========================================================================
    #===========================================================================
    #===========================================================================
    # this function stores all cards within the dictionary that is passed that
    # contains all the cards that have been found within the link searched
    def store_card_info(self,card_dict):
        #card_dict = dictionary from
        
        card_names=[]
        
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # writes to file passed as fpath. 
        # in this function appending to the file is used to speed up
        # the writing of the informaion since opening and reading and then
        # rewriting takes way to long. the format of this appending always adds
        # a comma to the end because if the need to read this file comes up
        # the comma can be easily removed. these info files will not be able to
        # be evaluated because it currently does not have a diction or list format
        def write_to_path(info,fpath):
            # eval=self.evaluate(fpath)
            # eval+=info
            
            file=open(fpath,'a',encoding='utf-8')
            for i in info:
                file.write(str(i)+',')
            file.close()
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # used to store the monsters that belong in the main deck
        def store_main_monsters(m_list):
            
            mon_dic={'Ritual':[],'Normal':[],'Pendulum':[],'Effect':[]}
            
            #main deck monster file paths
            rit_path=self.mon_dir+'\\'+self.file_names['Monsters'][4]
            norm_path=self.mon_dir+'\\'+self.file_names['Monsters'][3]
            eff_path=self.mon_dir+'\\'+self.file_names['Monsters'][0]
            pend_path=self.mon_dir+'\\'+self.file_names['Monsters'][5]
            
            
            # this for statement is create as such because the varibale "effects"
            # is a dictionary that can contain more than one item and cannot be
            # stored without this for statement and the conditional statements below
            for i in m_list:
                effects=i['effect_type']
                
                
                if effects != None:
                    if i['ability']!=None:
                        abil=i['ability']
                        if 'Ritual' in abil:
                            mon_dic['Ritual'].append(i)
                            
                    elif 'Normal' in effects:
                        mon_dic['Normal'].append(i)
                        
                    elif 'Pendulum' in effects:
                        mon_dic['Pendulum'].append(i)
                    
                    elif 'Effect' in effects:
                        mon_dic['Effect'].append(i)
                    
                else:
                    mon_dic['Normal'].append(i)
                    
                card_names.append(i['name'])
            
            # these conditionals are used to lessen the storage time
            # becasue not all lists within the dictionary will hold informaton
            # of cards
            if len(mon_dic['Ritual'])>0:
                write_to_path(mon_dic['Ritual'],rit_path)
            
            if len(mon_dic['Normal'])>0:
                write_to_path(mon_dic['Normal'],norm_path)
            
            if len(mon_dic['Pendulum'])>0:
                write_to_path(mon_dic['Pendulum'],pend_path)
            
            if len(mon_dic['Effect']):
                write_to_path(mon_dic['Effect'],eff_path)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # stores monter info that belongs in the extra_deck    
        def store_extra_monsters(e_list):
            
            mon_dic={'Link':[],'Xyz':[],'Synchro':[],'Fusion':[]}
            
            #extra deck monster file paths
            link_path=self.mon_dir+'\\'+self.file_names['Monsters'][2]
            xyz_path=self.mon_dir+'\\'+self.file_names['Monsters'][7]
            syn_path=self.mon_dir+'\\'+self.file_names['Monsters'][6]
            fus_path=self.mon_dir+'\\'+self.file_names['Monsters'][1]
            
            # unlike function 'store_main_monsters' we are able to exclude
            # conditional statements within this for statement because the
            # value of 'etype' will always contain one item and is not a list
            for i in e_list:
                card_names.append(i['name'])
                etype=i['extra_type']
                if etype==None:
                    print(i['name'])
                mon_dic[etype].append(i)
                
            # if statments used for same reason in 'store_main_monsters' function
            if len(mon_dic['Link'])>0:
                write_to_path(mon_dic['Link'],link_path)
            if len(mon_dic['Xyz'])>0:
                write_to_path(mon_dic['Xyz'],xyz_path)
            if len(mon_dic['Synchro'])>0:
                write_to_path(mon_dic['Synchro'],syn_path)
            if len(mon_dic['Fusion'])>0:
                write_to_path(mon_dic['Fusion'],fus_path)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # stores all spells
        def store_spells(spell_list):
            
            spell_dic={'Normal':[],'Continuous':[],'Field':[],'Quick-Play':[],'Equip':[],'Ritual':[]}
            
            #spell file paths
            con_path=self.spell_dir+'\\'+self.file_names['Spells'][0]
            eq_path=self.spell_dir+'\\'+self.file_names['Spells'][1]
            field_path=self.spell_dir+'\\'+self.file_names['Spells'][2]
            nor_path=self.spell_dir+'\\'+self.file_names['Spells'][3]
            qui_path=self.spell_dir+'\\'+self.file_names['Spells'][4]
            ri_path=self.spell_dir+'\\'+self.file_names['Spells'][5]
            
            # appends each card info into 'spell_dic' into
            # its respective list
            for i in spell_list:
                card_names.append(i['name'])
                stype=i['spell_type']
                spell_dic[stype].append(i)
            
            # conditional statements used to speed up Information
            # storage
            if len(spell_dic['Normal'])>0:
                write_to_path(spell_dic['Normal'],nor_path)
                
            if len(spell_dic['Continuous'],)>0:
                write_to_path(spell_dic['Continuous'],con_path)
                
            if len(spell_dic['Field'])>0:
                write_to_path(spell_dic['Field'],field_path)
                
            if len(spell_dic['Quick-Play'])>0:
                write_to_path(spell_dic['Quick-Play'],qui_path)
                
            if len(spell_dic['Equip'])>0:
                write_to_path(spell_dic['Equip'],eq_path)
                
            if len(spell_dic['Ritual'])>0:
                write_to_path(spell_dic['Ritual'],ri_path)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
                
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # stores traps information
        def store_traps(trap_list):
            trap_dic={'Normal':[],'Continuous':[],'Counter':[]}
            
            #trap file paths
            nor_path=self.trap_dir+'\\'+self.file_names['Traps'][2]
            counter_path=self.trap_dir+'\\'+self.file_names['Traps'][1]
            cont_path=self.trap_dir+'\\'+self.file_names['Traps'][0]
            
            for i in trap_list:
                card_names.append(i['name'])
                ttype=i['trap_type']
                trap_dic[ttype].append(i)
                
            # conditional statement to speed up storage time
            if len(trap_dic['Normal'])>0:
                write_to_path(trap_dic['Normal'],nor_path)
                
            if len(trap_dic['Counter'])>0:
                write_to_path(trap_dic['Counter'],counter_path)
                
            if len(trap_dic['Continuous'])>0:
                write_to_path(trap_dic['Continuous'],cont_path)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #writes names to all name file    
        def store_names():
            write_to_path(card_names,self.all_names_file)
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++    
                
                
        # calls all the functions needed to complete the storage 
        # of the card information
        store_main_monsters(card_dict['mdeck'])
        store_extra_monsters(card_dict['edeck'])
        store_spells(card_dict['spell'])
        store_traps(card_dict['trap'])
        store_names()
    #===========================================================================
    #===========================================================================
    #===========================================================================
        
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////