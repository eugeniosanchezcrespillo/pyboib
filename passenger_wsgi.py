import os
import sys
import requests
from bs4 import BeautifulSoup
import re

#Check url function
def check_url(link):
    #links
    base = "https://www.caib.es"
    autoritats = "/seccio-ii-autoritats-i-personal/473"

    #regular expression
    match = r'(.*)(?:conv|orsa|orsí)(.*)'
    match_compiled = re.compile(match)

    #Source code sub page
    req = requests.get(base+link+autoritats)
    source = req.text
    soup = BeautifulSoup(source, "html.parser")

    #getting info
    ulse = soup.find_all('ul', attrs={'class':'entitats'})
    titulo = soup.find('title')
    result = ''

    for ule in ulse:

        for div in ule.find_all('div', attrs={'class':'caja'}):
            subtitulo = div.find('h3')

            for ulr in div.find_all('ul', attrs={'class':'resolucions'}):
                enlacehtml = ulr.find('a', attrs={'class':'html'})
                enlacepdf = ulr.find('a', attrs={'class':'pdf'})

                for p in ulr.find_all('p'):
                    text = p.text.strip()
                    matching = match_compiled.fullmatch(text)

                    if matching:
                        title    = '<a href='+base+link+autoritats+' target="_blank">'+titulo.text+'</a><br />'
                        subtitle = '<strong>'+subtitulo.text+'</strong><br />'
                        html     = '<a href='+base+enlacehtml.get('href')+' target="_blank">Versio HTML</a><br />'
                        pdf      = '<a href='+base+enlacepdf.get('href')+' target="_blank">Versio PDF</a><br />'
                        content  = str(p)+'<br /><br />'

                        result += title+subtitle+html+pdf+content

    return result
    
#Source code main page
url = "https://www.caib.es/eboibfront/ca"
req = requests.get(url)
source = req.text
soup = BeautifulSoup(source, "html.parser")

#Getting resultat
resultat=''
boibs = soup.find_all('div', attrs={'class': 'boib'})
for boib in boibs:
    for a in boib.find_all('a'):
        link = a.get('href')
        resultat += check_url(link)+""

resultat += '</body></html>'

sys.path.insert(0, os.path.dirname(__file__))

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    message = '<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body>BOIB reader!<br />'
    response = '<br />'.join([message, resultat])
    return [response.encode()]
