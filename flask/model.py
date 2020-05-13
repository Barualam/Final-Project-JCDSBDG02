import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from listgame import data_model
import pickle
import re
from re import finditer
import string
from nltk.corpus import stopwords


nlp_model = pickle.load(open('nlp_model.sav', 'rb'))
tfidf = pickle.load(open('tfid.sav', 'rb'))

def clean_review(reviews):
    
    # Menghapus Early access
    reviews = reviews.replace('Early Access Review', "")
    
    # Pemisahan huruf dan angka
    reviews = re.split('(\d+)', reviews)
    reviews = " ".join(reviews)
    reviews = reviews.strip()
    
    # Pemisahan camelcase
    camel = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', reviews)
    reviews = " ".join([m.group(0) for m in camel])
    
    # Membuang punctuation
    nopunc = [char for char in reviews if char not in string.punctuation]
    reviews = ''.join(nopunc)
    
    waste_symbols = "人̳⣟⣦̪⠓▒͎¸⠟⣅>⡾ ⠻⣀⣛„ͭ⣮⡻⠦⡀͐‘̨⣆̤⣿<／丶⣞͇⣵͞⠹ͩ⢒̯⢸⣤̗̫ͯ͆̔͠⠛⢻⠏-́☐̺͛̋⠸⣥⠄̷＼͟·⌒͗⠁́｀⢹\\⢄͈̌ͨ⢤彡~¯/⠶⠲ˆ⡥̮̻͔☉⣻̣ゝ⡞̧͙̿̒̊̑ノ⠭ͤ_⠐⣇҉̚–⡄´̓█▄☑⣧̴͖̍｜⣷̭͘͝｡⠴̜̄ʖ¨̵̏͢⢂͋;͒:⢉つ̾＿̈⣴⣌ͫ⢛⡹⣈へ⢯,̅⣭̩̬̕⡈ム͡⣼ͦ)̛͜ヽ̝̥⣠⢟̶⠤̡͉⠘̹̈́⡴̠⢀）⠇⣾͊⢰̞ͮ̇`⠑⡿\u3000⠃⣸⠾͍̆ͅ￣⢚̓⠂⡵─⢬ー⠿(⠆⠉̦*͕ﾉ⣹⡟⣬⠙▓⡐7͏̟̲⢿⢦（̰♥̸̢⣙͓̂▀くﾌ⠀.⠰⡒°̖̎､⣒⣰̼⢅⣁⠒͑⢾⡂͌̀ͧ…̃▐ﾚ、丿⢌|̱⢴⡠⣩▌⣉͚ͪ'⢆⢠⡇⡛⣏⡶⣜⣄⡸⠈̘ͣ⣽̉̽̐ͥ⡏ͬ⣗⣶░⠋⠔̙͂^"
    
    # Membuang symbol-symbol
    for item in waste_symbols:
        reviews = reviews.replace(item, " ")
        
    # Menghapus whitespace
    reviews = " ".join(reviews.split())
    reviews = reviews.strip()
    
    # Membuang Stopwords
    reviews = [word for word in reviews.split() if word.lower() not in stopwords.words('english')]
    reviews = ' '.join(reviews)
    return reviews

def nlp(review):
    clean = clean_review(review)
    vector_review = tfidf.transform([clean])
    result = nlp_model.predict(vector_review)
    if result == 1:
        return 'Positive review'
    else:
        return 'Negative review'

