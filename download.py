# only tv show
from bs4 import BeautifulSoup
import requests, os

base = "https://www.springfieldspringfield.co.uk/"
show = "view_episode_scripts.php?tv-show="
        
def get_episodes(title):
    url = f'{base}{show}{title}'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html5lib')
    episodes = soup.select('.season-episodes > a')
    return {'status': res.status_code, 'episodes': episodes}

def download_files(title, sub_title, script, format):
    with open(f'static/scripts/{title}/{sub_title}.{format}', 'w', encoding='utf-8') as file:
        file.write(f'{sub_title}\n\n')
        for sentence in script:
            file.write(f'{sentence.strip()}.\n')

def get_scripts(title, episodes, format):
    try:
        if not os.path.exists(f'static/scripts/{title}'):
            os.makedirs(f'static/scripts/{title}')
    except OSError:
        print ('Error: Creating directory')
 
    for ep in episodes:
        url = f'{base}{ep["href"]}'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html5lib')
        h1 = soup.select_one('h1').get_text().strip()
        script = soup.select_one('.scrolling-script-container').get_text().strip()

        # script 정제
        s = ""
        for alph in script:
            if alph != '\n':
                s = s + alph
                
        new_script = ' '.join(s.split()).replace(" - ", "").split('.') #다중 공백 & "-" 제거 후 리스트로 변환
        download_files(title, h1, new_script, format) # txt, hwp, docx