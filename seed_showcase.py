"""Seed an entirely fictional, family-friendly EmberWriter demonstration project.

Only creates a project whose name starts with [DEMO]. Never reads or edits any
other project; rerunning is safe. Uses localhost API exclusively.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("EMBER_DEMO_URL", "http://127.0.0.1:42005").rstrip("/")
# --offline seeds a fresh demo via in-process FastAPI calls, without a server,
# network access, or any access to the personal project data root.
CLIENT = None
if "--offline" in sys.argv:
    from fastapi.testclient import TestClient
    from serve import create_app
    CLIENT = TestClient(create_app(mode="demo"))
NAME = "[DEMO] The Lanterns of Asterfall"
DESCRIPTION = "A clean, inclusive fantasy-and-science-fiction tour of chapters, characters, worldbuilding, notes, screenplay, scene planning, corkboard, binder, and revisions. Fictional sample data only."

def api(method, route, payload=None):
    if CLIENT is not None:
        result = CLIENT.request(method, route, json=payload)
        if result.status_code >= 400:
            raise RuntimeError(f"{method} {route}: HTTP {result.status_code}: {result.text[:800]}")
        return result.json()
    body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(BASE + route, data=body, method=method,
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"{method} {route}: HTTP {exc.code}: {exc.read()[:800]!r}") from exc

projects = api("GET", "/api/projects")
existing = next((p for p in projects if p.get("name") == NAME), None)
if existing:
    print("EXISTS", existing["slug"], "- demo already installed; no changes.")
    raise SystemExit(0)
created = api("POST", "/api/projects", {"name": NAME, "description": DESCRIPTION})
slug = created["slug"]
root = "/api/projects/" + slug
print("CREATED", slug)

documents = {
 "manuscript/01-the-arrival.md": """# Chapter One: The Arrival

The first lantern went dark at precisely seventeen minutes past dawn.

Captain Mira Solen watched its blue flame fold into itself above the harbor of Asterfall, where ancient stone bridges connected a thousand floating gardens. On the horizon, the scientific research vessel *Far Meridian* drifted through a sky threaded with aurora.

'That isn't a power failure,' said Tavi, examining a palm-sized scanner. 'The light is being translated. Into a language.'

Mira touched the brass compass she had inherited from her grandmother. Its needle pointed not north, but toward the oldest library in the city. 'Then we'd better find out who's speaking.'

Below them, a market vendor lowered the shutters of her shop. Above them, another lantern blinked out.

And in the silence between two distant bells, the city answered.

## Scene intent
Introduce the mystery, establish partnership and wonder, end on a gentle cliffhanger.
""",
 "manuscript/02-the-archive.md": """# Chapter Two: The Archive

Archivist Ren Vale had catalogued comets, treaties, and several exceptionally rude botanical specimens. A lantern speaking in a forgotten mathematical language was new.

'All signals have a sender,' Ren said, spreading translucent star maps across the table. 'And all messages have a listener.'

Mira leaned closer. The symbols on the lantern glass matched an unfinished mural of explorers from three hundred years earlier.

Tavi smiled. 'So the past is sending us a message from the future?'

'Not quite,' Ren replied. 'I think someone is asking us to remember a promise.'

Outside, the lanterns brightened together—one by one, like constellations waking.
""",
 "manuscript/03-the-crossing-outline.md": """# Chapter Three: The Crossing (outline)

- Mira, Tavi and Ren sail the Far Meridian to the observatory island.
- A navigation puzzle requires their different expertise.
- They learn the lantern network protects the city from a recurring cosmic storm.
- End on a discovery: the missing keeper left instructions for rebuilding the network.

**Status:** Outline. **Target:** 1,500 words. **Tension:** curiosity to urgency.
""",
 "characters/mira-solen.md": """# Mira Solen
**Role:** Protagonist; skyship captain. **Pronouns:** she/her. **Age:** 34.
**Appearance:** Dark curls kept beneath a weathered pilot cap; practical blue coat.
**Strengths:** Decisive, empathetic, resourceful. **Flaw:** Takes responsibility for everything.
**Goal:** Keep Asterfall safe. **Need:** Learn to share leadership and ask for help.
**Voice:** Direct, lightly dry humor; prefers concrete plans.
**Arc:** From lone protector to collaborative captain.
**Connections:** Trusts Tavi's ingenuity; initially challenges Ren's caution.
""",
 "characters/tavi-orr.md": """# Tavi Orr
