import os
import time
import pickle
import urllib.request
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_binary

#**** Parameters to set at runtime ****#
search_key = '+"product development" +"environmental protection" +"profit"' #Search word
#**** Parameters to set at runtime ****#


scroll_num = 0 #number of scrolls
sleep_length = 1 #Sleep time (seconds)
google_url = 'https://www.google.co.jp/imghp?hl=ja&ogbl' #Image search URL
query_node_name = 'q' #Search term field name
parent_node_name = 'islrc' #The class name of the parent DIV tag that encloses the list of image items
item_node_name = 'isv-r' #Class name of the DIV tag that contains the image item
image_url_name = 'rg_i' #Class name of IMG tag for each image item
page_url_name = 'VFACy' #Class name of A tag that stores the posting page of each image item
image_url_attr1 = 'src'
image_url_attr2 = 'data-src'
page_url_attr = 'href'
cont_btn_name = 'r0zKGf' #Class name for the "See more images" button
img_dir = "img" #image output directory
page_dict_file = "page_dict.dat" #File name containing dictionary object of page ID and URL

#Chrome driver option settings
opt = webdriver.ChromeOptions()
#Option to suppress the error indicationg that the WebUSB device is not working
opt.add_experimental_option('excludeSwitches', ['enable-logging'])

#Get Chrome Driver
driver  = webdriver.Chrome(options=opt)

#Perform a search on the image search page
driver.get(google_url)
search = driver.find_element(By.NAME, query_node_name)
search.send_keys(search_key)
search.submit()
time.sleep(sleep_length)

#Click "See more images" to view more images
btn = driver.find_element(By.CLASS_NAME, cont_btn_name)
btn.click()

#Scroll the screen several times if necessary
for _ in range(scroll_num):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(sleep_length)

    
#Get DIV tag list containing image items
div_p = driver.find_element(By.CLASS_NAME, parent_node_name)
lst = div_p.find_elements(By.CLASS_NAME, item_node_name)

#Initialize count of page ID and image ID
p_id_cnt = 1
i_id_cnt = 1

#Initialize a dictionary containing page IDs and URLs(page_dict =(p_id,page_url))
page_dict = {}

#Get the DIV tag containing each image item
for item in lst:
    image_url = None
    page_url = None
    
    #Skip if not a DIV tag
    if item.tag_name.lower() != 'div':
        continue

    try:
        #Get image URL
        item_i = item.find_element(By.CLASS_NAME, image_url_name)
        
        image_url = item_i.get_attribute(image_url_attr1)
        if image_url is None:
            image_url = item.find_element(By.CLASS_NAME, image_url_name).get_attribute(image_url_attr2)
        if image_url is None:
            continue
    
        #Get page URL
        item_p = item.find_element(By.CLASS_NAME, page_url_name)
        
        page_url = item_p.get_attribute(page_url_attr)
        if page_url is None:
            continue
    except selenium.common.exceptions.NoSuchElementException:
        #Skip any DIV tags that do not contain image items
        continue

    if (image_url is not None) and (page_url is not None):
        #Check image file extension first and skip unsupported image formats
        with urllib.request.urlopen(image_url) as web_in:
            img_ext = (web_in.info().get_content_type().split('/'))[1]
            if img_ext not in ('jpeg','jpg','png'):
                continue

            #Get or Generate Page ID
            if page_url in page_dict.values():
                #Get registered page id if page url is already in the list
                p_id = [k for k,v in page_dict.items() if v == page_url][0]
            else:
                #If not registered, assign the latest count as a new page ID
                p_id = p_id_cnt
                p_id_cnt += 1
                page_dict[p_id] = page_url
            
            #Save image file (page ID_image ID.extension)
            img_data = web_in.read()
            file_name = str(p_id)+'_'+str(i_id_cnt)+'.'+img_ext
            file_name =  os.path.join(img_dir, file_name)
            with open(file_name, mode='wb') as f_out:
                f_out.write(img_data)
            i_id_cnt += 1

#Serialize the result and store it in a file
with open(page_dict_file, 'wb') as f:
    pickle.dump({'page_dict':page_dict},f)

#Chrome driver finalization
driver.close()
driver.quit()
