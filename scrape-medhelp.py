# -*- coding: utf-8 -*-
"""
@author: Serdarcan Dilbaz
Python code for scraping medhelp posts
"""

from urllib.request import urlopen
from urllib.request import build_opener
from bs4 import BeautifulSoup
from multiprocessing import Pool, Manager, TimeoutError
import multiprocessing as mp
import time, argparse, os
from argparse import RawTextHelpFormatter
import xml.etree.cElementTree as ET
import numpy as np

def process_page(forum_dict,url,url_list):
    print('Processing Page {}'.format(url.split('=')[-1]))
    opener = build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    for k in range(10):
        try:
            response=opener.open(url)
            break
        except Exception as e:
            print(e)
            if k==9:
                return 
            time.sleep(3)

    page_html = response.read()
    
    soup=BeautifulSoup(page_html,'lxml')
    mydivs = soup.findAll("h2", {"class": "subj_title"})

    for div in mydivs:
#            post_links[key].append('https://www.medhelp.org'+div.select("a")[0].attrs["href"])
        url_list.append('https://www.medhelp.org'+div.select("a")[0].attrs["href"])

def process_text(some_string):
    some_string=some_string.replace("\xa0"," ")
    some_string=some_string.strip()
    some_string=' '.join([word for word in some_string.split(' ') if not word.startswith('\r') and word])
    some_string=some_string.replace("\r","")
    return some_string


