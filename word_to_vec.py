from gensim.models import word2vec
import numpy as np
import pickle

#**** Parameters to set at runtime ****#
keys = ['product development','environmental protection','profit']  #base keywords
#**** Parameters to set at runtime ****#

#The number of words that are candidates for measuring the distance from the plane
# (those with close COS values to the combined vector of keys)
num_candidate = 100 
dim = 10 #the number of dimensions of the word vector
in_txt_file = 'refined_word_list.txt' #filename of the refined word list
res = 'word_vecs.dat' #Name of object file containing word vector
cmp = 'normal_word_list.csv' #List of keywords and vectors obtained by normal Word2Vec analysis

word_vecs = {} #initialization of dictionary of word strings and word vectors

#****** Vectorization with Word2Vec *****#
sentences = word2vec.LineSentence(in_txt_file)
#sg=1 skip-gram
#hs=0 negative sampling
#negative=5 number of noise words used for negative sampling
#epochs=10 number of learning iterations
#window=20 Same value as keyword acquisition range in refine_wordlist.py
model = word2vec.Word2Vec(sentences, sg=1, hs=0, negative=5, vector_size=dim, window=20, min_count=5,epochs=10)
word_vectors = model.wv
del model #Discard non-result data to save memory

#****** Get candidate keywords ******#
#Narrow down to words whose COS values are close to the vector of combined keys
words = [word for word, cos_value in word_vectors.most_similar(positive=keys, topn= num_candidate)]
words = keys + words #Most_similar results may not include keys, so put them at the top here

#****** Normalize the candidate keywords and store them in a tuple array along with the word string ******#
for word in words:
    vec_tmp = word_vectors.get_vector(word)
    norm_tmp = np.linalg.norm(vec_tmp) 
    vec = vec_tmp / norm_tmp
    word_vecs[word] = vec

#****** output the results at this stage for comparison ******#
with open(cmp, 'w', encoding='utf_8_sig') as f:
    for word, vec in word_vecs.items():
        f.write(word + ',' + ','.join(map(str,vec)) + '\n')
    
#****** Serialize the result and store it in a file *****#
with open(res, 'wb') as f:
    pickle.dump({'word_vecs':word_vecs},f)

