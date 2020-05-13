import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import itertools
import json
import plotly
from listgame import visual_game

def year():
    df = visual_game()
    fig = make_subplots(rows=2, cols=1, subplot_titles=('Banyak Game Yang dirilis tiap tahun', 'Banyak Game yang dirilis tiap bulan'))

    fig.append_trace(go.Bar(x=df['year'].value_counts().index, y=df['year'].value_counts().values,
                        marker_color='#00abff', marker_line_color='#00abff',
                        marker_line_width=2, opacity=1), row=1, col=1)

    fig.append_trace(go.Bar(x=df['month'].value_counts().index, y=df['month'].value_counts().values,
                        marker_color='#00abff', marker_line_color='#00abff',
                        marker_line_width=2, opacity=1), row=2, col=1)

    fig.update_layout(height=600, width=900, showlegend=False, font=dict(family="Courier New, monospace",size=18, color="white"))
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig.update_yaxes(showgrid=True, gridcolor='gray')
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json

def language():
    fig = go.Figure(data=go.Pie(labels=['English', 'Non-English'], values=[26564,511], 
                             pull=[0,0.2], marker_colors=['#00abff','#ffffff'],rotation=-45, opacity=1))
    fig.layout = dict(height=600, width=900)
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'}, 
    font=dict(family="Courier New, monospace",size=18, color="white"))
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json

def developer():
    df = visual_game()
    developer = df['developer'].value_counts()
    fig = go.Figure(data=go.Bar(x=developer.sort_values()[-15:].values, y=developer.sort_values()[-15:].index, 
                        orientation='h', marker_color='#00abff', marker_line_color='#00abff',
                           marker_line_width=2, opacity=1))
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig.update_layout(height=600, width=1300, font=dict(family="Courier New, monospace",size=18, color="white"))
    fig.update_xaxes(showgrid=True, gridcolor='gray')
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json

def publisher():
    df = visual_game()
    publisher = df['publisher'].value_counts()
    fig = go.Figure(data=go.Bar(x=publisher.sort_values()[-15:].values, y=publisher.sort_values()[-15:].index, 
                        orientation='h', marker_color='#00abff', marker_line_color='#00abff',
                           marker_line_width=2, opacity=1))
    fig.update_layout(height=600, width=1300,font=dict(family="Courier New, monospace",size=18, color="white"))
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig.update_xaxes(showgrid=True, gridcolor='gray')
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json

def platform():
    df = visual_game()
    Platforms=list(platform.split(';') for platform in df.platforms)
    Platforms=list(itertools.chain.from_iterable(Platforms))
    Platforms=pd.value_counts(Platforms)

    fig = go.Figure(data=go.Bar(x=Platforms.values/len(df), y=Platforms.index, 
                        orientation='h', marker_color='#00abff', marker_line_color='#00abff',
                           marker_line_width=2, opacity=1))
    fig.update_xaxes(showgrid=True, gridcolor='gray')
    fig.update_layout(height=600, width=1000, showlegend=False, font=dict(family="Courier New, monospace",size=18, color="white"))
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json

def requiere_age():
    df = visual_game()
    umur = df[df['required_age']>0]['required_age'].value_counts()
    fig = go.Figure(data=go.Pie(labels=umur.index, values=umur.values, 
                             pull=(0.1,0,0.1,0.05,0.2), marker_colors=['#71c7ec','#1ebbd7','#189ad3','#107dac','#005073'],rotation=90))
    fig.layout = dict(height=600, width=900)
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'}, 
    font=dict(family="Courier New, monospace",size=18, color="white"))
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json

def category():
    df = visual_game()
    Categories=list(category.split(';') for category in df.categories)
    Categories=list(itertools.chain.from_iterable(Categories))
    Categories=pd.value_counts(Categories)

    trace = go.Table(
    header=dict(values=['<b>CATEGORIES</b>', '<b>TOTAL</b>'],line_color='#00abff', fill_color='#00abff', align='left', font_size=17), 
    cells=dict(values=[Categories.index,Categories.values],line_color='#00abff',fill_color='white',align='left', font_size=15, font_color='black'),
    domain=dict(x=[0, 0.2],y=[0, 1]) )

    trace1 = go.Bar(x=Categories.index[0:11],y=Categories.values[0:11],
                marker_color='#00abff', marker_line_color='#00abff',
                marker_line_width=2, opacity=1)

    layout = dict(xaxis1=dict( dict(domain=[0.25, 1])), yaxis1=dict( dict(domain=[0, 1])), 
                height=600, width=1300, font=dict(family="Courier New, monospace",size=14, color="white"))

    fig = go.Figure(data = [trace,trace1], layout = layout)
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig.update_yaxes(showgrid=True, gridcolor='gray')
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json

