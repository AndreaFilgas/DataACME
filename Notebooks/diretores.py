## Load libraries e dataset

#load libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline
import numpy as np

# load dataset
df= pd.read_csv('C:/Users/camil/Desktop/Projeto Integrador/dados/df.csv')




## Funcao para pegar a media e numero de filmes que o diretor fez

# filtrar apenas os diretores e retornar os dados
def get_director(diretor):
    df1 = df[df.type == 'director']
    df1 = df1[df1.name == diretor]
    return (df1.n, df1.avg)

# salvar as informacoes em um objeto
director = get_director('Alan Miller')



## Funcao para pegar a media e numero de filmes que o ator fez

# filtrar apenas os atores e retornar os dados
def get_actor(ator):
    df1 = df[df.type == 'actor']
    df1 = df1[df1.name == ator]
    return df1.n, df1.avg

# salvar as informacoes em um objeto
actor = get_actor('Will Smith')



## Funcao para pegar a media e numero de filmes que o roteirista fez
def get_writer(roteirista):
    df1 = df[df.type == 'writer']
    df1 = df1[df1.name == roteirista]
    return (df1.n, df1.avg)

# salvar as informacoes em um objeto
writer = get_writer('William Plyler')


# salvar todas as informacoes em um dataset
df_eda = pd.DataFrame(np.array([[int(director[0]), float(director[1]),int(actor[0]), float(actor[1]), int(writer[0]), float(writer[1])]]),
                   columns= ['director_n', 'director_avg','actor_n','actor_avg','writer_n','writer_avg'])