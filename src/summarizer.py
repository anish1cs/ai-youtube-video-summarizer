from transformers import pipeline

def summarize_text(text, length=100, model_name="facebook/bart-large-cnn"):
    """
    Summarizes the given text using a Hugging Face transformer model.

    Args:
        text (str): The input text to summarize.
        length (int): Target maximum length of the summary in tokens.
        model_name (str): Pretrained model name for summarization.

    Returns:
        str: The generated summary text.
    """
    summarizer = pipeline("summarization", model=model_name)
    result = summarizer(text, max_length=length, min_length=length // 2, do_sample=False)
    return result[0]['summary_text']
