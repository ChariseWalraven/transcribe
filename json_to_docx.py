import json

from docx import Document

# set origin file
o_filename = 'transcription/ageeth_hoofd_en_deelvragen_09_10_2025_11_12_24.json'

# create filenames & paths
filename_sans_extension = o_filename.split('/')[-1].split('.')[0]
dst_filename = f'docx/{filename_sans_extension}.docx'

# setup document
document = Document()


# functions
def map_speaker_to_name(utterance, speaker_map):
    utterance['speaker'] = speaker_map[utterance['speaker']]
    return utterance


# main code
of = open(o_filename, 'r')

o_obj = json.loads(of.read())

speaker_map = {
    "A": "Khalil",
    "B": "Kaj",
}

# document title
document.add_heading('Kaj Blanken Interview 5 jun 2025')

# comment the following line out if you don't want to map speakers to names
# o_obj = map(lambda o: map_speaker_to_name(o, speaker_map), o_obj). 

for utterance in o_obj:
    p = document.add_paragraph('')
    p.add_run(utterance['speaker']).bold = True
    p.add_run(': ')
    p.add_run(utterance['text'])

document.save(dst_filename)
