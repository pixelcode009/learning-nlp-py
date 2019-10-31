

from collections import Counter
from nltk.probability import FreqDist
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy as np

from conftest import TOKEN_SETS, DOCUMENTS

DOCS1 = [
    "did not like that movie", "not a good movie", "popcorn smells good",
    "i like it", "lots of action", "very funny"
]

DOCS2 = ["good movie", "not a good movie", "did not like", "i like it", "good one"]

def test_counter():
    counter = Counter()
    for tokens in TOKEN_SETS:
        counter.update(tokens) # pass a list of words to group by word, pass a word to group by char
    assert counter.most_common(3) == [('all', 3), ('the', 2), ('kings', 2)]

def test_nltk_frequency_dist():
    TOKENS = np.concatenate(TOKEN_SETS)
    dist = FreqDist(TOKENS)
    assert dist.most_common(3) == [('all', 3), ('the', 2), ('kings', 2)]

def test_count_vectorizer():
    cv = CountVectorizer()
    matrix = cv.fit_transform(DOCUMENTS) #> <class 'scipy.sparse.csr.csr_matrix'>
    expected_vals = np.array([
        [1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0], # "all the kings men"
        [1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0], # "ate all the kings hens"
        [1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1]  # "until they all got tired and went to sleep zzz"
    ])
    assert np.array_equal(matrix.toarray(), expected_vals)
    assert np.array_equal(matrix.todense(), expected_vals)
    features = cv.get_feature_names()
    assert features == ['all', 'and', 'ate', 'got', 'hens', 'kings', 'men', 'sleep', 'the', 'they', 'tired', 'to', 'until', 'went', 'zzz']

    cv = CountVectorizer()
    matrix = cv.fit_transform(DOCS1) #> <class 'scipy.sparse.csr.csr_matrix'>
    expected_vals = np.array([
        [0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0], # "did not like that movie"
        [0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0], # "not a good movie"
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0], # "popcorn smells good"
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], # "i like it"
        [1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0], # "lots of action"
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]  # "very funny"
    ])
    assert np.array_equal(matrix.toarray(), expected_vals)
    assert np.array_equal(matrix.todense(), expected_vals)
    assert cv.get_feature_names() == ['action', 'did', 'funny', 'good', 'it', 'like', 'lots', 'movie', 'not', 'of', 'popcorn', 'smells', 'that', 'very']

    cv = CountVectorizer()
    matrix = cv.fit_transform(DOCS2) #> <class 'scipy.sparse.csr.csr_matrix'>
    expected_vals = np.array([
        [0, 1, 0, 0, 1, 0, 0], # "good movie"
        [0, 1, 0, 0, 1, 1, 0], # "not a good movie"
        [1, 0, 0, 1, 0, 1, 0], # "did not like"
        [0, 0, 1, 1, 0, 0, 0], # "i like it"
        [0, 1, 0, 0, 0, 0, 1]  # "good one"
    ])
    assert np.array_equal(matrix.toarray(), expected_vals)
    assert np.array_equal(matrix.todense(), expected_vals)
    assert cv.get_feature_names() == ['did', 'good', 'it', 'like', 'movie', 'not', 'one']

def test_count_vectorizer_vocab():
    vocab = ['hens', 'kings', 'men', 'sleep']
    cv = CountVectorizer(vocabulary=vocab) # pass vocab to specify desired features
    matrix = cv.fit_transform(DOCUMENTS) #> <class 'scipy.sparse.csr.csr_matrix'>
    expected_vals = np.array([
        [0, 1, 1, 0], # "all the kings men"
        [1, 1, 0, 0], # "ate all the kings hens"
        [0, 0, 0, 1]  # "until they all got tired and went to sleep zzz"
    ])
    assert np.array_equal(matrix.toarray(), expected_vals)
    assert np.array_equal(matrix.todense(), expected_vals)
    assert cv.get_feature_names() == vocab

def test_count_vectorizer_stopwords():
    cv = CountVectorizer(stop_words="english")
    matrix = cv.fit_transform(DOCUMENTS)
    expected_features = ['ate', 'got', 'hens', 'kings', 'men', 'sleep', 'tired', 'went', 'zzz']
    expected_vals = np.array([
        [0, 0, 0, 1, 1, 0, 0, 0, 0], # "all the kings men"
        [1, 0, 1, 1, 0, 0, 0, 0, 0], # "ate all the kings hens"
        [0, 1, 0, 0, 0, 1, 1, 1, 1] # "until they all got tired and went to sleep zzz"
    ])
    assert np.array_equal(matrix.toarray(), expected_vals)
    assert cv.get_feature_names() == expected_features

