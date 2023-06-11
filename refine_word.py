
#**** Parameters to set at runtime ****#
keys = ['product development','environmental protection','profit'] 
#**** Parameters to set at runtime ****#

word_range = 20 #Specify how many words before and after the keyword to analyze
in_txt_file = 'word_list.txt' #word list file name
out_txt_file = 'refined_word_list.txt' #filename of the refined word list

#read input word list from file and store in list
with open(in_txt_file, 'r', encoding='utf-8') as f_in:
    word_list_in = f_in.read().split()

word_list_out = []
index = 0

#Store words located before and after keys (within the width of word_range) in word_list_out
while index < len(word_list_in):
    word = word_list_in[index]
    if word in keys:
       start = max(0,index-word_range)
       end = min(index+word_range, len(word_list_in))
       word_list_out.extend(word_list_in[start:end])
    index += 1

#Output the contents of word_list_out to a file
with open(out_txt_file,'w',encoding='utf-8') as f_out:
    f_out.write('\n'.join(word_list_out))

