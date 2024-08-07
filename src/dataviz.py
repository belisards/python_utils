#import os
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import unicodedata

def remove_accents(text):
    nfkd_form = unicodedata.normalize('NFKD', text)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def format_filename(graph_title,base_path,format=".svg"):
    graph_title_no_accents = remove_accents(graph_title)
    svg_filename = graph_title_no_accents.replace(" ", "_").lower() + format
    return base_path + svg_filename

def plot_ngrams_bar(ngrams, graph_title):
    fig = px.bar(ngrams, x='Freq', y='Word', orientation='h', title=graph_title)

    fig.update_layout(
        height=1200,
        width=1000,
        title={'x': 0.5, 'xanchor': 'center'},
        xaxis_title='Frequency',
        yaxis_title='Unigram',
        yaxis=dict(
            autorange='reversed'
        )
    )

    fig.show()
    fig.write_image(format_filename(graph_title))

def plot_wordclouds(ngrams,title):
  wordcloud = WordCloud(width=800, height=400, background_color='white').\
  generate_from_frequencies(dict(zip(ngrams['Word'], ngrams['Freq'])))

  plt.figure(figsize=(10, 5))
  plt.imshow(wordcloud, interpolation='bilinear')
  plt.axis('off')
  filename = format_filename(title,format=".png")
  plt.savefig(filename)
  plt.show()


def plot_ngrams_bar(ngrams, graph_title,IMG_PATH):
    fig = px.bar(ngrams, x='Freq', y='Word', orientation='h', title=graph_title)

    fig.update_layout(
        height=1200,
        width=1000,
        title={'x': 0.5, 'xanchor': 'center'},
        xaxis_title='Frequency',
        yaxis_title='Unigram',
        yaxis=dict(
            autorange='reversed'
        )
    )

    fig.show()
    fig.write_image(format_filename(graph_title,IMG_PATH))

def plot_wordclouds(ngrams,title,IMG_PATH):
  wordcloud = WordCloud(width=800, height=400, background_color='white').\
  generate_from_frequencies(dict(zip(ngrams['Word'], ngrams['Freq'])))

  plt.figure(figsize=(10, 5))
  plt.imshow(wordcloud, interpolation='bilinear')
  plt.axis('off')
  filename = format_filename(title,IMG_PATH,format=".png")
  plt.savefig(filename)
  plt.show()
