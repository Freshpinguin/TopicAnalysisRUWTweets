# Expose

1. Introduction
2. Objective
3. State of Research
3. 1. NLP on Russian-Ukraine War
3. 2. Multilingual Topic Modelling
4. Starting Point
5. Methodology
6. Schedule




## 1. Introduction
Der Ukraine Krieg ist die wichtigste Außenpolitische Herausforderung Deutschlands und Europas [Olaf Scholz Zeitenwende]. Die Rolle der sozialen Medien im Ukraine Krieg ist enorm. Einerseits als Mittel politischen Einfluss auszuüben, andererseits als potentielle Quelle militärisch relevanter Informationen. [KAS die sozialen Medien...]. Twitter hat hier eine besondere Bedeutung mit über 350 Millionen Nutzern in 2022 und und 2023 [Statista] und großer Bedeutung bei anderen politischen Ereignissen. [twitter brexiit, pandemic]

## 2. Objective
Frage:

Sind moderne Techniken des multilingualen Topic Modellings geeignet, um aus großen mehrsprachigen Twitter Datensätzen Erkenntnisse zu gewinnen.

Hierfür wird ein großer mehrsprachiger Twitter Datensatz von Kaggle [Link siehe Notebook] analysiert und aufbereitet.
Hierfür muss ein Überblick über die aktuellen Entwicklungen des (multilingualen) Topic Modellings gegeben werden.
Geeignete Techniken des multilingualen Topic Modellings werden dann auf diesem Datensatz angewandt und die Ergebnisse bewertet.

## 3.1 NLP on RUssian-Ukraine War
Zusammenfassung der gelesenen Paper in RUWNLP:

6 and 9 doing Topic Analysis and Sentiment Analysis (not multilingual only first 6 months telegramm data) (Non Negative Matrix factorisation with kullback-leibler divergence )  < 50000
10 (BertTopic, LDA twitter ) ~80000
11 LDA (news websites) < 1200 News articles
2 LDA (twitter) <40000

=> Mein Wissenstand: Keine Multilinguales Topic Modelling über den Ukraine Krieg. Kein Topic Modelling auf so großen Datensätzen bis jetzt.

## 3.2 
Zusammenfassung der Paper über BertTopic, LDA, SentenceBert, Labse usw.

## 4. Starting Point
Beschreibung über den Datensatz.

## 5. Methodology
Google Translate API
Fallstudie: 100 Selbstklassifizierte Tweets zum Vergleich von meinen Topics, LDA, BertTopic (Roberta), Labse
Fallstudie: Vergleich LDA, BertTopic, Labse auf übersetzten Tweets
Auswahl des geeignetesten Verfahren auf allen Daten.

## 6. Schedule

Fallstudie 1 und Fallstudie 2 abgeschlossen und aufbereitet bis mitte Februar -> BachelorVortrag
Topic Modelling und Darstellung der Topics und Erkenntnisse auf allen Daten -> Mitte Märze
Abgabe der Bachelorarbeit -> Ende März