import streamlit as st
import os
import sys
import time
import random
import urllib.request
import json
import io
import math
import struct

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="The Secret of Blackwood Manor",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SYNTH RETRO AUDIO CHIMES (Browser-Side WAV Synth) ---
def generate_beep_wav(frequencies, durations, volume=0.2, sample_rate=11025):
    """Generates synthetic WAV file bytes for a sequence of beep tones."""
    wav_io = io.BytesIO()
    try:
        import wave
        with wave.open(wav_io, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2) # 16-bit PCM
            wav_file.setframerate(sample_rate)
            
            for freq, dur in zip(frequencies, durations):
                num_samples = int(sample_rate * (dur / 1000.0))
                for i in range(num_samples):
                    t = float(i) / sample_rate
                    val = math.sin(2.0 * math.pi * freq * t)
                    # Smooth linear fade out in the last 15% to avoid audio pops
                    fade_start = int(num_samples * 0.85)
                    if i > fade_start:
                        scale = 1.0 - (float(i - fade_start) / (num_samples - fade_start))
                        val *= scale
                    sample = int(val * volume * 32767)
                    wav_file.writeframesraw(struct.pack('<h', sample))
    except Exception:
        pass
    return wav_io.getvalue()

def play_audio_chime(chime_type):
    """Generates and autoplays WAV bytes inside Streamlit for browser-side chimes."""
    if chime_type == "clue":
        data = generate_beep_wav([523, 659, 784], [120, 120, 180])
    elif chime_type == "contradiction":
        data = generate_beep_wav([523, 523, 659, 784], [100, 100, 150, 250])
    elif chime_type == "twist":
        data = generate_beep_wav([220, 207, 196], [300, 300, 400])
    elif chime_type == "success":
        data = generate_beep_wav([523, 659, 784, 1046], [120, 120, 120, 300])
    elif chime_type == "failure":
        data = generate_beep_wav([392, 349, 311, 262], [200, 200, 200, 400])
    else:
        return
    st.audio(data, format="audio/wav", autoplay=True)

