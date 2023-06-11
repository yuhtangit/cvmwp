from sklearn.manifold import TSNE
import numpy as np
import warnings
import pickle

#**** Parameters to set at runtime ****#
keys = ['product development','environmental protection','profit'] #base keywords
imgs=['0_1','0_2'] #file name of reference image
#**** Parameters to set at runtime ****#

num = 100 #Number of keywords retrieved when sorted in order of priority
res = 'reviesed_word_list.csv' #file containing the selected combined vectors
word_img_vecs_file = 'word_img_vecs.dat' #object file that stores word-image combined vectors

#function that returns the distance between a point and the hyperplane with normal vector n
def psdist(p,n):
    ret = abs(np.dot(p,n))/np.linalg.norm(n)
    return(ret)

#function that returns the distance between a point and the hyperplane with normal vector n
def nvector(m):
    #find the normal vector n with the first vector component fixed to 1 by solving a linear equation
    m = np.array(m)
    b = m[:,0]*(-1) #the first column is taken to the right side of the equation, so it is multiplied by a negative number.
    a = m[:,1:] #the second and subsequent columns are the left side of the equation
    n = np.linalg.solve(a,b)
    n = np.append(1,n) #set the first vector component of the resulting solution to 1
    return(n)

#hide future warnings in TSNE
warnings.simplefilter('ignore', FutureWarning)

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

#Number of dimensions to be reduced (= number of reference keywords x number of reference images + 1)
dim = len(c_base_keys)+1

#****** Dimensional reduction by t-SNE *****#
#after expanding the list into a 2-dimensional tuple with *-operator, convert it into two lists with zip
c_keys = list([tup for tup in zip(*word_img_list)][0]) #list of "word text_page ID_image ID"
base_vectors = np.array([tup for tup in zip(*word_img_list)][1]) #list of combined vectors

#random_state: specification for constant random number generation for always getting the same result
#method: must specify method=exact if the reduced dimension is 4 or more
#perplexity: execute with the default value (= 30) (5 to 50 is recommended), as the result is the same under different values
print('t-SNE Start')
tsne = TSNE(n_components=dim, random_state=0, method='exact', perplexity=30)
#tsne = TSNE(n_components=dim, random_state=0, method='barnes_hut')
rd_vectors = tsne.fit_transform(base_vectors) #dimensionally reduced vectors
print('t-SNE End')

#***** Create a list of keywords arranged in order of closeness to the hyperplane spanned by keys *****#
#find the normal vector (n)
m = []
for key in c_base_keys:
    m.append(rd_vectors[c_keys.index(key)]) #get dimensionally reduced combined base vector
n=nvector(m)

#create a list of distance between the hyperplane spanned by the base combined vector and the other combined vectors
result_list =[]
i=0
for key in c_keys:
    vector = rd_vectors[c_keys.index(key)]
    item = (key,psdist(n,vector))
    result_list.append(item) #add a tuple pairing the combined vector key and the distance to the hyperplane to the list

#sort the list in descending order of distance to the hyperplane
result_list.sort(key=lambda x: x[1],reverse=False) 

#output top "num" keywords and combined vectors 
with open(res, 'w', encoding='utf_8_sig') as f:
    for key, val in result_list[0:num]:
        f.write(key + ',' + ','.join(map(str,rd_vectors[c_keys.index(key)])) + '\n')

