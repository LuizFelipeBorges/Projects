import requests as rq
import bs4 as bs4


def download_search_page(key, value, page):
    url = "https://www.shopcar.com.br/busca.php?tipo=1&marca={}&string={}&ordenar=valor_desc&pagina={}" 
    urll = url.format(key, value, page)
    response = rq.get(urll)

    return response.text


def download_ad_page(link):
    response = rq.get(link)

    return response.text


def parse_search_page(page_html):
    parsed = bs4.BeautifulSoup(page_html, features="html.parser")
            
    tags = parsed.findAll("a", "link")

    ad_list = []

    for e in tags:
        link = e['href']
        modelo = link.split("/")[-3]

        data = {"link": link, "modelo": modelo}
        ad_list.append(data)
    return ad_list

def parse_ad_page(page_html):
    parsed = bs4.BeautifulSoup(page_html, features="html.parser")

    especs = parsed.find("ul", "especs")
    
    especs1 = especs.span.extract()
    especs2 = especs.span.extract()
    especs2 = especs.span.extract()

    ano = especs1.get_text()
    km = especs2.get_text()

    preco = parsed.find("div", "barra-preco")
    for string in preco.stripped_strings:
      valor = string
    
    taged_modelo = parsed.find("span", "modelo")
    for s in taged_modelo.stripped_strings:
      modelo = s

    data = {"ano": ano, "valor": valor, "km": km, "form_modelo": modelo}
          
    return data
