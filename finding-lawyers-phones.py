import os

from googlesearch.googlesearch import GoogleSearch

os.system('clear')

response = GoogleSearch().search('"JOAO JOSE MACHADO DE CARVALHO"')
for result in response.results:
    print("Title: " + result.title)
    # print("Title: " + result.url)
    # print("Content: " + str(result.getText()))