# --- DETECTIVE THEMES (Theme-Synced CSS Variables) ---
def inject_custom_css():
    theme = st.session_state.get("theme", "dark")
    if theme == "dark":
        primary_color = "#D4AF37"  # Gold accent
        bg_color = "#121212"       # Dark charcoal
        card_bg = "#1E1E1E"        # Dark grey card
        text_color = "#E0E0E0"
        title_color = "#D4AF37"
        border_color = "#2D2D2D"
        accent_blue = "#4A90E2"
        success_green = "#2ECC71"
        error_red = "#E74C3C"
        sidebar_bg = "#1A1A1A"
    else:
        primary_color = "#8B0000"  # Burgundy accent
        bg_color = "#FDFBF7"       # Cream parchment
        card_bg = "#F5F2EB"        # Warm card panel
        text_color = "#2C2C2C"
        title_color = "#8B0000"
        border_color = "#D3C2A0"
        accent_blue = "#0056B3"
        success_green = "#196F3D"
        error_red = "#922B21"
        sidebar_bg = "#F0EAD6"

    css = f"""
    <style>
    /* Hide default streamlit audio controls completely */
    div[data-testid="stAudio"] {{
        display: none !important;
    }}
    
    .stApp {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}
    
    /* Sidebar customization */
    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {border_color};
    }}
    
    h1, h2, h3, h4 {{
        color: {title_color} !important;
        font-family: 'Georgia', serif;
    }}
    
    /* Premium Styled Cards */
    .mystery-card {{
        background-color: {card_bg};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.15);
    }}
    
    .suspect-card-box {{
        background-color: {card_bg};
        border: 1px solid {border_color};
        border-top: 4px solid {primary_color};
        border-radius: 6px;
        padding: 15px;
        margin-bottom: 12px;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
    }}
    
    .clue-locker-card {{
        background-color: {card_bg};
        border-left: 4px solid {primary_color};
        border-radius: 4px;
        padding: 12px;
        margin-bottom: 10px;
        box-shadow: 1px 1px 4px rgba(0,0,0,0.08);
    }}
    
    /* Badges */
    .hud-badge {{
        background-color: {primary_color};
        color: {"#121212" if theme == "dark" else "#FFFFFF"};
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 13px;
        display: inline-block;
        margin-bottom: 5px;
    }}
    
    .stProgress > div > div > div > div {{
        background-color: {primary_color} !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- DYNAMIC CRIME SCENE FLOOR PLAN (Theme-Synced CSS Grid) ---
def render_study_diagram():
    theme = st.session_state.get("theme", "dark")
    if theme == "dark":
        v_bg = "rgba(231, 76, 60, 0.2)"
        v_border = "#E74C3C"
        f_bg = "rgba(212, 175, 55, 0.15)"
        f_border = "#D4AF37"
        e_bg = "rgba(46, 204, 113, 0.15)"
        e_border = "#2ECC71"
        border = "#444444"
        text = "#E0E0E0"
    else:
        v_bg = "rgba(146, 43, 33, 0.15)"
        v_border = "#922B21"
        f_bg = "rgba(139, 0, 0, 0.1)"
        f_border = "#8B0000"
        e_bg = "rgba(25, 111, 61, 0.1)"
        e_border = "#196F3D"
        border = "#C0B090"
        text = "#2C2C2C"

    html = f"""
    <body style="background-color: transparent; margin: 0; padding: 0; overflow: hidden;">
    <div style="text-align: center; margin-bottom: 10px; font-family: 'Georgia', serif; color: {text};">
        <h4 style="margin: 0; font-size: 16px;">🗺️ Study Floor Plan (Crime Scene)</h4>
        <span style="font-size: 11px; opacity: 0.8;">Colors adjust automatically to theme toggle</span>
    </div>
    <div style="
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 6px;
        background-color: transparent;
        padding: 5px;
        border: 1px solid {border};
        border-radius: 8px;
        max-width: 100%;
        width: 100%;
        margin: 0 auto;
        font-family: 'Courier New', monospace;
        color: {text};
        font-size: 10px;
    ">
        <!-- Row 0 -->
        <div style="border: 1px solid {f_border}; background-color: {f_bg}; border-radius: 4px; padding: 8px 2px; text-align: center; word-wrap: break-word;">
            <strong>DESK</strong><br><span style="font-size: 8px; opacity: 0.8;">Mahogany</span>
        </div>
        <div style="border: 2px solid {v_border}; background-color: {v_bg}; border-radius: 4px; padding: 8px 2px; text-align: center; box-shadow: 0 0 5px {v_border}; word-wrap: break-word;">
            <strong>💀 BODY</strong><br><span style="font-size: 8px; opacity: 0.8; font-weight: bold;">Slumped</span>
        </div>
        <div style="border: 1px solid {e_border}; background-color: {e_bg}; border-radius: 4px; padding: 8px 2px; text-align: center; word-wrap: break-word;">
            <strong>🔍 GLASS</strong><br><span style="font-size: 8px; opacity: 0.8;">Whiskey</span>
        </div>
        <div style="border: 1px solid {e_border}; background-color: {e_bg}; border-radius: 4px; padding: 8px 2px; text-align: center; word-wrap: break-word;">
            <strong>📄 WILL</strong><br><span style="font-size: 8px; opacity: 0.8;">Drawer</span>
        </div>

        <!-- Row 1 -->
        <div style="border: 1px solid {f_border}; background-color: {f_bg}; border-radius: 4px; padding: 8px 2px; text-align: center; word-wrap: break-word;">
            <strong>SHELVES</strong><br><span style="font-size: 8px; opacity: 0.8;">Books</span>
        </div>
        <div style="border: 1px solid {f_border}; background-color: {f_bg}; border-radius: 4px; padding: 8px 2px; text-align: center; word-wrap: break-word;">
            <strong>CHAIR</strong><br><span style="font-size: 8px; opacity: 0.8;">Armchair</span>
        </div>
        <div style="border: 1px dashed {border}; border-radius: 4px; padding: 8px 2px; text-align: center; opacity: 0.4; word-wrap: break-word;">
            <strong>FLOOR</strong><br><span style="font-size: 8px; opacity: 0.8;">Carpet</span>
        </div>
        <div style="border: 1px solid {e_border}; background-color: {e_bg}; border-radius: 4px; padding: 8px 2px; text-align: center; word-wrap: break-word;">
            <strong>💎 PEARL</strong><br><span style="font-size: 8px; opacity: 0.8;">Earring</span>
        </div>

        <!-- Row 2 -->
        <div style="border: 1px solid {f_border}; background-color: {f_bg}; border-radius: 4px; padding: 8px 2px; text-align: center; word-wrap: break-word;">
            <strong>FIREPLACE</strong><br><span style="font-size: 8px; opacity: 0.8;">Hearth</span>
        </div>
        <div style="border: 1px solid {border}; border-radius: 4px; padding: 8px 2px; text-align: center; word-wrap: break-word;">
            <strong>🚪 DOOR</strong><br><span style="font-size: 8px; opacity: 0.8;">to Foyer</span>
        </div>
        <div style="border: 1px solid {border}; border-radius: 4px; padding: 8px 2px; text-align: center; word-wrap: break-word;">
            <strong>🚪 DOOR</strong><br><span style="font-size: 8px; opacity: 0.8;">to Library</span>
        </div>
        <div style="border: 1px dashed {border}; border-radius: 4px; padding: 8px 2px; text-align: center; opacity: 0.4; word-wrap: break-word;">
            <strong>WINDOW</strong><br><span style="font-size: 8px; opacity: 0.8;">Locked</span>
        </div>
    </div>
    </body>
    """
    st.components.v1.html(html, height=310)

# --- DYNAMIC MANOR MAP (Theme-Synced Layout) ---
def render_manor_map():
    current = st.session_state.current_room
    theme = st.session_state.theme
    
    def get_style(room_id):
        if room_id == current:
            fill = "#D4AF37" if theme == "dark" else "#8B0000"
            stroke = "#FFFFFF"
            stroke_width = "2"
            text_color = "#121212" if theme == "dark" else "#FFFFFF"
        else:
            fill = "#1E1E1E" if theme == "dark" else "#F5F2EB"
            stroke = "#444444" if theme == "dark" else "#D3C2A0"
            stroke_width = "1"
            text_color = "#E0E0E0" if theme == "dark" else "#2C2C2C"
        return fill, stroke, stroke_width, text_color

    border_color = "#444444" if theme == "dark" else "#D3C2A0"
    line_color = "#D4AF37" if theme == "dark" else "#8B0000"
    bg_svg = "transparent"
    
    # Study style
    s_fill, s_stroke, s_sw, s_txt = get_style('study')
    # Library style
    lib_fill, lib_stroke, lib_sw, lib_txt = get_style('library')
    # Foyer style
    foy_fill, foy_stroke, foy_sw, foy_txt = get_style('foyer')
    # Lounge style
    lng_fill, lng_stroke, lng_sw, lng_txt = get_style('lounge')
    # Conservatory style
    con_fill, con_stroke, con_sw, con_txt = get_style('conservatory')

    html = f"""
    <body style="background-color: transparent; margin: 0; padding: 0; overflow: hidden; display: flex; justify-content: center; align-items: center;">
    <svg viewBox="0 0 500 280" style="width: 100%; max-width: 500px; height: auto; background-color: {bg_svg}; font-family: Arial, sans-serif; border: 1px solid {border_color}; border-radius: 8px;">
        <!-- Connecting lines -->
        <line x1="165" y1="42.5" x2="335" y2="42.5" stroke="{line_color}" stroke-width="3" />
        <line x1="95" y1="70" x2="95" y2="145" stroke="{line_color}" stroke-width="3" />
        <line x1="405" y1="70" x2="405" y2="145" stroke="{line_color}" stroke-width="3" />
        <line x1="140" y1="180" x2="220" y2="180" stroke="{line_color}" stroke-width="3" />
        <line x1="280" y1="180" x2="360" y2="180" stroke="{line_color}" stroke-width="3" />
        <line x1="250" y1="165" x2="250" y2="205" stroke="{line_color}" stroke-width="3" />

        <!-- Study Node -->
        <g>
            <rect x="25" y="15" width="140" height="55" rx="6" fill="{s_fill}" stroke="{s_stroke}" stroke-width="{s_sw}" />
            <text x="95" y="40" fill="{s_txt}" font-weight="bold" font-size="11" text-anchor="middle">STUDY</text>
            <text x="95" y="52" fill="{s_txt}" font-size="9" text-anchor="middle" opacity="0.8">(Crime Scene)</text>
        </g>

        <!-- Library Node -->
        <g>
            <rect x="335" y="15" width="140" height="55" rx="6" fill="{lib_fill}" stroke="{lib_stroke}" stroke-width="{lib_sw}" />
            <text x="405" y="48" fill="{lib_txt}" font-weight="bold" font-size="11" text-anchor="middle">LIBRARY</text>
        </g>

        <!-- Foyer Node -->
        <g>
            <rect x="180" y="110" width="140" height="55" rx="6" fill="{foy_fill}" stroke="{foy_stroke}" stroke-width="{foy_sw}" />
            <text x="250" y="143" fill="{foy_txt}" font-weight="bold" font-size="11" text-anchor="middle">FOYER</text>
        </g>

        <!-- Lounge Node -->
        <g>
            <rect x="25" y="205" width="140" height="55" rx="6" fill="{lng_fill}" stroke="{lng_stroke}" stroke-width="{lng_sw}" />
            <text x="95" y="238" fill="{lng_txt}" font-weight="bold" font-size="11" text-anchor="middle">LOUNGE</text>
        </g>

        <!-- Conservatory Node -->
        <g>
            <rect x="335" y="205" width="140" height="55" rx="6" fill="{con_fill}" stroke="{con_stroke}" stroke-width="{con_sw}" />
            <text x="405" y="238" fill="{con_txt}" font-weight="bold" font-size="11" text-anchor="middle">CONSERVATORY</text>
        </g>
    </svg>
    </body>
    """
    st.components.v1.html(html, height=290)

# --- API CASE GENERATION ---
def load_api_key():
    # 1. Check Streamlit Secrets (for cloud deployment)
    try:
        if "GEMINI_API_KEY" in st.secrets:
            key = st.secrets["GEMINI_API_KEY"]
            if key:
                return key.strip().strip("'\"").strip()
    except Exception:
        pass

    # 2. Check environment variable
    key = os.environ.get("GEMINI_API_KEY", "").strip().strip("'\"").strip()
    if key:
        return key
    if os.path.exists(".env"):
        try:
            with open(".env", "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("GEMINI_API_KEY="):
                        key = line.split("=", 1)[1].strip().strip("'\"").strip()
                        if key:
                            return key
        except Exception:
            pass
    return ""

def generate_ai_case(api_key):
    prompt = (
        "You are an expert murder mystery writer. Generate a completely new, unique, "
        "and logical murder mystery case for a text-based game. "
        "Your output MUST be a single, valid JSON object matching this schema EXACTLY:\n\n"
        "{\n"
        '  "victim": { "name": "Victim\'s Full Name", "desc": "Short description of victim" },\n'
        '  "suspects": {\n'
        '    "suspect_1": {\n'
        '      "name": "Suspect 1 Full Name",\n'
        '      "role": "Relationship to victim (e.g. Spouse, Partner, Doctor)",\n'
        '      "description": "Short visual description of suspect",\n'
        '      "alibi": "Public alibi statement",\n'
        '      "motive": "Why they wanted the victim dead",\n'
        '      "dialogue": {\n'
        '        "alibi": "Response about their alibi",\n'
        '        "motive": "Response about their motive",\n'
        '        "secret": "Response about their secrets",\n'
        '        "about_1": "Their opinion on suspect 1",\n'
        '        "about_2": "Their opinion on suspect 2",\n'
        '        "about_3": "Their opinion on suspect 3",\n'
        '        "about_clue_1": "What they say about clue 1",\n'
        '        "about_clue_2": "What they say about clue 2",\n'
        '        "about_clue_3": "What they say about clue 3. Note: If this is their alibi contradiction clue, this string must contain \\"[CONTRADICTION FOUND!]\\" followed by their nervous confession explaining how their alibi is broken.",\n'
        '        "about_clue_4": "What they say about clue 4 (similar to above)",\n'
        '        "about_clue_5": "What they say about clue 5 (similar)",\n'
        '        "about_clue_6": "What they say about clue 6 (similar)",\n'
        '        "about_clue_7": "What they say about clue 7 (similar)"\n'
        '      }\n'
        '    },\n'
        '    "suspect_2": { ... },\n'
        '    "suspect_3": { ... }\n'
        '  },\n'
        '  "clues": {\n'
        '    "clue_1": { "name": "Clue 1 Name", "description": "Clue 1 description", "room": "foyer|study|library|conservatory|lounge" },\n'
        '    "clue_2": { "name": "Clue 2 Name", "description": "Clue 2 description", "room": "..." },\n'
        '    "clue_3": { "name": "Clue 3 Name", "description": "Clue 3 description", "room": "..." },\n'
        '    "clue_4": { "name": "Clue 4 Name", "description": "Clue 4 description", "room": "..." },\n'
        '    "clue_5": { "name": "Clue 5 Name", "description": "Clue 5 description", "room": "..." },\n'
        '    "clue_6": { "name": "Clue 6 Name", "description": "Clue 6 description", "room": "..." },\n'
        '    "clue_7": { "name": "Clue 7 Name", "description": "Clue 7 description", "room": "..." }\n'
        '  },\n'
        '  "killer_id": "suspect_1|suspect_2|suspect_3",\n'
        '  "weapon_clue_id": "clue_1",\n'
        '  "proof_clue_id": "clue_2",\n'
        '  "suspect_1_contradiction_clue_id": "clue_3",\n'
        '  "suspect_2_contradiction_clue_id": "clue_4",\n'
        '  "suspect_3_contradiction_clue_id": "clue_5"\n'
        '}\n\n'
        "Rules:\n"
        "- The Study (study) is the CRIME SCENE. The murder weapon (weapon_clue_id) MUST be hidden in the study.\n"
        "- The proof clue (proof_clue_id) must be key evidence linking the killer to the crime.\n"
        "- Place at least 2 clues in the study (crime scene).\n"
        "- Suspect 1 alibi is contradicted by suspect_1_contradiction_clue_id.\n"
        "- Suspect 2 alibi is contradicted by suspect_2_contradiction_clue_id.\n"
        "- Suspect 3 alibi is contradicted by suspect_3_contradiction_clue_id.\n"
        "- Return JSON ONLY. Do not write markdown tags like ```json or ```."
    )
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=40) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            text_response = res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
            if text_response.startswith("```json"):
                text_response = text_response[7:]
            elif text_response.startswith("```"):
                text_response = text_response[3:]
            if text_response.endswith("```"):
                text_response = text_response[:-3]
            text_response = text_response.strip()
            return json.loads(text_response)
    except Exception as e:
        return None

def generate_ai_plot_twist():
    api_key = load_api_key()
    if not api_key:
        return None
        
    suspect_info = []
    for s_id, s in st.session_state.SUSPECTS.items():
        suspect_info.append(f"- {s['name']} ({s['role']}): Alibi was '{s['alibi']}'")
    suspects_summary = "\n".join(suspect_info)
    
    prompt = (
        f"You are a master mystery writer. Introduce a sudden plot twist to our current case.\n\n"
        f"Current Victim: {st.session_state.victim_name}\n"
        f"Suspects involved:\n{suspects_summary}\n\n"
        "Your twist must belong to exactly one of these types:\n"
        "1. 'Hidden Witness' (e.g., a maid saw someone creep near the study)\n"
        "2. 'Secret Motive' (e.g., a hidden affair or a second secret will)\n"
        "3. 'Fake Alibi' (e.g., a suspect's alibi is broken by a timestamp check)\n\n"
        "Generate a coherent and surprising twist that fits this specific case.\n"
        "Your output MUST be a single, valid JSON object matching this schema exactly:\n"
        "{\n"
        '  "type": "Hidden Witness|Secret Motive|Fake Alibi",\n'
        '  "title": "Title of the Twist",\n'
        '  "description": "Details of the plot twist written in an engaging, detective-story style."\n'
        "}\n"
        "Return JSON ONLY. Do not write markdown tags like ```json."
    )
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            text_response = res_data["candidates"][0]["content"]["parts"][0]["text"].strip()
            if text_response.startswith("```json"):
                text_response = text_response[7:]
            elif text_response.startswith("```"):
                text_response = text_response[3:]
            if text_response.endswith("```"):
                text_response = text_response[:-3]
            text_response = text_response.strip()
            return json.loads(text_response)
    except Exception:
        return None

def trigger_plot_twist_event():
    st.session_state.plot_twist_triggered = True
    twist_data = generate_ai_plot_twist()
    
    if not twist_data:
        default_twists = [
            {
                "type": "Secret Motive",
                "title": "The Threatened Exposure Letter",
                "description": "You discover a hidden lockbox in the Study containing a draft letter. Lord Harrington had discovered the killer's financial embezzlements and wrote that they would report them to the police the very next morning. This gave the killer an extremely urgent motive to commit the crime tonight!"
            },
            {
                "type": "Hidden Witness",
                "title": "The Silent Servant",
                "description": "An aged maid, trembling with fear, pulls you aside in the hallway. She whispers that at exactly 9:15 PM, she saw someone creeping quietly towards the Study door wearing dark medical gloves and holding something concealed in their hand."
            },
            {
                "type": "Fake Alibi",
                "title": "The Frozen Pocketwatch",
                "description": "You notice a shattered pocketwatch dropped near the foyer floorboards. The glass is crushed and the hands are frozen precisely at 8:45 PM. This physical timestamp completely contradicts one of the suspect's timeline statements!"
            }
        ]
        victim_name = st.session_state.victim_name
        # Customize victim name in description if default offline twist is used
        for twist in default_twists:
            twist["description"] = twist["description"].replace("Lord Harrington", victim_name)
        
        twist_data = random.choice(default_twists)
    
    st.session_state.plot_twist_data = twist_data
    st.session_state.detective_score += 15
    st.session_state.audio_trigger = "twist"
    st.session_state.custom_notes += f"\n[PLOT TWIST - {twist_data['type']}] {twist_data['title']}: {twist_data['description']}"
    st.session_state.feedback = f"PLOT TWIST TRIGGERED: {twist_data['title']} (+15 pts)"
    update_difficulty()

# --- STATE INITIALIZATION & RESET ---
def init_game_state(force_reset=False, custom_api_key=""):
    if "initialized" not in st.session_state or not st.session_state.initialized or force_reset:
        st.session_state.initialized = False
        st.session_state.victim_name = "Lord Reginald Harrington"
        st.session_state.victim_desc = "a wealthy philanthropist and art collector"
        
        # Room connection mappings
        st.session_state.ROOMS = {
            "foyer": {
                "name": "The Foyer",
                "description": "The grand entrance hall of Blackwood Manor. A large chandelier hangs from the ceiling.",
                "connections": ["study", "library", "lounge", "conservatory"],
                "clues": [],
                "suspects": []
            },
            "study": {
                "name": "The Study (CRIME SCENE)",
                "description": "The official CRIME SCENE where the victim's body was found slumped at his desk.",
                "connections": ["foyer", "library"],
                "clues": ["whiskey_glass", "will_papers", "pearl_earring"],
                "suspects": []
            },
            "library": {
                "name": "The Library",
                "description": "A quiet room filled with tall, dusty bookshelves and a warm, crackling fireplace.",
                "connections": ["foyer", "study"],
                "clues": ["ledger_page"],
                "suspects": ["lady_eleanor"]
            },
            "conservatory": {
                "name": "The Conservatory",
                "description": "A glass greenhouse filled with damp air and exotic, shadow-casting plants.",
                "connections": ["foyer"],
                "clues": ["latex_glove"],
                "suspects": ["dr_croft"]
            },
            "lounge": {
                "name": "The Lounge",
                "description": "A comfortable room containing a green-felt billiard table, leather armchairs, and a drinks cabinet.",
                "connections": ["foyer"],
                "clues": ["bookie_letter", "billiard_cover"],
                "suspects": ["arthur"]
            }
        }
        
        # Default Clues
        st.session_state.CLUES = {
            "whiskey_glass": {
                "name": "Poisoned Whiskey Glass",
                "description": "A crystal glass on Lord Harrington's desk smelling of bitter almonds (a sign of Aconite poison)."
            },
            "will_papers": {
                "name": "Confidential Will",
                "description": "Signed papers in the study desk showing Lord Harrington was cutting off Lady Eleanor completely."
            },
            "ledger_page": {
                "name": "Torn Ledger Page",
                "description": "A discarded sheet detailing a charity audit showing 'J.C.' embezzled £50,000 from Lord Harrington's funds."
            },
            "bookie_letter": {
                "name": "Threatening Letter",
                "description": "A bookie letter addressed to Arthur Harrington demanding £20,000 immediately."
            },
            "pearl_earring": {
                "name": "Dropped Pearl Earring",
                "description": "A white pearl earring found on the floor of the Study (Crime Scene). It matches Lady Eleanor's set."
            },
            "billiard_cover": {
                "name": "Dusty Billiard Cover",
                "description": "A thick, dusty canvas cover completely draped over the billiard table. It hasn't been removed in weeks."
            },
            "latex_glove": {
                "name": "Stained Latex Glove",
                "description": "A medical glove in the Conservatory bin, stained with whiskey and trace elements of Aconite."
            }
        }
        
        # Default Suspects
        st.session_state.SUSPECTS = {
            "lady_eleanor": {
                "name": "Lady Eleanor Harrington",
                "role": "The Estranged Wife",
                "description": "The elegant wife of the victim. She stands tall, wearing black lace and looking cold.",
                "alibi": "I was in the Library reading my historical novel all evening. I did not go to any other rooms, especially not the Study.",
                "motive": "Yes, Lord Harrington and I had our disagreements, but I would not resort to murder.",
                "dialogue": {
                    "alibi": "I went to the Library around 7 PM and stayed there until the housekeeper found him. I did not leave the room.",
                    "motive": "He was planning to divorce me and leave me with nothing, but I would have fought him in court, not poisoned Lord Harrington.",
                    "secret": "We argued in the study before dinner because he was being unreasonable. But that is all.",
                    "about_arthur": "Arthur is a foolish boy who spends too much money gambling. But he is not a murderer.",
                    "about_croft": "Dr. Croft has been our doctor for years. My husband trusted him completely with charity accounts.",
                    "about_whiskey_glass": "Lord Harrington always had a glass of whiskey before bed. He kept the bottle in his study.",
                    "about_will_papers": "So you found the will. Yes, he wanted to cut me off. He was a cruel partner.",
                    "about_ledger_page": "A ledger page? I know nothing of charity finances. Dr. Croft managed those accounts.",
                    "about_bookie_letter": "Another one of Arthur's debts... It is disappointing.",
                    "about_pearl_earring": "My... pearl earring? You found it in the Study? [CONTRADICTION FOUND!] Oh dear... okay, fine. I did slip into the Study briefly after dinner to look for the Will. I lied because I was terrified of being suspected. But he was already dead when I got there, I swear!",
                    "about_billiard_cover": "I know nothing of Arthur's games.",
                    "about_latex_glove": "Medical gloves? Those belong to Dr. Croft, surely."
                }
            },
            "arthur": {
                "name": "Arthur Harrington",
                "role": "The Spendthrift Son",
                "description": "The victim's son. He looks disheveled, nervously tapping his foot and biting his nails.",
                "alibi": "I was in the Lounge playing billiards all evening. I never left.",
                "motive": "Sure, my dad and I didn't get along, and he cut off my allowance. But I wouldn't kill him!",
                "dialogue": {
                    "alibi": "I was in the Lounge knocking balls around from 8 PM onwards. Ask anyone.",
                    "motive": "He expected me to be perfect. When I wasn't, he cut me off. I needed help, not lectures.",
                    "secret": "Fine! I have massive gambling debts. But murder doesn't pay debts, inheritance does... wait, that came out wrong!",
                    "about_eleanor": "My stepmother Eleanor? She's cold as ice. I saw them shouting at each other today in the study.",
                    "about_croft": "Dr. Croft? Dad's physician. He's always around talking about his botanical laboratory experiments.",
                    "about_whiskey_glass": "Dad drank whiskey. A lot. I saw someone leave the study with a glass earlier, but I couldn't see who.",
                    "about_will_papers": "A new Will? Wow. I didn't know he was actually going through with it. Eleanor must have been furious.",
                    "about_ledger_page": "Discrepancies? I don't know anything about dad's charity ledger. Talk to Dr. Croft.",
                    "about_bookie_letter": "Please, Detective, don't show that to the police! I was going to ask my father for one last loan.",
                    "about_pearl_earring": "Eleanor's jewelry? She wears them constantly.",
                    "about_billiard_cover": "Wait... you found the table covered in dust? [CONTRADICTION FOUND!] Ah... you caught me. I didn't play billiards. I was actually sitting in the corner drinking alone, trying to summon the courage to ask my father for money. I was ashamed to admit it.",
                    "about_latex_glove": "I don't use medical gloves."
                }
            },
            "dr_croft": {
                "name": "Dr. Julian Croft",
                "role": "The Family Physician",
                "description": "The family doctor. He looks calm and professional, cleaning his glasses with a cloth.",
                "alibi": "I was in the Conservatory cataloging botanical specimens all evening.",
                "motive": "Lord Harrington was my dearest friend. I have no reason to wish him harm.",
                "dialogue": {
                    "alibi": "I was in the Conservatory from 7:30 PM until I heard the screams. I was sorting through my collection.",
                    "motive": "We were co-founders of the charity. Our friendship was built on mutual respect.",
                    "secret": "I have nothing to hide, Inspector. I spent my evening in study and observation.",
                    "about_eleanor": "Lady Eleanor is a proud woman. Her marriage to Lord Harrington was a union of convenience. They argued frequently.",
                    "about_arthur": "Arthur is a troubled young man. His gambling habits are a tragedy, and Lord Harrington was incredibly disappointed in him.",
                    "about_whiskey_glass": "Aconite in his whiskey? Horrible. Aconite causes swift cardiorespiratory failure. It is a terrible way to die.",
                    "about_will_papers": "Ah, Lord Harrington mentioned he was considering a new Will. Eleanor stood to lose everything.",
                    "about_ledger_page": "A charity ledger page? Let me see... I-I don't recognize this. This looks like a draft. Our accounts are in perfect order.",
                    "about_bookie_letter": "Ah, another threat to Arthur. It seems Arthur had a powerful motive.",
                    "about_pearl_earring": "Lady Eleanor's earring? I believe I saw her wearing it earlier.",
                    "about_billiard_cover": "Arthur playing billiards? He spends more time drinking than playing.",
                    "about_latex_glove": "A latex glove stained with medical solution and whiskey? [CONTRADICTION FOUND!] Wait, that solution is from my laboratory... Ah! I must have dropped it when I was examining Lord Harrington's body... wait, no! I mean... when I checked on him after the housekeeper found him! Yes, that's it!"
                }
            }
        }
        
        # Default Targets
        st.session_state.killer_id = "dr_croft"
        st.session_state.weapon_clue_id = "whiskey_glass"
        st.session_state.proof_clue_id = "ledger_page"
        st.session_state.CONTRADICTIONS = {
            "lady_eleanor": "pearl_earring",
            "arthur": "billiard_cover",
            "dr_croft": "latex_glove"
        }
        
        # State Variables
        st.session_state.current_room = "foyer"
        st.session_state.collected_clue_ids = []
        st.session_state.clues_found = []
        st.session_state.interrogated_suspects = []
        st.session_state.resolved_contradictions = []
        st.session_state.custom_notes = ""
        st.session_state.visited_rooms = ["foyer"]
        st.session_state.detective_score = 0
        st.session_state.difficulty_level = "Beginner"
        st.session_state.plot_twist_triggered = False
        st.session_state.plot_twist_data = None
        st.session_state.audio_trigger = None
        st.session_state.game_over = False
        st.session_state.game_over_reason = None
        st.session_state.feedback = ""
        st.session_state.interrogated_dialogues = [] # logs questions asked
        
        # Load API case if key available
        active_key = custom_api_key if custom_api_key else load_api_key()
        if active_key:
            ai_data = generate_ai_case(active_key)
            if ai_data:
                try:
                    # Transactional parsing
                    temp_victim_name = ai_data["victim"]["name"]
                    temp_victim_desc = ai_data["victim"]["desc"]
                    temp_clues = ai_data["clues"]
                    temp_suspects = ai_data["suspects"]
                    temp_killer_id = ai_data["killer_id"]
                    temp_weapon_clue_id = ai_data["weapon_clue_id"]
                    temp_proof_clue_id = ai_data["proof_clue_id"]
                    
                    if temp_killer_id not in temp_suspects:
                        raise KeyError("Killer ID not in suspects")
                    if temp_weapon_clue_id not in temp_clues:
                        raise KeyError("Weapon ID not in clues")
                    if temp_proof_clue_id not in temp_clues:
                        raise KeyError("Proof ID not in clues")
                        
                    temp_contradictions = {}
                    suspect_keys = list(temp_suspects.keys())
                    clue_keys = list(temp_clues.keys())
                    
                    for i, s_key in enumerate(suspect_keys):
                        field_name = f"suspect_{i+1}_contradiction_clue_id"
                        contradiction_clue = ai_data.get(field_name)
                        if contradiction_clue and contradiction_clue in temp_clues:
                            temp_contradictions[s_key] = contradiction_clue
                        else:
                            temp_contradictions[s_key] = clue_keys[min(len(clue_keys)-1, i + 2)]
                    
                    # Update State
                    st.session_state.victim_name = temp_victim_name
                    st.session_state.victim_desc = temp_victim_desc
                    st.session_state.CLUES = temp_clues
                    st.session_state.SUSPECTS = temp_suspects
                    st.session_state.killer_id = temp_killer_id
                    st.session_state.weapon_clue_id = temp_weapon_clue_id
                    st.session_state.proof_clue_id = temp_proof_clue_id
                    st.session_state.CONTRADICTIONS = temp_contradictions
                    
                    # Clear and distribute
                    for r_id in st.session_state.ROOMS:
                        st.session_state.ROOMS[r_id]["clues"] = []
                        st.session_state.ROOMS[r_id]["suspects"] = []
                        
                    for c_id, clue_data in st.session_state.CLUES.items():
                        r_id = clue_data.get("room", "study").lower().strip()
                        if r_id not in st.session_state.ROOMS:
                            r_id = "study"
                        st.session_state.ROOMS[r_id]["clues"].append(c_id)
                        
                    target_rooms = ["library", "lounge", "conservatory"]
                    for i, s_key in enumerate(suspect_keys):
                        r_id = target_rooms[i % len(target_rooms)]
                        st.session_state.ROOMS[r_id]["suspects"].append(s_key)
                        
                    st.session_state.feedback = "Success! Loaded dynamic Gemini mystery case."
                except Exception as e:
                    st.session_state.feedback = f"Parsing failed ({e}). Defaulting to offline case."
            else:
                st.session_state.feedback = "API call failed. Defaulting to offline case."
        else:
            st.session_state.feedback = "Playing default offline mystery: The Secret of Blackwood Manor"
            
        st.session_state.initialized = True

def update_difficulty():
    score = st.session_state.detective_score
    if score <= 50:
        st.session_state.difficulty_level = "Beginner"
    elif score <= 150:
        st.session_state.difficulty_level = "Intermediate"
    else:
        st.session_state.difficulty_level = "Advanced"

# Ensure base proxy variables exist on every run to prevent hot-reload AttributeErrors
base_states = {
    "theme": "dark",
    "audio_trigger": None,
    "feedback": "",
    "active_interrogation": None,
    "interrogated_dialogues": [],
    "initialized": False,
    "game_over": False,
    "game_over_reason": None,
    "plot_twist_triggered": False,
    "plot_twist_data": None
}
for key, default in base_states.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- STATE CHECK ---
init_game_state()
inject_custom_css()

# Render Audio Trigger if loaded
if st.session_state.audio_trigger:
    play_audio_chime(st.session_state.audio_trigger)
    st.session_state.audio_trigger = None

# --- SIDEBAR (HUD & Configuration) ---
st.sidebar.markdown(f"## 🕵️‍♂️ HUD Panel")
theme_mode = st.sidebar.toggle("☀️ Light Mode / 🌙 Dark Mode", value=(st.session_state.theme == "light"))
new_theme = "light" if theme_mode else "dark"
if new_theme != st.session_state.theme:
    st.session_state.theme = new_theme
    st.rerun()

# Detective metrics
st.sidebar.markdown(f"**Detective Rank:**")
score = st.session_state.detective_score
# Get rank
if score <= 30:
    rank = "Amateur Constable 👮"
    next_rank = "Local Deputy 🕵️‍♂️"
    prev_limit, next_limit = 0, 31
elif score <= 70:
    rank = "Local Deputy 🕵️‍♂️"
    next_rank = "Private Detective 🔍"
    prev_limit, next_limit = 31, 71
elif score <= 120:
    rank = "Private Detective 🔍"
    next_rank = "Special Investigator 🗂️"
    prev_limit, next_limit = 71, 121
elif score <= 180:
    rank = "Special Investigator 🗂️"
    next_rank = "Sherlock Holmes Master Sleuth 🧠🏆"
    prev_limit, next_limit = 121, 181
else:
    rank = "Sherlock Holmes Master Sleuth 🧠🏆"
    next_rank = "MAX RANK"
    prev_limit, next_limit = 181, 181

st.sidebar.markdown(f"<div class='hud-badge'>{rank}</div>", unsafe_allow_html=True)

# Progress bar
if next_rank != "MAX RANK":
    progress_val = min(1.0, max(0.0, (score - prev_limit) / (next_limit - prev_limit)))
    st.sidebar.progress(progress_val)
    st.sidebar.caption(f"Score: {score} pts ({score}/{next_limit} to {next_rank})")
else:
    st.sidebar.progress(1.0)
    st.sidebar.caption(f"Score: {score} pts (MAX RANK REACHED)")

st.sidebar.divider()

# Difficulty
diff_color = {"Beginner": "green", "Intermediate": "orange", "Advanced": "red"}[st.session_state.difficulty_level]
st.sidebar.markdown(f"**Difficulty Level:** <span style='color:{diff_color}; font-weight:bold;'>{st.session_state.difficulty_level}</span>", unsafe_allow_html=True)

# Custom Case Notes Text Area
st.sidebar.markdown("### 📓 Case Notes")
notes_val = st.sidebar.text_area("Write custom notes:", st.session_state.custom_notes, height=200)
if notes_val != st.session_state.custom_notes:
    st.session_state.custom_notes = notes_val

st.sidebar.divider()

# Game Restart Controls
api_val = st.sidebar.text_input("Gemini API Key:", value=load_api_key(), type="password")
if st.sidebar.button("Restart Mystery (Regen Case)"):
    if api_val:
        # Save key
        try:
            with open(".env", "w", encoding="utf-8") as f:
                f.write(f"GEMINI_API_KEY={api_val}\n")
        except Exception:
            pass
    init_game_state(force_reset=True, custom_api_key=api_val)
    st.rerun()

# --- MAIN SCREEN INTERFACE ---

# 1. Header Banner
st.markdown("<h1 style='text-align: center;'>🕵️‍♂️ The Secret of Blackwood Manor</h1>", unsafe_allow_html=True)
st.markdown(f"""
<div class="mystery-card" style="border-left: 5px solid #E74C3C; background-color: rgba(231, 76, 60, 0.05); padding: 15px 20px; border-radius: 6px; margin-bottom: 20px;">
    <h3 style="margin-top: 0; color: #E74C3C !important; font-family: 'Georgia', serif;">🎬 The Case File: A Stormy Night at Blackwood Manor</h3>
    <p style="font-size: 15px; line-height: 1.6; font-style: italic; font-family: 'Georgia', serif;">
        "The grandfather clock struck 9:00 PM on a rain-swept night, its chimes drowned out by the thunder shaking the heavy windows of Blackwood Manor. 
        Seconds later, a chilling scream echoed from the private Study. 
        <strong>{st.session_state.victim_name}</strong>, {st.session_state.victim_desc}, was found slumped lifelessly over his mahogany desk. 
        The room was locked from the inside. On the desk sat a half-empty glass of crystal whiskey, emitting the faint, sweet scent of bitter almonds... 
        Aconite poison, the silent killer. 
        Three suspects remain in the manor, each hiding behind convenient alibis. You have stepped through the doors as the lead investigator. 
        Piece together the clues, cross-examine the suspects, expose their lies, and solve the murder before the storm passes and the killer escapes..."
    </p>