def genre():
    df = visual_game()
    Genres=list(genre.split(';') for genre in df.genres)
    Genres=list(itertools.chain.from_iterable(Genres))
    Genres=pd.value_counts(Genres)

    trace = go.Table(
    header=dict(values=['<b>GENRES</b>', '<b>TOTAL</b>'],line_color='#00abff', fill_color='#00abff', align='left', font_size=17), 
    cells=dict(values=[Genres.index,Genres.values],line_color='#00abff',fill_color='white',align='left', font_size=15, font_color='black'),
    domain=dict(x=[0, 0.20], y=[0, 1]))

    trace1 = go.Bar(x=Genres.index[0:11],y=Genres.values[0:11], marker_color='#00abff', marker_line_color='#00abff',
                marker_line_width=2, opacity=1)

    layout = dict(xaxis1=dict( dict(domain=[0.25, 1])), yaxis1=dict( dict(domain=[0, 1])), 
                height=600, width=1300,font=dict(family="Courier New, monospace",size=14, color="white"))

    fig = go.Figure(data = [trace,trace1], layout = layout)
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig.update_yaxes(showgrid=True, gridcolor='gray')
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json

def steamspy_tags():
    df = visual_game()
    Steam_tags=list(tags.split(';') for tags in df.steamspy_tags)
    Steam_tags=list(itertools.chain.from_iterable(Steam_tags))
    Steam_tags=pd.value_counts(Steam_tags)

    trace = go.Table(
        header=dict(values=['<b>STEAM TAGS</b>', '<b>TOTAL</b>'],line_color='#00abff', fill_color='#00abff', align='left', font_size=17), 
        cells=dict(values=[Steam_tags.index,Steam_tags.values],line_color='#00abff',fill_color='white',align='left', font_size=15, font_color='black'),
        domain=dict(x=[0, 0.2], y=[0, 1]))

    trace1 = go.Bar(x=Steam_tags.index[0:11],y=Steam_tags.values[0:11],
                marker_color='#00abff', marker_line_color='#00abff',
                marker_line_width=0, opacity=1)

    layout = dict(xaxis1=dict( dict(domain=[0.25, 1])), yaxis1=dict( dict(domain=[0, 1])), 
                height=600, width=1300, font=dict(family="Courier New, monospace",size=13, color="white"))

    fig = go.Figure(data = [trace,trace1], layout = layout)
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig.update_yaxes(showgrid=True, gridcolor='gray')
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json

def achievement():
    fig = go.Figure(data=go.Pie(labels=['Have achievement', 'no achievement'], values=[15211,11864], 
                             pull=[0,0.1], marker_colors=['#66CCFF','#00abff'],rotation=-45))
    fig.layout = dict(height=600, width=900,font=dict(family="Courier New, monospace",size=14, color="white"))
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json

def positive_rate():
    df = visual_game()
    fig = make_subplots(rows=3, cols=1, subplot_titles=('Distribusi Data positive_rate untuk semua game', 
                                                    'Distribusi Data positive_rate untuk semua game dengan jumlah reviews > 50',
                                                    'Distribusi Data positive_rate untuk semua game dengan jumlah reviews > 100'))

    fig.append_trace(go.Histogram(x=df.positive_rate, marker_color='#00abff', opacity=1), row=1, col=1)

    fig.append_trace(go.Histogram(x=df[df.overall_reviews > 50].positive_rate, marker_color='#00abff', opacity=1), row=2, col=1)

    fig.append_trace(go.Histogram(x=df[df.overall_reviews > 100].positive_rate, marker_color='#00abff', opacity=1), row=3, col=1)

    fig.update_layout(height=600, width=900, showlegend=False,font=dict(family="Courier New, monospace",size=14, color="white"))
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)','paper_bgcolor': 'rgba(0, 0, 0, 0)'})
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json