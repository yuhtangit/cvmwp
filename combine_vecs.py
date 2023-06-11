import os
import glob
import pickle
import numpy as np

#**** Parameters to set at runtime ****#
keys = ['product development','environmental protection','profit'] #base keywords
#**** Parameters to set at runtime ****#

word_vecs_file = 'word_vecs.dat' #object file containing word vector
img_vecs_file = 'img_vecs.dat' #object file that stores the file name and probability vector for each image
word_img_vecs_file = 'word_img_vecs.dat' #object file that stores the combined vectors of words and images
in_txt_dir = 'txt' #directory of input files (text of each page)

#Get a dictionary object containing word vectors and image vectors
with open(word_vecs_file, 'rb') as f:
    obj = pickle.load(f)
    word_vecs_dict = obj['word_vecs'] #Dictionary of "word-text:word-vector"

with open(img_vecs_file, 'rb') as f:
    obj = pickle.load(f)
    img_vecs_dict = obj['img_vecs'] #Dictionary of "page ID_image ID: image vector"

#Prepare a page text file for linking word vectors and page IDs
text_dict = {}    
fpath = os.path.join(in_txt_dir,'*')
files = glob.glob(fpath)
for file in files:
    with open(file, 'r', encoding='shift-jis') as f_in:
        p_text = f_in.read()
        file_name = os.path.basename(file)
        p_id = os.path.splitext(file_name)[0]
        text_dict[p_id] = p_text #Dictionary of "page ID: page text"

#Create a dictionary containing a list of page IDs containing each word
word_dict = {}        
for w_key in word_vecs_dict.keys():
    if w_key in keys:
        word_dict[w_key] = [0] #Add "0" as page ID for base keywords
    else:
        p_id_list = [int(p_id) for p_id, p_text in text_dict.items() if w_key in p_text]    
        word_dict[w_key] = p_id_list
   
#Combine word vector and image vector
word_img_list = [] #Tuple list of (word text_page ID_image ID, word vector + image vector)
for w_key in word_dict.keys():
    p_id_list = word_dict[w_key]
    word_vec = word_vecs_dict[w_key]
    for p_id in p_id_list:
        #Get the image id with the page ID of the page containing the word 'w_key' and combine the word and image vectors
        for i_key in [key for key in img_vecs_dict.keys() if p_id == int(key.split('_')[0])]:
            img_vec = img_vecs_dict[i_key]
            c_key = w_key + '_' + i_key
            c_vec = np.hstack([word_vec,img_vec])
            word_img_list.append((c_key,c_vec))            

#Serialize the result and store it in a file
with open(word_img_vecs_file, 'wb') as f:
    pickle.dump({'word_img_vecs':word_img_list},f)


