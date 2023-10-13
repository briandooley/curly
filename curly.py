import sys
import requests
from bs4 import BeautifulSoup, Comment
import re

def highlight_words_in_text(text):
    # Regex to match words in curly braces
    pattern = r'\{([^}]+)\}'

    # Replace matched words with highlighted versions
    def replace(match):
        word = match.group(1)
        return f'\033[91m{{{word}}}\033[0m' 

    return re.sub(pattern, replace, text)

def fetch_and_display_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Process text outside of HTML tags, code blocks, and lines starting with '$'
        for element in soup.find_all(string=True):
            if (
                element.parent.name not in ['script', 'style']
                and not isinstance(element, Comment)
                and all(keyword not in element.parent.get('class', []) for keyword in ['codeblock', 'programlisting'])
                and not element.strip().startswith('$')
                and not any(
                    ancestor.get('class', []) == ['codeblock__inner-wrapper']
                    for ancestor in element.parents
                )
            ):
                text = str(element)
                if re.search(r'\{([^}]+)\}', text):
                    highlighted_text = highlight_words_in_text(text)
                    print(highlighted_text)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    fetch_and_display_url_content(url)
