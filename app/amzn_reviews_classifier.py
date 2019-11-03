import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

from app.tokenizer import REVIEWS_CSV_FILEPATH, tokenize, tokenize_v4, tokenize_v5

if __name__ == "__main__":

    print("--------------------------")
    print("PROCESSING AMAZON REVIEWS DATASET")
    print("--------------------------")

    print("READING CSV...")
    df = pd.read_csv(REVIEWS_CSV_FILEPATH)
    x = df["reviews.text"] # inputs
    y = df["reviews.rating"] # outputs
    #print("  + DOC LENGTHS:")
    #print(x.str.len().value_counts())
    #print("  + STAR-RATINGS:")
    ##print(y.value_counts())
    ##> 5    19897
    ##> 4     5648
    ##> 3     1206
    ##> 1      965
    ##> 2      616
    #print(y.value_counts(normalize=True).sort_index())
    ##> 1    0.034060
    ##> 2    0.021742
    ##> 3    0.042567
    ##> 4    0.199351
    ##> 5    0.702280

    print("SPLITTING...")
    xtrain, xtest, ytrain, ytest = train_test_split(x.values, y.values, test_size=0.2, random_state=812)
    #print(len(xtrain), len(xtest), len(ytrain), len(ytest)) #> 22665 5667 22665 5667

    print("VECTORIZING...")
    tv = TfidfVectorizer()
    tv.fit(xtrain)
    print("  + FEATURES:", len(tv.get_feature_names())) #> 9621
    mtrain = tv.transform(xtrain)
    mtest = tv.transform(xtest)
    print("  + FEATURE MATRIX (TRAINING)", type(mtrain), mtrain.shape) #> (22665, 9621)
    print("  + FEATURE MATRIX (TESTING)", type(mtest), mtest.shape)

    #print("--------------------------")
    #print("CLASSIFIER MODELS")
    #print("--------------------------")
#
    #print("LOGISTIC REGRESSION...")
    #lr = LogisticRegression(random_state=42)
    #lr.fit(mtrain, ytrain)
    #ptrain = lr.predict(mtrain)
    #ptest = lr.predict(mtest)
    #atrain = accuracy_score(ytrain, ptrain)
    #atest = accuracy_score(ytest, ptest)
    #print("  + ACCY (TRAIN):", atrain) #> 0.7755129053606883
    #print("  + ACCY (TEST):", atest) #> 0.7561319922357508
#
    #print("NAIVE BAYES (MULTINOMIAL)...")
    #nb = MultinomialNB()
    #nb.fit(mtrain, ytrain)
    #ptrain = nb.predict(mtrain)
    #ptest = nb.predict(mtest)
    #atrain = accuracy_score(ytrain, ptrain)
    #atest = accuracy_score(ytest, ptest)
    #print("  + ACCY (TRAIN):", atrain) #> 0.7165232737701301
    #print("  + ACCY (TEST):", atest) #> 0.7196047291335804
#
    #print("RANDOM FOREST...")
    #rf = RandomForestClassifier()
    #rf.fit(mtrain, ytrain)
    #ptrain = rf.predict(mtrain)
    #ptest = rf.predict(mtest)
    #atrain = accuracy_score(ytrain, ptrain)
    #atest = accuracy_score(ytest, ptest)
    #print("  + ACCY (TRAIN):", atrain) #> 0.9834546657842489
    #print("  + ACCY (TEST):", atest) #> 0.8524792659255338

    #
    # WHAT ABOUT STOPWORDS? TUNING...
    #

    print("--------------------------")
    print("GRID SEARCH")
    print("--------------------------")

    #reset these...
    cv = CountVectorizer()
    #tv = TfidfVectorizer()
    transformer = TfidfTransformer()

    # reset these...
    lr = LogisticRegression(random_state=42)
    nb = MultinomialNB()
    rf = RandomForestClassifier()

    #pipeline = Pipeline([
    #    ('vect', cv),
    #    ('vect', tv),
    #    ('clf', lr),
    #    ('clf', nb),
    #    ('clf', rf)
    #]) #> need to be unique hmm...

    pipeline = Pipeline([
        ('vect', cv),
        ('tfidf', transformer),
        ('clf', rf)
    ])

    params_grid = {
        "vect__stop_words": [None, "english"],
        "vect__ngram_range": [(1,1), (1,2), (1,3)],
        "vect__tokenizer": [None, tokenize, tokenize_v4, tokenize_v5],
        #"vect__min_df": (0.02, 0.05),
        #"vect__max_df": (0.75, 1.0),
        #"vect__max_features": (500, 1000),
        "clf__n_estimators": (5, 10),
        "clf__max_depth": (15, 20)
    }

    # GridSearchCV exhaustively generates candidates from a grid of parameter values
    gs = GridSearchCV(estimator=pipeline, param_grid=params_grid, cv=5, n_jobs=-1, verbose=1)

    gs.fit(xtrain, ytrain)
    print("BEST SCORE:", gs.best_score_) #> 0.828546216633576
    print("BEST PARAMS:", gs.best_params_) #> {'vect__stop_words': None}
    # pprint(gs.cv_results_)

    report = classification_report(ytest, gs.predict(xtest))
    print(report)

    #breakpoint()

    #print("EXAMPLE PREDICTIONS...")
    #for i in range(0, 15):
    #    review = xtest[i]
    #    rating = ytest[i]
    #    prediction = gs.predict([review]) # wrap in list to avoid... ValueError: Iterable over raw text documents expected, string object received.
    #    print("---------")
    #    print(f"CLASSIFYING {rating}-STAR REVIEW AS: {prediction}")
    #    print(review)