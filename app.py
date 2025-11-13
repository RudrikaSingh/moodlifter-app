import streamlit as st
import google.generativeai as genai
import requests

# Configure the API key from Streamlit's secrets
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception:
    st.error("API key not found! Please add it to your Streamlit secrets.")
    st.stop()

model = genai.GenerativeModel("gemini-pro")

# Streamlit UI
st.set_page_config(page_title="MoodLifter", page_icon="🌟")
st.title("🌟 MoodLifter – AI Compliment + Self-Care + Song 🌟")

mood = st.selectbox("How are you feeling today?", ["Happy", "Sad", "Tired", "Anxious", "Motivated", "Bored"])

if st.button("Lift My Mood"):
    if not mood:
        st.warning("Please select a mood first.")
    else:
        with st.spinner("Generating your vibe..."):
            prompt = f"""
            You are a kind, empathetic AI friend. Your task is to provide a thoughtful compliment and a short, actionable self-care tip for someone feeling {mood.lower()}.

            Format your response exactly like this:
            Compliment: <A warm and sincere compliment related to their strength in feeling this way.>
            Tip: <A simple, easy-to-do self-care tip.>
            """

            try:
                response = model.generate_content(prompt)
                output = response.text.strip()

                # Split compliment and tip
                compliment = "Could not generate a compliment."
                tip = "Could not generate a tip."
                
                lines = output.split('\n')
                for line in lines:
                    if line.startswith("Compliment:"):
                        compliment = line.replace("Compliment:", "").strip()
                    elif line.startswith("Tip:"):
                        tip = line.replace("Tip:", "").strip()

                # iTunes API for music suggestion
                song_markdown = "Song not found."
                try:
                    search_term = mood.lower()
                    res = requests.get(f"https://itunes.apple.com/search?term={search_term}&media=music&entity=song&limit=1")
                    res.raise_for_status() # Will raise an error for bad status codes
                    song_data = res.json()
                    if song_data.get("resultCount", 0) > 0:
                        track = song_data["results"][0]
                        song_markdown = f"🎵 **[{track['trackName']} by {track['artistName']}]({track['trackViewUrl']})**"
                except requests.exceptions.RequestException as e:
                    song_markdown = f"🎵 Could not fetch a song suggestion: {e}"

                # Display results
                st.subheader("💬 A little something for you...")
                st.write(compliment)

                st.subheader("💡 Self-Care Tip")
                st.write(tip)

                st.subheader("🎶 Mood Song")
                st.markdown(song_markdown, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
