# Voice FX playbook (use on purpose, not everywhere)

Rule: the voice stays dry and clear for ~90% of the edit. An effect marks a **moment**: a name, a number, a punchline, the last word before a cut to black. One effect every 8–15 s at most.

All of these are ffmpeg filter chains. Apply them to a word-time range taken from a word-level transcript (Groq whisper-large-v3 works here), then mix back over the dry track.

## 1. Echo throw (attention grabber on the last word of a phrase)
The word plays dry, then 3–5 repeats fade out into the pause; each repeat is darker and thinner.
```
[word]asplit[d][w];
[w]highpass=f=300,lowpass=f=4500,
   aecho=0.8:0.7:250|500|750|1000:0.5|0.32|0.2|0.12,
   volume=0.9[wet];
[d][wet]amix=inputs=2:normalize=0
```
- Delay = 1 beat or a ½ beat of the music (at 120 bpm: 250 ms for ⅛, 500 ms for ¼).
- Duck the tail under the next spoken word (sidechaincompress with the dry voice as key) or end the phrase on a pause.
- Ping-pong: pan repeats L/R for width (`adelay` per channel).

## 2. Deep / authoritative voice ("cinematic narrator")
```
rubberband=pitch=0.89:formant=preserved,   # about -2 semitones
equalizer=f=110:t=q:w=1:g=4,               # chest
equalizer=f=350:t=q:w=1.2:g=-3,            # remove mud
equalizer=f=4000:t=q:w=1:g=2,              # presence
acompressor=threshold=-20dB:ratio=4:attack=5:release=120:makeup=4
```
Add a small room for size: convolve with a 0.8–1.2 s IR at 10–15% wet. In practice, the "deep feeling" in the documentary refs comes mainly from a **sub drone + impact under a dry voice** (see the r03/r04 breakdown), so try the bed first.

## 3. Big hall / "thought" reverb tail
Large hall (2.5–4 s decay, 40 ms pre-delay), 100% wet on a copy of the word, high-passed at 250 Hz. The dry voice cuts off on the word end and the tail rings into silence or the music drop.
Synthetic IR: exponentially decaying stereo noise (`aevalsrc` noise × `exp(-t*2.3/RT)`), then `afir`.

## 4. Reverse-reverb swell (riser into a word)
Take the word, add a 2 s reverb, reverse it, and place it so it *ends* exactly where the dry word starts: a ghostly suck-in. Good into a name reveal.

## 5. Telephone / radio (phone call, flashback, quote)
```
highpass=f=400,lowpass=f=3200,acrusher=bits=10:mix=0.3,
equalizer=f=1500:t=q:w=1:g=5,volume=1.5
```
Mark Cuban edit: use on the boss's lines in the phone-call scene.

## 6. Slow-mo voice drop (dramatic stop)
Pitch and time down together on the final syllable (`asetrate=44100*0.75,aresample=44100`) with a low-pass sweep to 800 Hz: a "time stops" moment. Pair it with a freeze frame.

## Final mix chain (every export)
`highpass=80, de-mud -3 dB @300 Hz, presence +2 dB @4 kHz, compressor 3:1, music ducked 8–10 dB under the voice, loudnorm I=-14:TP=-1.5:LRA=7` for TikTok/Reels/Shorts.
