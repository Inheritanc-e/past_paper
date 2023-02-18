import json
import webbrowser

BASE_LINK = "https://gceguide.com/papers/A%20Levels/{}%20({})/{}/{}_{}_ms_{}.pdf"

MOCK_VALUE = "9709/13/M/J/22"

with open('past_paper/subject_info.json') as f:
    s_info = json.load(f)

def get_link_info(parsing_string:str) -> dict:
    splitted = parsing_string.split('/')
    return {
        'subject_name':s_info['Subject_Info'][splitted[0]],
        'subject_code': splitted[0],
        'year':splitted[-1], 
        'paper':splitted[1], 
        'season':s_info['Season'][splitted[2]+splitted[3]]
    }

def get_paper_link(info:dict) -> str:     
    return BASE_LINK.format(
        info['subject_name'] if len(info['subject_name'].split()) <= 1 else "%20-%20".join(info['subject_name'].split()), 
        info['subject_code'], 
        f"20{info['year']}", 
        info['subject_code'], 
        f"{info['season']}{info['year']}", 
        info['paper']
    )
    
    
def open_url(link:str) -> None:
    webbrowser.open(link)
    
while True:
    parse_object = input("\n Enter the subject code -> ")
    if parse_object == 'q':
        break
    open_url(get_paper_link(get_link_info(parse_object)))
