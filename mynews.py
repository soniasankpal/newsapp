#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This is a News App module.
   This extracts the useful content from domain web page
   and stores to local for end user reading.
"""

from bs4 import BeautifulSoup
import requests

__author__ = "Sonia Sankpal"
__copyright__ = "Copyright (C) 2020 Sonia Sankpal"
__credits__ = ["Sonia Sankpal"]
__license__ = "Public Domain"
__version__ = "1.0"
__maintainer__ = "Sonia Sankpal"
__email__ = "soniasankpal@gmail.com"
__status__ = "Production"

def _get_html(url):
    
    status = 0
    html = ""
    header_text = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) ' \
        'AppleWebKit/537.36 (KHTML, like Gecko) ' \
        'Chrome/53.0.2785.143 Safari/537.36'
    headers = {'user-agent': header_text}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        status = response.status_code
        html = response.text
        
    except Exception as e:
        print(e)
    
    return status,html

def _get_a_tags(url, html):
    
    a_list = []
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.find_all('a', href=True):
        if a['href'].startswith(url):
            a_list.append(a['href'])
    
    return a_list

def _collect_articles_and_store(urls):

    result_data = []
    counter = 1
    
    for url in urls:

        status,html = _get_html(url)
        if status != 200:
            print(f"Status : {str(status)}")
            continue
        
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find_all("h1", {"class" : "title"})
        
        if len(results) > 0:
        
            heading = results[0].get_text()
            _html = ""
            
            att = {'class' : 'article', 'role' : 'main'}
            article_results = soup.findAll("div", att)
            if len(article_results) > 0:
                _html = article_results[0]
            
            file_path = r'D:\work\newsapp\today_articles\news' + str(counter) + '.html'
            file1 = open(file_path, 'w', encoding='utf-8')
            file1.write(str(_html))
            file1.close()
            
            result_data.append((heading, file_path))
        
        counter += 1
    
    return result_data

def _generate_user_file(results):

    file_path = r'D:\work\newsapp\mynews.html'
    file1 = open(file_path, 'w')
    file1.write("<html><body>")
    
    for header,html_path in results:
        s = f'<br><a href="file:///{html_path}">{header}</a><br>'
        file1.write(s)
    
    file1.write("</html></body>")
    file1.close()

def main():
    
    url_list = ['https://www.thehindu.com/']
    url = url_list[0]

    status,html = _get_html(url)
    if status != 200:
        print(f"Status : {str(status)}")
        return
    
    links = _get_a_tags(url, html)
    results = _collect_articles_and_store(links)
    _generate_user_file(results)

if __name__=="__main__":
    main()

