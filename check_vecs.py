import numpy as np
import pickle

#**** Parameters to set at runtime ****#
keys = ['product development','environmental protection','profit'] #base keywords
imgs=['0_1','0_2'] #file name of reference image
#**** Parameters to set at runtime ****#

num = 1000 #Number of keywords retrieved when sorted in order of priority
dim = 20 #dimension of combined vectors
res = 'combined_word_list.csv' #file containing the selected combined vectors
word_img_vecs_file = 'word_img_vecs.dat' #object file that stores word-image combined vectors

#load combined vector list, a tuple list of (word text_page ID_image ID, word vector + image vector) 
with open(word_img_vecs_file, 'rb') as f:
    obj = pickle.load(f)
    word_img_list = obj['word_img_vecs']
print('number of vecs=' + str(len(word_img_list)))

#generate keys for base word-image vectors
c_base_keys = []
for key in keys:
    for img in imgs:
        c_base_keys.append(key+'_'+img)
print(c_base_keys)

#Initialize the vector that stores the mean of the component absolute values for each dimension
abs_avg = []
for _ in range(dim):
    abs_avg.append(0.0)

#generatet mean vector of base combined vectors
mean_vec = sum([vec for key, vec in word_img_list if key in c_base_keys])/len(c_base_keys)

#Get inner product of vectors, tuple list of (word text_page ID_image ID, inner product value) 
#since combined vectors are normalized here, inner products are same wiht COS similarities
#starting position of the index is adjusted to exclude the base combined vector
#simultaneously calculate the mean of the component absolute values of combiend vectors
dot_list = []
for key, vec in word_img_list[len(c_base_keys):]:
    dot_list.append((key,np.dot(mean_vec,vec)))
    abs_avg += np.array(list(map(abs, vec)))

#the mean of component absolute values of combined vectors
print(abs_avg/num)

#sort in descending order of inner product value
dot_list.sort(key=lambda x: x[1],reverse=True) 

#output top "num" keywords and combined vectors 
with open(res, 'w', encoding='utf_8_sig') as f:
    for key, _ in dot_list[0:num]:
        vec = [vec_work for key_work, vec_work in word_img_list if key_work == key][0]
        f.write(key + ',' + ','.join(map(str,vec)) + '\n')
