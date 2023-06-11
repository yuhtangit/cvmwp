This document explains source codes of the paper 
"Improving corporate multi-modal message by Combined Vectors 
Measured with Hyper Plane Distance Method" 
and how to execute the example case described in the paper.
Please read the paper first before reading this document.

******** Source code list **********
[get_image.py]

 overview:
  Search for web pages that contain base words,
  and output image data and URLs of the web pages.

 input parameters:
  search_key
   Text with base words surrounded by ", prefixed with + 
   and concatenated with spaces.(designated at the beginning 
   of the source code)

 output:
  page_dict.dat 
    Object data file listing pair of sequence number and URL of Web pages
  image data
    Image data obtained by search, stored in the pre-created "img" subfolder

 required libraries:
  os, time, pickle, urllib.request, selenium.common.exceptions
  selenium.webdriver, selenium.webdriver.common.by.By
  chromedriver_binary
---------------------
[img_to_vec.py]

 overview:
  vectorize image data

 input parameters:
  kls
   number of dimensions of image vector

 output:
  img_vecs.dat 
   dictionary file of "page ID_image ID (serial number)" and image vector

required libraries:
 os, numpy, cv2, pickle
---------------------
[get_text.py]

 overview:
  Access Web pages and get texts

 input parameters/files:
  None

 output:
  page_dict.dat
   object data file listing pair of page ID and URL of Web pages
  text data 
   Text data extracted from Web pages, stored in the pre-created "txt" subfolder

required libraries:
 urllib.request, os, pickle, bs4.BautifulSoap
---------------------
[tokenize_text.py]

 overview:
  Break text into words by morphological analysis

 input files:
  userdict.csv
   Own dictionary file to add business knowledge etc
  stop_words.csv
   File specifying stopwords

 output:
  word_list.txt
   a list of words obtained from Web page text

required libraries:
 os, glob, MeCab, numpy
---------------------
[refine_word.py]

 overview:
  Narrow the scope of suggested keywords according to distance from base words

 input files:
  word_list.txt
   a list of words obtained from Web page text

 input parameters:
  keys
   the same parameter with search_key in get_image.py

 output:
  refined_word_list.txt
   a list of words obtained from word_list.txt by narrowing process

 required libraries:
  None
---------------------
[word_to_vec.py]

 overview:
  vectorize word data

 input files:
  refined_word_list.txt
   a list of words obtained from word_list.txt by narrowing process

 input parameters:
  keys
   the same parameter with search_key in get_image.py

 output:
  word_vecs.dat
   dictionary file of words and word vectors

  normal_word_list.csv
   Word list selected by COS similarity with text-only combined vector

required libraries:
 gensim.models.word2vec, numpy, pickle
---------------------
[combine_vecs.py]

 overview:
  Join word vector and image vector with page ID

 input parameters:
  keys
   the same parameter with search_key in get_image.py

 input files:
  word_vecs.dat
   dictionary file of words and word vectors
  img_vecs.dat 
   dictionary file of "page ID_image ID (serial number)" and image vector

 output:
  word_img_vecs.dat
   object data file containing a list of word-image combined vectors

required libraries:
 os, glob, numpy, pickle
---------------------
[select_vecs.py]

 overview:
  Reduce the dimension of word-image vectors and prioritize them according 
  to the distance to the hyperplane spanned by base vectors

 input parameters:
  keys
   the same parameter with search_key in get_image.py
  imgs
   file name of reference image

 input files:
  word_img_vecs.dat
   object data file containing a list of word-image combined vectors

 output:
  revised_word_list.csv
   Word list selected by the proposed method

required libraries:
 sklearn.manifold.TSNE, numpy, warnings, pickle
---------------------
[check_vecs.py]

 overview:
  For comparison, select word-image combined vectors using conventional method

 input parameters:
  keys
   the same parameter with search_key in get_image.py
  imgs
   file name of reference image

 input files:
  word_img_vecs.dat
   object data file containing a list of word-image combined vectors

 output:
  combined_word_list.csv
   Word list selected by conventional method

required libraries:
 numpy, pickle

******** How to run the code **********

requirements:
 Python3.* or later
 Chrome Browser
 
 Chrome Driver suitable for the version of Chrome Browser should be properly installed.
 The required libraries are listed in the source code description above.
 Following subfolders are to be prepared in the folder where the  code is running.
  img   subfolder storing retrieved image files 
  txt   subfolder storing retrieved text files

  The execution environment in the example case of the paper is as follows
  Hardware: DELL XPS15 12th Gen Intel(R) Core(TM) i5-12500H 2.50 GHz 32GB RAM
  OS: Windows 11 Pro 22H2 64bit
  Development platform: Python 3.10.7

Execution procedure is as follows according to the steps described in Fig2 of the paper.

Preparation:
 Specify the base keywords and images in the search_key, keys, imgs parameters of each source code

Step1: Web Page Crawling
 Run get_text.py and get_image.py. 
 This perfoms Web page crawling including base keywords and retrieves text in the txt subfolder 
 and images in the img folder from Web pages.

Step2: Tokenize Text
 Run tokenize_text.py and refine_word.py.
 This decomposes text into words as preparation for vectrization.

Step3: Vectroize Words and Images
 Run word_to_vec.py and img_to_vec.py.
 This vectroizes word and image data respectively.

Step4: Combination and Dimension Reduction
 Run combine_vecs.py.
 This combine word vectors and image vectors.
 In the description of the paper, dimensional reduction is performed here, 
 but in the source code, because of efficiency, it is performed in select_vecs.py.

Step5: Measure the distance from the hyper plane.
 Run select_vecs.py and check_vecs.py.
 select_vecs.py performs dimensional reduction and prioritize combined vectors
 according to the distance to the hyperplane spanned by base vectors.
 For comparison, check_vecs.py performs the prioritization with conventional method.

