import streamlit as st
import google.generativeai as genai
import requests

# Configure the API key from Streamlit's secrets
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception:
    st.error("API key not found! Please add it to your Streamlit secrets.")
    st.stop()
model = genai.GenerativeModel("gemini-1.5-flash")


# Streamlit UI
st.set_page_config(page_title="MoodLifter", page_icon="🌟")
st.title("🌟 MoodLifter – AI Compliment + Self-Care + Song 🌟")

mood = st.selectbox("How are you feeling today?", ["Happy", "Sad", "Tired", "Anxious", "Motivated", "Bored"])

if st.button("Lift My Mood"):
    if not mood:
        st.warning("Please select a mood first.")
    else:
        with st.spinner("Generating your vibe... (Running Test)"):
            try:
                # --- 1. (SKIPPED) GENERATE AI CONTENT ---
                # We are skipping the AI call to see if it's the part that hangs
                st.write("DEBUG: AI Call is SKIPPED.") # Debug message

                # --- 2. (MOCKED) PARSE AI CONTENT ---
                # We will use 'mock' data instead
                compliment = "This is a test compliment to see if the app works."
                tip = "This is a test self-care tip."
                st.write("DEBUG: Mock content is ready.") # Debug message


                # --- 3. FETCH SONG FROM ITUNES ---
                st.write("DEBUG: Attempting to fetch song from iTunes...") # Debug message
                song_markdown = "Song not found."
                try:
                    search_term = mood.lower()
                    res = requests.get(
                        f"https://itunes.apple.com/search?term={search_term}&media=music&entity=song&limit=1",
                        timeout=10 
                    )
                    res.raise_for_status() 
                    song_data = res.json()
                    if song_data.get("resultCount", 0) > 0:
                        track = song_data["results"][0]
                        song_markdown = f"🎵 **[{track['trackName']} by {track['artistName']}]({track['trackViewUrl']})**"
                    
                    st.write("DEBUG: Song fetch finished.") # Debug message

                except requests.exceptions.RequestException as e:
                    st.warning(f"Could not fetch song suggestion: {e}")
                    song_markdown = "🎵 Could not fetch a song suggestion."

                # --- 4. DISPLAY RESULTS ---
                st.subheader("💬 A little something for you...")
                st.write(compliment)

                st.subheader("💡 Self-Care Tip")
                st.write(tip)

                st.subheader("🎶 Mood Song")
                st.markdown(song_markdown, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {e}")
                st.exception(e)