**Role:** Engineer and inventor. **Pronouns:** they/them. **Age:** 27.
**Appearance:** Copper spectacles, close-cropped hair, tool-filled vest.
**Strengths:** Patient curiosity, improvisation, generosity. **Flaw:** Overexplains under pressure.
**Goal:** Decode the lantern network. **Need:** Believe their ideas deserve to be heard.
**Voice:** Enthusiastic, precise, often uses vivid comparisons.
**Arc:** From quiet technician to confident co-discoverer.
**Connections:** Long-time friend of Mira; debates scientific theories with Ren.
""",
 "characters/ren-vale.md": """# Ren Vale
**Role:** Archivist and linguist. **Pronouns:** he/him. **Age:** 46.
**Appearance:** Silver-streaked hair, ink-stained sleeves, small notebook.
**Strengths:** Attentive, scholarly, fair-minded. **Flaw:** Hesitates when evidence is incomplete.
**Goal:** Preserve Asterfall's knowledge. **Need:** Act before every answer is certain.
**Voice:** Measured and thoughtful, with unexpected gentle jokes.
**Arc:** From observer to brave participant.
**Connections:** Respects Tavi's unconventional thinking; comes to trust Mira's instincts.
""",
 "world/asterfall-guide.md": """# World Bible: Asterfall
**Genre:** Hopeful science-fantasy. **Tone:** Wonder, cooperation, discovery. **Rating:** General audiences.
Asterfall is a harbor city built on floating islands. Its historic lanterns are a distributed navigation and storm-warning system, powered by resonant crystals and old orbital technology.

## Locations
- **Glass Harbor:** Market, moorings, and the first failing lantern.
- **The Archive:** Living library containing star charts and historical agreements.
- **Observatory Island:** Abandoned monitoring station beyond the cloud belt.
- **Far Meridian:** Mira's compact exploration skyship.

## Rules of the world
Magic is the name given to science not yet understood. Lanterns transmit information as color and rhythm. Rebuilding the network requires trust, not a chosen-one bloodline.

## Themes
Shared responsibility, cultural memory, curiosity, mutual respect.
""",
 "relationships/team-dynamics.md": """# Team dynamics
**Mira + Tavi:** Lifelong friends; affection expressed through practical help.
**Tavi + Ren:** Mutual respect develops through collaborative decoding.
**Mira + Ren:** Friction between acting quickly and verifying facts.
**Group promise:** Nobody is left behind; disagreements are settled by evidence and empathy.
""",
 "timeline/story-timeline.md": """# Timeline
Day 1, 07:17 — First lantern fades at Glass Harbor.
Day 1, 08:05 — Tavi detects a structured message.
Day 1, 10:30 — Team consults Ren in the Archive.
Day 1, 13:00 — Star map reveals Observatory Island.
Day 2 — Planned voyage aboard Far Meridian.
Day 3 — Planned restoration of network before storm.
""",
 "scenes/scene-01-brief.md": """# Scene Card 01 — The first lantern
**POV:** Mira, close third. **Setting:** Glass Harbor at dawn.
**Objective:** Identify anomaly and gather the team.
**Conflict:** Time pressure, uncertain threat, differing interpretations.
**Turn:** Failure is a coded message.
**Emotional movement:** Unease → wonder → resolve.
**Continuity:** Mira has her brass compass; Tavi carries a scanner.
**Revision checklist:** Sharpen sensory description; keep exposition in motion.
""",
 "scenes/sample-screenplay.md": """# Sample screenplay — Lantern Signal

EXT. GLASS HARBOR — DAWN

Golden mist curls around floating docks. A blue lantern flickers.

MIRA SOLEN, a skyship captain, checks the compass at her belt.

                         MIRA
            It should still be lit.

TAVI ORR raises a scanner. Thin lines of light form a repeating pattern.

                         TAVI
            It's not broken. It's sending something.

                         MIRA
            To whom?

The entire harbor grows quiet.

                         TAVI
            That is an excellent question.

CUT TO:

INT. ASTERFALL ARCHIVE — MORNING

