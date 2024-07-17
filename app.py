import wikipediaapi
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import spacy
import pytextrank
import streamlit as st  # Import Streamlit

# Load a spaCy model
nlp = spacy.load("en_core_web_sm")

# Add PyTextRank to the spaCy pipeline
nlp.add_pipe("textrank")

# Initialize the Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia(
    user_agent='MyProjectName (merlin@example.com)',
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI
)

# Streamlit app layout
st.title("Chatbot with TinyLLaMA Model")
st.write("Chat with the bot by entering your messages below.")

# Initialize the conversation history
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Text input widget for user message
user_input = st.text_input("You:", "")

# Generate response when the user submits a message
if st.button("Send"):
    if user_input:
        # Append user message to history
        st.session_state.history.append({"role": "user", "content": user_input})

        # Create a formatted input for the model
        conversation = ""
        for message in st.session_state.history:
            if message["role"] == "user":
                conversation += f"User: {message['content']}\n"
            else:
                conversation += f"Chatbot: {message['content']}\n"

        # Extract key phrases from the user input
        doc = nlp(user_input)
        if doc._.phrases:
            inp = doc._.phrases[0].text
            # Fetch the Wikipedia page for the user's input
            p_wiki = wiki_wiki.page(inp)
            if p_wiki.exists():
                text = p_wiki.text
                parser = PlaintextParser.from_string(text, Tokenizer("english"))
                summarizer = LsaSummarizer()

                # Summarize the text
                summary = summarizer(parser.document, 10)  # Adjust the number of sentences as needed

                # Create summary text
                intro_text = "\n".join([str(sentence) for sentence in summary])
            else:
                intro_text = "Page not found."
        else:
            intro_text = "No key phrases found."

        # Append the generated response to history
        st.session_state.history.append({"role": "chatbot", "content": intro_text})

# Display the conversation
for message in st.session_state.history:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**Chatbot:** {message['content']}")
