# EmberWriter RC2: Audio Director — available to test in Pinokio

We just added something I've wanted in local audiobook production for a long time: **an audiobook-only performance manuscript**. The book remains untouched; the audio version tracks each dialogue line, its speaker, and the intended delivery.

In the previous preview, some dialogue accidentally stayed in the narrator's voice. RC2 changes the production pipeline rather than patching individual recordings. Dialogue is segmented before synthesis, speaker corrections are saved, and uncertain speakers must be reviewed before a neural book render. No more silently assigning every unattributed quote to the narrator.

The new **Audio Director** screen lets you inspect a chapter line by line, correct who is speaking, and set directions like fear, relief, joy, urgency, or restraint. Kokoro uses each assigned character voice, and our earlier CMU/IPA pronunciation dictionary and 1.35-second chapter-title pauses remain in place. Unchanged, hash-verified audio chunks can be reused when other passages change.

We also added an engine-independent performance format and wired it into Fish Speech rehearsal planning. **Important:** Kokoro does not natively perform all emotion tags. The Fish adapter is experimental; the Fish server wasn't running during RC2 validation, so we are *not* claiming verified Fish-quality emotional performances yet.

Our original synthetic three-chapter demonstration, *The Bell Below Low Water*, has been regenerated with narrator, Mara, Ivo, Nessa, and Sal. All 70 quoted passages now have speaker assignments in the cue sheet. Thirty assignments were context-checked suggestions and still need author approval. The resulting ~17-minute audiobook is a **human-review draft**, not publication-approved audio.

## Screenshots — real RC2 interface with synthetic sample data

![Audio Director: speaker validation](../media/rc2/audio-director-overview.png)

![Audio Director: character voice and delivery controls](../media/rc2/audio-director-character-casting.png)

## Hear the difference — actual Kokoro audition excerpts

- [Mara and Ivo: character voice exchange (20 seconds)](../media/rc2/sample-01-mara-ivo-dialogue.mp3)
- [The rescue decision: character response (22 seconds)](../media/rc2/sample-02-rescue-decision.mp3)
- [A four-character conversation (26 seconds)](../media/rc2/sample-03-multiple-character-voices.mp3)

These clips are rendered by **Kokoro**, not Fish, and come from the synthetic demonstration novel.

## Try RC2 through Pinokio

Already installed? Choose **Update** in EmberWriter's Pinokio launcher. New user? Install using `https://github.com/grumpystrongman/EmberWriter-Pinokio`. Open **Publish → Audiobook → Audio Director**, select a chapter, and review **all dialogue and performance cues** before narration.

We passed **559 backend tests** and the frontend production build. We have not yet signed off on a fresh Pinokio clean install or a full human listening review, so this remains a **release candidate**, not a final commercial audiobook release.

I'd particularly appreciate feedback on incorrect character attribution, awkward voice transitions, pronunciation, emotional direction, or installation failures. Those details matter more than a prettier progress bar.

[App source and RC2 release notes](https://github.com/grumpystrongman/EmberWriter/blob/main/RELEASE_NOTES_RC2.md) · [Pinokio launcher](https://github.com/grumpystrongman/EmberWriter-Pinokio)
