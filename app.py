import streamlit as st
import wikipediaapi

# Initialize the Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia('en')

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

        # Fetch the Wikipedia page for the user's input
        page = wiki_wiki.page(user_input)

        # Check if the page exists
        if not page.exists():
            intro_text = "Page not found."
        else:
            # Extract the full text of the page
            full_text = page.text

            # Get the title of the first section
            if page.sections:
                first_section_title = page.sections[0].title
            else:
                first_section_title = None

            # Find the position of the first section
            if first_section_title:
                first_section_pos = full_text.find(first_section_title)
                intro_text = full_text[:first_section_pos].strip()
            else:
                intro_text = full_text

        # Append the generated response to history
        st.session_state.history.append({"role": "chatbot", "content": intro_text})

# Display the conversation
for message in st.session_state.history:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**Chatbot:** {message['content']}")