def extract_post(url,save_dir):
    href_flag=False
    root = ET.Element("post")
    post_fields=ET.SubElement(root, "post_fields")

    opener = build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response=opener.open(url)
    
    html_contents = response.read()
    soup=BeautifulSoup(html_contents,'lxml')

    title_div=soup.findAll("h1", {"class": "subj_title"})
    title=title_div[0].text.strip()

    subj_header=soup.find("div", {"class": "subj_header"})
    poster_name=subj_header.find("span", {"itemprop": "name"}).text
    try:
        poster_link=subj_header.find("a",href=True)['href']
        ET.SubElement(post_fields, "user_link").text = poster_link
    except TypeError:
        pass
            
    try:
        post_time=time.ctime(int(subj_header.find("time",{"class":"mh_timestamp"})['data-timestamp']))
    except TypeError:
        post_time=time.ctime(int(subj_header.find("span",{"class":"mh_timestamp"})['data-timestamp']))

    post_text_div=soup.findAll("div", {"id": "subject_msg"})[0]
    for div in post_text_div.findAll("a"): 
        div.decompose()
    post_text=process_text(post_text_div.text)
    
    post_id=url[-url[::-1].find('/'):]
    print('Post ID: {}'.format(post_id.rjust(8)))
    
    ET.SubElement(post_fields, "href").text = url
    ET.SubElement(post_fields, "title").text = title
    ET.SubElement(post_fields, "username").text = poster_name
    ET.SubElement(post_fields, "time").text = post_time
    ET.SubElement(post_fields, "body").text = post_text
    
    response_divs=soup.findAll("div",{"itemprop":"suggestedAnswer"})
    for resp_id,response in enumerate(response_divs):
        current_resp_branch=ET.SubElement(root,"response",resp_id=str(resp_id))
        
        user_info=response.find("div",{"class":"username"})
        resp_username=user_info.text.strip()
        
        try:
            resp_link=user_info.find("a",href=True)['href']
            ET.SubElement(current_resp_branch, "user_link").text = resp_link
        except TypeError:
            pass

        try:
            resp_time=time.ctime(int(user_info.find("span",{"class":"mh_timestamp"})['data-timestamp']))
        except TypeError:
            resp_time=time.ctime(int(user_info.find("time",{"class":"mh_timestamp"})['data-timestamp']))
        
        resp_text=process_text(response.find("div",{"class":"resp_body"}).text)

        ET.SubElement(current_resp_branch, "username").text = resp_username
        ET.SubElement(current_resp_branch, "time").text = resp_time
        ET.SubElement(current_resp_branch, "body").text = resp_text

        comments=[]
        comment_divs=response.findAll("div", {"class": "comment_ctn"})
        for comm_id,comment_div in enumerate(comment_divs):
            current_comm_branch=ET.SubElement(current_resp_branch,"comment",resp_id=str(comm_id))
            user_info=comment_div.find("div",{"class":"username"})
            commenter_username=user_info.text.strip()

            try:
                commenter_link=user_info.find("a",href=True)['href']
                ET.SubElement(current_comm_branch, "user_link").text = commenter_link
            except TypeError:
                pass
            
            comment_time=time.ctime(int(user_info.find("span",{"class":"mh_timestamp"})['data-timestamp']))
            
            comment_text=process_text(comment_div.find("div",{"class":"comment_body"}).text)

            ET.SubElement(current_comm_branch, "username").text = commenter_username
            ET.SubElement(current_comm_branch, "time").text = comment_time
            ET.SubElement(current_comm_branch, "body").text = comment_text

    tree = ET.ElementTree(root)
    tree.write(os.path.join(save_dir,post_id+".xml"))
    if href_flag:
        print(url)

    
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Scrapes MedHelp post, responses and comments and saves as ETrees', formatter_class=RawTextHelpFormatter)
    parser.add_argument('saving_dir',help='Save Location for MedHelp data')
    parser.add_argument('--ncpu', nargs='?', help='Number of cores for multiprocessing, 1 by default', default=1, type=int, dest='mpcpu')

    args = parser.parse_args()

    saving_dir=args.saving_dir
    mpcpu=max(args.mpcpu,1)
    
    manager=Manager()
    url_list = manager.list()
    pool = Pool(processes=mpcpu)

    if not os.path.isdir(saving_dir):
        msg="Saving directory does not exist. You entered: %s" %saving_dir
        raise argparse.ArgumentTypeError(msg)
    
    data_folder=os.path.join(saving_dir,'MedHelp-Data')
    if not os.path.isdir(data_folder):
        os.mkdir(data_folder)

    base='https://www.medhelp.org/forums/list'
    
    opener = build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    
    response=opener.open(base)
    
    html_contents = response.read()
    
    soup=BeautifulSoup(html_contents,'lxml')
    mydivs = soup.findAll("div", {"class": "forums_link"})
    
    forum_dict={}
    for element in mydivs:
        forum_category=element.text.strip()
        forum_category=forum_category.replace('\\','-')
        forum_category=forum_category.replace('/','-')
        if not forum_category in forum_dict:
            href=element.select("a")[0].attrs["href"]
            if href.startswith('/forums/'):
                forum_dict[forum_category]='https://www.medhelp.org'+href

    if os.path.isfile(os.path.join(data_folder,"dones.txt")):
        with open(os.path.join(data_folder,"dones.txt"), "r") as f:
            temp=f.read()
        dones=temp.split('\n')    
    else:
        dones=[]

    if not os.path.isdir(os.path.join(data_folder,"post_indexes")):
        os.mkdir(os.path.join(data_folder,"post_indexes"))

    for key in forum_dict.keys():
        if not key in dones:
            print('Indexing post urls of {}'.format(key))
            processes=[pool.apply_async(process_page, (forum_dict,forum_dict[key],url_list))]
            response=opener.open(forum_dict[key])
            page_html = response.read()
            soup=BeautifulSoup(page_html,'lxml')
            num_div = soup.find("div", {"class": "forum_title"})
            max_post_num=num_div.text
            max_post_num=int(max_post_num[max_post_num.find('of')+3:max_post_num.find(')')])
            processes.extend([pool.apply_async(process_page, (forum_dict,url,url_list)) for url in [forum_dict[key]+'?page='+str(k) for k in range(2,int(max_post_num/20)+1)]])
            if processes:
                [proc.get(300) for proc in processes]
            
            
            with open(os.path.join(data_folder,"post_indexes",key+'.txt'),"w+") as file:
                file.write('\n'.join(list(url_list)))
            
            url_list = manager.list()
    
    if not os.path.isdir(os.path.join(data_folder,"trees")):
        os.mkdir(os.path.join(data_folder,"trees"))
    print('\t\tPost Extraction Started')
    for key in forum_dict.keys():
        print('\tPost Extraction of {} started'.format(key))
        with open(os.path.join(data_folder,"post_indexes",key+".txt"), "r") as f:
            temp=f.read()

        save_dir=os.path.join(data_folder,"trees",key)
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)
        
        processes=[pool.apply_async(extract_post, (url,save_dir)) for url in temp.split('\n') if url and not os.path.isfile(os.path.join(save_dir,url[-url[::-1].find('/'):]+".xml"))]
        
        for proc in processes:
            try:
                proc.get(timeout=60)
            except TimeoutError:
                print('Process timed out.')

