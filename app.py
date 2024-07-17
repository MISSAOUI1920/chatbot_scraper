import streamlit as st
import wikipediaapi
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import spacy
import pytextrank

# Load spaCy model and add PyTextRank to the pipeline
nlp = spacy.load("en_core_web_sm")

# Add PyTextRank to the spaCy pipeline
tr = pytextrank.TextRank()
nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)

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
st.title("Interactive Chatbot")

# Define a function to handle user input and display responses
def chatbot_response(user_input):
    if user_input.strip() == "":
        return "Please enter a query."

    # Get the summary based on user input
    summary = get_summary(user_input)

    # Return the summary as a formatted string
    return "\n".join(summary)

# Input box for user query
user_input = st.text_input("You: ", "")

# Button to trigger the response
if st.button("Ask"):
    response = chatbot_response(user_input)
    st.text_area("Chatbot:", value=response, height=150)

# Instructions
st.markdown("Ask a question and click 'Ask' to get a summarized response from Wikipedia.")
