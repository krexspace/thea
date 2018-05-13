'''
JUPYTER HTML RENDERER
'''
from IPython.core.display import display, HTML

def render(html):
    display(HTML(html))

def img(node):
    src = node.dat['src']
    title = node.dat['title']
    html = '<h1> {0} </h1><img src="{1}">'.format(title, src)
    render(html)

def txt(node):
    body = node.dat['body']
    title = node.dat['title']
    html = '<h1> {0} </h1><p>{1}</p>'.format(title, body)
    render(html)
    
def lnk(node):
    title = node.dat['title']
    url = node.dat['url']
    html = '<p><a href="{1}">{0}</p>'.format(title, url)
    render(html)