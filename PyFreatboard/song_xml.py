from xml.dom.minidom import parse
from section import Section, Chord, Note


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
    try:
        root, type = __get_root_and_type__(chord)
        duration = chord.getElementsByTagName("duration")[0].firstChild.data
        return Chord(root, type, int(duration))
    except:
        print("Invalid chord tag")
