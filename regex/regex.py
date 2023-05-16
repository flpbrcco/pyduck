import re

string1 = "Timóteo"

print(re.match('frase\n', string1))

re.sub(["à","á","ã","â"], "a", string1)