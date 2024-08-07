def find_text(text, column='automatic_subtitle'):
    condition = df[column].str.contains(text, regex=False)
    # Check if the text is in the automatic_subtitle column
    if not condition.any():
        print(f"No occurrences of '{text}' found.")
        return

    # Get a random sample containing the text
    sample = df[condition].sample(1)

    # Print the title column
    print("Title:", sample['title'].values[0])

    # Get the automatic_subtitle text
    subtitle = sample[column].values[0]

    # Find the position of the text and extract part of the subtitle near it
    start_pos = max(subtitle.find(text) - 100, 0)
    end_pos = subtitle.find(text) + 100
    context = subtitle[start_pos:end_pos]

    print(context)


def extract_urls(text):
  """Extracts URLs from a given text.

  Args:
    text: The input text string.

  Returns:
    A list of URLs found in the text.
  """
  url_pattern = re.compile(
      r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
  )
  urls = url_pattern.findall(text)
  return urls


def remove_accents(text):
    nfkd_form = unicodedata.normalize('NFKD', text)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def format_filename(graph_title,base_path,format=".svg"):
    graph_title_no_accents = remove_accents(graph_title)
    svg_filename = graph_title_no_accents.replace(" ", "_").lower() + format
    return base_path + svg_filename

def clean_text(text):
  text = str(text)
  text = text.lower()
  text = ''.join([c for c in text if not c.isdigit()])
  return text

def remove_hyperlinks(text):
  pattern = r'https?://[^\s]+'
  clean_text = re.sub(pattern, '', text)
  return clean_text

def extract_domain(urls):
    """Extracts the main domain name from a list of URLs.

    Args:
        urls: A list of URLs.

    Returns:
        A list of main domain names.
    """
    domains = []
    for url in urls:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        main_domain = get_sld(domain)
        domains.append(main_domain)
    return domains

def get_top_ngrams(corpus, ngram_range, stop_words=None, n=None):
    vec = CountVectorizer(stop_words=stop_words, ngram_range=ngram_range).fit(corpus)
    bag_of_words = vec.transform(corpus)

    sum_words = bag_of_words.sum(axis=0)

    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)

    common_words = words_freq[:n]
    words = []
    freqs = []
    for word, freq in common_words:
        words.append(word)
        freqs.append(freq)

    df = pd.DataFrame({'Word': words, 'Freq': freqs})
    return df