def test_count_vectorizer_ngrams():
    cv = CountVectorizer(ngram_range=(1,2))
    matrix = cv.fit_transform(DOCUMENTS)
    expected_features = ['all', 'all got', 'all the', 'and', 'and went', 'ate', 'ate all', 'got', 'got tired', 'hens', 'kings', 'kings hens', 'kings men', 'men', 'sleep', 'sleep zzz', 'the', 'the kings', 'they', 'they all', 'tired', 'tired and', 'to', 'to sleep', 'until', 'until they', 'went', 'went to', 'zzz']
    expected_vals = np.array([
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # "all the kings men"
        [1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # "ate all the kings hens"
        [1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # "until they all got tired and went to sleep zzz"
    ])
    assert np.array_equal(matrix.toarray(), expected_vals)
    assert np.array_equal(matrix.todense(), expected_vals)
    assert cv.get_feature_names() == expected_features

def test_count_vectorizer_custom(nlp):
    #def my_preprocessor(text):
    #    return text.upper() # LOOKS LIKE THIS GETS RE-CONVERTED LATER TO LOWERCASE (BUT YOU COULD DO MORE COMPLICATED PROCESSING HERE, LIKE REMOVING CERTAIN SPECIAL CHARS)

    def my_tokenizer(text):
        doc = nlp(text) #> <class 'spacy.tokens.doc.Doc'>
        tokens = [token.lemma_.lower() for token in doc if token.is_stop == False and token.is_punct == False and token.is_space == False]
        return tokens

    #cv = CountVectorizer(preprocessor=my_preprocessor, tokenizer=my_tokenizer, ngram_range=(1,2), stop_words='english')
    cv = CountVectorizer(tokenizer=my_tokenizer, ngram_range=(1,2), stop_words='english')
    matrix = cv.fit_transform(DOCUMENTS)
    expected_features = ['eat', 'eat king', 'hen', 'king', 'king hen', 'king man', 'man', 'sleep', 'sleep zzz', 'tired', 'tired sleep', 'zzz']
    expected_vals = np.array([
        [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0], # "all the kings men"
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0], # "ate all the kings hens"
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]  # "until they all got tired and went to sleep zzz"
    ])
    assert np.array_equal(matrix.toarray(), expected_vals)
    assert np.array_equal(matrix.todense(), expected_vals)
    assert cv.get_feature_names() == expected_features

def test_tfidf_vectorizer():
    tv = TfidfVectorizer()
    matrix = tv.fit_transform(DOCUMENTS)
    expected_features = ['all', 'and', 'ate', 'got', 'hens', 'kings', 'men', 'sleep', 'the', 'they', 'tired', 'to', 'until', 'went', 'zzz']
    assert tv.get_feature_names() == expected_features
    #expected_vals = np.array([
    #    [0.37311881, 0.        , 0.        , 0.        , 0.        , 0.4804584 , 0.63174505, 0.        , 0.4804584 , 0.        ,0.        , 0.        , 0.        , 0.        , 0.        ],
    #    [0.31544415, 0.        , 0.53409337, 0.        , 0.53409337, 0.40619178, 0.        , 0.        , 0.40619178, 0.        , 0.        , 0.        , 0.        , 0.        , 0.        ],
    #    [0.19316423, 0.32705548, 0.        , 0.32705548, 0.        , 0.        , 0.        , 0.32705548, 0.        , 0.32705548, 0.32705548, 0.32705548, 0.32705548, 0.32705548, 0.32705548]
    #]) # assertions messing up due to float datatypes
    converted_vals = [
        [round(float(val), 4) for val in matrix.toarray()[0]],
        [round(float(val), 4) for val in matrix.toarray()[1]],
        [round(float(val), 4) for val in matrix.toarray()[2]],
    ] # clean up dataset to facilitate assertions
    expected_vals = [
        [0.3731, 0.0,   0.0,    0.0,    0.0,    0.4805, 0.6317, 0.0,    0.4805, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.3154, 0.0,   0.5341, 0.0,    0.5341, 0.4062, 0.0,    0.0,    0.4062, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.1932, 0.3271, 0.0,   0.3271, 0.0,    0.0,    0.0,    0.3271, 0.0,    0.3271, 0.3271, 0.3271, 0.3271, 0.3271, 0.3271]
    ]
    assert np.array_equal(converted_vals, expected_vals)
    assert(matrix.toarray().shape) == (3, 15)
    #dense_vals = [
    #    [round(float(val), 4) for val in matrix.todense()[0]],
    #    [round(float(val), 4) for val in matrix.todense()[1]],
    #    [round(float(val), 4) for val in matrix.todense()[2]],
    #] # clean up dataset to facilitate assertions
    #> TypeError: only size-1 arrays can be converted to Python scalars
    #assert np.array_equal(dense_vals, expected_vals)
    assert(matrix.todense().shape) == (3, 15)

def test_tfidf_vectorizer_custom():
    tfidf = TfidfVectorizer(min_df=2, max_df=0.5, ngram_range=(1,2))

    features = tfidf.fit_transform(DOCS1) #> <6x4 sparse matrix of type '<class 'numpy.float64'>'
    assert tfidf.get_feature_names() == ['good', 'like', 'movie', 'not']
    assert features.todense().shape == (6,4) #> ( len(DOCUMENTS), len(feature_names)  )
    #>matrix(
    #>   [[0.        , 0.57735027, 0.57735027, 0.57735027],
    #>    [0.57735027, 0.        , 0.57735027, 0.57735027],
    #>    [1.        , 0.        , 0.        , 0.        ],
    #>    [0.        , 1.        , 0.        , 0.        ],
    #>    [0.        , 0.        , 0.        , 0.        ],
    #>    [0.        , 0.        , 0.        , 0.        ]])

    features = tfidf.fit_transform(DOCS2)
    assert tfidf.get_feature_names() == ['good movie', 'like', 'movie', 'not']
    assert features.todense().shape == (5,4)
    #>matrix(
    #>    [[0.70710678, 0.        , 0.70710678, 0.        ],
    #>    [0.57735027, 0.        , 0.57735027, 0.57735027],
    #>    [0.        , 0.70710678, 0.        , 0.70710678],
    #>    [0.        , 1.        , 0.        , 0.        ],
    #>    [0.        , 0.        , 0.        , 0.        ]])
