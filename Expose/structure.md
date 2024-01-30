# Expose

1. Introduction
2. Objective
3. State of Research
4. Technology
5. Data Set
6. Methodology





## 1. Introduction
Der Ukraine Krieg ist die wichtigste Außenpolitische Herausforderung Deutschlands und Europas [Olaf Scholz Zeitenwende]. Die Rolle der sozialen Medien im Ukraine Krieg ist enorm. Einerseits als Mittel politischen Einfluss auszuüben, andererseits als potentielle Quelle militärisch relevanter Informationen. [KAS die sozialen Medien...]. Twitter hat hier eine besondere Bedeutung mit über 350 Millionen Nutzern in 2022 und und 2023 [Statista] und großer Bedeutung bei anderen politischen Ereignissen. [twitter brexiit, pandemic]

https://chat.openai.com/share/1fe6e7af-7b16-4dda-ae14-adbf41e77087
## 2. Objective
Frage:

Sind moderne Techniken des multilingualen Topic Modellings geeignet, um aus großen mehrsprachigen Twitter Datensätzen Erkenntnisse zu gewinnen.

Hierfür wird ein großer mehrsprachiger Twitter Datensatz von Kaggle [Link siehe Notebook] analysiert und aufbereitet.
Hierfür muss ein Überblick über die aktuellen Entwicklungen des (multilingualen) Topic Modellings gegeben werden.
Geeignete Techniken des multilingualen Topic Modellings werden dann auf diesem Datensatz angewandt und die Ergebnisse bewertet.

https://chat.openai.com/share/c12195fd-59fe-43b6-8516-9d564487f0e8

## 3 State of Research
Zusammenfassung der gelesenen Paper in RUWNLP:

6 and 9 doing Topic Analysis and Sentiment Analysis (lda, telegramm data) (Non Negative Matrix factorisation with kullback-leibler divergence )  < 50000      (Maathuis, Karkhof, TopicModellingTelegram1, TopicModellingTelegram2)


10 (BertTopic, LDA twitter ) ~80000   (Sazzed, TopicTwitterLDABERt)


11 LDA (news websites) < 1200 News articles  (Nayak, JVN, Bhagat TopicModelingconflig, )
2 LDA (twitter) <40000  (Sufi, SocialMediaanalysis)
Ivanka (twitter) selber Datensatz (lda) (Ivanna)

=> Mein Wissenstand: Keine Multilinguales Topic Modelling über den Ukraine Krieg. Kein Topic Modelling auf so großen Datensätzen bis jetzt.

https://chat.openai.com/share/b2b43b8b-2be0-4f83-b337-26f3407d4ec7

## 4 Technology
Zusammenfassung der Paper über BertTopic, LDA, SentenceBert, Labse usw.

LDA 1   (LDA)
BerTopic (=> HDBSCAN, UMAP )
Labse
BertSentenceEmbeddings
RoberTa
Bert

Evaluation:
PCA for visualisation
Wordclouds, Top N Words....


Coherence: NPMI
Diversity: [10] Topocmodellingembedd....

https://chat.openai.com/share/e5b049da-2ae8-4dc4-b8cf-7d9d5e3a66ea
## 4. Data Set

The dataset was downloaded from the online platform [Kaggle](https://www.kaggle.com/). Kaggle is an online community for data science and machine learning (ML) enthusiasts. It is a top learning tool for novices and pros, with realistic practice problems to sharpen your data science skills.

Owned by Google, it is currently the world’s largest crowdsourced web platform for data scientists and ML practitioners. Thus, Kaggle gives you access to several professionals in your field that you can brainstorm, compete, and solve real-life problems with. [[ "A Beginner's Guide to Kaggle for Data Science"](https://www.makeuseof.com/beginners-guide-to-kaggle/). MUO. 2023-04-17. Retrieved 2023-06-10.]

The dataset can be downloaded for free and with no restrictions here: [Link to Website](https://www.kaggle.com/datasets/bwandowando/ukraine-russian-crisis-twitter-dataset-1-2-m-rows/data).
The dataset was published on Kaggle by User [BwandoWando](https://www.kaggle.com/bwandowando). 



Dataset Preparation [Albrechts Buch] and short oversight over steps.
Deduplication using Min-Hash [Dedup Papers]
Translating using Google Translate API

https://chat.openai.com/share/7e821f1d-1dd6-485b-91d8-b37f2f4060e6

## 5. Methodology

Fallstudie: 100 Selbstklassifizierte Tweets zum Vergleich von meinen Topics, LDA, BertTopic (Roberta), Labse   
Fallstudie: Vergleich LDA, BertTopic, Labse auf übersetzten Tweets
Auswahl des geeignetesten Verfahren auf allen Daten.

Evaluation:

https://chat.openai.com/share/c3d59f6c-32b5-4220-a80e-f143ca8d1f2c

## 6. Schedule

Fallstudie 1 und Fallstudie 2 abgeschlossen und aufbereitet bis mitte Februar -> BachelorVortrag
Topic Modelling und Darstellung der Topics und Erkenntnisse auf allen Daten -> Mitte Märze
Abgabe der Bachelorarbeit -> Ende März