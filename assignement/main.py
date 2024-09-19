import requests

import dotenv
import os
import datetime

# load the environment variables
dotenv.load_dotenv()


def get_url(url, filename):
    if not os.path.exists(filename):

        # fetch the page if it doesn't exist
        page = requests.get(url)

        # save the page to a file
        with open(filename, 'w', encoding='UTF8') as f:
            f.write(page.text)

        page = page.text

    else:
        # if the page exists, read it from the file
        with open(filename, 'r', encoding='UTF8') as f:
            page = f.read() 
            
    return page


for i in range(40,58):
    tab = get_url(os.getenv('URL').format(id=f'{i:02}'), f'tab{i:02}')
    if tab:
        lines = tab.splitlines()
        lines = [line for line in lines if line]
        data = lines[-11:]
        data = [[ d for d in l.split(" ") if d] for l in data]

        print(data)
                    
