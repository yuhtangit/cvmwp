import os
import glob
import MeCab
import numpy as np

in_txt_dir = 'txt' #directory of input files (text of each page)
out_txt_file = 'word_list.txt' #file containing a list of words obtained from Web page text
stop_words_file = 'stop_words.csv' #File listing stopwords

#Preparation for morphological analysis
ma = MeCab.Tagger()

#Preparing input files
fpath = os.path.join(in_txt_dir,'*')
files = glob.glob(fpath)

#Preparing a stopword list
stop_words = []
line_list = np.loadtxt(stop_words_file, dtype = 'unicode', encoding= 'utf_8_sig')
for line in line_list:
    stop_words.extend(line.split(','))

#read files one by one, divide into words and add to list for output
out_list = []
for file in files:
    with open(file, 'r', encoding='shift-jis') as f_in:
        line_list = f_in.readlines()
        for line_txt in line_list:
            out_line = []
            #Split text into words line by line, then process into words
            for parse_txt in ma.parse(line_txt).splitlines():
                parse_list = parse_txt.split('\t') #Surface form and attributes are separated by tabs
                if len(parse_list) == 2:
                    word = parse_list[0] #get surface form of a word
                    attrs = parse_list[1].split(',') #Attributes are separated by commas
                    #Attribute items are part of speech (0), sub-classification 1 (1), sub-classification 2 (2), 
                    #sub-classification 3 (3), conjugation type (4), conjugation form (5), base form (6), 
                    #Reading (7), Pronunciation (8)
                    if attrs[0] in ('noun') and \
                       attrs[1] not in ('number', 'Independence', 'pronoun','suffix'):
                        if attrs[6] != '*':
                            word_result = attrs[6]
                        else:
                            word_result = word
                        #Exclude stopwords
                        if word_result not in stop_words:
                            out_line.append(word_result)              
            if len(out_line) > 1:
                out_list.append(' '.join(out_line)) #Output words separated by spaces for each line of source file
                                        
with open(out_txt_file,'w',encoding='utf-8') as f_out:
    f_out.write('\n'.join(out_list))

    