REN VALE unfolds an ancient star map.
""",
 "style/voice-and-guardrails.md": """# Style guide
Audience: all ages. Inclusive, respectful language. No explicit sexual content, slurs, graphic violence or stereotyping.
Balance vivid imagery with readable action. Distinguish characters through intentions and speech, not caricature.
Prefer character choices that solve problems through cooperation and cleverness.
""",
 "summaries/story-synopsis.md": """# Project synopsis
When the lanterns protecting the floating city of Asterfall begin to fail, a skyship captain, an inventive engineer, and a careful archivist decode a message hidden in their light. Their investigation reveals an ancient promise and a looming cosmic storm. Together they must restore a forgotten network before the city loses its way.
**Beginning:** An impossible lantern failure.
**Middle:** Clues in old maps; expedition to a remote observatory.
**Ending:** The team rebuilds the system through shared expertise.
""",
 "notes/research-questions.md": """# Research and continuity notes
- How does a lantern translate mathematics into visible rhythm?
- Establish the skyship's fuel and travel limitations.
- Track compass direction consistently across chapters.
- Make all scientific claims fictional unless independently verified.
- Check that day/time transitions match the timeline.
""",
}
from urllib.parse import quote
for path, content in documents.items():
    api("PUT", root + "/file?path=" + quote(path, safe=""), {"content": content})
print("FILES", len(documents))

# Create explicitly typed binder sections; binder sync also discovers document files.
api("POST", root + "/binder/sync")
binder = api("GET", root + "/binder")
print("BINDER_NODES", len(binder.get("nodes", [])))
api("POST", root + "/revisions/checkpoint", {
    "path": "manuscript/01-the-arrival.md", "note": "Demo first-chapter milestone."
})
api("PUT", root + "/studio-state", {
    "studio_mode": "scene", "title": "The Observatory Puzzle",
    "prompt": "Draft a gentle science-fantasy scene in which Mira, Tavi and Ren unlock an observatory door by combining navigation, engineering and historical knowledge. Keep it appropriate for all ages.",
    "scene_brief": "POV: Tavi. Emotional beat: from self-doubt to confident collaboration. Include a visual puzzle and a clue for the next chapter.",
    "scratchpad": "Continuity: no one can solve the puzzle alone. Compass points to the archive, not magnetic north. Avoid violence.",
    "destination": "studio", "delivery_scope": "full_scene"
})
cards = [
 ("Start here", "This is a complete FICTIONAL demo, not your personal writing. Open the binder to explore chapters, cast, world bible, screenplay, research notes and a scene brief.", 40, 40, "amber"),
 ("Mystery / Story Hook", "Asterfall's lanterns are speaking in a forgotten mathematical language. What promise is the city being asked to remember?", 360, 40, "blue"),
 ("Character Arcs", "Mira: share leadership. Tavi: trust their voice. Ren: act with incomplete knowledge. The team succeeds through cooperation.", 680, 40, "green"),
 ("Chapter Roadmap", "Ch 1: The Arrival — draft. Ch 2: The Archive — draft. Ch 3: The Crossing — outline. Each demonstrates a different writing phase.", 40, 280, "violet"),
 ("Worldbuilding", "Glass Harbor → Archive → Observatory Island. Ancient lanterns = distributed storm-warning network. See world/asterfall-guide.md.", 360, 280, "blue"),
 ("Continuity Check", "Mira's brass compass, Tavi's scanner, the 07:17 lantern failure, and the three-day timeline must remain consistent.", 680, 280, "amber"),
 ("Revision / Editing", "Try editing Chapter One, compare the revision history and create another checkpoint. Work only inside this demo project.", 40, 520, "green"),
 ("Screenplay Sample", "Open scenes/sample-screenplay.md to see formatted dialogue and scene headings. Compare its scene with the prose chapter.", 360, 520, "violet"),
 ("AI Studio Prompt", "The studio contains a prepared all-ages writing prompt for a collaborative puzzle scene. Generate only after checking the selected local model.", 680, 520, "amber"),
]
for title, body, x, y, color in cards:
    api("POST", root + "/board/items", {"kind":"sticky","title":title,"body":body,"x":x,"y":y,"width":275,"height":195,"color":color})
print("BOARD_CARDS", len(cards))
print("DEMO_READY", slug)
