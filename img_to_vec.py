import os
import numpy as np
import cv2
import pickle

#**** Parameters to set at runtime ****#
kls = 10 #number of clusters (= number of dimensions of image vector)
#**** Parameters to set at runtime ****#

dir = 'img' #image file folder
res = 'img_vecs.dat' #object file that stores each image file name and the probability vector
col = cv2.IMREAD_GRAYSCALE #Convert colors to grayscale
siz = 200 #Set image size to 200 pixels

detector = cv2.KAZE_create() #image feature extractor
classifier = cv2.BOWKMeansTrainer(kls) #K-Means cluster classifier for feature vector

#Read an image file and classify feature vectors into clusters
for file in os.listdir(dir):
    print(file)
    #Load image in grayscale and resize
    img = cv2.imread(os.path.join(dir,file), col) #Note that imread() cannot be used if the file name is double-byte
    img = cv2.resize(img, dsize = (siz,siz))
    #Extract feature points and feature vectors (the feature points are included in the first return tuple, 
    #but the variables are not set because they are not used here)
    #The second argument is the filter, the dimension of vecs is determined by the type of extractor
    _, vecs = detector.detectAndCompute(img, None) 
    #Add feature vectors to the cluster classifier (it is required to convert int to float)
    classifier.add(vecs.astype(np.float32))
#Get feature cluster (cluster centroid)
centers = classifier.cluster()

#Define a histogram extractor that matches feature vectors and feature clusters for each image in a brute-force manner
matcher = cv2.BFMatcher()
extractor = cv2.BOWImgDescriptorExtractor(detector, matcher)
extractor.setVocabulary(centers)

#For each image, calculate the probability vector that the feature point belongs to the feature cluster 
img_probs = {} #initialization of dictionary of image filenames and probability vectors
for file in os.listdir(dir):
    #Load image in grayscale and resize
    img = cv2.imread(os.path.join(dir,file), col) #Note that imread() cannot be used if the file name is double-byte
    img = cv2.resize(img, dsize = (siz,siz))
    #get feature points
    pts, _ = detector.detectAndCompute(img, None)
    vec_tmp = extractor.compute(img, pts)[0] #compute() returns three values, and the probability vector is the first
    #(Note that the above code will cause an error in feature extraction using binary code like AKAZE)
    #normalize the norm of the probability vector to 1 (because we normalize the word vector as well)
    norm_tmp = np.linalg.norm(vec_tmp) 
    vec = vec_tmp / norm_tmp
    #Get file name without extension
    file_name = os.path.splitext(file)[0]
    #Add to dictionary for output
    img_probs[file_name] = vec
 
#Serialize the result and store it in a file
with open(res, 'wb') as f:
    pickle.dump({'img_vecs':img_probs},f)
    
