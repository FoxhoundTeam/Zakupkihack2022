import numpy as np
import pandas as pd
from collections import Counter

from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    PER,
    NamesExtractor,
    Doc
)
import fasttext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import euclidean_distances




CONTRACTS_FILE = "small_data/Контракты 44ФЗ.csv"
PRODUCTS_FILE = "small_data/Справочник пром производства.csv"
OFFERS_FILE = "small_data/Ценовые предложения поставщиков.csv"
INN_COLUMN = "inn"

def count_contractors_by_category(category: str, contracts_data: pd.DataFrame):
    """Количество поставщиков для данной категории."""


def count_contracts_by_contractors(contracts_data: pd.DataFrame) -> Counter:
    """Количество исполненных контрактов.

    Количество исполненных контрактов используется в качестве
    метрики надежности поставщика."""

    contractors_counter = Counter()
    for inn in contracts_data[INN_COLUMN]:
        contractors_counter[inn] += 1

    return contractors_counter


class Recommendator:

    def __init__(self):
        self.contracts_data = pd.read_csv(CONTRACTS_FILE, sep=';')
        #self.reliability: Counter = count_contracts_by_contractors(self.contracts_data)
        self.products_data = pd.read_csv(PRODUCTS_FILE, sep=';')

        self.segmenter = Segmenter()
        self.emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.morph_vocab = MorphVocab()
        self.syntax_parser = NewsSyntaxParser(self.emb)
        #self.products_data['BOW'] = self.products_data['product_name'].apply(self.get_BOW)

        self.offers_data = pd.read_csv(OFFERS_FILE, sep=';')
        #rows = range(1000)
        #self.offers_data = self.offers_data.loc[rows]

        #self.model = fasttext.load_model("model_filename.bin")

        columns = ["product_name", "okpd2_name", "inn"]

        contractor_BOWs = {}
        product_BOWs = {}

        for df in [self.offers_data, self.products_data, self.contracts_data]:
        #for df in [self.offers_data]:
            for row in df[columns].itertuples():
                _, product_name, okpd2, inn = row
                product_bow = self.get_BOW(". ".join((product_name, okpd2)))
                try:
                    contractor_BOWs[inn] = contractor_BOWs[inn] | product_bow
                except KeyError:
                    contractor_BOWs[inn] = product_bow
                try:
                    product_BOWs[product_name] = product_BOWs[inn] | product_bow
                except KeyError:
                    product_BOWs[product_name] = product_bow


        self.contractor_BOWs = contractor_BOWs
        self.product_BOWs = product_BOWs

        texts = [" ".join(list(bow)) for key, bow in contractor_BOWs.items()]

        self.vectorizer = TfidfVectorizer(use_idf=True, norm='l1')
        matrix = self.vectorizer.fit_transform(texts)

        number_of_clusters = 150
        km = KMeans(n_clusters=number_of_clusters)
        # Normally people fit the matrix
        km.fit(matrix)


        self.contractor_labels = {contractor: label for contractor, label in zip(contractor_BOWs, km.labels_)}


    def get_product_distances(self, product_name):
        texts = [" ".join(list(bow)) for key, bow in self.product_BOWs.items()]
        texts.append(" ".join(list(self.get_BOW(product_name))))
        self.features = self.vectorizer.fit_transform(texts)
        return [euclidean_distances(features_i, self.features[-1]) for features_i in self.features]


    def get_BOW(self, text: str) -> set:
        """Получение bag of words для указанной ТРУ."""
        doc = Doc(text)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        doc.parse_syntax(self.syntax_parser)
        for token in doc.tokens:
            token.lemmatize(self.morph_vocab)

        return set([_.lemma for _ in doc.tokens])


if __name__ == '__main__':
    recom = Recommendator()

    ttt = list(zip(recom.contractor_labels.items(), recom.contractor_BOWs.items()))
    ttt.sort(key=lambda tup: tup[0][1], reverse=False)
    for elem in ttt[:3]:
        print(f"contractor: {elem[0][0]}\ngroup: {elem[0][1]}\nbag of words: {elem[1][1]}")

    new_product_name = "компьютер"
    print(f'Distances for "{new_product_name}"')
    product_distances = zip(recom.product_BOWs.items(), [dist[0][0] for dist in recom.get_product_distances(new_product_name)], recom.features)
    dists = list(product_distances)
    #print(dists)
    dists.sort(key=lambda tup: tup[1])
    for elem in dists[0:10]:
        print(f"product_name: {elem[0][0]}\nproduct BOW: {elem[0][0]}\ndistance: {elem[1]})")
        print("tf-idf vectorized matrix:")
        print(elem[2])