</div>
""", unsafe_allow_html=True)

# 2. Check Game Over state
if st.session_state.game_over:
    st.divider()
    success = (st.session_state.game_over_reason == "won")
    
    if success:
        st.balloons()
        st.success("🎉 CASE SOLVED! You arrested the correct killer with perfect weapon and proof evidence!")
        play_chime = "success"
    else:
        st.error(f"❌ CASE CLOSED - UNSOLVED. Reason: {st.session_state.game_over_reason.upper()}")
        play_chime = "failure"

    # Show Final closing card
    st.markdown(f"""
    <div class="mystery-card" style="border: 2px solid {'#D4AF37' if success else '#E74C3C'}; max-width: 700px; margin: 20px auto;">
        <h3 style="text-align: center; color: {'#D4AF37' if success else '#E74C3C'} !important;">CASE CLOSURE REPORT</h3>
        <hr style="margin: 10px 0;">
        <table style="width: 100%; font-size: 15px; border-collapse: collapse;">
            <tr style="border-bottom: 1px solid #333; height: 35px;">
                <td><strong>Case Status:</strong></td>
                <td style="text-align: right; color: {'#2ECC71' if success else '#E74C3C'}; font-weight: bold;">{"CASE SOLVED" if success else "UNSOLVED"}</td>
            </tr>
            <tr style="border-bottom: 1px solid #333; height: 35px;">
                <td><strong>Victim Name:</strong></td>
                <td style="text-align: right;">{st.session_state.victim_name}</td>
            </tr>
            <tr style="border-bottom: 1px solid #333; height: 35px;">
                <td><strong>Clues Discovered:</strong></td>
                <td style="text-align: right;">{len(st.session_state.collected_clue_ids)} / 7 clues</td>
            </tr>
            <tr style="border-bottom: 1px solid #333; height: 35px;">
                <td><strong>Contradictions Solved:</strong></td>
                <td style="text-align: right;">{len(st.session_state.resolved_contradictions)} / 3 solved</td>
            </tr>
            <tr style="border-bottom: 1px solid #333; height: 35px;">
                <td><strong>Final Score:</strong></td>
                <td style="text-align: right; font-weight: bold; color: #2ECC71;">{st.session_state.detective_score} pts</td>
            </tr>
            <tr style="height: 35px;">
                <td><strong>Detective Rating:</strong></td>
                <td style="text-align: right; font-weight: bold; color: #D4AF37;">{rank}</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Play Again / Generate New Mystery"):
        init_game_state(force_reset=True, custom_api_key=api_val)
        st.rerun()
    st.stop()

