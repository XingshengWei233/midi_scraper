import requests  
from bs4 import BeautifulSoup 
import os
import argparse
from multiprocessing import Pool
import pickle as pk


HEADERS = {
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
        'Cookie':"menunew=0-0-0-0; PHPSESSID=de1cd01801c326a22326ad8d4aff821b; think_language=en-US; username=szdqt; password=Qweszxc%40123; remember=1; huiyuan=5237ij2KdH%2FFO9Ze9uqvyyhDbmyfW87VgIPLpdqkm9fj%2F1vc75yM8ZU; FWE_getuser=szdqt; FWE_getuserid=253026; login_mima=c8122c2b69c95522513555570479f2c1"
        }  

SAVE_DIR = '/media/xingshengwei/Seagate Portable Drive/scrape/EOP_data_pdf'

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--begin', type=int, default=0) 
    parser.add_argument('--end', type=int, default=14212) 
    return parser.parse_args()


def test_EOP_cookie():
    url = "https://www.everyonepiano.cn/Myspace" 
    page = requests.get(url=url,headers=HEADERS)
    soup = BeautifulSoup(page.text, 'html.parser')
    for item in soup.find_all('p',{'class': 'UserName'}): #'id': 'search-result'
        print(item.text)



def scrape_one(url_tuple):
    #for i,file in enumerate(os.listdir(SAVE_DIR)):

    print(f'number: {url_tuple[0]} start')
    page = requests.get(url=url_tuple[1],headers=HEADERS)
    soup = BeautifulSoup(page.text, 'html.parser')
    dl_page = ''
    for item in soup.find_all('a',{'class': 'btn btn-success btn-block BtnDown'}): 
        if item["href"][0:6]=='/Music':
            #print(item["href"])
            file_name = item["href"][15:].replace('/','-') + '.pdf'
            print(file_name)
            dl_page = 'https://www.everyonepiano.cn' + item["href"]
            #print(dl_page)
            pdf = requests.get(url=dl_page,headers=HEADERS)
            with open(os.path.join(SAVE_DIR,file_name), 'wb') as f:
                f.write(pdf.content)

    log_path = os.path.join(SAVE_DIR,'log.pkl')
    with open(log_path, "rb") as f:
        log = pk.load(f)
    with open(log_path, "wb") as f:
        log.append(url_tuple[0])
        pk.dump(log,f)

    print(f'number: {url_tuple[0]} done')


def get_num_score_from_EOP(begin, end):
    
    log_path = os.path.join(SAVE_DIR,'log.pkl')
    if not os.path.exists(log_path):
        with open(log_path, "wb") as f:
            pk.dump([0],f)
    with open(log_path, "rb") as f:
        log = pk.load(f)
        print(log)

    all_url_tuples = []
    for i in range(begin,end): #14212
        url = f"https://www.everyonepiano.cn/PDF-{i}.html"
        url_tuple = (i,url)
        all_url_tuples.append(url_tuple)
    for index in log:
        all_url_tuples[index] = (-1,'')
    for i,url_tuple in reversed(list(enumerate(all_url_tuples))):
        if url_tuple[0] == -1: all_url_tuples.pop(i)

    with Pool(30) as p:
        p.map(scrape_one, all_url_tuples)


if __name__ == '__main__':
    args = get_args()
    test_EOP_cookie()
    get_num_score_from_EOP(args.begin, args.end)
    
