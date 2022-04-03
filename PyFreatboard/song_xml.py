from xml.dom.minidom import parse
from PyFreatboard.section import Section, Chord, Note


def parse_song_xml(xml_file_path):
    """Parse XML file into Song Object"""
    doc = parse(xml_file_path)
    # get song title
    title = ""
    try:
        title = doc.getElementsByTagName("title")[0].firstChild.data
    except:
        print("No title found")

    # get song author
    author = ""
    try:
        author = doc.getElementsByTagName("author")[0].firstChild.data
    except:
        print("No author found")

    # get all section tags
    secs = []
    sections = doc.getElementsByTagName("section")
    for section in sections:
        s = __parse_section__(section)
        secs.append(s)
    
    return title, author, secs
    
def __parse_section__(section):
    """Parse section tag into Section tag"""

    # get section scale
    try:
        scale = section.getElementsByTagName("scale")
        root, type = __get_root_and_type__(scale[0])
        s = Section(root, type)
    except:
        print("No scale found")

    # get section chords
    chords = section.getElementsByTagName("chord")
    for chord in chords:
        c = __get_chords__(chord)
        s.add_chord(c)
    return s

def __get_root_and_type__(element):
    """Get root and type from scale or chord tag"""
    try:
        root = element.getElementsByTagName("root")[0].firstChild.data
        type = element.getElementsByTagName("type")[0].firstChild.data
        return root, type
    except:
        print("No root or type found")

def __get_chords__(chord):
    c = None
    try:
        root, type = __get_root_and_type__(chord)
        duration = chord.getElementsByTagName("duration")[0].firstChild.data
        c = Chord(root, type, int(duration))
    except:
        print("Invalid chord tag")
    
    # get section chords
    melodies = chord.getElementsByTagName("melody")
    for melody in melodies:
        melody_id = melody.getAttribute("id")
        notes = melody.getElementsByTagName("note")
        melody_notes = []
        for note in notes:
            n = __get_note__(note)
            melody_notes.append(n)
        c.add_melody(melody_id, melody_notes)
    return c

def __get_note__(note):
    try:
        pitch = note.getElementsByTagName("pitch")[0].firstChild.data
        octave = note.getElementsByTagName("octave")[0].firstChild.data
        duration = note.getElementsByTagName("duration")[0].firstChild.data
        return Note(pitch, int(octave), int(duration))
    except:
        print("No note pitch, octave or duration found")
