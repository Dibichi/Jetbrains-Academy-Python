import sys
import os
import requests
from collections import deque
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
init(autoreset=True)
folder_name = sys.argv[1]
os.makedirs(folder_name, exist_ok=True)
view_stack = deque()


def tag_remover(s):
    text = ''
    for tag in s.find_all(True):
        if tag.name == 'a':
            text_in_tag = Fore.BLUE + tag.text
        else:
            text_in_tag = Style.RESET_ALL + tag.text
        text = text + text_in_tag
    return text


while True:
    search = input()
    if search == 'exit':
        break

    if search.endswith(('.com', '.org', '.net')):
        res = requests.get('https://' + search)
        if res:
            soup = BeautifulSoup(res.content, 'html.parser')
            web_text = tag_remover(soup)
            web_data = {search.replace('.', '_'): web_text}
            view_stack.append(web_data)
            print(web_text)
            with open('{}\\{}'.format(folder_name, search.replace(".com", "")), 'w') as web_file:
                web_file.write(web_text)
        else:
            print('error')

    elif any(True for x in view_stack if search in x):
        for website in view_stack:
            formatted = f'{search}_com'
            if formatted in website:
                print(website[formatted])
                break

    elif search == 'back':
        while len(view_stack) > 1:
            view_stack.pop()
            print(view_stack[-1])

    else:
        print('error')