# cases.py
# Module containing default offline cases for the Murder Mystery game.

OFFLINE_CASES_DB = [
    {
        "title": "The Secret of Blackwood Manor",
        "victim_pool": [
            {"name": "Lord Reginald Harrington", "desc": "a wealthy philanthropist and art collector"},
            {"name": "Lord Albert Blackwood", "desc": "a reclusive estate owner and history buff"},
            {"name": "Lord Montgomery Vance", "desc": "a wealthy coal baron and industrialist"}
        ],
        "rooms_templates": {
            "foyer": {
                "name": "The Foyer",
                "description": "The grand entrance hall of Blackwood Manor. A large chandelier hangs from the ceiling.",
                "connections": ["study", "library", "lounge", "conservatory"]
            },
            "study": {
                "name": "The Study (CRIME SCENE)",
                "description": "The official CRIME SCENE where the victim's body was found slumped at his desk.",
                "connections": ["foyer", "library"]
            },
            "library": {
                "name": "The Library",
                "description": "A quiet room filled with tall, dusty bookshelves and a warm, crackling fireplace.",
                "connections": ["foyer", "study"]
            },
            "conservatory": {
                "name": "The Conservatory",
                "description": "A glass greenhouse filled with damp air and exotic, shadow-casting plants.",
                "connections": ["foyer"]
            },
            "lounge": {
                "name": "The Lounge",
                "description": "A comfortable room containing a green-felt billiard table, leather armchairs, and a drinks cabinet.",
                "connections": ["foyer"]
            }
        },
        "clues_template": {
            "whiskey_glass": {
                "name": "Poisoned Whiskey Glass",
                "description": "A crystal glass on {victim_surname}'s desk smelling of bitter almonds (a sign of Aconite poison).",
                "room": "study"
            },
            "will_papers": {
                "name": "Confidential Will",
                "description": "Signed papers in the study desk showing {victim_name} was cutting off Lady Eleanor completely.",
                "room": "study"
            },
            "ledger_page": {
                "name": "Torn Ledger Page",
                "description": "A discarded sheet detailing a charity audit showing 'J.C.' embezzled £50,000 from {victim_surname}'s funds.",
                "room": "library"
            },
            "bookie_letter": {
                "name": "Threatening Letter",
                "description": "A bookie letter addressed to Arthur Harrington demanding £20,000 immediately.",
                "room": "lounge"
            },
            "pearl_earring": {
                "name": "Dropped Pearl Earring",
                "description": "A white pearl earring found on the floor of the Study (Crime Scene). It matches Lady Eleanor's set.",
                "room": "study"
            },
            "billiard_cover": {
                "name": "Dusty Billiard Cover",
                "description": "A thick, dusty canvas cover completely draped over the billiard table. It hasn't been removed in weeks.",
                "room": "lounge"
            },
            "latex_glove": {
                "name": "Stained Latex Glove",
                "description": "A medical glove in the Conservatory bin, stained with whiskey and trace elements of Aconite.",
                "room": "conservatory"
            }
        },
        "suspects_template": {
            "lady_eleanor": {
                "name": "Lady Eleanor {victim_surname}",
                "role": "The Estranged Wife",
                "description": "The elegant wife of the victim. She stands tall, wearing black lace and looking cold.",
                "alibi": "I was in the Library reading my historical novel all evening. I did not go to any other rooms, especially not the Study.",
                "motive": "Yes, {victim_name} and I had our disagreements, but I would not resort to murder.",
                "dialogue": {
                    "alibi": "I went to the Library around 7 PM and stayed there until the housekeeper found him. I did not leave the room.",
                    "motive": "He was planning to divorce me and leave me with nothing, but I would have fought him in court, not poisoned {victim_name}.",
                    "secret": "We argued in the study before dinner because he was being unreasonable. But that is all.",
                    "about_arthur": "Arthur is a foolish boy who spends too much money gambling. But he is not a murderer.",
                    "about_croft": "Dr. Croft has been our doctor for years. My husband trusted him completely with charity accounts.",
                    "about_whiskey_glass": "{victim_name} always had a glass of whiskey before bed. He kept the bottle in his study.",
                    "about_will_papers": "So you found the will. Yes, he wanted to cut me off. He was a cruel partner.",
                    "about_ledger_page": "A ledger page? I know nothing of charity finances. Dr. Croft managed those accounts.",
                    "about_bookie_letter": "Another one of Arthur's debts... It is disappointing.",
                    "about_pearl_earring": "My... pearl earring? You found it in the Study? [CONTRADICTION FOUND!] Oh dear... okay, fine. I did slip into the Study briefly after dinner to look for the Will. I lied because I was terrified of being suspected. But he was already dead when I got there, I swear!",
                    "about_billiard_cover": "I know nothing of Arthur's games.",
                    "about_latex_glove": "Medical gloves? Those belong to Dr. Croft, surely."
                },
                "room": "library"
            },
            "arthur": {
                "name": "Arthur {victim_surname}",
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
                },
                "room": "lounge"
            },
            "dr_croft": {
                "name": "Dr. Julian Croft",
                "role": "The Family Physician",
                "description": "The family doctor. He looks calm and professional, cleaning his glasses with a cloth.",
                "alibi": "I was in the Conservatory cataloging botanical specimens all evening.",
                "motive": "{victim_name} was my dearest friend. I have no reason to wish him harm.",
                "dialogue": {
                    "alibi": "I was in the Conservatory from 7:30 PM until I heard the screams. I was sorting through my collection.",
                    "motive": "We were co-founders of the charity. Our friendship was built on mutual respect.",
                    "secret": "I have nothing to hide, Inspector. I spent my evening in study and observation.",
                    "about_eleanor": "Lady Eleanor is a proud woman. Her marriage to {victim_name} was a union of convenience. They argued frequently.",
                    "about_arthur": "Arthur is a troubled young man. His gambling habits are a tragedy, and {victim_name} was incredibly disappointed in him.",
                    "about_whiskey_glass": "Aconite in his whiskey? Horrible. Aconite causes swift cardiorespiratory failure. It is a terrible way to die.",
                    "about_will_papers": "Ah, {victim_name} mentioned he was considering a new Will. Eleanor stood to lose everything.",
                    "about_ledger_page": "A charity ledger page? Let me see... I-I don't recognize this. This looks like a draft. Our accounts are in perfect order.",
                    "about_bookie_letter": "Ah, another threat to Arthur. It seems Arthur had a powerful motive.",
                    "about_pearl_earring": "Lady Eleanor's earring? I believe I saw her wearing it earlier.",
                    "about_billiard_cover": "Arthur playing billiards? He spends more time drinking than playing.",
                    "about_latex_glove": "A latex glove stained with medical solution and whiskey? [CONTRADICTION FOUND!] Wait, that solution is from my laboratory... Ah! I must have dropped it when I was examining {victim_name}'s body... wait, no! I mean... when I checked on him after the housekeeper found him! Yes, that's it!"
                },
                "room": "conservatory"
            }
        },
        "weapon_clue_id": "whiskey_glass",
        "contradictions": {
            "lady_eleanor": "pearl_earring",
            "arthur": "billiard_cover",
            "dr_croft": "latex_glove"
        },
        "killers": {
            "dr_croft": {
                "proof": "ledger_page",
                "explanation": "Dr. Julian Croft had been embezzling money from the charity funds, as shown in the Torn Ledger Page. Knowing Lord {victim_surname} had discovered the audit discrepancies and would expose him, Dr. Croft poisoned the whiskey glass with Aconite. His stained latex glove found in the Conservatory bin proved he handled the poisoned drink."
            },
            "lady_eleanor": {
                "proof": "will_papers",
                "explanation": "Lady Eleanor {victim_surname} discovered that Lord {victim_surname} was planning to divorce her and leave her completely out of his new will (as shown in the Confidential Will). To secure her inheritance, she slipped Aconite poison into his nightly whiskey glass. Her pearl earring was found dropped at the crime scene, exposing her presence there during the murder."
            },
            "arthur": {
                "proof": "bookie_letter",
                "explanation": "Arthur {victim_surname} was in massive financial trouble due to mounting gambling debts, as shown in the Threatening Letter. When his father refused to lend him any more money, Arthur poisoned his father's whiskey glass to claim his inheritance immediately. The dusty cover on the billiard table proved he lied about playing billiards all evening."
            }
        },
        "hints": [
            "The Study is the crime scene. Search it first to find the murder weapon (Poisoned Whiskey Glass) and look for Lady Eleanor's dropped pearl earring.",
            "Lady Eleanor claims she stayed in the Library and never went to the Study. But her pearl earring was found at the crime scene. Ask her about it!",
            "Arthur claims he played billiards in the Lounge all night. Check the Lounge and search for the billiard table cover to see if he's telling the truth.",
            "Search the Library to find the Torn Ledger Page detailing the charity funds discrepancy.",
            "Examine Dr. Julian Croft's alibi in the Conservatory. The stained latex glove found in the bin will crack his story."
        ],
        "hidden_hint": "A secret ledger note indicates the killer purchased Aconite poison from a chemist in London under an alias. Double check the medical alibi in the Conservatory!"
    },
    {
        "title": "The Sterling Estate Theft",
        "victim_pool": [
            {"name": "Sir Charles Sterling", "desc": "an eccentric archaeologist and museum curator"},
            {"name": "Sir Donald Carter", "desc": "a famous Egyptologist and antique dealer"},
            {"name": "Sir Arthur Pendelton", "desc": "a retired explorer and research professor"}
        ],
        "rooms_templates": {
            "foyer": {
                "name": "The Exhibition Hall",
                "description": "A grand hall filled with glass display cases showing Sir {victim_surname}'s private collection.",
                "connections": ["study", "library", "lounge", "conservatory"]
            },
            "study": {
                "name": "The Curator's Study (CRIME SCENE)",
                "description": "The office where Sir {victim_surname} was found strangled at his desk with an ancient rope.",
                "connections": ["foyer", "library"]
            },
            "library": {
                "name": "The Archive Room",
                "description": "A quiet library housing rare historical texts, excavation maps, and translation journals.",
                "connections": ["foyer", "study"]
            },
            "conservatory": {
                "name": "The Restoration Lab",
                "description": "A laboratory filled with stone cleaning solutions, brushes, and partially cataloged artifacts.",
                "connections": ["foyer"]
            },
            "lounge": {
                "name": "The Vault Room",
                "description": "A reinforced security room where the most valuable gold relics are kept locked behind a vault door.",
                "connections": ["foyer"]
            }
        },
        "clues_template": {
            "ancient_rope": {
                "name": "Ancient Hemp Rope",
                "description": "A piece of thick, coarse rope found near the body in the Study, covered in dust and shipping grease.",
                "room": "study"
            },
            "dropped_necklace": {
                "name": "Dropped Gold Necklace",
                "description": "A fine gold necklace found on the study floor matching Clara's jewelry set.",
                "room": "study"
            },
            "vault_log": {
                "name": "Electronic Vault Log",
                "description": "A digital log showing that the vault door remained locked and unopened all evening.",
                "room": "lounge"
            },
            "broken_glass_shard": {
                "name": "Broken Shard of Glass",
                "description": "A shard of glass from the Restoration Lab door showing it was broken and locked from 8 PM onwards.",
                "room": "conservatory"
            },
            "smuggling_ledger": {
                "name": "Smuggling Ledger",
                "description": "A log of black market antique sales detailing smuggled relics matching Vance's exports.",
                "room": "library"
            },
            "will_donation": {
                "name": "Museum Donation Statement",
                "description": "A signed statement declaring Sir {victim_surname}'s intent to donate his entire collection to the public museum.",
                "room": "study"
            },
            "bribe_ledger": {
                "name": "Bribe Record",
                "description": "A guard's debt notice with an envelope containing cash and a signed note from the killer.",
                "room": "lounge"
            }
        },
        "suspects_template": {
            "clara_sterling": {
                "name": "Clara {victim_surname}",
                "role": "The Rebellious Niece",
                "description": "The niece of the victim, looking restless, wearing bohemian clothing and gold rings.",
                "alibi": "I was in the Archive Room translating excavation guides all evening. I did not go to any other rooms, especially not the Curator's Study.",
                "motive": "He was planning to donate his entire collection to the public museum, leaving me with nothing!",
                "dialogue": {
                    "alibi": "I went to the Archive Room around 7 PM and stayed there studying. I did not leave.",
                    "motive": "He valued his dusty relics more than his own family. But I would not kill him for that.",
                    "secret": "We argued in the study before dinner because he wanted to donate everything. But that is all.",
                    "about_vance": "Marcus Vance is a greedy dealer who only cares about money. I saw him talking to my uncle in the study today.",
                    "about_higgins": "Harold is a nervous guard. He's always complaining about his debts.",
                    "about_ancient_rope": "A thick rope? Smugglers use those to pack crates, don't they?",
                    "about_smuggling_ledger": "I know nothing of smuggling. Speak to Marcus.",
                    "about_will_donation": "The Museum Donation Statement... so you found it. Yes, he wanted to donate the entire collection. It is a cruel decision.",
                    "about_bribe_ledger": "Bribe records? I know nothing of this.",
                    "about_dropped_necklace": "My... gold necklace? You found it in the Study? [CONTRADICTION FOUND!] Oh dear... okay, fine. I did slip into the Study briefly after dinner to look for the Donation statement. I lied because I was terrified of being suspected. But he was already dead when I got there, I swear!",
                    "about_vault_log": "A vault log? I don't manage security.",
                    "about_broken_glass_shard": "Broken glass? I know nothing about that."
                },
                "room": "library"
            },
            "marcus_vance": {
                "name": "Marcus Vance",
                "role": "The Shady Antiquities Dealer",
                "description": "A wealthy dealer in a sleek suit, cleaning a gold ring with a handkerchief.",
                "alibi": "I was in the Vault Room examining the gold sarcophagus all evening. I never left.",
                "motive": "Sir {victim_surname} accused me of smuggling, but we were just in the middle of a business negotiation.",
                "dialogue": {
                    "alibi": "I went to the Vault Room around 8 PM to catalog the sarcophagus. I stayed there all night.",
                    "motive": "Our deal fell through, but I wouldn't murder a business partner over a collection.",
                    "secret": "Fine, we had a disagreement over pricing, but that is standard in this business.",
                    "about_clara": "Clara is a spoiled niece who only wants her uncle's money.",
                    "about_higgins": "Harold Higgins is a security guard. He's incompetent.",
                    "about_ancient_rope": "A rope? I don't deal in packing materials.",
                    "about_smuggling_ledger": "Smuggling sales? Let me see... I-I don't recognize this. This looks like a draft. My accounts are in perfect order.",
                    "about_will_donation": "Sir {victim_surname} donating his collection? That would have ruined our deal.",
                    "about_bribe_ledger": "Bribe records? It seems Harold was in debt.",
                    "about_dropped_necklace": "Clara's jewelry? She wears it constantly.",
                    "about_vault_log": "Wait... you found the vault log showing no logins? [CONTRADICTION FOUND!] Ah... you caught me. I didn't enter the vault room. I was actually sitting in the lobby corner drinking, trying to salvage our negotiation. I was ashamed to admit my deal failed.",
                    "about_broken_glass_shard": "Broken glass? I know nothing."
                },
                "room": "lounge"
            },
            "harold_higgins": {
                "name": "Harold Higgins",
                "role": "The Night Watchman",
                "description": "The estate guard, looking disheveled, nervously checking his watch and biting his nails.",
                "alibi": "I was performing my patrols around the Restoration Lab and conservatory grounds the entire time.",
                "motive": "Sir {victim_surname} was a good boss. I have no reason to want him dead.",
                "dialogue": {
                    "alibi": "I was patrolling the Restoration Lab and the conservatory grounds from 7:30 PM until the alarms went off.",
                    "motive": "I needed my job. I wouldn't kill my employer.",
                    "secret": "I was on duty all night. I didn't see anyone enter the study.",
                    "about_clara": "Clara? She's always shouting at her uncle. I saw them arguing in the study today.",
                    "about_vance": "Marcus Vance? He's a suspicious character. He was hanging around the vault room earlier.",
                    "about_ancient_rope": "A rope? We use rope in the restoration lab to secure heavy stone pieces.",
                    "about_smuggling_ledger": "Smuggling? I don't know anything about antique ledgers.",
                    "about_will_donation": "Museum donation? That would mean the collection is public, I guess.",
                    "about_bribe_ledger": "Please, Detective, don't show that to the police! I was going to pay it back!",
                    "about_dropped_necklace": "Clara's jewelry? I saw her wearing it before dinner.",
                    "about_vault_log": "Vault logs? I don't have access to the vault keys.",
                    "about_broken_glass_shard": "Wait... you found a broken glass shard showing the Restoration Lab door was locked from 8 PM? [CONTRADICTION FOUND!] Ah... you caught me. I didn't patrol the lab. I was actually sleeping in the guard room, trying to recover from a double shift. I was ashamed to admit it."
                },
                "room": "conservatory"
            }
        },
        "weapon_clue_id": "ancient_rope",
        "contradictions": {
            "clara_sterling": "dropped_necklace",
            "marcus_vance": "vault_log",
            "harold_higgins": "broken_glass_shard"
        },
        "killers": {
            "marcus_vance": {
                "proof": "smuggling_ledger",
                "explanation": "Marcus Vance was smuggling valuable artifacts out of Sir {victim_surname}'s collection, as detailed in the Smuggling Ledger. When Sir {victim_surname} uncovered the smuggling ring and threatened to call Scotland Yard, Marcus strangled him in his study using the ancient rope from the shipping crates. The vault log proved Marcus lied about being in the vault room, breaking his alibi."
            },
            "clara_sterling": {
                "proof": "will_donation",
                "explanation": "Clara {victim_surname} discovered that her uncle, Sir {victim_surname}, was planning to donate his entire collection of antiquities to a public museum instead of leaving them to her (as shown in the Museum Donation Statement). To secure the inheritance, Clara strangled her uncle in his study using the ancient rope. Her dropped necklace found at the crime scene broke her alibi."
            },
            "harold_higgins": {
                "proof": "bribe_ledger",
                "explanation": "Harold Higgins was deeply in debt and accepted bribes from antiquities smugglers, as detailed in the Bribe Record. When Sir {victim_surname} caught him stealing a relic from the study desk, Harold panicked and strangled him with the ancient rope. The broken glass shard found in the Restoration Lab proved Harold lied about patrolling there, breaking his alibi."
            }
        },
        "hints": [
            "The Curator's Study is the crime scene. Search it to find the murder weapon (Ancient Hemp Rope) and Clara's dropped necklace.",
            "Clara Sterling claims she stayed in the Archive Room all night. Ask her about the dropped necklace found at the crime scene!",
            "Marcus Vance claims he was in the Vault Room examining the sarcophagus. Check the Vault Room for the Electronic Vault Log.",
            "Ask Marcus Vance about the Electronic Vault Log. It will reveal if he was actually in the Vault Room!",
            "Harold Higgins claims he was patrolling the Restoration Lab. Search the Conservatory for the Broken Shard of Glass to see if the lab was locked."
        ],
        "hidden_hint": "An archaeologist's note mentions Sir {victim_surname} suspected Marcus Vance of smuggling relics out of the country tonight. Look at the vault logs!"
    },
    {
        "title": "The Countess's Last Toast",
        "victim_pool": [
            {"name": "Count Victor Romanov", "desc": "a mysterious wealthy socialite and antique collector"},
            {"name": "Count Sergei Volkov", "desc": "a charismatic diplomat with deep political secrets"},
            {"name": "Count Alexander Orlov", "desc": "a wealthy foreign socialite and art patron"}
        ],
        "rooms_templates": {
            "foyer": {
                "name": "The Grand Ballroom",
                "description": "A massive ballroom decorated with velvet drapes and lit by flickering candles.",
                "connections": ["study", "library", "lounge", "conservatory"]
            },
            "study": {
                "name": "The Private Salon (CRIME SCENE)",
                "description": "The luxurious salon where the Count was found shot at his desk with a silenced pistol.",
                "connections": ["foyer", "library"]
            },
            "library": {
                "name": "The Cigar Lounge",
                "description": "A quiet lounge filled with heavy smoke, leather armchairs, and expensive spirits.",
                "connections": ["foyer", "study"]
            },
            "conservatory": {
                "name": "The Botanical Garden",
                "description": "A greenhouse housing exotic, rare, and poisonous plants from around the world.",
                "connections": ["foyer"]
            },
            "lounge": {
                "name": "The Wine Cellar",
                "description": "A subterranean room stocked with rare vintage wines and oak barrels.",
                "connections": ["foyer"]
            }
        },
        "clues_template": {
            "silenced_pistol": {
                "name": "Silenced Pistol",
                "description": "A caliber-22 pistol fitted with a silencer, found hidden behind the drapes in the Salon.",
                "room": "study"
            },
            "lipstick_cigar": {
                "name": "Lipstick-Stained Cigar",
                "description": "A luxury cigar stub found in the Wine Cellar, marked with Countess Sasha's signature crimson lipstick.",
                "room": "lounge"
            },
            "torn_butler_uniform": {
                "name": "Torn Butler Uniform Cuff",
                "description": "A scrap of black wool fabric caught on the Salon desk drawer, matching Novak's livery.",
                "room": "study"
            },
            "chemical_flask": {
                "name": "Chemical Flask",
                "description": "A specialized glass flask containing trace chemical residue, found dropped in the Botanical Garden.",
                "room": "conservatory"
            },
            "spy_ledger": {
                "name": "Spy Decryption Ledger",
                "description": "A ledger containing decryption keys for foreign intelligence transmissions.",
                "room": "library"
            },
            "blackmail_letters": {
                "name": "Blackmail Correspondence",
                "description": "Letters from Count {victim_surname} threatening to expose Countess Sasha's espionage past.",
                "room": "study"
            },
            "stolen_formula": {
                "name": "Stolen Formula Draft",
                "description": "A draft chemical formula for a synthetic toxin stolen from Count {victim_surname}'s safe.",
                "room": "lounge"
            }
        },
        "suspects_template": {
            "countess_sasha": {
                "name": "Countess Sasha {victim_surname}",
                "role": "The Glamorous Widow",
                "description": "The Count's widow, looking cold and elegant in a red velvet gown, smoking a long cigarette.",
                "alibi": "I was in the Cigar Lounge discussing art with Gregory Novak all evening. I never went to the Private Salon.",
                "motive": "He threatened to leave me for a rival, but I would not murder my own husband.",
                "dialogue": {
                    "alibi": "I went to the Cigar Lounge around 7 PM and stayed there until the housekeeper found him. I did not leave the room.",
                    "motive": "He was planning to divorce me and leave me with nothing, but I would have fought him in court, not shot him.",
                    "secret": "We argued in the Salon before dinner because he was being unreasonable. But that is all.",
                    "about_novak": "Greg Novak is a quiet butler. He is very professional and has been with us for years.",
                    "about_petrov": "Sophia is a chemist hired by my husband to catalog his rare spirits. They worked closely.",
                    "about_silenced_pistol": "A caliber-22 pistol? My husband kept a small handgun collection in his desk.",
                    "about_spy_ledger": "A spy decryption ledger? I know nothing of intelligence operations.",
                    "about_blackmail_letters": "Blackmail letters... so you found them. Yes, he wanted to expose my past. He was a cruel partner.",
                    "about_stolen_formula": "A formula draft? Sophia managed those botanical files.",
                    "about_lipstick_cigar": "My... lipstick-stained cigar? You found it in the Wine Cellar? [CONTRADICTION FOUND!] Oh dear... okay, fine. I did slip into the Wine Cellar briefly after dinner to look for the letters. I lied because I was terrified of being suspected. But he was already dead when I got there, I swear!",
                    "about_torn_butler_uniform": "A torn cuff? That belongs to Gregory Novak, surely.",
                    "about_chemical_flask": "A chemical flask? Sophia's lab equipment, no doubt."
                },
                "room": "library"
            },
            "greg_novak": {
                "name": "Gregory Novak",
                "role": "The Espionage Butler",
                "description": "The loyal butler, standing straight, looking calm and formal in his black tuxedo.",
                "alibi": "I was in the Ballroom greeting guests and serving drinks. I did not step foot in the Salon.",
                "motive": "The Count was a generous employer. I had no reason to wish him harm.",
                "dialogue": {
                    "alibi": "I was in the Grand Ballroom greeting guests and serving drinks all evening.",
                    "motive": "Our friendship was built on mutual respect. I had no motive to murder him.",
                    "secret": "I spent my evening performing my butler duties. I have nothing to hide.",
                    "about_sasha": "Countess Sasha is a proud woman. Her marriage to the Count was a union of convenience. They argued frequently.",
                    "about_petrov": "Sophia Petrov is a troubled young woman. She spends all her time in the botanical garden.",
                    "about_silenced_pistol": "A caliber-22 pistol? That is a very dangerous weapon.",
                    "about_spy_ledger": "A spy ledger? Let me see... I-I don't recognize this. This looks like a draft. Our accounts are in perfect order.",
                    "about_blackmail_letters": "Blackmail letters? It seems Sasha had a powerful motive.",
                    "about_stolen_formula": "Sophia's chemical formula? I know nothing of her research.",
                    "about_lipstick_cigar": "Countess Sasha's cigar? I believe she was smoking earlier.",
                    "about_torn_butler_uniform": "Wait... you found a torn black wool cuff caught on the study desk drawer? [CONTRADICTION FOUND!] Wait, that is from my uniform... Ah! I must have caught it when I was checking the Count's pulse after the housekeeper found him! Yes, that's it!",
                    "about_chemical_flask": "Sophia's flask? I saw her carrying it earlier."
                },
                "room": "ballroom"
            },
            "sophia_petrov": {
                "name": "Sophia Petrov",
                "role": "The Brilliant Chemist",
                "description": "The chemist, looking disheveled, nervously adjusting her laboratory goggles.",
                "alibi": "I was in the Wine Cellar cataloging vintage spirits. I never went to the Salon.",
                "motive": "The Count funded my research. I would never kill my patron.",
                "dialogue": {
                    "alibi": "I was in the Wine Cellar from 7:30 PM until I heard the screams. I was sorting through my collection.",
                    "motive": "He was my patron. His funding was crucial for my research.",
                    "secret": "I spent my evening in study and observation. I have nothing to hide.",
                    "about_sasha": "Countess Sasha? She's cold as ice. I saw them shouting at each other today in the Salon.",
                    "about_novak": "Gregory Novak? The butler. He's always around talking about security systems.",
                    "about_silenced_pistol": "A pistol? I don't use firearms.",
                    "about_spy_ledger": "Espionage logs? I don't know anything about the Count's political dealings.",
                    "about_blackmail_letters": "Blackmail? Countess Sasha must have been furious.",
                    "about_stolen_formula": "Please, Detective, don't show that to the police! I was going to return the formula!",
                    "about_lipstick_cigar": "Sasha's cigar? She smokes them constantly.",
                    "about_torn_butler_uniform": "Gregory Novak's uniform? He wears it every day.",
                    "about_chemical_flask": "Wait... you found my chemical flask dropped in the Botanical Garden? [CONTRADICTION FOUND!] Ah... you caught me. I didn't stay in the Wine Cellar. I was actually in the garden gathering rare nightshade leaves for my experiments. I lied because I was terrified of being suspected."
                },
                "room": "conservatory"
            }
        },
        "weapon_clue_id": "silenced_pistol",
        "contradictions": {
            "countess_sasha": "lipstick_cigar",
            "greg_novak": "torn_butler_uniform",
            "sophia_petrov": "chemical_flask"
        },
        "killers": {
            "greg_novak": {
                "proof": "spy_ledger",
                "explanation": "Gregory Novak was a sleeper agent using his position as butler to steal state secrets from the Count, which he decrypted using the Spy Decryption Ledger. When the Count caught Greg searching his private safe, Greg shot him using the silenced pistol. A torn piece of his butler uniform caught on the desk drawer proved Greg was at the crime scene, breaking his alibi."
            },
            "countess_sasha": {
                "proof": "blackmail_letters",
                "explanation": "Countess Sasha Romanov was being blackmailed by her husband, who threatened to expose her secret past to the public (as detailed in the Blackmail Correspondence). To silence him, she shot him with the silenced pistol in the study Salon. The lipstick-stained cigar found in the wine cellar proved she sneaked away, breaking her alibi."
            },
            "sophia_petrov": {
                "proof": "stolen_formula",
                "explanation": "Sophia Petrov had stolen Count {victim_surname}'s patented chemical formulas to sell to a rival corporation, as shown in the Stolen Formula Draft. When the Count threatened her with immediate arrest, she shot him with the silenced pistol in his study. The chemical flask found in the botanical garden broke her alibi."
            }
        },
        "hints": [
            "The Private Salon is the crime scene. Search it to find the murder weapon (Silenced Pistol) and the Torn Butler Uniform Cuff.",
            "Gregory Novak claims he was serving guests in the Ballroom. Confront him with the Torn Butler Uniform Cuff found at the crime scene!",
            "Countess Sasha claims she stayed in the Cigar Lounge. Check the Wine Cellar for the Lipstick-Stained Cigar to break her story.",
            "Sophia Petrov claims she was cataloging spirits in the Wine Cellar all evening. Search the Botanical Garden for her Chemical Flask!",
            "Locate the Spy Decryption Ledger in the Library to expose Gregory Novak's espionage activities."
        ],
        "hidden_hint": "A deciphered spy message reveals the butler was seen near the Salon's back entrance. Check the Salon details!"
    }
]
