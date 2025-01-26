from hazm import word_tokenize as hazm_tokenize  # Persian tokenization
import nltk
from nltk.tokenize import word_tokenize as nltk_tokenize  # English tokenization

# Ensure that NLTK punkt tokenizer is downloaded for English tokenization
nltk.download('punkt')


def tokenize_task_data(title, description):
    """
    Tokenize both task title and description, handling both English and Persian text.

    Args:
    - title (str): The title of the task (could be in English or Persian)
    - description (str): The description of the task (could be in English or Persian)

    Returns:
    - tuple: (title_tokens, description_tokens)
        title_tokens: List of tokens from the title (both English and Persian words)
        description_tokens: List of tokens from the description (both English and Persian words)
    """

    # Tokenize the title and description
    title_tokens = tokenize_text(title)
    description_tokens = tokenize_text(description)

    return title_tokens, description_tokens


def tokenize_text(text):
    """
    Tokenize text by detecting if it's Persian or English, and apply respective tokenizers.

    Args:
    - text (str): The text to tokenize (either in Persian or English)

    Returns:
    - list: Tokenized words
    """

    # Check if the text contains Persian characters
    if any('\u0600' <= char <= '\u06FF' for char in text):
        # If Persian, use Hazm for tokenization
        return hazm_tokenize(text)
    else:
        # If not Persian (assumed to be English), use NLTK for tokenization
        return nltk_tokenize(text)
