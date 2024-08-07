# import os
import re
# import sys
from urllib.parse import urlparse
from publicsuffix2 import get_sld

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

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

def clean_text(text):
  text = str(text)
  # Transform to lowercase
  text = text.lower()
  # Remove digits
  text = ''.join([c for c in text if not c.isdigit()])
  return text

def remove_hyperlinks(text):
  pattern = r'https?://[^\s]+'
  text_nolinks = re.sub(pattern, '', text)
  return text_nolinks

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

def extract_terms(description,terms):
    description = description.lower()
    return [keyword for keyword in terms if keyword in description.lower()]

def bold_fraktur_to_regular(text):
    # Mapping of Bold Fraktur characters to regular characters
    bold_fraktur_map = {
        '𝗔': 'A', '𝗕': 'B', '𝗖': 'C', '𝗗': 'D', '𝗘': 'E', '𝗙': 'F', '𝗚': 'G',
        '𝗛': 'H', '𝗜': 'I', '𝗝': 'J', '𝗞': 'K', '𝗟': 'L', '𝗠': 'M', '𝗡': 'N',
        '𝗢': 'O', '𝗣': 'P', '𝗤': 'Q', '𝗥': 'R', '𝗦': 'S', '𝗧': 'T', '𝗨': 'U',
        '𝗩': 'V', '𝗪': 'W', '𝗫': 'X', '𝗬': 'Y', '𝗭': 'Z', '𝗮': 'a', '𝗯': 'b',
        '𝗰': 'c', '𝗱': 'd', '𝗲': 'e', '𝗳': 'f', '𝗴': 'g', '𝗵': 'h', '𝗶': 'i',
        '𝗷': 'j', '𝗸': 'k', '𝗹': 'l', '𝗺': 'm', '𝗻': 'n', '𝗼': 'o', '𝗽': 'p',
        '𝗾': 'q', '𝗿': 'r', '𝘀': 's', '𝘁': 't', '𝘂': 'u', '𝘃': 'v', '𝘄': 'w',
        '𝘅': 'x', '𝘆': 'y', '𝘇': 'z'
    }

    # Convert text using the mapping
    regular_text = ''.join(bold_fraktur_map.get(char, char) for char in text)
    return regular_text

def count_next_word_after(tokens,keyword):
  """
  This function takes a string and counts the occurrences of the next word after keywords

  Args:
    text (str): The input string to analyze.

  Returns:
    Counter: A Counter object containing the counts of words following keywords.
  """

  # tokens = nltk.word_tokenize(text.lower())
  next_words_counter = Counter()

  for i in range(len(tokens) - 1):
    if tokens[i] in keywords:
      next_word = tokens[i + 1]
      next_words_counter[next_word] += 1

  return next_words_counter