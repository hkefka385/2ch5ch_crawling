import bs4
from bs4 import BeautifulSoup
import argparse
import requests
import json
import time
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--f',metavar = 'file')
    args = parser.parse_args()
    filename = args.f
    file_f = filename.split('_')[0]
    print(file_f)
    
    with open('save/' + file_f + '/save_' + file_f+ '.txt', 'w', encoding = 'utf-8') as fall:
        with open('server_url/' + filename, mode = 'r') as f:
            line = f.readline()
            name = 0
            pbar = tqdm(range(1000000))
            while line:
                URL = line.split('\t')[0]
                #print(URL)
                threadname = line.split('\t')[1]
                # try:
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
                r = requests.get(URL, headers=headers, timeout=5)
                if r.apparent_encoding == None:
                    r.encoding = 'shift_jis'
                else:
                    r.encoding = r.apparent_encoding
                soup = bs4.BeautifulSoup(r.text, 'html5lib')
                try:
                    title = soup.find_all('h1')[0].get_text()
                    posts = soup.find_all(class_ = 'thread')

                    meta = posts[0].find_all('dt')
                    text = posts[0].find_all('dd')
                    texts = []
                    for post_i in range(len(meta)):
                        each_text = {}
                        if meta[post_i].get_text().split('：')[0] == '1001 ':
                            continue
                        try:
                            each_text['text'] = text[post_i].get_text()
                            each_text['userid'] = meta[post_i].get_text().split('：')[1].strip()
                            each_text['threadid'] = meta[post_i].get_text().split('：')[0].strip() 
                            each_text['threadname'] = threadname
                            each_text['username'] = meta[post_i].get_text().split('：')[2].split('ID:')[0][:-1]
                            each_text['date'] = meta[post_i].get_text().split('：')[2].split('ID:')[1]
                            texts.append(each_text)
                        except:
                            continue
                    if len(texts) < 10:
                        line = f.readline()
                        time.sleep(1)
                        continue
                    with open('save/'+ file_f + '/'+ file_f +'_'+str(name) + '.txt', 'w', encoding = 'utf8') as fr:
                        for text in texts:
                            fr.write(json.dumps(text))
                            fr.write('\n')
                    
                    fall.write(file_f + '_'+ str(name) + '.txt' + '\t' + title + '\t' + URL)
                    fall.write('\n')
            
                    time.sleep(1)
                    name += 1
                    line = f.readline()
                    pbar.update(1)

                except:
                    print(URL)
                    print('error')
                    time.sleep(1)
                    pbar.update(1)
                    line = f.readline()


    
main()