from keybert import KeyBERT

def extract_keywords(text, num_keywords=5):
    """
    Extracts key topics or phrases from the given text using KeyBERT.

    Args:
        text (str): The input text to analyze.
        num_keywords (int): The number of keywords/phrases to return.

    Returns:
        list[str]: List of extracted keywords/phrases.
    """
    try:
        model = KeyBERT()
        keywords = model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 2),  # Unigrams and bigrams
            stop_words='english',
            top_n=num_keywords
        )
        return [kw[0] for kw in keywords]
    except Exception as e:
        print(f"[ERROR] Keyword extraction failed: {e}")
        return []
