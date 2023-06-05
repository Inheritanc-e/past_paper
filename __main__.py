import itertools
import json
import webbrowser
import typing as t
import os
import contextlib

import requests

BASE_MS_LINK = "https://papers.gceguide.com/A%20Levels/{}%20({})/{}/{}_{}_ms_{}.pdf"
BASE_QP_LINK = "https://papers.gceguide.com/A%20Levels/{}%20({})/{}/{}_{}_qp_{}.pdf"

with open('past_paper/subject_info.json') as f:
    s_info = json.load(f)

def get_link_info(parsing_string:str) -> dict:
    splitted = parsing_string.split('/')
    return {
        'subject_name':s_info['Subject_Info'][splitted[0]],
        'subject_code': splitted[0],
        'year':splitted[-1], 
        'paper':splitted[1], 
        'season':s_info['Season'][splitted[2].upper()+splitted[3].upper()]
    }
    
def get_link(info:dict, type:str) -> str:    
    return (
        BASE_MS_LINK.format(
            info['subject_name']
            if len(info['subject_name'].split()) <= 1
            else "%20-%20".join(info['subject_name'].split()),
            info['subject_code'],
            f"20{info['year']}",
            info['subject_code'],
            f"{info['season']}{info['year']}",
            info['paper'],
        )
        if type == 'ms'
        else BASE_QP_LINK.format(
            info['subject_name']
            if len(info['subject_name'].split()) <= 1
            else "%20-%20".join(info['subject_name'].split()),
            info['subject_code'],
            f"20{info['year']}",
            info['subject_code'],
            f"{info['season']}{info['year']}",
            info['paper'],
        )
    )
    
def get_qp(parsing_string:str) -> t.List[dict]: 
    parsed = parsing_string.split('/')
    paper_range = range(int(f"{parsed[1]}1"), 
                        int(f"{parsed[1]}4"))
    season_range = list(s_info['Season'].values())
    year_range = list(map(lambda x: int(x), parsed[-1].split('-')))
    print(paper_range)
    return [
        {
            'subject_name': s_info['Subject_Info'][parsed[0]],
            'subject_code': parsed[0],
            'year': y,
            'paper': p,
            'season': s,
        }
        for y, s, p in itertools.product(
            range(year_range[0], year_range[1] + 1),
            season_range,
            paper_range,
        )
    ]
    
    
def download_qp(link_codes, parsing_string:str) -> None:
    # sourcery skip: avoid-builtin-shadow
    links = [(f"{link['year']}-{link['season']}-{link['paper']}", get_link(link, 'qp')) for link in link_codes]
    with contextlib.suppress(FileExistsError):
        dir = f"papers/{'.'.join(parsing_string.split('/'))}"
        os.makedirs(dir)
        
    for l in links:
        print(l)
        res = requests.get(l[1])
        if res.status_code == 200:
            with open(f"{dir}/{l[0]}.pdf", 'wb') as f:
                f.write(res.content)
    
def open_url(link:str) -> None:
    webbrowser.open(link)
    
while True:
    mode = input("\n Enter your working mode:")
    if mode in ["ms", "qp"]:
        while True:
            parse_object = input("Enter the subject code -> ")
            if parse_object == 'q':
                break
            open_url(get_link(get_link_info(parse_object), mode))        
    elif mode == 'get paper':
        with contextlib.suppress(FileExistsError):
            os.mkdir('papers')
        while True:
            parse_object = input("Enter the subject-code/paper/year-range:")# 9709/1/18-21
            if parse_object == 'q':
                break
            download_qp(
                get_qp(parse_object), parse_object
        )
    else:
        break
    