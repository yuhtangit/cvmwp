import urllib.request
import os
import pickle
from bs4 import BeautifulSoup

txt_dir = "txt" #text output directory
page_dict_file = "page_dict.dat" #File name containing dictionary object of page ID and URL
time_out = 30 #Number of seconds before timing out in web access
     
#A function that outputs HTML text to out_filename
def get_html_txt(res, out_filename):
    #Get HTML text after setting encoding
    charset_def ='utf-8'
    html_txt_tmp = res.read()
    charset = res.info().get_content_charset()
    if charset is None:
        charset = charset_def
    html_txt = html_txt_tmp.decode(charset)

    #Remove tags with BeautifulSoup
    soup = BeautifulSoup(html_txt,"html.parser")
    #Remove leading and trailing whitespace and blank lines
    plain_txt_tmp1 = soup.get_text()
    #remove special characters
    plain_txt_tmp2 = plain_txt_tmp1.translate(str.maketrans({'_': '', '-': '', '.': '', ',': '', ':': '', ';': ''})) 
    #Split into line list and remove leading and trailing whitespace
    plain_txt_tmp3 = [line.strip() for line in plain_txt_tmp2.splitlines()] 
    #Exclude blank lines and concatenate with line feed code
    plain_txt = "\n".join(line for line in plain_txt_tmp3 if line) 
    #Transform once and undo to eliminate untranslatable code
    plain_txt = plain_txt.encode('shift-jis','ignore')
    plain_txt = plain_txt.decode('shift-jis')

    with open(out_filename, 'w',encoding='shift-jis') as f:
        f.write(plain_txt)

#Body processing

#Load a dictionary containing page IDs and URLs(page_dict =(p_id,page_url))
with open(page_dict_file, 'rb') as f:
    obj = pickle.load(f)
    page_dict = obj['page_dict']

#Access each Web page and save the text to a file
for p_id, page_url in page_dict.items():
    #Since access denial etc. may occur, include exception handling
    try:
        res = urllib.request.urlopen(page_url, timeout=time_out)
        content_type = res.info().get_content_type()
        if (res.getcode() < 300) and (content_type == 'text/html') :
            #Setting the output file path
            file_name = str(p_id)+'.txt'
            file_name =  os.path.join(txt_dir, file_name)
            #Go to website and get text
            get_html_txt(res, file_name)
            print(page_url + ':OK\n')
        else:
            print(page_url + 'Not HTML or Error: ' + res.getcode()+'\n')    
    except Exception as e:
        print(page_url + ':Exception: ' + str(e) + '\n')
    finally:
        res.close()