def content_based_rec(judul_game, recomendation = 'Genre'):
    df = data_model()

    # Index Game
    games_index = pd.Series(df.index, index=df.name)

    # Mengambil feature judul dan genre saja
    dfmod_genre = df[['name', 'genres']]
    dfdummy_genre = dfmod_genre['genres'].str.get_dummies(';')
    dfmod_genre = pd.concat((dfmod_genre['name'], dfdummy_genre), axis=1)

     # Dataframe Name & tags
    dfmod_tags = df[['name', 'steamspy_tags']]
    dfdummy_tags = dfmod_tags['steamspy_tags'].str.get_dummies(';')
    dfmod_tags = pd.concat((dfmod_tags['name'], dfdummy_tags), axis=1)

    # Nilai cosine similarity untuk genre dan tags
    cosine_mod_genre = cosine_similarity(dfdummy_genre.values, dfdummy_genre.values)
    cosine_mod_tags = cosine_similarity(dfdummy_tags.values, dfdummy_tags.values)

    # DataFrame Hasil yang akan ditampilkan
    hasil = df[['name', 'release_date', 'developer', 'genres','steamspy_tags', 'owners', 'price', 'overall_reviews', 'positive_rate', 'price']]
    
    # Mengetahui index dari game yang diinput
    idx = games_index[judul_game]
    
    # Membuat Feature Score untuk masing-masing rekomendasi
    hasil = hasil.assign(**{'Genre_Score':cosine_mod_genre[idx]})
    hasil = hasil.assign(**{'Tags_Score':cosine_mod_tags[idx]})
    hasil = hasil.assign(**{'TagsGenre_Score':(cosine_mod_genre[idx] + cosine_mod_tags[idx])/2})
    
    # Print Dataframe Berdasarkan rekomendasi yang diinginkan
    
    if recomendation == 'Genre':
        hasil = hasil.sort_values(['Genre_Score', 'positive_rate'], ascending=False).drop(idx).head(15)
    elif recomendation == 'Tags':
        hasil = hasil.sort_values(['Tags_Score', 'positive_rate'], ascending=False).drop(idx).head(15)
    elif recomendation == 'TagsGenre':
        hasil = hasil.sort_values(['TagsGenre_Score', 'positive_rate'], ascending=False).drop(idx).head(15)
    
    return hasil.round(2)


def profile_recommended(list_name, list_score, recomendation = 'Genre'):
    
    try:
        df = data_model()

        # Membuat Data Frame dari profil pengguna
        inputGames = pd.DataFrame({
            'name':list_name,
            'rating':list_score
        })

        index = df[df['name'].isin(list_name)].index

        # Mengambil feature judul dan genre saja
        dfmod_genre = df[['name', 'genres']]
        dfdummy_genre = dfmod_genre['genres'].str.get_dummies(';')
        dfmod_genre = pd.concat((dfmod_genre['name'], dfdummy_genre), axis=1)

        # Dataframe Name & tags
        dfmod_tags = df[['name', 'steamspy_tags']]
        dfdummy_tags = dfmod_tags['steamspy_tags'].str.get_dummies(';')
        dfmod_tags = pd.concat((dfmod_tags['name'], dfdummy_tags), axis=1)

        
        hasil = df[['name', 'release_date', 'developer', 'genres','steamspy_tags', 'owners', 'price', 'overall_reviews', 'positive_rate', 'price']]
        hasil.columns = ['NAME', 'RELEASE_DATE', 'DEVELOPER', 'GENRES', 'STEAMSPY_TAGS', 'OWNERS', 'PRICE', 'OVERALL_REVIEWS', 'POSITVIE_RATE', 'PRICE']

        # filter game dari input
        userGamesGenre = dfmod_genre[dfmod_genre['name'].isin(inputGames['name'].tolist())]
        userGamesTags = dfmod_tags[dfmod_tags['name'].isin(inputGames['name'].tolist())]
        
        # Matriks karakteristik dari user profil
        userGenreTable = userGamesGenre.reset_index(drop=True).drop('name', 1)
        userTagsTable = userGamesTags.reset_index(drop=True).drop('name', 1)
        
        #Bobot dari profil pengguna
        userProfileGenre =userGenreTable.transpose().dot(inputGames['rating'])
        userProfileTags =userTagsTable.transpose().dot(inputGames['rating'])

        # Ambil karakteristik genre & tags dari setiap games
        genreTable = dfmod_genre.drop('name',1)
        tagsTable = dfmod_tags.drop('name',1)
        
        # Pengalian genre & tags dengan bobot rata-rata
        recomendationGenre_score = ((genreTable*userProfileGenre).sum(axis=1))/(userProfileGenre.sum())
        recomendationTags_score = ((tagsTable*userProfileTags).sum(axis=1))/(userProfileTags.sum())
        
        # Memasukan score kedalam dataframe hasil
        hasil = hasil.assign(**{'Genre_Score':recomendationGenre_score})
        hasil = hasil.assign(**{'Tags_Score':recomendationTags_score})
        hasil = hasil.assign(**{'TagsGenre_Score':(recomendationGenre_score + recomendationTags_score)/2})
        
        if recomendation == 'Genre':
            hasil = hasil.sort_values(['Genre_Score', 'positive_rate'], ascending=False).drop(index)
        elif recomendation == 'Tags':
            hasil = hasil.sort_values(['Tags_Score', 'positive_rate'], ascending=False).drop(index)
        elif recomendation == 'TagsGenre':
            hasil = hasil.sort_values(['TagsGenre_Score', 'positive_rate'], ascending=False).drop(index)
        return hasil.head(15).round(2)
    except:
        return ('Wrong Input')