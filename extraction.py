import urllib.request as libreq
import xml.etree.ElementTree as ET

def grep_articles(keyword, max_articles):
    """
    Effectue une recherche d'articles sur arxviv suivant le mot-clé et le nombre max d'articles passés en paramètre.
    :param keyword: Le mot clés de la recherche
    :param max_articles: Le nombre d'articles que vous souhaitez
    :return: une liste d'articles sous forme de dictionnaires contenant les informations des articles
    """
    with libreq.urlopen('http://export.arxiv.org/api/query?search_query=all:'+keyword+"&max_results="+str(max_articles)) as url:
        r = url.read()
    f = open("articles.xml", 'w')
    f.write(r.decode('utf-8'))
    f.close()
    return parse_articles()

def parse_articles():
    """
    Parcours le fichier xml contenant les articles recherchés pour en extraire une liste.
    :return: une liste d'articles sous forme de dictionnaires contenant les informations des articles
    """
    articles = []
    tree = ET.parse('articles.xml')
    racine = tree.getroot()
    #
    for article in racine.findall('{http://www.w3.org/2005/Atom}entry'):
        articles.append({
            "id": article.find('{http://www.w3.org/2005/Atom}id').text,
            "published": article.find('{http://www.w3.org/2005/Atom}published').text,
            "title": article.find('{http://www.w3.org/2005/Atom}title').text,
            "summary": article.find('{http://www.w3.org/2005/Atom}summary').text,
            "author": [],
        })
        # Ajoute les différents auteurs de l'article au dictionnaire associé
        for auteur in article.findall('{http://www.w3.org/2005/Atom}author'):
            articles[len(articles)-1]["author"].append(auteur.find('{http://www.w3.org/2005/Atom}name').text)
       # Ajoute le lien du pdf de l'article
        for link in article.findall('{http://www.w3.org/2005/Atom}link'):
            if link.get('title') == "pdf":
                articles[len(articles)-1]["pdf"] = link.get('href')
            if link.get('title') == "doi":
                articles[len(articles)-1]["doi"] = link.get('href')
    return articles

liste = grep_articles("6g", 100)
print(len(liste))
print(liste)
