import bs4
from bs4 import BeautifulSoup
import argparse
import requests
import json
import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--f',metavar = 'file')
    args = parser.parse_args()
    filename = args.f
    file_f = filename.split('_')[0]
    print(file_f)
    with open('server_url/' + filename, mode = 'r') as f:
        line = f.readline()
        name = 0
        while line:
            try:
                URL = line.split('\t')[0]
                threadname = line.split('\t')[1]
                # try:
                headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
                r = requests.get(URL, headers=headers, timeout=5)
                r.encoding = r.apparent_encoding
                soup = bs4.BeautifulSoup(r.text, 'html5lib')
                title = soup.find_all('h1')[0].get_text()

                posts = soup.find_all(class_ = 'thread')

                date = posts[0].find_all('dt')
                text = posts[0].find_all('dd')
                texts = []
                for post_i in range(len(date)):
                    each_text = {}
                    each_text['userid'] = post_i['data-userid']
                    each_text['threadid'] = post_i['id']
                    each_text['threadname'] = threadname
                    meta = post_i.find_all('div')[0]
                    #each_text['meta'] = meta
                    each_text['username'] = meta.find_all('span')[1].get_text()
                    each_text['date'] = meta.find_all('span')[2].get_text()       
                    texts.append(each_text)

                with open('save/'+ file_f + '/'+ file_f +'_'+str(name) + '.txt', 'w', encoding = 'utf8') as f:
                    for text in texts:
                        f.write(json.dumps(text))
                        f.write('\n')
                
                with open('save/' + file_f + '/save_' + file_f+ '.txt', 'w', encoding = 'utf-8') as f:
                    f.write(file_f + '_'+ str(name) + '.txt' + '\t' + title + '\t' + URL)
                    f.write('\n')
        
                time.sleep(1)
                name += 1
                line = f.readline()
    
            except:
                print('no')
                line = f.readline()

    
main()