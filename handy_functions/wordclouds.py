def plot_wordclouds(ngrams,title):
  wordcloud = WordCloud(width=800, height=400, background_color='white').\
  generate_from_frequencies(dict(zip(ngrams['Word'], ngrams['Freq'])))

  plt.figure(figsize=(10, 5))
  plt.imshow(wordcloud, interpolation='bilinear')
  plt.axis('off')
  filename = format_filename(title,format=".png")
  plt.savefig(filename)
  plt.show()
