# PyFretboard

PyFretboard is a Python API for drawing guitar fretboard diagrams (also called shapes) and automatically generating new shapes. It uses Matplotlib as its plotting engine, and its generated fingerings broadly follow the Berklee fingering style.

## Installation

Create a virtual environment and install the project dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install -e .
```

## Rendering shapes from SongXML

`PyFretboard/render_shapes.py` reads all explicitly defined chord and scale shapes from a SongXML file and writes one PNG per shape. Chords are rendered vertically and scales horizontally by default. Diagram titles are hidden unless `--title` is provided.

Example: _Render the included triads_

```bash
python3 -m PyFretboard.render_shapes shapes_xml/triads.xml
```

The default output directory is `triads_rendered/`. Use `--output` to choose another directory:

```bash
python3 -m PyFretboard.render_shapes shapes_xml/triads.xml --output rendered/triads
```

Display the chord or scale name above each diagram with `--title`:

```bash
python3 -m PyFretboard.render_shapes shapes_xml/triads.xml --title
```

The script can also transpose shapes, render notation and tablature, change the orientation, or change the text shown inside each note:

```bash
# Render every shape as a G-root chord or scale.
python3 -m PyFretboard.render_shapes shapes_xml/triads.xml --root G

# Generate both fretboard diagrams and score/tab figures.
python3 -m PyFretboard.render_shapes shapes_xml/triads.xml \
  --render both --tab --output rendered/triads

# Display pitches on horizontal fretboards.
python3 -m PyFretboard.render_shapes shapes_xml/triads.xml \
  --orientation horizontal --text pitch
```

Run `python3 -m PyFretboard.render_shapes --help` for all options. Direct execution with `python3 PyFretboard/render_shapes.py ...` is supported as well.

## Basic shape syntax

Shapes are stored inside a `<chord>` or `<scale>` element. The following is a minimal chord example:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<song>
  <title>My shapes</title>
  <author>Your name</author>
  <time>
    <beats>4</beats>
    <beat-type>4</beat-type>
  </time>
  <section id="examples">
    <chord>
      <root>C</root>
      <type>M</type>
      <duration>4</duration>
      <shape id="C major triad">
        <type>strum</type>
        <fingers>
          <finger>
            <pitch>C</pitch>
            <string>G</string>
            <fret>5</fret>
            <function>1</function>
            <fingering>3</fingering>
            <barrel>False</barrel>
            <visual>0</visual>
          </finger>
          <finger>
            <pitch>E</pitch>
            <string>B</string>
            <fret>5</fret>
            <function>3</function>
            <fingering>4</fingering>
            <barrel>False</barrel>
            <visual>0</visual>
          </finger>
          <finger>
            <pitch>G</pitch>
            <string>e</string>
            <fret>3</fret>
            <function>5</function>
            <fingering>1</fingering>
            <barrel>False</barrel>
            <visual>0</visual>
          </finger>
        </fingers>
      </shape>
    </chord>
  </section>
</song>
```

Each `<shape>` has a unique `id`, a rendering `<type>` (`strum` or `arpeggio`), and one or more `<finger>` elements. A finger contains:

- `pitch`: note name, including accidentals when needed, such as `C`, `F#`, or `Bb`.
- `string`: one of `E`, `A`, `D`, `G`, `B`, or `e`; lowercase `e` is the highest string.
- `fret`: zero for an open string, otherwise the fret number.
- `function`: the harmonic function shown in the diagram, such as `1`, `b3`, `3`, or `5`.
- `fingering`: left-hand finger (`1` to `4`; `1s` and `4s` are supported for extensions).
- `barrel`: `True` for notes that belong to a barre, otherwise `False`.
- `visual`: `0` for the normal note style or `1` for the alternate, muted style.

To define a scale, replace the `<chord>` wrapper with `<scale>`, keep `<root>` and `<type>`, and omit `<duration>`.

More complete examples are available in [`shapes_xml`](shapes_xml/), and API examples are available in [`tutorial.ipynb`](tutorial.ipynb).

*Created by Narcís Palomeras.*
