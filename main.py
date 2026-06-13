# main.py
# ==============================================================================
#                      THE SECRET OF BLACKWOOD MANOR
#         A Beginner-Friendly Console Murder Mystery Game in Python
# ==============================================================================
# In this game, we use standard Python concepts:
# - LISTS: To store and track items found by the player.
# - DICTIONARIES: To organize information about Rooms, Suspects, and Clues.
# - FUNCTIONS: To group pieces of code that perform specific tasks.
# - DYNAMIC SCALING: Altering difficulty and mechanics based on score and time.
# ==============================================================================

import os
import sys
import time
import textwrap
import random
import urllib.request
import json
import threading

# --- ANSI escape codes for coloring console text ---
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

# ==============================================================================
# 1. RANDOMIZED VICTIM GENERATOR
# ==============================================================================
VICTIMS = [
    {"name": "Lord Reginald Harrington", "desc": "a wealthy philanthropist and art collector"},
    {"name": "Sir Charles Sterling", "desc": "an eccentric archaeologist and museum curator"},
    {"name": "Count Victor Romanov", "desc": "a mysterious wealthy socialite and antique collector"}
]

# Randomly select a victim for this run of the game
selected_victim = random.choice(VICTIMS)
victim_name = selected_victim["name"]
victim_desc = selected_victim["desc"]
victim_surname = victim_name.split()[-1]

# ==============================================================================
# 2. DICTIONARIES: Setting up the game database
# ==============================================================================

# Database of all clues in the game.
CLUES = {
    "whiskey_glass": {
        "name": "Poisoned Whiskey Glass",
        "description": f"A crystal glass on {victim_name}'s desk smelling of bitter almonds (a sign of Aconite poison)."
    },
    "will_papers": {
        "name": "Confidential Will",
        "description": f"Signed papers in the study desk showing {victim_name} was cutting off Lady Eleanor completely."
    },
    "ledger_page": {
        "name": "Torn Ledger Page",
        "description": f"A discarded sheet detailing a charity audit showing 'J.C.' embezzled £50,000 from {victim_name}'s funds."
    },
    "bookie_letter": {
        "name": "Threatening Letter",
        "description": "A bookie letter addressed to Arthur Harrington demanding £20,000 immediately."
    },
    "pearl_earring": {
        "name": "Dropped Pearl Earring",
        "description": f"A white pearl earring found on the floor of the Study (Crime Scene). It matches Lady Eleanor's set."
    },
    "billiard_cover": {
        "name": "Dusty Billiard Cover",
        "description": "A thick, dusty canvas cover completely draped over the billiard table. It hasn't been removed in weeks."
    },
    "latex_glove": {
        "name": "Stained Latex Glove",
        "description": f"A medical glove in the Conservatory bin, stained with whiskey and trace elements of Aconite."
    }
}

# Suspects profile database.
SUSPECTS = {
    "lady_eleanor": {
        "name": f"Lady Eleanor {victim_surname}",
        "role": "The Estranged Wife",
        "description": "The elegant wife of the victim. She stands tall, wearing black lace and looking cold.",
        "alibi": "I was in the Library reading my historical novel all evening. I did not go to any other rooms, especially not the Study.",
        "motive": f"Yes, {victim_name} and I had our disagreements, but I would not resort to murder.",
        "dialogue": {
            "alibi": "I went to the Library around 7 PM and stayed there until the housekeeper found him. I did not leave the room.",
            "motive": f"He was planning to divorce me and leave me with nothing, but I would have fought him in court, not poisoned {victim_name}.",
            "secret": "We argued in the study before dinner because he was being unreasonable. But that is all.",
            "about_arthur": "Arthur is a foolish boy who spends too much money gambling. But he is not a murderer.",
            "about_croft": "Dr. Croft has been our doctor for years. My husband trusted him completely with charity accounts.",
            "about_whiskey_glass": f"{victim_name} always had a glass of whiskey before bed. He kept the bottle in his study.",
            "about_will_papers": f"So you found the will. Yes, he wanted to cut me off. He was a cruel partner.",
            "about_ledger_page": "A ledger page? I know nothing of charity finances. Dr. Croft managed those accounts.",
            "about_bookie_letter": "Another one of Arthur's debts... It is disappointing.",
            "about_pearl_earring": "My... pearl earring? You found it in the Study? [CONTRADICTION FOUND!] Oh dear... okay, fine. I did slip into the Study briefly after dinner to look for the Will. I lied because I was terrified of being suspected. But he was already dead when I got there, I swear!",
            "about_billiard_cover": "I know nothing of Arthur's games.",
            "about_latex_glove": "Medical gloves? Those belong to Dr. Croft, surely."
        }
    },
    "arthur": {
        "name": f"Arthur {victim_surname}",
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
        "motive": f"{victim_name} was my dearest friend. I have no reason to wish him harm.",
        "dialogue": {
            "alibi": "I was in the Conservatory from 7:30 PM until I heard the screams. I was sorting through my collection.",
            "motive": "We were co-founders of the charity. Our friendship was built on mutual respect.",
            "secret": "I have nothing to hide, Inspector. I spent my evening in study and observation.",
            "about_eleanor": f"Lady Eleanor is a proud woman. Her marriage to {victim_name} was a union of convenience. They argued frequently.",
            "about_arthur": f"Arthur is a troubled young man. His gambling habits are a tragedy, and {victim_name} was incredibly disappointed in him.",
            "about_whiskey_glass": "Aconite in his whiskey? Horrible. Aconite causes swift cardiorespiratory failure. It is a terrible way to die.",
            "about_will_papers": f"Ah, {victim_name} mentioned he was considering a new Will. Eleanor stood to lose everything.",
            "about_ledger_page": "A charity ledger page? Let me see... I-I don't recognize this. This looks like a draft. Our accounts are in perfect order.",
            "about_bookie_letter": "Ah, another threat to Arthur. It seems Arthur had a powerful motive.",
            "about_pearl_earring": "Lady Eleanor's earring? I believe I saw her wearing it earlier.",
            "about_billiard_cover": "Arthur playing billiards? He spends more time drinking than playing.",
            "about_latex_glove": f"A latex glove stained with medical solution and whiskey? [CONTRADICTION FOUND!] Wait, that solution is from my laboratory... Ah! I must have dropped it when I was examining {victim_name}'s body... wait, no! I mean... when I checked on him after the housekeeper found him! Yes, that's it!"
        }
    }
}

