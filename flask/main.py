from flask import Flask, render_template, request
from listgame import list_game, visual_game, best_game, worst_game, games_name
from data_visualization import year, language, developer, publisher, platform, requiere_age, category, genre, steamspy_tags, achievement, positive_rate
from model import content_based_rec, profile_recommended, nlp

## translate flask to python object

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/about2')
def about2():
    return render_template('about2.html')

@app.route('/about_recom')
def about_recom():
    return render_template('about_recom.html')

@app.route('/list_game')
def table_data():
    data = list_game()
    return render_template('gamelist.html', data = data)

@app.route('/best_game')
def best_data():
    data = best_game()
    return render_template('gamelist_best.html', data = data)

@app.route('/worst_game')
def worst_data():
    data = worst_game()
    return render_template('gamelist_worst.html', data = data)

@app.route('/visualisasi_year')
def plots_year():
    data = year()
    return render_template('plot_year.html', data = data)

@app.route('/visualisasi_language')
def plots_language():
    data = language()
    return render_template('plot_language.html', data = data)

@app.route('/visualisasi_developer')
def plots_developer():
    data = developer()
    return render_template('plot_developer.html', data = data)

@app.route('/visualisasi_publisher')
def plots_publisher():
    data = publisher()
    return render_template('plot_publisher.html', data = data)

@app.route('/visualisasi_platform')
def plots_platform():
    data = platform()
    return render_template('plot_platform.html', data = data)

@app.route('/visualisasi_requiere_age')
def plots_requiere_age():
    data = requiere_age()
    return render_template('plot_requiere_age.html', data = data)

@app.route('/visualisasi_category')
def plots_category():
    data = category()
    return render_template('plot_category.html', data = data)

@app.route('/visualisasi_genre')
def plots_genre():
    data = genre()
    return render_template('plot_genre.html', data = data)

@app.route('/visualisasi_steamspy_tags')
def plots_steamspy_tags():
    data = steamspy_tags()
    return render_template('plot_steamspy_tags.html', data = data)

@app.route('/visualisasi_achievement')
def plots_achievement():
    data = achievement()
    return render_template('plot_achievement.html', data = data)

@app.route('/visualisasi_positive_rate')
def plots_positive_rate():
    data = positive_rate()
    return render_template('plot_positive_rate.html', data = data)

@app.route('/model_nlp')
def model_nlp():
    return render_template('model_nlp.html', game_names=games_name()) 

@app.route("/output_nlp")
def output_nlp():
    review = request.args.get('areview')
    hasil = nlp(review)
    return render_template('output_nlp.html', hasil=hasil)

@app.route('/model_recommended')
def recommended():
    return render_template('model_recom.html', game_names=games_name()) 

@app.route("/output_recommended")
def output_recommended():
    game = request.args.get('game')
    by = request.args.get('recommendation_by')
    test = content_based_rec(game, by)
    return render_template('output_recom.html', game=game, test=test, check='available')

@app.route('/model_profil')
def profil():
    return render_template('model_profil.html', game_names=games_name()) 

@app.route("/output_profil")
def output_profil():
    game1 = request.args.get('game1')
    game2 = request.args.get('game2')
    game3 = request.args.get('game3')
    game4 = request.args.get('game4')
    game5 = request.args.get('game5')
    by = request.args.get('recommendation_by')

    try:
        rating1 = int(request.args.get('rating1'))
    except:
        rating1 = 0
    try:
        rating2 = int(request.args.get('rating2'))
    except:
        rating2 = 0 
    try:
        rating3 = int(request.args.get('rating3'))
    except:
        rating3 = 0
    try:
        rating4 = int(request.args.get('rating4'))
    except:
        rating4 = 0
    try:
        rating5 = int(request.args.get('rating5'))
    except:
        rating5 = 0

    games = [game1,game2,game3,game4,game5]
    game = [game for game in games if game != None]
    ratings = [rating1,rating2,rating3,rating4,rating5]
    rating = [rating for rating in ratings if rating != 0]

    test = profile_recommended(game, rating, by)

    if type(test) == type('string'):
        return render_template('output_profil.html', test=test, result='wrong')
    else:
        return render_template('output_profil.html', test=test, result='valid')

if __name__ == '__main__':
    app.run(debug=True, port=7777)