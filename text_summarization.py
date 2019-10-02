import bs4 as bs
import urllib.request
import re
import nltk
nltk.download('stopwords')

#load text from url
scraped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Artificial_intelligence')
article = scraped_data.read()

parsed_article = bs.BeautifulSoup(article, 'lxml')
#the above parsed article will contain the inspect page content

paragraphs = parsed_article.find_all('p')
#the above contains only contents that lie within <p>

article_text = ""

for p in paragraphs:
    article_text += p.text

#preprocessing
article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
article_text = re.sub(r'\s+', ' ', article_text)
formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
formatted_article_text = re.sub('\s+', ' ', formatted_article_text)


stopwords = nltk.corpus.stopwords.words('english')
tokens = nltk.word_tokenize(formatted_article_text)
word_frequencies = {}

#calculating  frequency of all words which are not stopwords
for word in tokens:
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word]=1
        else:
            word_frequencies[word] += 1


maximum_frequnecy = max(word_frequencies.values())

#weighted frequency of each word
for word in word_frequencies.keys():
    word_frequencies[word]= (word_frequencies[word]/maximum_frequnecy)


#calculating score of each sentence
#tokenizing original para to snetences
sentence_list = nltk.sent_tokenize(article_text)
sentence_scores = {}

for sent in sentence_list:
    #tokenizing each sentence
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if sent not in sentence_scores.keys():
                sentence_scores[sent]= word_frequencies[word]
            else:
                sentence_scores[sent] += word_frequencies[word]

#sort in descending order of their weighted frequency
#display first 3 sentences as summary
import heapq
summary_sentences = heapq.nlargest(3, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)
print(summary)