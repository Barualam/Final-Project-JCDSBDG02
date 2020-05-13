import pandas as pd

def list_game():
    list_game = pd.read_csv('steam_model.csv')
    list_game.drop('Unnamed: 0',axis = 1, inplace = True)
    list_game = list_game[['name', 'release_date', 'publisher', 'genres', 'steamspy_tags']]
    list_game.columns = ['NAME', 'RELEASE DATA', 'PUBLISHER', 'GENRES', 'STEAMPSPY TAGS']
    return list_game

def visual_game():
    visual_game = pd.read_csv('steam_visual.csv')
    visual_game.drop('Unnamed: 0',axis = 1, inplace = True)
    return visual_game

def best_game():
    df = pd.read_csv('steam_visual.csv')
    colum = ['name', 'release_date', 'developer', 'genres', 'average_playtime', 'owners', 'price', 'overall_reviews', 'positive_rate']
    best = df[df.overall_reviews > 50000].sort_values('positive_rate', ascending=False)[colum].head(25).round(2)
    best.columns = ['NAME', 'RELEASE_DATE', 'DEVELOPER', 'GENRES', 'AVERAGE_PLAYTIME', 'OWNERS', 'PRICE', 'OVERALL_REVIEWS', 'POSITIVE_RATE']
    return best

def worst_game():
    df = pd.read_csv('steam_visual.csv')
    colum = ['name', 'release_date', 'developer', 'genres', 'average_playtime', 'owners', 'price', 'overall_reviews', 'positive_rate']
    worst = df[df.overall_reviews > 500].sort_values('positive_rate', ascending=True)[colum].head(25).round(2)
    worst.columns = ['NAME', 'RELEASE_DATE', 'DEVELOPER', 'GENRES', 'AVERAGE_PLAYTIME', 'OWNERS', 'PRICE', 'OVERALL_REVIEWS', 'POSITIVE_RATE']
    return worst

def data_model():
    data_model = pd.read_csv('steam_model.csv')
    data_model.drop('Unnamed: 0',axis = 1, inplace = True)
    return data_model

def games_name():
    games_name = pd.read_csv('steam_model.csv')
    games_name.drop('Unnamed: 0',axis = 1, inplace = True)
    return games_name.name.values