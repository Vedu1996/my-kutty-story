import streamlit as st
from constants import genres, app_name
from storyteller import generate_story, generate_image_description
from openai import APIConnectionError
from artist import get_image

st.set_page_config(page_title=app_name, page_icon="📖", layout="wide")

st.title(app_name)

def check_selection():
    """Callback function to limit selections to 3"""
    if len(st.session_state.genre_selection) > 3:
      st.session_state.genre_selection = st.session_state.genre_selection[1:]

selected_genres = st.pills(
    "Pick up to 3 genres for your story",
    options=genres,
    selection_mode="multi",
    key="genre_selection",
    on_change=check_selection,
)

custom_characters = st.text_input(
    "Enter custom characters separated by commas (optional)",
    placeholder="e.g., Alice, Bob, Charlie",
    key="custom_characters"
)

num_paragraphs = st.slider(
    "How many paragraphs do you want in your story?",
    min_value=1,
    max_value=10,
    value=3,
    step=1,
    key="num_paragraphs"
)

render_images = True

def render_with_image(paragraph: str):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(paragraph)
    with col2:
        placeholder = st.empty()
        with placeholder:
          st.image("assets/placeholder.png", width=256)
        response = generate_image_description(paragraph)
        image_description = response.get("image_description", "")
        image_prompt = response.get("image_prompt", "")
        image = get_image(image_prompt)
        with placeholder:
          st.image(
              image,
              width=256,
          )
        st.caption(image_description)

def render_story_panel(paragraph: str):
    """Render the story panel."""
    if render_images:
      render_with_image(paragraph)
    else:
      st.markdown(paragraph)

def render_story(story: str):
    """Render the story with paragraphs."""
    paragraphs = story.split("\n\n")
    for paragraph in paragraphs:
        if paragraph.strip():
            render_story_panel(paragraph.strip())
            st.divider()

st.markdown('<div id="story"></div>', unsafe_allow_html=True)
if selected_genres and len(selected_genres) > 0 and num_paragraphs > 0:
    st.write("### Your Story Preview")
    st.write(f"**Selected Genres:** {', '.join(selected_genres)}")
    if custom_characters:
        st.write(f"**Custom Characters:** {custom_characters}")
    st.write(f"**Number of Paragraphs:** {num_paragraphs}")
    if st.button("Generate Story"):
          try:
            with st.spinner("Spinning up a kutty story...", show_time=True):
              story_content = generate_story(selected_genres, custom_characters, num_paragraphs)
              title, story, summary = story_content.get("title", ""), story_content.get("story", ""), story_content.get("summary", "")
              st.divider()
              st.header(title, anchor=title.replace(" ", "-").lower())
              if summary:
               st.html(f'<p style="color: grey">{summary}</p>')
              render_story(story)
              st.toast('Story generated successfully!', icon="✅")
          except APIConnectionError:
            st.error("Failed to connect to the story generation service. Please try again later.")
            st.stop()
          except Exception as e:
            st.error(f"An error occurred while generating the story.")
            print(e)
            st.stop()
          



