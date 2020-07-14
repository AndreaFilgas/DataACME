## Load libraries e csv

# load libraries
from rake_nltk import Rake
import nltk
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import warnings
import string
warnings.filterwarnings("ignore")

# load csv
df_csv = pd.read_csv('C:/Users/camil/Desktop/Projeto Integrador/dados/rotten_imdb.csv')



## Selecionar features

# criar copias dos dois datasets para manipular os dados
df = df_csv.copy()
df2 = dfx.copy()

# excluir linhas repetidas
df.drop_duplicates(subset = 'movie_info', inplace = True)

# remover os filmes que nao tem avg_rating
df.dropna(subset = ['tomatometer_avg_rating'], inplace = True)

# selecionar colunas de interesse dos dois datasets
df = df[['tconst','movie_name_imdb', 'directors','casts','movie_info','genres']]
df2 = df2[['tconst','movie_name_imdb', 'directors','casts','movie_info','genres']]

# excluir missing values
df.dropna(inplace=True)

# juntar os dois datasets
df.append(df2, ignore_index=True)



## Tratamento das features

# remoção da pontuação de 'Plot'
df['movie_info'] = df['movie_info'].str.replace('[{}]'.format(string.punctuation), '')

 # inicialização das lista que será a nova coluna
df['Key_words'] = ''  

# instanciação do objeto do Rake para descartar as 'stop words' (baseado naquilo que está no NLTK)
r = Rake()

for index, row in df.iterrows():
    # extração das key words - que já remove as 'stop words' do texto
    r.extract_keywords_from_text(row['movie_info'])   
    # dicionário com as key words e scores
    key_words_dict_scores = r.get_word_degrees()    
    # nova coluna que será inserida
    row['Key_words'] = list(key_words_dict_scores.keys())  


# to extract all genre into a list, only the first three actors into a list, and all directors into a list
df['genres'] = df['genres'].map(lambda x: x.split(','))
df['directors'] = df['directors'].map(lambda x: x.split(','))
df['casts'] = df['casts'].map(lambda x: x.split(',')[:3])

# Retirada dos espaços dos campos e conversão para minúsculas
for index, row in df.iterrows():
    row['genres'] = [x.lower().replace(' ','') for x in row['genres']]
    row['casts'] = [x.lower().replace(' ','') for x in row['casts']]
    row['directors'] = [x.lower().replace(' ','') for x in row['directors']]



## Bag of Words

# inicialização da lista
df['Bag_of_words'] = ''
# colunas que farão parte da Bag of Words
columns = ['genres', 'directors', 'casts', 'Key_words']
# percorre cada coluna e adiciona cada palavra individualmente
for index, row in df.iterrows():
    words = ''
    for col in columns:
        words += ' '.join(row[col]) + ' '
    row['Bag_of_words'] = words

# remoção dos "espaços" de todas as palavras na BoW
df['Bag_of_words'] = df['Bag_of_words'].str.strip().str.replace('   ', ' ').str.replace('  ', ' ')




## Simplificar o daset para inculuir apenas o titulo e a bag of words

# selecionar as features de interesse e salvar em um novo dataframe
df_bag = df[['tconst','movie_name_imdb','Bag_of_words']]



## Criar uma funcao para recomendacao

# Geração da Matriz com a frequência de cada palavra com filme 250 x quantidade total de palavras únicas
count = CountVectorizer()
count_matrix = count.fit_transform(df_bag['Bag_of_words'])

cosine_sim = cosine_similarity(count_matrix, count_matrix)

# to create a Series for movie titles which can be used as indices (each index is mapped to a movie title)
indices = pd.Series(df_bag['movie_name_imdb'])

def recommend(title, cosine_sim = cosine_sim):
    # inicialização da lista
    recommended_movies = []
    # captura o índice que corresponde ao título
    idx = indices[indices == title].index[0]   
    # scores de similaridade em ordem descendente
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)   
    # captura os 10 filmes com o maior índice de similaridade
    top_10_indices = list(score_series.iloc[1:11].index)   
    # [1:11] para excluir o primeiro (0) que é o próprio filme selecionado
    
    # monta uma lista com os filmes retornados
    for i in top_10_indices:   
        recommended_movies.append(list(df_bag['movie_name_imdb'])[i])
        
    return recommended_movies




 ## obter a media do filme recomendado

# recomendacao para o filme que sera produzido
filme = recommend(df2.movie_name)

# pegar a rating_avg desse filme mais proximo e salvar como uma nova coluna para o filme a ser feito
df_x['rating_avg'] = float(df.tomatometer_avg_rating[df.movie_name_imdb == filme])

