import os
import pandas as pd

from app.vectorizer import count_vectorized_dataframe, tfidf_vectorized_dataframe, cosine_similarity_df
from conftest import DOCUMENTS

MOCK_EXPORTS_DIRPATH = os.path.join(os.path.dirname(__file__), "data", "exports")

texts_df = pd.DataFrame({"txt.filename": ["Doc 1", "Doc 2", "Doc 3"], "txt.contents": DOCUMENTS})

def test_count_vectorized_dataframe():
    df = count_vectorized_dataframe(texts_df)
    df.to_csv(os.path.join(MOCK_EXPORTS_DIRPATH, "counts_matrix.csv"))
    assert df.shape == (3, 17)
    assert df.columns.tolist() == [
        'txt.filename', 'txt.contents', 'all', 'and', 'ate', 'got', 'hens', 'kings', 'men', 'sleep', 'the', 'they', 'tired', 'to', 'until', 'went', 'zzz'
    ]
    assert df.iloc[0].values.tolist() == [
        'Doc 1', 'all the kings men', 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0
    ]

def test_tfidf_vectorized_dataframe():
    df = tfidf_vectorized_dataframe(texts_df)
    df.to_csv(os.path.join(MOCK_EXPORTS_DIRPATH, "tfidf_matrix.csv"))
    assert df.shape == (3, 17)
    assert df.columns.tolist() == [
        'txt.filename', 'txt.contents', 'all', 'and', 'ate', 'got', 'hens', 'kings', 'men', 'sleep', 'the', 'they', 'tired', 'to', 'until', 'went', 'zzz'
    ]
    assert df.iloc[0].values.tolist() == [
        'Doc 1', 'all the kings men', 0.3731188059313277, 0.0, 0.0, 0.0, 0.0, 0.4804583972923858, 0.6317450542765208, 0.0, 0.4804583972923858, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    ]
