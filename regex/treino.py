import re

print("RegEx - básico\n")  # explicação comentada
string1 = "frase que será analisada pelo regex porque regex é legal e útil"

print(re.match('frase\n', string1))  # na qual se inicia

print(re.search('regex', string1))  # busca da palavra na frase

print(re.findall('que', string1))  # busca por toda a frase

for i in re.finditer('regex', string1):
    print(i)  # retorna um iterador a cada vez que se encontra por durante a frase

print(re.sub('analisada', 'avaliada', string1))  # substituição

print("RegEx - Padrões\n")  # explicação comentada

lista1 = ['www.google.com', 'https://www.google.com', 'google.com.br']

for string in lista1:
    print(re.search("^www", string))  # negação ou início da expressão

for string in lista1:
    print(re.search("com$", string))  # marca o final da string

lista2 = ['naiara', 'naiaraaaaaa', 'naaaaaaiara', 'naiar', 'naiars']

for string in lista2:
    print(re.search("naiar.", string))