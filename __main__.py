import itertools
import json
import webbrowser
import typing as t
import os
import contextlib

import fitz
import requests

from fitz import TextWriter

BASE_MS_LINK = "https://papers.gceguide.com/A%20Levels/{}%20({})/{}/{}_{}_ms_{}.pdf"
BASE_QP_LINK = "https://papers.gceguide.com/A%20Levels/{}%20({})/{}/{}_{}_qp_{}.pdf"

with open('subject_info.json') as f:
    s_info = json.load(f)

def get_link_info(parsing_string:str) -> dict:
    """It goes through the input and respectively assigns it to aligned position."""
    
    splitted = parsing_string.split('/')
    return {
        'subject_name':s_info['Subject_Info'][splitted[0]],
        'subject_code': splitted[0],
        'year':splitted[-1], 
        'paper':splitted[1], 
        'season':s_info['Season'][splitted[2].upper()+splitted[3].upper()]
    }

def get_link(info:dict, type:str) -> str:    
    """Returns the link object which would open the papers."""
    print(info['year'])
    return (
        BASE_MS_LINK.format(
            info['subject_name'],
            info['subject_code'],
            '20'+info['year'],
            info['subject_code'],
            info['season']+info['year'],
            info['paper'],
        )
        if type == 'ms'
        else BASE_QP_LINK.format(
            info['subject_name'],
            info['subject_code'],
            '20'+info['year'],
            info['subject_code'],
            info['season']+info['year'],
            info['paper'],
        )
    )
    
def get_qp(parsing_string:str) -> t.List[dict]: 
    """
    Returns a list containing dictionary with question paper info to download.
    The dictionary is given in terms that would work for `get_link`
    """
    parsed = parsing_string.split('/')
    paper_range = range(int(f"{parsed[1]}1"), 
                        int(f"{parsed[1]}4"))
    season_range = list(s_info['Season'].values())
    year_range = list(map(lambda x: int(x), parsed[-1].split('-')))
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
    """Downloads the list of question paper extracted from `get_qp`"""
    # sourcery skip: avoid-builtin-shadow
    
    links = [(f"{link['year']}-{link['season']}-{link['paper']}", get_link(link, 'qp')) for link in link_codes]
    with contextlib.suppress(FileExistsError):
        dir = f"papers/{'.'.join(parsing_string.split('/'))}"
        os.makedirs(dir)
        
    for l in links:
        res = requests.get(l[1])
        if res.status_code == 200:
            with open(f"{dir}/{l[0]}.pdf", 'wb') as f:
                f.write(res.content)
                
class Compilation:
    """Provides a clean and compiled version of the set of papers."""
    
    def __init__(self, files, text, difference):
        self.files = files
        self.text = text
        self.difference = difference - 1
    
    def set_first_page(self):
        """Sets the first page of the compilation."""
        
        doc = fitz.open()
        parsed_text = "".join(s_info['Subject_Info'][self.text.split('/')[0]]) + f" Paper {self.text.split('/')[1]}"
        page = doc.new_page()
        page.draw_rect(page.rect, color=None, fill=(0, 1, 1), overlay=False)
        tw = TextWriter(page.rect)
        font = fitz.Font("times-bold")
        tw.append((76,400), parsed_text, font=font, fontsize=24)
        tw.write_text(page, color=(0,0,0))
        return doc
    
    def set_last_page(self):
        """Sets the last page of the compilation"""
        doc = fitz.open()
        page = doc.new_page()
        page.draw_rect(page.rect, color=None, fill=(0, 1, 1), overlay=False)
        return doc
    
    def merge_questions(self):
        """Merges all of the pdf questions inot a single file."""
        merged_ = fitz.open()
        for file in self.files:
            doc = fitz.open(file)
            merged_.insert_pdf(doc, from_page=self.difference, to_page=len(doc))
        return merged_
    
    def create_paper_compilation(self):
        doc = fitz.open()
        doc.insert_pdf(self.set_first_page())
        doc.insert_pdf(self.merge_questions())
        doc.insert_pdf(self.set_last_page())
        return doc
    

def open_url(link:str) -> None:
    webbrowser.open(link)
    
# sourcery skip: de-morgan
while True:
    mode = input("\n Enter your working mode:")

    if mode in ["ms", "qp"]:
        while True:
            parse_object = input("Enter the subject code -> ")
            if parse_object == 'q':
                break
            open_url(get_link(get_link_info(parse_object), mode))
    elif mode in ['get paper', 'compile paper']:
        with contextlib.suppress(FileExistsError):
            os.mkdir('papers')
        while True:
            parse_object = input("Enter the subject-code/paper/year-range:")# 9709/1/18-21
            if parse_object == 'q':
                break

            download_qp(
                get_qp(parse_object), parse_object
            )

            if mode == 'compile paper':
                second_parse = input("Enter the difference number of pages from the front page to your first page: ")
                if second_parse == 'q':
                    break
                
                file_path = f"papers/{'.'.join(parse_object.split('/'))}"
                file_list = [f"{file_path}/{file}" for file in list(os.walk(file_path))[0][2]]
                
                Compile = Compilation(file_list, parse_object, int(second_parse))
                compiled_document = Compile.create_paper_compilation()
                compiled_name = f"{s_info['Subject_Info'][parse_object.split('/')[0]].lower()}_p{parse_object.split('/')[1]}.pdf"
                

                compiled_document.save(compiled_name)

                with contextlib.suppress(FileNotFoundError):    
                    for file in file_list:
                        os.remove(file)
                    os.rmdir(file_path)
    else:
        break
    