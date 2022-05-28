import requests  
from bs4 import BeautifulSoup
import json  
import os
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--begin', type=int, default=0) 
    parser.add_argument('--end', type=int, default=14212) 
    return parser.parse_args()

def test_EOP_cookie(cookie):
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
        'Cookie':cookie
        }  
    url = "https://www.everyonepiano.cn/Myspace" 
    page = requests.get(url=url,headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    for item in soup.find_all('p',{'class': 'UserName'}): #'id': 'search-result'
        print(item.text)

def get_midi_from_EOP(cookie, begin, end):
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
        'Cookie':cookie
        }  
    save_dir = 'midi_data_scored'
    for i in range(begin,end): #14212
        url = f"https://www.everyonepiano.cn/Midi-{i}.html"
        page = requests.get(url=url,headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        dl_page = ''
        for item in soup.find_all('a',{'class': 'btn btn-success btn-block BtnDown'}): 
            if item["href"][0:6]=='/Music':
                #print(item["href"])
                file_name = item["href"][15:].replace('/','-') + '.mid'
                print(file_name)
                dl_page = 'https://www.everyonepiano.cn' + item["href"]
                #print(dl_page)
                midi = requests.get(url=dl_page,headers=headers)
                with open(os.path.join(save_dir,file_name), 'wb') as f:
                    f.write(midi.content)
        print(f'number: {i} done')

def get_num_score_from_EOP(cookie, begin, end):
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
        'Cookie':cookie
        }  
    save_dir = 'EOP_data'
    for i in range(begin,end): #14212
        url = f"https://www.everyonepiano.cn/PDF-{i}.html"
        page = requests.get(url=url,headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        dl_page = ''
        for item in soup.find_all('a',{'class': 'btn btn-success btn-block BtnDown'}): 
            if item["href"][0:6]=='/Music':
                #print(item["href"])
                file_name = item["href"][15:].replace('/','-') + '.pdf'
                print(file_name)
                dl_page = 'https://www.everyonepiano.cn' + item["href"]
                #print(dl_page)
                pdf = requests.get(url=dl_page,headers=headers)
                with open(os.path.join(save_dir,file_name), 'wb') as f:
                    f.write(pdf.content)
        print(f'number: {i} done')


if __name__ == '__main__':
    args = get_args()
    cookie = "menunew=0-0-0-0; PHPSESSID=de1cd01801c326a22326ad8d4aff821b; think_language=en-US; username=szdqt; password=Qweszxc%40123; remember=1; huiyuan=5237ij2KdH%2FFO9Ze9uqvyyhDbmyfW87VgIPLpdqkm9fj%2F1vc75yM8ZU; FWE_getuser=szdqt; FWE_getuserid=253026; login_mima=c8122c2b69c95522513555570479f2c1"
    test_EOP_cookie(cookie)
    get_num_score_from_EOP(cookie, args.begin, args.end)
    