# 3. Toast Notifications for status updates
if st.session_state.feedback:
    st.info(f"🔎 {st.session_state.feedback}")
    st.session_state.feedback = ""

# 4. Check for Plot Twist
if st.session_state.plot_twist_triggered and st.session_state.plot_twist_data:
    twist = st.session_state.plot_twist_data
    st.markdown(f"""
    <div class="mystery-card" style="border: 2px solid #E74C3C; background-color: rgba(231, 76, 60, 0.1);">
        <h3 style="color:#E74C3C !important; margin-top:0;">💥 PLOT TWIST: {twist['title']}</h3>
        <p><strong>Twist Type:</strong> <span class="hud-badge">{twist['type']}</span></p>
        <p style="font-size:15px; font-style:italic;">{twist['description']}</p>
        <p style="font-size:12px; color:#2ECC71;">+15 Detective Points awarded! Case notes updated.</p>
    </div>
    """, unsafe_allow_html=True)

# 5. Core Interface columns (Unified Single-page Dashboard)
col_investigate, col_notebook = st.columns([1.1, 0.9])

with col_investigate:
    # Quick Investigator Guide
    with st.expander("📖 Basic Guide: How to Play the Game", expanded=True):
        st.markdown("""
        ### 🕵️‍♂️ Detective Field Guide
        Welcome to the investigation! Follow these basic steps to crack the case:
        
        1. **🧭 Explore the Manor**:
           Look at the **Manor Map** and use the travel buttons at the bottom of the screen to move from room to room. Different suspects and clues are scattered across the manor.
        
        2. **🔍 Search for Evidence**:
           Inside any room, click **"Search room for clues"** to scour the area. If you find any clues, they will be added to your **Evidence Locker** (under the Notebook on the right). Finding clues increases your score (+10 pts).
        
        3. **🗣️ Cross-Examine Suspects**:
           If suspects are present in a room, click **"Interrogate"** to question them. You can ask them about their alibis, motives, or ask them about specific clues you have found.
        
        4. **🧩 Solve Alibi Contradictions (Crucial!)**:
           Suspects will lie to cover their tracks. If you question a suspect about an item that disproves their alibi, you will break their alibi! This awards **+20 Detective Points** and unlocks their confession.
        
        5. **⚖️ Accuse the Suspect**:
           Once you are confident, go to the **Accusation Chamber** on the right side. Select the correct **Killer**, the **Weapon**, and the **Embezzlement/Key Proof**. 
           * **⚠️ CAUTION:** A wrong accusation is costly and will deduct **-10 Detective Points** (if you have enough points)!
        """)

    room_id = st.session_state.current_room
    room = st.session_state.ROOMS[room_id]
    
    st.subheader(f"📍 Location: {room['name']}")
    st.markdown(f"*{room['description']}*")
    
    st.markdown("### 🔎 Room Actions")
    
    # Search room trigger
    if st.button("Search room for clues", key="search_room_btn", use_container_width=True):
        room_clues = room["clues"]
        found_new = False
        found_clues_list = []
        
        for c_id in room_clues:
            if c_id not in st.session_state.collected_clue_ids:
                st.session_state.collected_clue_ids.append(c_id)
                st.session_state.clues_found.append(st.session_state.CLUES[c_id]["name"])
                st.session_state.detective_score += 10
                found_new = True
                found_clues_list.append(st.session_state.CLUES[c_id]["name"])
                
        update_difficulty()
        
        if found_new:
            st.session_state.audio_trigger = "clue"
            st.session_state.feedback = f"You found clues: {', '.join(found_clues_list)}! (+10 pts each)"
            
            # Check Plot Twist threshold (>= 3 clues)
            if len(st.session_state.collected_clue_ids) >= 3 and not st.session_state.plot_twist_triggered:
                trigger_plot_twist_event()
        else:
            st.session_state.feedback = "You searched thoroughly but found no new clues here."
        
        st.rerun()

    st.markdown("#### 👥 Suspects Present here:")
    room_suspects = room["suspects"]
    if room_suspects:
        for s_id in room_suspects:
            suspect = st.session_state.SUSPECTS[s_id]
            met = s_id in st.session_state.interrogated_suspects
            met_badge = "🟢 MET" if met else "⚪ UNMET"
            
            # Draw suspect profile summary card
            st.markdown(f"""
            <div style="background-color: rgba(128,128,128,0.05); padding: 12px; border-radius: 4px; margin-bottom: 6px; border-left: 3px solid #D4AF37;">
                <span class="hud-badge" style="font-size:10px;">{suspect['role']}</span>
                <strong style="font-size:14px; margin-left:5px;">{suspect['name']}</strong> ({met_badge})
                <p style="font-size:12px; margin: 4px 0 0 0; opacity:0.85;">{suspect['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Interrogation trigger button
            if st.button(f"🗣️ Interrogate {suspect['name']}", key=f"int_{s_id}", use_container_width=True):
                st.session_state.active_interrogation = s_id
                if s_id not in st.session_state.interrogated_suspects:
                    st.session_state.interrogated_suspects.append(s_id)
                    st.session_state.detective_score += 5
                    st.session_state.feedback = f"First meeting with {suspect['name']}! (+5 pts)"
                    update_difficulty()
                    st.rerun()
    else:
        st.info("No suspects are currently in this room.")
        st.session_state.active_interrogation = None

    # Render interrogation options if suspect selected
    if st.session_state.get("active_interrogation"):
        active_id = st.session_state.active_interrogation
        active_suspect = st.session_state.SUSPECTS[active_id]
        st.markdown(f"---")
        st.markdown(f"💬 **Questioning {active_suspect['name']}**")
        
        # Question Options
        question_choices = [
            ("Ask about their alibi", "alibi"),
            ("Ask about their motive", "motive"),
            ("Ask about their secrets", "secret")
        ]
        for other_id, other_s in st.session_state.SUSPECTS.items():
            if other_id != active_id:
                question_choices.append((f"Ask about {other_s['name']}", f"about_{other_id.split('_')[-1]}"))
        for c_id in st.session_state.collected_clue_ids:
            c_name = st.session_state.CLUES[c_id]["name"]
            question_choices.append((f"Ask about {c_name}", f"about_{c_id}"))

        selected_q_label, q_key = st.selectbox("Select question to ask:", question_choices, format_func=lambda x: x[0], key="q_select")
        
        if st.button("Ask Suspect", use_container_width=True):
            # Interrogation dynamics checks
            is_about_other = q_key.startswith("about_") and not any(c in q_key for c in st.session_state.CLUES)
            
            if (st.session_state.difficulty_level in ["Intermediate", "Advanced"]) and q_key == "secret" and len(st.session_state.collected_clue_ids) < 2:
                ans = "I don't trust you enough to share private secrets, detective. Find more evidence first."
            elif st.session_state.difficulty_level == "Advanced" and is_about_other:
                ans = "How dare you ask me to gossip or accuse others! This interrogation is over!"
                st.session_state.active_interrogation = None
            else:
                ans = active_suspect["dialogue"].get(q_key, "I have nothing to say about that.")
                
                # Contradiction Resolution Check
                is_contradiction = False
                clue_asked = q_key[6:] if q_key.startswith("about_") else ""
                if active_id in st.session_state.CONTRADICTIONS and st.session_state.CONTRADICTIONS[active_id] == clue_asked:
                    is_contradiction = True
                    
                if is_contradiction:
                    contr_id = f"{active_id}_{q_key}"
                    if contr_id not in st.session_state.resolved_contradictions:
                        st.session_state.resolved_contradictions.append(contr_id)
                        st.session_state.detective_score += 20
                        st.session_state.audio_trigger = "contradiction"
                        st.session_state.feedback = f"Alibi Broken! caught contradiction in {active_suspect['name']}'s statements (+20 pts)!"
                        update_difficulty()
                        ans = ans.replace("[CONTRADICTION FOUND!]", "[CONTRADICTION FOUND!]")
                    else:
                        ans = ans.replace("[CONTRADICTION FOUND!]", "[CONTRADICTION ALREADY RESOLVED]")

            # Save question response log
            st.session_state.interrogated_dialogues.insert(0, {
                "suspect": active_suspect["name"],
                "question": selected_q_label,
                "answer": ans
            })
            st.rerun()

        # Display dialogue responses logs
        if st.session_state.interrogated_dialogues:
            st.markdown("**Dialogue Log:**")
            for d in st.session_state.interrogated_dialogues[:3]:
                st.markdown(f"> **You asked:** *\"{d['question']}\"*  \n> 🗣️ **{d['suspect']} responds:** \"{d['answer']}\"")

    st.markdown("### 🗺️ Manor Map & Travel")
    render_manor_map()
    
    st.markdown("#### Move to connected room:")
    cols_nav = st.columns(len(room["connections"]))
    for idx, conn in enumerate(room["connections"]):
        conn_name = st.session_state.ROOMS[conn]["name"]
        clue_count = len(st.session_state.ROOMS[conn]["clues"])
        found_count = len([cid for cid in st.session_state.ROOMS[conn]["clues"] if cid in st.session_state.collected_clue_ids])
        unfound = clue_count - found_count
        
        btn_label = f"🚪 Go to {conn_name.split('(')[0].strip()}"
        if unfound > 0 and st.session_state.difficulty_level == "Beginner":
            btn_label += f" ({unfound} 🔍)"
            
        with cols_nav[idx]:
            if st.button(btn_label, key=f"nav_{conn}", use_container_width=True):
                st.session_state.current_room = conn
                st.session_state.active_interrogation = None
                st.session_state.feedback = f"You entered {st.session_state.ROOMS[conn]['name']}."
                st.rerun()

    # Beginner hints
    if st.session_state.difficulty_level == "Beginner":
        st.info("💡 **Beginner Hint:** Check the Study first for the weapon, then search the Library for finances. Confront suspects with items that break their alibis!")

with col_notebook:
    # 1. Detective Checklist
    st.markdown("### 📋 Detective's Checklist")
    
    total_rooms = len(st.session_state.ROOMS)
    if "visited_rooms" not in st.session_state:
        st.session_state.visited_rooms = ["foyer"]
    if st.session_state.current_room not in st.session_state.visited_rooms:
        st.session_state.visited_rooms.append(st.session_state.current_room)
        
    rooms_visited = len(st.session_state.visited_rooms)
    clues_found_count = len(st.session_state.collected_clue_ids)
    suspects_met = len(st.session_state.interrogated_suspects)
    contradictions_solved = len(st.session_state.resolved_contradictions)
    
    st.markdown(f"🧭 **Rooms Visited:** `{rooms_visited} / {total_rooms}`")
    st.markdown(f"👥 **Suspects Met:** `{suspects_met} / 3`")
    st.markdown(f"🎒 **Clues Discovered:** `{clues_found_count} / 7`")
    st.markdown(f"🧩 **Alibi Contradictions Resolved:** `{contradictions_solved} / 3`")
    
    # 2. Evidence Locker
    st.markdown("### 🎒 Evidence Locker")
    if st.session_state.collected_clue_ids:
        for c_id in st.session_state.collected_clue_ids:
            clue = st.session_state.CLUES[c_id]
            clue_room = "Unknown"
            for r_id, r in st.session_state.ROOMS.items():
                if c_id in r["clues"]:
                    clue_room = r["name"]
                    break
            if clue_room == "Unknown" and c_id in ["whiskey_glass", "will_papers", "pearl_earring"]:
                clue_room = "The Study (CRIME SCENE)"
            elif clue_room == "Unknown" and c_id == "ledger_page":
                clue_room = "The Library"
            elif clue_room == "Unknown" and c_id == "latex_glove":
                clue_room = "The Conservatory"
            elif clue_room == "Unknown" and c_id in ["bookie_letter", "billiard_cover"]:
                clue_room = "The Lounge"
                
            st.markdown(f"🔎 **{clue['name']}** *(Found in: {clue_room})*")
            st.markdown(f"<p style='font-size:12px; margin: -5px 0 5px 15px; opacity:0.8; font-style:italic;'>{clue['description']}</p>", unsafe_allow_html=True)
    else:
        st.info("No clues discovered yet. Move to rooms like the Study and search for evidence.")

    # 3. Suspect Dossiers
    st.markdown("### 👥 Suspect Dossiers")
    for s_id, suspect in st.session_state.SUSPECTS.items():
        met = s_id in st.session_state.interrogated_suspects
        alibi_broken = any(cid.startswith(s_id) for cid in st.session_state.resolved_contradictions)
        
        if alibi_broken:
            status_header = "🔴 ALIBI BROKEN ❌"
            border_style = "border-left: 4px solid #E74C3C;"
        elif met:
            status_header = "🟡 INTERROGATED"
            border_style = "border-left: 4px solid #D4AF37;"
        else:
            status_header = "⚪ UNMET"
            border_style = "border-left: 4px solid #E0E0E0;"
            
        st.markdown(f"""
        <div style="background-color: rgba(128,128,128,0.05); padding: 8px 12px; border-radius: 4px; margin-bottom: 5px; {border_style}">
            <strong style="font-size:11px; color: #D4AF37;">{suspect['role']}</strong>
            <h5 style="margin: 2px 0; font-size:13px;">{suspect['name']} ({status_header})</h5>
        </div>
        """, unsafe_allow_html=True)
        
        if met:
            with st.expander(f"View profiles/alibis for {suspect['name']}", expanded=alibi_broken):
                st.markdown(f"**Alibi statement:** *\"{suspect['alibi']}\"*")
                st.markdown(f"**Motive:** *\"{suspect['motive']}\"*")
                if alibi_broken:
                    contradiction_clue_id = st.session_state.CONTRADICTIONS.get(s_id)
                    if contradiction_clue_id:
                        response = suspect["dialogue"].get(f"about_{contradiction_clue_id}", "")
                        clean_resp = response.replace("[CONTRADICTION FOUND!]", "").replace("[CONTRADICTION ALREADY RESOLVED]", "").strip()
                        clean_resp = clean_resp.replace(st.session_state.theme, "")
                        st.error(f"Broken Confession: \"{clean_resp}\"")

    # 4. Crime Scene Dossier (Floor Plan)
    with st.expander("📁 Crime Scene Dossier & Floor Plan", expanded=False):
        st.markdown(f"""
        **Victim profile:**
        - **Name:** {st.session_state.victim_name}
        - **Description:** {st.session_state.victim_desc}
        
        **Coroner Report:**
        - **Estimated Time of Death:** 9:00 PM
        - **Cause of Death:** Cardiac/respiratory failure induced by Aconite poison slipped into a crystal whiskey glass.
        """)
        render_study_diagram()

    # 5. Accusation Chamber
    st.markdown("### ⚖️ Accusation Chamber")
    st.warning("⚠️ **Accusation Rules:** You must select the correct killer, weapon, and key proof. An incorrect guess will cause the killer to escape!")
    
    if not st.session_state.collected_clue_ids:
        st.info("You must gather at least some clues before you can make an accusation.")
    else:
        accused_killer_name = st.selectbox(
            "Select Accused Suspect:",
            options=list(st.session_state.SUSPECTS.keys()),
            format_func=lambda x: st.session_state.SUSPECTS[x]["name"],
            key="accuse_s"
        )
        accused_weapon_id = st.selectbox(
            "Select Murder Method / Weapon Clue:",
            options=st.session_state.collected_clue_ids,
            format_func=lambda x: st.session_state.CLUES[x]["name"],
            key="accuse_w"
        )
        accused_proof_id = st.selectbox(
            "Select Key Link / Embezzlement Proof:",
            options=st.session_state.collected_clue_ids,
            format_func=lambda x: st.session_state.CLUES[x]["name"],
            key="accuse_p"
        )
        
        st.markdown("---")
        st.markdown(f"**Your Case Accusation File Summary:**")
        st.markdown(f"1. **Killer:** {st.session_state.SUSPECTS[accused_killer_name]['name']}")
        st.markdown(f"2. **Weapon:** {st.session_state.CLUES[accused_weapon_id]['name']}")
        st.markdown(f"3. **Proof:** {st.session_state.CLUES[accused_proof_id]['name']}")
        
        if st.button("⚖️ SUBMIT FINAL ACCUSATION CASE", use_container_width=True):
            # Check correctness
            if (accused_killer_name == st.session_state.killer_id and 
                accused_weapon_id == st.session_state.weapon_clue_id and 
                accused_proof_id == st.session_state.proof_clue_id):
                st.session_state.game_over = True
                st.session_state.game_over_reason = "won"
                st.session_state.audio_trigger = "success"
            else:
                # Wrong accusation: deduct 10 points if enough points
                deduct = 0
                if st.session_state.detective_score >= 10:
                    st.session_state.detective_score -= 10
                    deduct = 10
                else:
                    st.session_state.detective_score = 0
                    
                st.session_state.audio_trigger = "failure"
                if deduct > 0:
                    st.session_state.feedback = f"Incorrect Accusation! The suspect has an alibi or the evidence doesn't match up. You lost {deduct} points. Try again!"
                else:
                    st.session_state.feedback = "Incorrect Accusation! The suspect has an alibi or the evidence doesn't match up. (You have 0 points, so no score was deducted). Try again!"
                update_difficulty()
            st.rerun()
