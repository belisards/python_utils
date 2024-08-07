
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
