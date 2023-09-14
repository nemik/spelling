#!/env/python3

import os
import genanki

mp3_convert_cmd = "ffmpeg -i tmp.wav -vn -ar 44100 -ac 2 -b:a 192k tmp.mp3"
tts_cmd = 'tts --text "__word__" --model_name tts_models/en/jenny/jenny --out_path tmp.wav'

def create_sound_files(words):
    for word in words:
        # replace __word__ with the word
        cmd = tts_cmd.replace('__word__', word)
        # run the command
        os.system(cmd)
        # run the command to convert wav to mp3
        os.system(mp3_convert_cmd)
        # rename the mp3 file
        os.rename('tmp.mp3', word + '.mp3')
        # remove the wav file
        os.remove('tmp.wav')

spelling_model = genanki.Model(
  1607392319,
  'Spelling model',
  fields=[
    {'name': 'SpokenWord'},
    {'name': 'SpelledWord'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{SpokenWord}}',
      'afmt': '{{FrontSide}}<hr id="answer"><h1>{{SpelledWord}}</h1>',
    },
  ])

def create_deck(words):
    spelling_deck = genanki.Deck(
        2059400110,
        'Spelling Words')
    for word in words:
        note = genanki.Note(
          model=spelling_model,
          fields=[f"[sound:{word}.mp3]", word],
          tags=[word]
        )
        spelling_deck.add_note(note)
    package = genanki.Package(spelling_deck)
    package.media_files = [f"{word}.mp3" for word in words]
    package.write_to_file('spelling.apkg')

# word list, get from file called words.txt
words = []
# open file
with open('words.txt', 'r') as f:
    # read line by line
    for line in f.readlines():
        # remove \n
        line = line.strip()
        # if line is not empty
        if line:
            # add to word list
            words.append(line)

# create sounds files
create_sound_files(words)

# create a deck
create_deck(words)

print(f'Done!')
print(f'Created {len(words)} cards for the words: {words}')
print(f'Import spelling.apkg into Mochi or Anki')