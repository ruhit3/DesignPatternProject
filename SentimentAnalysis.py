import nltk
import sklearn
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

def getSentiment(user_review):
    movie_train = load_files(r'C:\Users\uce\Desktop\DesignPatternProject\movie_reviews', shuffle=True)
    movie_vec = CountVectorizer(min_df=2, tokenizer=nltk.word_tokenize)
    movie_counts = movie_vec.fit_transform(movie_train.data)
    tfidf_transformer = TfidfTransformer()
    movie_tfidf = tfidf_transformer.fit_transform(movie_counts)
    docs_train, docs_test, y_train, y_test = train_test_split(movie_tfidf, movie_train.target, test_size = 0.2, random_state = 12)
    clf = MultinomialNB().fit(docs_train, y_train)
    reviews_new = [user_review]
    reviews_new_counts = movie_vec.transform(reviews_new)
    reviews_new_tfidf = tfidf_transformer.transform(reviews_new_counts)
    pred = clf.predict(reviews_new_tfidf)
    for review, category in zip(reviews_new, pred):
        result = movie_train.target_names[category]
    if result == 'positive':
        return 1
    elif result == 'negative':
        return 0
    else:
        return -1

print(getSentiment('hate this movie too much'))