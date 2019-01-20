# https://estnltk.github.io/estnltk/1.4.1/tutorials/installation.html
import estnltk
from estnltk import Text

text = Text('Tere maailm!')
text = Text('Kõrred, millel on toitunud viljasääse vastsed, jäävad õhukeseks.')
text2 = Text('Usjas kaslane ründas künklikul maastikul raudteejaamadeski puhkavat tünjat Tallinnfilmi režissööri')
text3 = Text('Kass ja hiir ei söönud juustu ega ka võileiba.')
text4 = Text('Esimesed nelikümmend mitte-täidlast öötöölist jõudsid koju.')
text5 = Text('Pane või saia peale! lambahakklihast pelmeen')
text6 = Text('Oled see mina, mis ei saa kunagi aega?')

s=text6.analysis
for i in s:
	print(len(i), i[0]['lemma'])
# print(s)
import pprint
pprint.pprint(s)

"""
    A - adjective
    C - comparative adjective
    D - adverb
    G - non declinable adjective
    H - real name
    I - interjection
    J - conjunction  		<- Tuleks eemaldada statistikast.
    K - co-expression
    N - cardinal numeral
    O - ordinal numeral
    P - pronoun
    S - noun
    U - superlative adjective
    V - verb
    X - other type of word belonging together with a verb
    Y - abbreviation
    Z - sign
"""
