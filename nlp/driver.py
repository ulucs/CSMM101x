import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
import os

train_path = "aclImdb/train/"  # use terminal to ls files under this directory
test_path = "imdb_te.csv"  # test data for grade evaluation


def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
    sentences = []
    for filename in os.listdir(os.path.join(inpath, 'pos')):
        with open(os.path.join(inpath, 'pos', filename)) as fi:
            sentences.append([fi.read(), 1])
    for filename in os.listdir(os.path.join(inpath, 'neg')):
        with open(os.path.join(inpath, 'neg', filename)) as fi:
            sentences.append([fi.read(), 0])
    pd.DataFrame(sentences, columns=['text', 'polarity']).to_csv(os.path.join(outpath, name))


if __name__ == "__main__":
    imdb_data_preprocess(train_path)

    traind = pd.read_csv('imdb_tr.csv', index_col=0)
    testd = pd.read_csv(test_path, index_col=0, encoding='latin-1')
    # originalTestPolarity = testd['polarity']
    stopwords = pd.read_csv('stopwords.en.txt', header=None)[0].tolist()
    clf = SGDClassifier()

    uni_vectorizer = CountVectorizer(ngram_range=(1, 1), analyzer='word', stop_words=stopwords)
    bi_vectorizer = CountVectorizer(ngram_range=(1, 2), analyzer='word', stop_words=stopwords)
    uni_tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 1), analyzer='word', stop_words=stopwords)
    bi_tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2), analyzer='word', stop_words=stopwords)

    uni_matrix = uni_vectorizer.fit_transform(traind['text'])
    bi_matrix = bi_vectorizer.fit_transform(traind['text'])
    uni_tfidf_matrix = uni_tfidf_vectorizer.fit_transform(traind['text'])
    bi_tfidf_matrix = bi_tfidf_vectorizer.fit_transform(traind['text'])

    # for seeing purposes only
    # unigrams = pd.DataFrame(uni_matrix.toarray(), columns=uni_vectorizer.get_feature_names(), index=traind.index)
    # bigrams = pd.DataFrame(bi_matrix.toarray(), columns=bi_vectorizer.get_feature_names(), index=traind.index)

    clf.fit(uni_matrix, np.array(traind.polarity.tolist()))
    print "Unigram train score"
    print clf.score(uni_matrix, np.array(traind.polarity.tolist()))
    testX = uni_vectorizer.transform(testd['text'])
    pred = clf.predict(testX)
    print "Unigram test score"
    print clf.score(testX, testd.polarity)
    pd.DataFrame(pred).to_csv('unigram.output.txt', index=False, header=False)

    clf.fit(uni_tfidf_matrix, np.array(traind.polarity.tolist()))
    print "Unigram ifidf train score"
    print clf.score(uni_tfidf_matrix, np.array(traind.polarity.tolist()))
    testX = uni_tfidf_vectorizer.transform(testd['text'])
    pred = clf.predict(testX)
    print "Unigram ifidf test score"
    print clf.score(testX, testd.polarity)
    pd.DataFrame(pred).to_csv('unigramtfidf.output.txt', index=False, header=False)

    clf.fit(bi_matrix, np.array(traind.polarity.tolist()))
    print "Bigram train score"
    print clf.score(bi_matrix, np.array(traind.polarity.tolist()))
    testX = bi_vectorizer.transform(testd['text'])
    pred = clf.predict(testX)
    print "Bigram test score"
    print clf.score(testX, testd.polarity)
    pd.DataFrame(pred).to_csv('bigram.output.txt', index=False, header=False)

    clf.fit(bi_tfidf_matrix, np.array(traind.polarity.tolist()))
    print "Bigram tfidf train score"
    print clf.score(bi_tfidf_matrix, np.array(traind.polarity.tolist()))
    testX = bi_tfidf_vectorizer.transform(testd['text'])
    pred = clf.predict(testX)
    print "Bigram tfidf test score"
    print clf.score(testX, testd.polarity)
    pd.DataFrame(pred).to_csv('bigramtfidf.output.txt', index=False, header=False)
