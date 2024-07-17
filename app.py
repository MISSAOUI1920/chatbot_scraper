import streamlit as st
import wikipediaapi
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import spacy
import pytextrank

# Load spaCy model and add PyTextRank to the pipeline
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank")

# Initialize Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia(
    user_agent='MyProjectName (merlin@example.com)',
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI
)

def get_summary(input_text):
    # Process the input text with spaCy and PyTextRank
    doc = nlp(input_text)
    inp = doc._.phrases[:10][0].text

    # Fetch the Wikipedia page
    p_wiki = wiki_wiki.page(inp)

    if p_wiki.exists():
        # Prepare the text for summarization
        text = p_wiki.text
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()

        # Summarize the text
        summary = summarizer(parser.document, 4)  # Adjust the number of sentences as needed
        return [str(sentence) for sentence in summary]
    else:
        return ["The page does not exist."]

# Streamlit app
st.title("Chatbot Scraper")
st.write("Enter your query and get a summarized response from Wikipedia.")

input_text = st.text_input("Enter your query:")

if st.button("Get Summary"):
    if input_text:
        summary = get_summary(input_text)
        st.write("\n".join(summary))
    else:
        st.write("Please enter a query.")
