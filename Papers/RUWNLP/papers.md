# Zusammenfassung von Papern

### [0] A dataset of Open Source Intelligence Tweets about the Russo-Ukrainian war

Description of a dataset of tweets from OSINT related users.

### [1]: TweEvent: A dataset if Twitter messages about events in the Ukraine conflict

Propsing an algorithm to identify location information in tweets to match them with ACLED (Armed Conflict Location Event Data) to add additionale information to ACLED dataset.

### [2]: Social Media Analysis on Russian-Ukraine Cyber War with NLP perspectives and challenges

Social media based cyber intelligence.
Translation via Microsoft Cognitive Services Text Analysis Api
Example for LDA with preprocessing pipeline.
Topic generated for russian ukraine for cyber related issues.
Example for performance metrics for LDA and topic keyword discussion.
BUT: completly exaggerate the importance of their proposed framework.

### [3]: Public Opinion Dynamics in Cyberspace on Russia-Urkaine-War: A case anaylsis with chinese Weibo

Point out importance of Russia Ukraine war cyber space social system. Use LDA combined with sentiment analysis. Analyse evolution of topics over time.
Minus: Only data from 1 Month, 100 000 tweets.
Related work: [15][17][18][21] 
Dimensional reduction with "T-Distributed stochastic neighbor embedding".

### [4]: An Unsupervised Graph-Based Approach for Detecting Relevant Topics: A Case Stuy on the Italian Twitter Cohort during the Russia-Ukraine Conflict

Italian social context study in the first month of the war ~2.4 mio tweets.
Literature to prove that twitter can be used to track real-world events.
Example of preprocessing pipelin.
Alternative way of finding topics via "nutrition" of a word to calclualte its importance and then link important words via coocurrence Graph.

### [5]: Content still matters. A machine learning model for predicting news longevity from textual and context feature.

Study of how sentiment polarisation, emotional compostion, topics and similiarity to main articels affects an articles lifespan.
Interseting methology, not so fitting otherwise.
Emotion detection:
Acheampong, Nonoo-Mensah and Chen (2021)
Nandwani and Verma (2021)
Murthy and Kuma (2021)
XLM-R: Conneau et al. (2019)

Multilanguage tokeniation:
Google's LaBSE model: Feng, Yang, Cer, Arivazhangang, Wang (2022)

K-Flexibles LDA:
Charemza, MMakarova, Rybinski (2022)

### [6]: The first two Months in the War in Ukraine through Topic Modelling and Sentiment Analysis.

Building a technical solution for capturing topics and sentiments discussed by ukrainian speaking telegram users ~10.000 Messages from first two months of the war.
Number of topics modelled:
9 per day or 100 over whole two months.

Twitter Crimmea Annexion related works:
Brodovskaya et al. (2019)
Chen and Ferrara (2022)
Saluscher (2014)

Other twitter Datasets:
Pohl et al. (2022)
Che and Ferrara (2022)
Haq et al. (2022)
Shertsov et al. (2022)
Polyzos (2022)

Chinese and Russian analysis:
Hanley et al. (2022)

Non Negative Matrix factorisation with kullback-leibler divergence (NMF-KL):
Hien and Gillis (2021)

### [7]: Data-Driven Governance in Crises: Topic Modelling for the Identifaction of Refugee Needs

Topic Analysis of refugee telegram data and interviews of refugess, public sector workers and voluntary helpers. All data from swiss.

BertTopic, Metrics for Topics [14] 
Bert [11]

Emphasize problem of translation before topic modelling. Suggest usage of multilanguage approaches like BertTopic.

### [8]: Topic Modelling on News Articles using Latent Dirchlet Allocation

LDA pipeline example and metrics example.
LDA explained in a new kinda interesting but also confusing way.
LDA trained on 100MB Wiki dataset and tested on Reuthers news articles.
Literature about generall use of lda.

### [9]: First Six Months of War from Urkainian Topic and Sentiment Analysis

Like [6] but with more data and time.
9 Topics a day or 300 over 6 Months.

### [10]: The Dynamics of Ukraine-Russian Conflict through the Lens of Demographically diverse Twitter Data

Salim Sazzed, Old Dominion University , Norfolg USA, 2022 IEEE International Conference on Big Data

Literature back the importance of twitter
80000 tweets from 7 countries
Sentiment Analysis/Topic Modelling with BERTopic/Lda splittet geographicly

Sentiment Analysis:
VADER [28]

### [11]: Topic Modelling of ongoing Conflict betweet Russia and Ukraine

Pradhan Nayak, Lakshmi JVN, Vandana V. Bhagat, 2022, International Conference on Trends in Quantum Computing and Emerging Business Technologies 

LDA on news websites articles
1178 articles 1.12.21 - 16.5.22

Good sentences on why to use topic modelling lda, good methodology

LDA - Mallet - Gibbons sampling approach?
Exploratory Data Analysis
Data Preprocessing Pipeline
Perplexity Score
Coherence Scroe
PyLDAvis to visualise