# Rooms database.
ROOMS = {
    "foyer": {
        "name": "The Foyer",
        "description": "The grand entrance hall of Blackwood Manor. A large chandelier hangs from the ceiling.",
        "connections": ["study", "library", "lounge", "conservatory"],
        "clues": [],
        "suspects": []
    },
    "study": {
        "name": "The Study (CRIME SCENE)",
        "description": f"The official CRIME SCENE where {victim_name}'s body was found slumped at his desk.",
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

# ==============================================================================
# 3. GLOBAL VARIABLES tracking player progress
# ==============================================================================
current_room = "foyer"
collected_clue_ids = []      # LIST: IDs of clues found (e.g. "whiskey_glass")
clues_found = []             # LIST: User-friendly names of clues discovered
interrogated_suspects = []   # LIST: Suspect IDs interrogated
resolved_contradictions = [] # LIST: Tracks which contradictions the player has solved
custom_notes = []            # LIST: Custom player notes
visited_rooms = []           # LIST: Track visited rooms for thought monologues
turns_left = 12              # Time limit
detective_score = 0          # Score tracking points
difficulty_level = "Beginner" # Dynamic difficulty state
plot_twist_triggered = False  # Track if plot twist has occurred

# Dynamic target keys (configured dynamically by Gemini AI or default offline case)
killer_id = "dr_croft"
weapon_clue_id = "whiskey_glass"
proof_clue_id = "ledger_page"

# Contradiction mapping (maps suspect_id -> contradiction_clue_id)
CONTRADICTIONS = {
    "lady_eleanor": "pearl_earring",
    "arthur": "billiard_cover",
    "dr_croft": "latex_glove"
}

# ==============================================================================
# 4. HELPER FUNCTIONS
# ==============================================================================

def clear_screen():
    """Clears the console screen."""
    os.system("cls" if os.name == "nt" else "clear")

def print_typewriter(text, delay=0.015):
    """Prints text character-by-character for suspense."""
    try:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    except KeyboardInterrupt:
        print(text)

def print_banner(title, color=BLUE):
    """Prints a styled banner block."""
    border = "=" * 60
    print(f"\n{color}{border}")
    print(f"{BOLD}{title.center(60)}")
    print(f"{border}{RESET}")

def print_wrapped(text, prefix=""):
    """Wraps long dialogue paragraphs."""
    wrapped = textwrap.fill(text, width=70)
    for line in wrapped.split('\n'):
        print(f"{prefix}{line}")

def print_detective_thought(text):
    """Prints Vance's thoughts in a beautifully highlighted format."""
    print(f"\n{MAGENTA}{BOLD}🕵️ Vance's Thoughts:{RESET} {WHITE}\"{text}\"{RESET}\n")

def draw_menu(options, title="ACTION MENU"):
    """Draws a beautiful boxed action menu in the console using standard box characters."""
    border = "┌" + "─" * 58 + "┐"
    print(f"{BLUE}{border}{RESET}")
    if title:
        padded_title = f" {title} "
        print(f"{BLUE}│{RESET}{BOLD}{padded_title.center(58)}{RESET}{BLUE}│{RESET}")
        print(f"{BLUE}├" + "─" * 58 + "┤{RESET}")
    for key, label in options.items():
        option_line = f"  [{key}] {label}"
        print(f"{BLUE}│{RESET}{option_line.ljust(58)}{BLUE}│{RESET}")
    print(f"{BLUE}└" + "─" * 58 + "┘{RESET}")

def print_end_game_summary(success, reason=""):
    """Prints a closing case closure report detailing stats, score, and rank."""
    print_banner("CASE CLOSURE REPORT", GREEN if success else RED)
    
    # Calculate rank based on score
    if detective_score <= 30:
        rank = "Amateur Constable 👮"
    elif detective_score <= 70:
        rank = "Local Deputy 🕵️‍♂️"
    elif detective_score <= 120:
        rank = "Private Detective 🔍"
    elif detective_score <= 180:
        rank = "Special Investigator 🗂️"
    else:
        rank = "Sherlock Holmes Grade Master Sleuth 🧠🏆"
        
    status = "CASE SOLVED (SUCCESS)" if success else f"CASE UNSOLVED - {reason.upper()}"
    time_spent = 12 - turns_left
    
    border = "┌" + "─" * 58 + "┐"
    print(f"{WHITE}{border}{RESET}")
    print(f"{WHITE}│{RESET}  {BOLD}Case Status:{RESET} {status.ljust(43)}{WHITE}│{RESET}")
    print(f"{WHITE}│{RESET}  {BOLD}Victim Name:{RESET} {victim_name.ljust(43)}{WHITE}│{RESET}")
    print(f"{WHITE}│{RESET}  {BOLD}Hours Spent:{RESET} {f'{time_spent} hours'.ljust(43)}{WHITE}│{RESET}")
    print(f"{WHITE}│{RESET}  {BOLD}Clues Found:{RESET} {f'{len(collected_clue_ids)}/7 clues'.ljust(43)}{WHITE}│{RESET}")
    print(f"{WHITE}│{RESET}  {BOLD}Alibi Breaks:{RESET} {f'{len(resolved_contradictions)}/3 contradictions'.ljust(42)}{WHITE}│{RESET}")
    print(f"{WHITE}│{RESET}  {BOLD}Final Score:{RESET} {f'{detective_score} points'.ljust(43)}{WHITE}│{RESET}")
    print(f"{WHITE}│{RESET}  {BOLD}Closing Rank:{RESET} {rank.ljust(50 - len(rank))}{WHITE}│{RESET}")
    print(f"{WHITE}└" + "─" * 58 + "┘{RESET}")
    print()

def play_retro_chime(chime_type):
    """Plays standard 8-bit retro chimes using winsound on Windows."""
    def beep_thread():
        try:
            import winsound
            if chime_type == "clue":
                # Rising arpeggio
                winsound.Beep(523, 100) # C5
                winsound.Beep(659, 100) # E5
                winsound.Beep(784, 150) # G5
            elif chime_type == "contradiction":
                # Triumphant fanfare
                winsound.Beep(523, 80)
                winsound.Beep(523, 80)
                winsound.Beep(659, 120)
                winsound.Beep(784, 200)
            elif chime_type == "twist":
                # Mysterious theme
                winsound.Beep(220, 250) # A3
                winsound.Beep(207, 250) # G#3
                winsound.Beep(196, 350) # G3
            elif chime_type == "success":
                # Victory arpeggio
                winsound.Beep(523, 100)
                winsound.Beep(659, 100)
                winsound.Beep(784, 100)
                winsound.Beep(1046, 250) # C6
            elif chime_type == "failure":
                # Descending sad tone
                winsound.Beep(392, 200) # G4
                winsound.Beep(349, 200) # F4
                winsound.Beep(311, 200) # D#4
                winsound.Beep(262, 400) # C4
        except Exception:
            pass
    threading.Thread(target=beep_thread, daemon=True).start()

def draw_map():
    """Draws a beautiful boxed ASCII map of the manor with the player's current location."""
    def pad_room(r_id):
        names = {
            "study": "STUDY (Crime Scene)",
            "library": "LIBRARY",
            "foyer": "FOYER",
            "lounge": "LOUNGE",
            "conservatory": "CONSERVATORY"
        }
        name = names.get(r_id, r_id.upper())
        if r_id == current_room:
            content = f"▶ {name} ◀"
            length = len(content)
            left = (19 - length) // 2
            right = 19 - length - left
            return f"{CYAN}{BOLD}" + " " * left + content + " " * right + f"{RESET}"
        else:
            length = len(name)
            left = (19 - length) // 2
            right = 19 - length - left
            return f"{WHITE}" + " " * left + name + " " * right + f"{RESET}"

    print(f"{BLUE}┌───────────────────────── MANOR MAP ─────────────────────────┐{RESET}")
    print(f"{BLUE}│{RESET}  ┌───────────────────┐               ┌───────────────────┐  {BLUE}│{RESET}")
    print(f"{BLUE}│{RESET}  │{pad_room('study')}│ ═════════════ │{pad_room('library')}│  {BLUE}│{RESET}")
    print(f"{BLUE}│{RESET}  └───────────────────┘               └───────────────────┘  {BLUE}│{RESET}")
    print(f"{BLUE}│{RESET}            ║                                   ║            {BLUE}│{RESET}")
    print(f"{BLUE}│{RESET}            ╠══════════════════╦════════════════╝            {BLUE}│{RESET}")
    print(f"{BLUE}│{RESET}                               ║                             {BLUE}│{RESET}")
    print(f"{BLUE}│{RESET}                      ┌───────────────────┐                  {BLUE}│{RESET}")
    print(f"{BLUE}│{RESET}                      │{pad_room('foyer')}│                  {BLUE}│{RESET}")
    print(f"{BLUE}│{RESET}                      └───────────────────┘                  {BLUE}│{RESET}")
    print(f"{BLUE}│{RESET}                               ║                             {BLUE}│{RESET}")
    print(f"{BLUE}│{RESET}            ╠══════════════════╩════════════════╣            {BLUE}│{RESET}")
    print(f"{BLUE}│{RESET}            ║                                   ║            {BLUE}│{RESET}")
    print(f"{BLUE}│{RESET}  ┌───────────────────┐               ┌───────────────────┐  {BLUE}│{RESET}")
    print(f"{BLUE}│{RESET}  │{pad_room('lounge')}│               │{pad_room('conservatory')}│  {BLUE}│{RESET}")
    print(f"{BLUE}│{RESET}  └───────────────────┘               └───────────────────┘  {BLUE}│{RESET}")
    print(f"{BLUE}└─────────────────────────────────────────────────────────────┘{RESET}")

def update_difficulty():
    """Updates the game difficulty level based on the detective score."""
    global difficulty_level
    if detective_score <= 50:
        difficulty_level = "Beginner"
    elif detective_score <= 150:
        difficulty_level = "Intermediate"
    else:
        difficulty_level = "Advanced"

# ==============================================================================
# 4.5 GEMINI AI DYNAMIC CASE GENERATOR FUNCTIONS
# ==============================================================================

def load_api_key():
    """Loads the API key from environment variables or a local .env file."""
    # 1. Check environment variable
    key = os.environ.get("GEMINI_API_KEY", "").strip().strip("'\"").strip()
    if key:
        return key
        
    # 2. Check local .env file
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
    """Queries Gemini to generate a unique case matching our game structure."""
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
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
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
            # Clean markdown formatting if present
            if text_response.startswith("```json"):
                text_response = text_response[7:]
            elif text_response.startswith("```"):
                text_response = text_response[3:]
            if text_response.endswith("```"):
                text_response = text_response[:-3]
            text_response = text_response.strip()
            return json.loads(text_response)
    except Exception as e:
        print(f"\n{RED}Gemini AI Case Generation failed: {e}{RESET}")
        return None

def initialize_game():
    """Initializes the mystery scenario using Gemini AI or falls back to default case."""
    global victim_name, victim_desc, CLUES, SUSPECTS, ROOMS
    global killer_id, weapon_clue_id, proof_clue_id, CONTRADICTIONS
    
    api_key = load_api_key()
    
    if not api_key:
        print(f"\n{YELLOW}No Gemini API key found in env or .env file.{RESET}")
        api_key = input(f"{BOLD}Enter Gemini API key (or press Enter for default offline mystery):{RESET} ").strip()
        if api_key:
            try:
                with open(".env", "w", encoding="utf-8") as f:
                    f.write(f"GEMINI_API_KEY={api_key}\n")
                print(f"{GREEN}API key saved to .env file!{RESET}")
            except Exception:
                pass
                
    if api_key:
        print(f"\n{CYAN}Connecting to Gemini AI to construct a dynamic mystery...{RESET}")
        
        # Query Gemini in a background thread to run the spinner animation in the main thread
        result = {"data": None}
        def query_thread():
            result["data"] = generate_ai_case(api_key)
            
        t = threading.Thread(target=query_thread)
        t.start()
        
        # Spinning loading wheel
        chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        idx = 0
        while t.is_alive():
            sys.stdout.write(f"\r{CYAN}{chars[idx % len(chars)]} Constructing dynamic case files via Gemini AI...{RESET}")
            sys.stdout.flush()
            idx += 1
            time.sleep(0.1)
        sys.stdout.write("\r" + " " * 60 + "\r")
        ai_data = result["data"]
        
        if ai_data:
            try:
                # 1. Parse everything first into temporary variables (Transactional safety)
                temp_victim_name = ai_data["victim"]["name"]
                temp_victim_desc = ai_data["victim"]["desc"]
                temp_clues = ai_data["clues"]
                temp_suspects = ai_data["suspects"]
                
                temp_killer_id = ai_data["killer_id"]
                temp_weapon_clue_id = ai_data["weapon_clue_id"]
                temp_proof_clue_id = ai_data["proof_clue_id"]
                
                # Check target keys exist to avoid KeyError later
                if temp_killer_id not in temp_suspects:
                    raise KeyError(f"killer_id '{temp_killer_id}' is not in suspects list")
                if temp_weapon_clue_id not in temp_clues:
                    raise KeyError(f"weapon_clue_id '{temp_weapon_clue_id}' is not in clues list")
                if temp_proof_clue_id not in temp_clues:
                    raise KeyError(f"proof_clue_id '{temp_proof_clue_id}' is not in clues list")
                
                # Support dynamic suspect contradiction mapping
                temp_contradictions = {}
                suspect_keys = list(temp_suspects.keys())
                clue_keys = list(temp_clues.keys())
                
                for i, s_key in enumerate(suspect_keys):
                    # Try to match the suspect's contradiction clue from response fields
                    # (e.g. suspect_1_contradiction_clue_id) or fallback dynamically
                    field_name = f"suspect_{i+1}_contradiction_clue_id"
                    contradiction_clue = ai_data.get(field_name)
                    if contradiction_clue and contradiction_clue in temp_clues:
                        temp_contradictions[s_key] = contradiction_clue
                    else:
                        # Fallback: assign a distinct clue (at index i + 2, wrapping if necessary)
                        temp_contradictions[s_key] = clue_keys[min(len(clue_keys)-1, i + 2)]
                
                # 2. Overwrite global database variables now that parsing succeeded
                victim_name = temp_victim_name
                victim_desc = temp_victim_desc
                CLUES = temp_clues
                SUSPECTS = temp_suspects
                killer_id = temp_killer_id
                weapon_clue_id = temp_weapon_clue_id
                proof_clue_id = temp_proof_clue_id
                CONTRADICTIONS = temp_contradictions
                
                # 3. Clear and redistribute clues & suspects into rooms
                for r_id in ROOMS:
                    ROOMS[r_id]["clues"] = []
                    ROOMS[r_id]["suspects"] = []
                    
                for c_id, clue_data in CLUES.items():
                    r_id = clue_data.get("room", "study").lower().strip()
                    if r_id not in ROOMS:
                        r_id = "study"
                    ROOMS[r_id]["clues"].append(c_id)
                    
                # Distribute suspect IDs dynamically to rooms
                target_rooms = ["library", "lounge", "conservatory"]
                for i, s_key in enumerate(suspect_keys):
                    r_id = target_rooms[i % len(target_rooms)]
                    ROOMS[r_id]["suspects"].append(s_key)
                    
                print(f"\n{GREEN}Success! A brand new mystery generated by Gemini is ready.{RESET}")
                time.sleep(2)
                return
            except Exception as e:
                print(f"\n{RED}Error parsing AI case details: {e}. Loading offline case.{RESET}")
                time.sleep(2)
        else:
            print(f"\n{YELLOW}AI generation failed. Loading offline case.{RESET}")
            time.sleep(2)
            
    print(f"\n{GREEN}Loading default offline case: The Secret of Blackwood Manor...{RESET}")
    time.sleep(2)

def generate_plot_twist():
    """Queries Gemini to generate a plot twist (Hidden Witness, Secret Motive, or Fake Alibi)
    based on the current case context. Falls back to a local default twist if offline.
    """
    global detective_score, plot_twist_triggered
    plot_twist_triggered = True
    
    api_key = load_api_key()
    
    suspect_info = []
    for s_id, s in SUSPECTS.items():
        suspect_info.append(f"- {s['name']} ({s['role']}): Alibi was '{s['alibi']}'")
    suspects_summary = "\n".join(suspect_info)
    
    prompt = (
        f"You are a master mystery writer. Introduce a sudden plot twist to our current case.\n\n"
        f"Current Victim: {victim_name}\n"
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
    
    twist_data = None
    if api_key:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": api_key
        }
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json"
            }
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
                twist_data = json.loads(text_response)
        except Exception:
            pass
            
    if not twist_data:
        default_twists = [
            {
                "type": "Secret Motive",
                "title": "The Threatened Exposure Letter",
                "description": f"You discover a hidden lockbox in the Study containing a draft letter. "
                               f"{victim_name} had discovered the killer's financial embezzlements and "
                               f"wrote that they would report them to the police the very next morning. "
                               f"This gave the killer an extremely urgent motive to commit the crime tonight!"
            },
            {
                "type": "Hidden Witness",
                "title": "The Silent Servant",
                "description": "An aged maid, trembling with fear, pulls you aside in the hallway. "
                               "She whispers that at exactly 9:15 PM, she saw someone creeping quietly "
                               "towards the Study door wearing dark medical gloves and holding something concealed in their hand."
            },
            {
                "type": "Fake Alibi",
                "title": "The Frozen Pocketwatch",
                "description": "You notice a shattered pocketwatch dropped near the foyer floorboards. "
                               "The glass is crushed and the hands are frozen precisely at 8:45 PM. "
                               "This physical timestamp completely contradicts one of the suspect's timeline statements!"
            }
        ]
        twist_data = random.choice(default_twists)
        
    clear_screen()
    print_banner("!!! PLOT TWIST !!!", RED)
    play_retro_chime("twist")
    print(f"{BOLD}Twist Type:{RESET} {YELLOW}{twist_data['type']}{RESET}")
    print(f"{BOLD}Title:{RESET} {WHITE}{twist_data['title']}{RESET}\n")
    print_typewriter(twist_data["description"], 0.02)
    print("-" * 60)
    
    custom_notes.append(f"[PLOT TWIST - {twist_data['type']}] {twist_data['title']}: {twist_data['description']}")
    
    detective_score += 15
    update_difficulty()
    print(f"\n{GREEN}* Case notes updated! +15 Detective Points *{RESET}")
    input("\nPress Enter to return to your investigation...")

# ==============================================================================
# 5. CORE GAMEPLAY ACTIONS
# ==============================================================================

def print_welcome():
    """Prints the welcome screen and introduction."""
    print_banner("THE SECRET OF BLACKWOOD MANOR", BLUE)
    intro_text = (
        f"Welcome, Detective! You have been called to Blackwood Manor.\n"
        f"The victim is {BOLD}{victim_name}{RESET}, {victim_desc}.\n"
        f"He was found dead in his private study!\n\n"
        "Cause of death: Poisoned with Aconite, slipped into his whiskey glass.\n"
        "You have exactly 12 hours (actions) before the chief inspector takes over.\n\n"
        "GAME RULES:\n"
        "- Search rooms to gather clues (+10 points each)\n"
        "- Interrogate suspects (+5 points on first meet)\n"
        "- Find hidden contradictions between alibis and clues (+20 points each)\n\n"
        "As your score increases, the difficulty will scale from Beginner -> Intermediate -> Advanced!\n"
        "To win, you must accuse the correct suspect, naming the exact weapon and the key proof."
    )
    print_wrapped(intro_text)
    input(f"\n{YELLOW}Press Enter to start your investigation...{RESET}")
    clear_screen()

def show_status():
    """Displays HUD, difficulty, hints (Beginner), room info, and exits."""
    room = ROOMS[current_room]
    update_difficulty()
    global visited_rooms
    
    # HUD Display
    diff_colors = {"Beginner": GREEN, "Intermediate": YELLOW, "Advanced": RED}
    color = diff_colors[difficulty_level]
    
    print_banner(room["name"], CYAN)
    
    # Print ASCII art icons based on the room to add a visual theme
    if current_room == "study":
        print(f"{CYAN}       🕵️‍♂️  [ STUDY ]\n        _______\n       |[_____]|\n       |  / \\  |\n{RESET}")
    elif current_room == "library":
        print(f"{CYAN}       📚  [ LIBRARY ]\n        _________\n       /   1.5   \\\n      |=========|\n      |_________|\n{RESET}")
    elif current_room == "lounge":
        print(f"{CYAN}       🎱  [ LOUNGE ]\n         o   o\n        \\___/\n{RESET}")
    elif current_room == "conservatory":
        print(f"{CYAN}       🌱  [ CONSERVATORY ]\n         _/\\_/\\_\n        \\\\      /\n         \\\\____/\n{RESET}")
    elif current_room == "foyer":
        print(f"{CYAN}       🔑  [ FOYER ]\n         |===|\n         |[_]|\n         |   |\n{RESET}")
    
    # Immersive room entry thoughts (prints once per room)
    if current_room not in visited_rooms:
        visited_rooms.append(current_room)
        if current_room == "study":
            print_detective_thought(f"The study. {victim_name}'s body was found slumped at the desk. I need to scan for traces.")
        elif current_room == "library":
            print_detective_thought("The Library... high shelves and hidden corners. A perfect place to store secrets.")
        elif current_room == "lounge":
            print_detective_thought("Billiards, drinks, and leather chairs. Arthur claims he spent his evening here.")
        elif current_room == "conservatory":
            print_detective_thought("The Conservatory. Damp heat and toxic botanical specimens. Dr. Croft's research lab.")
        elif current_room == "foyer":
            print_detective_thought("The foyer. The grand hall is quiet now, but the exits will lead me to the truth.")

    # Calculate Rank and Progress Bar
    if detective_score <= 30:
        current_rank = "Amateur Constable 👮"
        next_rank = "Local Deputy 🕵️‍♂️"
        prev_limit = 0
        next_limit = 31
    elif detective_score <= 70:
        current_rank = "Local Deputy 🕵️‍♂️"
        next_rank = "Private Detective 🔍"
        prev_limit = 31
        next_limit = 71
    elif detective_score <= 120:
        current_rank = "Private Detective 🔍"
        next_rank = "Special Investigator 🗂️"
        prev_limit = 71
        next_limit = 121
    elif detective_score <= 180:
        current_rank = "Special Investigator 🗂️"
        next_rank = "Sherlock Holmes Grade Master Sleuth 🧠🏆"
        prev_limit = 121
        next_limit = 181
    else:
        current_rank = "Sherlock Holmes Grade Master Sleuth 🧠🏆"
        next_rank = "MAX RANK"
        prev_limit = 181
        next_limit = 181

    if next_rank == "MAX RANK":
        bar = "█" * 20
        progress_str = f"{BOLD}Rank:{RESET} {YELLOW}{current_rank}{RESET} | [{GREEN}{bar}{RESET}] (MAX RANK ACHIEVED!)"
    else:
        range_pts = next_limit - prev_limit
        current_pts = detective_score - prev_limit
        fraction = min(1.0, max(0.0, current_pts / range_pts))
        filled = int(20 * fraction)
        bar_filled = "█" * filled
        bar_empty = "░" * (20 - filled)
        progress_str = f"{BOLD}Rank:{RESET} {YELLOW}{current_rank}{RESET} | [{GREEN}{bar_filled}{RESET}{WHITE}{bar_empty}{RESET}] ({detective_score}/{next_limit} to {next_rank})"

    print(f"{BOLD}Score:{RESET} {GREEN}{detective_score} pts{RESET} | "
          f"{BOLD}Difficulty:{RESET} {color}{difficulty_level}{RESET} | "
          f"{BOLD}Hours Left:{RESET} {RED}{turns_left}h{RESET}")
    print(progress_str)
    print("-" * 60)
    print_wrapped(room["description"])
    print()
    
    # Show suspects present
    room_suspects = room["suspects"]
    if room_suspects:
        print(f"{BOLD}Suspects present here:{RESET}")
        for s_id in room_suspects:
            suspect = SUSPECTS[s_id]
            print(f"  - {YELLOW}{suspect['name']}{RESET} ({suspect['role']})")
    else:
        print(f"{WHITE}There are no suspects in this room.{RESET}")
    print()

    # Show exits
    print(f"{BOLD}Accessible Rooms:{RESET}")
    for conn in room["connections"]:
        conn_name = ROOMS[conn]["name"]
        print(f"  -> {GREEN}{conn_name}{RESET} (type '{conn}')")
    print()

    # Beginner hints
    if difficulty_level == "Beginner":
        print(f"{BLUE}{BOLD}Detective Hint:{RESET}")
        if "whiskey_glass" not in collected_clue_ids:
            print(" - Search the Study (Crime Scene) for clues about the murder weapon.")
        elif "ledger_page" not in collected_clue_ids:
            print(" - Search the Library for documents regarding the victim's finances.")
        elif len(interrogated_suspects) < 3:
            print(" - Make sure to move to rooms with suspects and interrogate them about their alibis.")
        elif len(resolved_contradictions) < 3:
            print(" - Confront suspects by asking them about clues that break their alibis (e.g. ask Eleanor about her Earring).")
        else:
            print(" - You have found contradictions and key evidence! Head to the Library to accuse the killer.")
        print()

def move_room():
    """Lets the player move to connected rooms. Costs 1 hour."""
    global current_room, turns_left
    room = ROOMS[current_room]
    
    # Draw Manor Map
    draw_map()
    print()
    
    options = {}
    for idx, conn in enumerate(room["connections"], 1):
        conn_name = ROOMS[conn]["name"]
        options[str(idx)] = f"{conn_name}"
    draw_menu(options, "NAVIGATION MENU - SELECT DESTINATION")
        
    choice = input(f"\n{BOLD}Enter room number, name or ID:{RESET} ").strip().lower()
    
    target = None
    # 1. Check if selection is an option index number
    try:
        choice_idx = int(choice)
        if 1 <= choice_idx <= len(room["connections"]):
            target = room["connections"][choice_idx - 1]
    except ValueError:
        pass
        
    # 2. Check by name or ID matching
    if not target:
        for conn in room["connections"]:
            if choice == conn or choice == ROOMS[conn]["name"].lower() or choice.replace("the ", "") == ROOMS[conn]["name"].lower().replace("the ", ""):
                target = conn
                break
            
    if target:
        current_room = target
        turns_left -= 1
        clear_screen()
        print(f"\n{GREEN}* You moved to the {ROOMS[current_room]['name']}. (1 hour passed) *{RESET}")
    else:
        print(f"\n{RED}Error: That room is not connected here!{RESET}")
        input("\nPress Enter to continue...")

def search_room():
    """Searches the room for clues. Costs 1 hour (Beginner/Intermediate) or 2 hours (Advanced)."""
    global turns_left, detective_score
    room = ROOMS[current_room]
    update_difficulty()
    
    # Determine cost based on difficulty
    search_cost = 2 if difficulty_level == "Advanced" else 1
    
    clear_screen()
    print_banner(f"Searching {room['name']}...", YELLOW)
    if difficulty_level == "Advanced":
        print(f"{RED}{BOLD}Advanced Difficulty:{RESET} Due to police tape and patrols, searching takes {search_cost} hours.")
        
    print_typewriter("You examine the surroundings, searching cupboards, bookshelves, and bins...", 0.02)
    
    room_clues = room["clues"]
    found_any = False
    
    for clue_id in room_clues:
        if clue_id not in collected_clue_ids:
            clue = CLUES[clue_id]
            collected_clue_ids.append(clue_id)
            clues_found.append(clue["name"])
            
            # Award points for finding clues
            detective_score += 10
            play_retro_chime("clue")
            
            print(f"\n{GREEN}[NEW CLUE DISCOVERED! +10 Points] {BOLD}{clue['name']}{RESET}")
            print_wrapped(clue["description"], prefix="  ")
            
            # Dynamic detective thoughts
            if clue_id == "whiskey_glass":
                print_detective_thought("Trace almonds smell on the rim... Aconite, slipped into the glass.")
            elif clue_id == "will_papers":
                print_detective_thought(f"Eleanor stood to lose everything. That is a textbook motive for murder.")
            elif clue_id == "ledger_page":
                print_detective_thought("J.C. embezzled £50,000 from the charity. Croft had to silence him before he went public.")
            elif clue_id == "bookie_letter":
                print_detective_thought("Arthur's bookies are breathing down his neck. He needed his father's inheritance immediately.")
            elif clue_id == "pearl_earring":
                print_detective_thought("Eleanor's earring dropped right here in the study... she lied about never leaving the Library.")
            elif clue_id == "billiard_cover":
                print_detective_thought("This billiard cover is covered in dust. Arthur didn't hit a single ball tonight.")
            elif clue_id == "latex_glove":
                print_detective_thought("A doctor's glove containing traces of the poison... Croft was here.")
                
            found_any = True
            
    if not found_any:
        print(f"\n{WHITE}You search thoroughly but find no new clues here.{RESET}")
        
    turns_left -= search_cost
    update_difficulty()
    
    if found_any and len(collected_clue_ids) >= 3 and not plot_twist_triggered:
        print(f"\n{RED}{BOLD}* Search complete. ({search_cost} hour(s) passed) *{RESET}")
        input(f"\n{RED}{BOLD}Wait... you've found at least 3 clues! Press Enter as a sudden realization hits you...{RESET}")
        generate_plot_twist()
    else:
        print(f"\n{YELLOW}* Search complete. ({search_cost} hour(s) passed) *{RESET}")
        input("\nPress Enter to continue...")

def interrogate_suspect():
    """Interrogation dialogue with suspect. Refuses secrets in Intermediate/Advanced. Hostile in Advanced."""
    global turns_left, detective_score
    room = ROOMS[current_room]
    room_suspects = room["suspects"]
    update_difficulty()
    
    if not room_suspects:
        print(f"\n{RED}There is no one here to interrogate!{RESET}")
        input("\nPress Enter to continue...")
        return
        
    clear_screen()
    print_banner("INTERROGATION", MAGENTA)
    
    options = {}
    for idx, s_id in enumerate(room_suspects, 1):
        options[str(idx)] = f"{SUSPECTS[s_id]['name']} ({SUSPECTS[s_id]['role']})"
    options["0"] = "Go Back"
    draw_menu(options, "SELECT SUSPECT")
    
    try:
        sel = int(input(f"\n{BOLD}Select suspect number:{RESET} ").strip())
    except ValueError:
        print(f"{RED}Invalid input!{RESET}")
        input("\nPress Enter to continue...")
        return
        
    if sel == 0:
        return
    elif sel < 1 or sel > len(room_suspects):
        print(f"{RED}Invalid selection!{RESET}")
        input("\nPress Enter to continue...")
        return
        
    suspect_id = room_suspects[sel - 1]
    suspect = SUSPECTS[suspect_id]
    
    # Award points on first interrogation
    if suspect_id not in interrogated_suspects:
        interrogated_suspects.append(suspect_id)
        detective_score += 5
        print(f"\n{GREEN}[FIRST INTERROGATION! +5 Points] You begin questioning {suspect['name']}.{RESET}")
        time.sleep(1.5)
        
    while True:
        clear_screen()
        print_banner(f"Interrogating: {suspect['name']}", MAGENTA)
        print(f"{BOLD}Description:{RESET} {suspect['description']}\n")
        
        # Build question options
        questions = [
            ("Ask about their alibi", "alibi"),
            ("Ask about their motive", "motive"),
            ("Ask about their secrets", "secret")
        ]
        
        for other_id in SUSPECTS:
            if other_id != suspect_id:
                questions.append((f"Ask about {SUSPECTS[other_id]['name']}", f"about_{other_id.split('_')[-1]}"))
                
        for clue_id in collected_clue_ids:
            clue_name = CLUES[clue_id]["name"]
            questions.append((f"Ask about the {clue_name}", f"about_{clue_id}"))
            
        options = {}
        for idx, (label, _) in enumerate(questions, 1):
            options[str(idx)] = label
        options["0"] = "Finish questioning"
        draw_menu(options, f"QUESTIONING {suspect['name']}")
        
        print(f"\n{BOLD}Hours Left:{RESET} {turns_left}h")
        
        try:
            choice = int(input(f"\n{BOLD}Select question number (costs 1 hour):{RESET} ").strip())
        except ValueError:
            print(f"{RED}Invalid selection!{RESET}")
            time.sleep(1)
            continue
            
        if choice == 0:
            break
        elif choice < 1 or choice > len(questions):
            print(f"{RED}Invalid selection!{RESET}")
            time.sleep(1)
            continue
            
        # Deduct time
        turns_left -= 1
        
        question_label, dialogue_key = questions[choice - 1]
        
        # --- DIFFICULTY DYNAMICS ---
        # 1. Intermediate/Advanced: Suspects refuse secrets if clues are less than 2
        if (difficulty_level == "Intermediate" or difficulty_level == "Advanced") and dialogue_key == "secret" and len(collected_clue_ids) < 2:
            clear_screen()
            print_banner(f"Question: {question_label}", MAGENTA)
            print(f"{YELLOW}{suspect['name']}{RESET} responds:")
            print("-" * 60)
            print_wrapped('"I don\'t trust you enough to share private secrets, detective. Find more evidence first."')
            print("-" * 60)
            input("\nPress Enter to continue...")
            continue
            
        # 2. Advanced: Hostile suspects terminate conversation if asked about other suspects
        is_about_other_suspect = False
        if dialogue_key.startswith("about_"):
            target_key = dialogue_key[6:] # strip "about_"
            for other_id in SUSPECTS:
                if other_id != suspect_id and (other_id == target_key or other_id.split("_")[-1] == target_key):
                    is_about_other_suspect = True
                    break
                    
        if difficulty_level == "Advanced" and is_about_other_suspect:
            clear_screen()
            print_banner(f"Question: {question_label}", MAGENTA)
            print(f"{YELLOW}{suspect['name']}{RESET} responds:")
            print("-" * 60)
            print_wrapped('"How dare you ask me to gossip or accuse others! This interrogation is over!"')
            print("-" * 60)
            print(f"\n{RED}Advanced Level Alert: Interrogation terminated by suspect!{RESET}")
            input("\nPress Enter to continue...")
            break
            
        # Fetch dialogue response
        response = suspect["dialogue"].get(dialogue_key, "I have nothing to say about that.")
        
        # --- CONTRADICTION DETECTION AND SCORING ---
        is_contradiction = False
        contradiction_id = f"{suspect_id}_{dialogue_key}"
        
        # Define alibi-breaking matches
        if dialogue_key.startswith("about_"):
            clue_id_asked = dialogue_key[6:] # Strip "about_"
            if suspect_id in CONTRADICTIONS and CONTRADICTIONS[suspect_id] == clue_id_asked:
                is_contradiction = True
            
        if is_contradiction:
            if contradiction_id not in resolved_contradictions:
                resolved_contradictions.append(contradiction_id)
                detective_score += 20
                update_difficulty()
                play_retro_chime("contradiction")
                # Highlight points awarded
                response = response.replace("[CONTRADICTION FOUND!]", f"{GREEN}[CONTRADICTION FOUND! +20 Points]{RESET}")
            else:
                # Format without points if asked again
                response = response.replace("[CONTRADICTION FOUND!]", f"{GREEN}[CONTRADICTION ALREADY RESOLVED]{RESET}")
            
        clear_screen()
        print_banner(f"Question: {question_label}", MAGENTA)
        print(f"{YELLOW}{suspect['name']}{RESET} responds:")
        print("-" * 60)
        print_wrapped(response)
        print("-" * 60)
        
        if turns_left <= 0:
            print(f"\n{RED}You have run out of time during interrogation!{RESET}")
            input("\nPress Enter to proceed...")
            break
            
        input("\nPress Enter to continue interrogation...")

def view_clues():
    """Allows players to view the Detective Notebook via a structured, boxed menu."""
    while True:
        clear_screen()
        print_banner("DETECTIVE NOTEBOOK", WHITE)
        
        options = {
            "1": "View Collected Clues & Evidence",
            "2": "View Suspect Dossiers & Alibi Status",
            "3": "View Interactive Manor Map",
            "4": "View & Write Case Notes",
            "0": "Return to Room"
        }
        draw_menu(options, "NOTEBOOK SUB-SECTIONS")
        
        choice = input(f"\n{BOLD}Select a section (0-4):{RESET} ").strip()
        
        if choice == "1":
            # 1. View Collected Clues
            while True:
                clear_screen()
                print_banner("COLLECTED CLUES & EVIDENCE", GREEN)
                print(f"{BOLD}--- COLLECTED CLUES ({len(collected_clue_ids)}/7) ---{RESET}\n")
                if collected_clue_ids:
                    for idx, clue_id in enumerate(collected_clue_ids, 1):
                        clue = CLUES[clue_id]
                        print(f"  [{idx}] {GREEN}{clue['name']}{RESET}")
                        print_wrapped(clue["description"], prefix="      ")
                        print()
                else:
                    print(f"  {WHITE}No clues discovered yet. Search rooms to find them!{RESET}\n")
                
                print("-" * 60)
                input("Press Enter to return to Notebook menu...")
                break
                
        elif choice == "2":
            # 2. View Suspect Dossiers
            while True:
                clear_screen()
                print_banner("SUSPECT DOSSIERS & ALIBIS", YELLOW)
                print(f"{BOLD}--- SUSPECT FILES ---{RESET}\n")
                for s_id, suspect in SUSPECTS.items():
                    met_status = f"{GREEN}[Met]{RESET}" if s_id in interrogated_suspects else f"{WHITE}[Unmet]{RESET}"
                    
                    # Check if alibi is broken dynamically
                    alibi_broken = any(cid.startswith(s_id) for cid in resolved_contradictions)
                    if s_id in interrogated_suspects:
                        if alibi_broken:
                            status_str = f"{RED}{BOLD}[ALIBI BROKEN ❌]{RESET}"
                        else:
                            status_str = f"{YELLOW}[Interrogated]{RESET}"
                    else:
                        status_str = f"{WHITE}[Unmet - Question them]{RESET}"
                        
                    print(f" • {YELLOW}{suspect['name']}{RESET} - {suspect['role']}")
                    print(f"   Status: {status_str}")
                    if s_id in interrogated_suspects:
                        print(f"   {WHITE}Alibi:{RESET} {suspect['alibi']}")
                        print(f"   {WHITE}Motive:{RESET} {suspect['motive']}")
                        if alibi_broken:
                            # Print the broken confession dynamically
                            contradiction_clue_id = CONTRADICTIONS.get(s_id)
                            if contradiction_clue_id:
                                response = suspect["dialogue"].get(f"about_{contradiction_clue_id}", "")
                                clean_resp = response.replace("[CONTRADICTION FOUND!]", "").replace("[CONTRADICTION ALREADY RESOLVED]", "").strip()
                                clean_resp = clean_resp.replace(GREEN, "").replace(RESET, "")
                                print_wrapped(f"   {RED}Confession:{RESET} \"{clean_resp}\"")
                    print()
                
                print("-" * 60)
                input("Press Enter to return to Notebook menu...")
                break
                
        elif choice == "3":
            # 3. View Manor Map
            clear_screen()
            draw_map()
            print()
            input("Press Enter to return to Notebook menu...")
            
        elif choice == "4":
            # 4. Custom notes
            while True:
                clear_screen()
                print_banner("CUSTOM CASE NOTES", MAGENTA)
                if custom_notes:
                    for idx, note in enumerate(custom_notes, 1):
                        print(f"  {idx}. {note}")
                else:
                    print("  No custom notes written.")
                print()
                
                options = {
                    "1": "Add new note",
                    "0": "Return to Notebook menu"
                }
                draw_menu(options, "NOTES OPTIONS")
                note_choice = input(f"\n{BOLD}Select option:{RESET} ").strip()
                if note_choice == "1":
                    new_note = input(f"\n{BOLD}Type note contents:{RESET} ").strip()
                    if new_note:
                        custom_notes.append(new_note)
                        print(f"\n{GREEN}Note added successfully!{RESET}")
                        time.sleep(1)
                elif note_choice == "0" or note_choice == "":
                    break
                    
        elif choice == "0" or choice == "":
            break
        else:
            print(f"{RED}Invalid selection!{RESET}")
            time.sleep(1)

def accuse_killer():
    """Accusation system. Requires correct suspect, weapon, and proof. Exits on execution."""
    clear_screen()
    print_banner("FINAL ACCUSATION", RED)
    print_wrapped(
        "WARNING: You are about to present your final case. You must be certain. "
        "If you accuse the wrong suspect, or lack the correct proof, the killer will "
        "escape and you will lose the game!"
    )
    print()
    confirm = input("Are you ready to make your accusation? (yes/no): ").strip().lower()
    if confirm != "yes" and confirm != "y":
        return
        
    # 1. Accuse Killer
    clear_screen()
    print_banner("ACCUSE: Step 1 - The Killer", RED)
    suspect_ids = list(SUSPECTS.keys())
    
    options = {}
    for idx, s_id in enumerate(suspect_ids, 1):
        options[str(idx)] = f"{SUSPECTS[s_id]['name']} ({SUSPECTS[s_id]['role']})"
    options["0"] = "Cancel"
    draw_menu(options, "SELECT SUSPECT FOR ACCUSATION")
    
    try:
        killer_choice = int(input(f"\n{BOLD}Select the killer's number:{RESET} ").strip())
    except ValueError:
        print(f"{RED}Invalid selection. Accusation cancelled.{RESET}")
        input("\nPress Enter to continue...")
        return
        
    if killer_choice == 0:
        return
    if killer_choice < 1 or killer_choice > len(suspect_ids):
        print(f"{RED}Invalid selection. Accusation cancelled.{RESET}")
        input("\nPress Enter to continue...")
        return
        
    accused_killer = suspect_ids[killer_choice - 1]
    
    # 2. Accuse Weapon
    clear_screen()
    print_banner("ACCUSE: Step 2 - The Murder Weapon", RED)
    print("Select the murder weapon or method from your collected clues:")
    
    if not collected_clue_ids:
        print(f"\n{RED}You haven't found any clues to accuse anyone with! Search rooms first.{RESET}")
        input("\nPress Enter to continue...")
        return
        
    options = {}
    for idx, clue_id in enumerate(collected_clue_ids, 1):
        options[str(idx)] = CLUES[clue_id]['name']
    options["0"] = "Cancel"
    draw_menu(options, "SELECT MURDER WEAPON")
    
    try:
        weapon_choice = int(input(f"\n{BOLD}Select weapon clue number:{RESET} ").strip())
    except ValueError:
        print(f"{RED}Invalid selection. Accusation cancelled.{RESET}")
        input("\nPress Enter to continue...")
        return
        
    if weapon_choice == 0:
        return
    if weapon_choice < 1 or weapon_choice > len(collected_clue_ids):
        print(f"{RED}Invalid selection. Accusation cancelled.{RESET}")
        input("\nPress Enter to continue...")
        return
        
    accused_weapon = collected_clue_ids[weapon_choice - 1]
    
    # 3. Accuse Proof
    clear_screen()
    print_banner("ACCUSE: Step 3 - The Proof / Evidence", RED)
    print("Select the key evidence linking the killer to the crime:")
    
    options = {}
    for idx, clue_id in enumerate(collected_clue_ids, 1):
        options[str(idx)] = CLUES[clue_id]['name']
    options["0"] = "Cancel"
    draw_menu(options, "SELECT KEY PROOF")
    
    try:
        evidence_choice = int(input(f"\n{BOLD}Select proof clue number:{RESET} ").strip())
    except ValueError:
        print(f"{RED}Invalid selection. Accusation cancelled.{RESET}")
        input("\nPress Enter to continue...")
        return
        
    if evidence_choice == 0:
        return
    if evidence_choice < 1 or evidence_choice > len(collected_clue_ids):
        print(f"{RED}Invalid selection. Accusation cancelled.{RESET}")
        input("\nPress Enter to continue...")
        return
        
    accused_evidence = collected_clue_ids[evidence_choice - 1]
    
    # 4. Accusation Resolution
    clear_screen()
    print_banner("THE ACCUSATION AND RESOLUTION", BOLD)
    print_typewriter("You assemble the suspects in the Library...", 0.02)
    print_typewriter("You clear your throat and announce your findings...", 0.02)
    print(f"\n\"I accuse {BOLD}{SUSPECTS[accused_killer]['name']}{RESET} of the murder!\"")
    print(f"\"They poisoned {victim_name} using the {BOLD}{CLUES[accused_weapon]['name']}{RESET}!\"")
    print(f"\"And my proof is the {BOLD}{CLUES[accused_evidence]['name']}{RESET}!\"\n")
    time.sleep(2)
    
    # Validate details dynamically
    if accused_killer == killer_id and accused_weapon == weapon_clue_id and accused_evidence == proof_clue_id:
        play_retro_chime("success")
        win_outro = (
            "================================================================================\n"
            "                                 CASE SOLVED!\n"
            "================================================================================\n"
            f"{SUSPECTS[killer_id]['name']}'s face goes pale as you display the key proof.\n\n"
            f"\"Fine! Yes, I did it!\" they scream. \"{victim_name} was going to ruin me!\n"
            f"I used the {CLUES[weapon_clue_id]['name']}. I had no choice!\"\n\n"
            "The local police officers rush in and take the killer away in handcuffs.\n"
            f"Your deduction was flawless. You have solved the secret of Blackwood Manor!\n"
            f"Final Detective Score: {detective_score} points!\n"
            "================================================================================"
        )
        print_typewriter(win_outro, 0.005)
        print_end_game_summary(success=True)
        input("\nPress Enter to exit the game...")
        sys.exit(0)
    else:
        play_retro_chime("failure")
        print(f"{RED}{BOLD}YOUR ACCUSATION WAS INCORRECT!{RESET}")
        print("-" * 60)
        if accused_killer != killer_id:
            print_wrapped(f"Your accusation of {SUSPECTS[accused_killer]['name']} falls flat. They present a clear alibi and your accusations are laughed off. You arrested an innocent person!")
        elif accused_weapon != weapon_clue_id:
            print_wrapped(f"Your suspect sneers. While they are indeed guilty, your description of the murder weapon was incorrect.")
        else:
            print_wrapped(f"Your suspect laughs off your charges. 'You have no proof linking me to this!' Indeed, without the key proof, your case is circumstantial and dismissed.")
        print("-" * 60)
        print_end_game_summary(success=False, reason="False Arrest")
        input("\nPress Enter to exit the game...")
        sys.exit(0)

# ==============================================================================
# 6. MAIN GAME LOOP
# ==============================================================================

def main():
    global current_room, turns_left
    
    # Enable ANSI escape characters on Windows consoles
    if os.name == 'nt':
        os.system('color')
        
    clear_screen()
    initialize_game()
    clear_screen()
    print_welcome()
    
    while True:
        # Check game over timer
        if turns_left <= 0:
            clear_screen()
            play_retro_chime("failure")
            loss_outro = (
                "================================================================================\n"
                "                                 TIME IS UP!\n"
                "================================================================================\n"
                "The grandfather clock strikes midnight. The chief inspector arrives.\n"
                "\"Detective Vance, your time is up. We are taking over the case.\"\n\n"
                "Because of the delay, the killer managed to destroy the ledger and replace the poison vial.\n"
                "The case remains cold, and the killer escapes justice.\n\n"
                f"Final Detective Score: {detective_score} points.\n"
                "GAME OVER - You ran out of actions!"
                "================================================================================"
            )
            print_typewriter(loss_outro, 0.005)
            print_end_game_summary(success=False, reason="Out of Time")
            sys.exit(0)
            
        show_status()
        
        options = {
            "1": "Move to another room",
            "2": "Search this room for clues",
            "3": "Interrogate someone in this room",
            "4": "View collected clues & Notebook",
            "5": "Make Final Accusation",
            "0": "Quit Game"
        }
        draw_menu(options, "ACTION MENU")
        
        choice = input(f"\n{BOLD}Select an action (0-5):{RESET} ").strip()
        
        if choice == "1":
            move_room()
        elif choice == "2":
            search_room()
        elif choice == "3":
            interrogate_suspect()
        elif choice == "4":
            view_clues()
        elif choice == "5":
            accuse_killer()
        elif choice == "0":
            clear_screen()
            print("Thank you for playing!")
            break
        else:
            print(f"\n{RED}Invalid selection. Please choose between 0 and 5.{RESET}")
            time.sleep(1)
            clear_screen()

if __name__ == "__main__":
    main()
