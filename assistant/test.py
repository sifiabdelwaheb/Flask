import spacy
spacy_nlp = spacy.load('en_core_web_sm')

article1='Cette semaine, Express Orient vous emmène en Turquie, dans la plus grande ville du pays, Istanbul, \
qui concentre 60% des cas de coronavirus. La Turquie, première puissance économique du Moyen-Orient, \
est passée devant l’Iran en nombre de patients officiellement détectés. \
PUBLICITÉ Ces derniers jours, la Turquie a dépassé son voisin iranien en nombre de cas confirmés dinfections au Covid-19,\
a annoncé samedi 18 avril 2020 le ministre turc de la Santé. Désormais, le pays enregistre 2 140 décès et près de 91 000 personnes sont infectées par le coronavirus.\
Même si beaucoup doutent de la fiabilité des chiffres officiels, les autorités d Ankara restent confiantes. \
Nos correspondants à Istanbul, Shona Bhattacharyya et Ludovic De Foucaud, ont rencontré la présidente de la chambre médicale d’Istanbul qui leur explique pourquoi.\
En Israël, religion et lutte contre la pandémie de Covid-19 ne font pas toujours bon ménage... Nos correspondants au Proche-Orient, Cécile Galluccio et Antoine Mariotti, se sont rendus dans les quartiers juifs ultra-orthodoxes de Jérusalem, où vit une communauté qui est à la fois la plus touchée par le coronavirus et celle qui rejette la plupart des consignes sanitaires. '
for article in [article1]:
    print('Original Article: %s' % (article))
    print()
    doc = spacy_nlp(article)
    for i, token in enumerate(doc.sents):
        print('-->Sentence %d: %s' % (i, token.text))