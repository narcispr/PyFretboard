"""Render fretboard diagrams and scores from a SongXML file."""

from __future__ import annotations

import argparse
import copy
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Sequence

# Allow both ``python -m PyFretboard.render_shapes`` and direct script execution.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib

matplotlib.use("Agg")

from matplotlib import font_manager, pyplot as plt
from PIL import Image, ImageChops

from PyFretboard.definitions import PyFretboard as PF
from PyFretboard.draw_score import DrawScore
from PyFretboard.draw_shape import DrawShape
from PyFretboard.finger import Finger
from PyFretboard.shape import Shape
from PyFretboard.song import Song


TEXT_MODES = {
    "none": PF.TEXT_NONE,
    "function": PF.TEXT_FUNCTION,
    "finger": PF.TEXT_FINGER,
    "pitch": PF.TEXT_PITCH,
}


@dataclass(frozen=True)
class ShapeRecord:
    """A shape together with the XML metadata used to label it."""

    kind: str
    root: str
    harmony_type: str
    shape_id: str
    shape: Shape


def _iter_shapes(song: Song) -> Iterator[ShapeRecord]:
    for section in song.sections:
        for scale in section.scale:
            for shape_id, shape in scale.shape.items():
                yield ShapeRecord("scale", scale.root, scale.type, shape_id, shape)

        for chord in section.chord:
            for shape_id, shape in chord.shape.items():
                yield ShapeRecord("chord", chord.root, chord.type, shape_id, shape)


def _slug(value: str) -> str:
    value = (
        value.replace("#", "_sharp_")
        .replace("♯", "_sharp_")
        .replace("♭", "_flat_")
        .replace("-", "_minus_")
    )
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")
    return value or "unnamed"


def _output_name(index: int, record: ShapeRecord, root: str, figure_type: str) -> str:
    parts = (
        f"{index:03d}",
        record.kind,
        root,
        record.harmony_type,
        record.shape_id,
        figure_type,
    )
    return "_".join(_slug(part) for part in parts) + ".png"


def _register_music_font() -> None:
    font_path = Path(__file__).resolve().parents[1] / "Musisync-qYy6.ttf"
    if font_path.is_file():
        font_manager.fontManager.addfont(font_path)


def _crop_image(path: Path, dpi: int) -> None:
    """Trim unused white canvas while retaining a small safety margin."""

    with Image.open(path) as image:
        image_dpi = image.info.get("dpi")
        rgb_image = image.convert("RGB")
        background = Image.new("RGB", rgb_image.size, "white")
        content_box = ImageChops.difference(rgb_image, background).getbbox()
        if content_box is None:
            return

        padding = max(2, round(dpi * 0.02))
        left, top, right, bottom = content_box
        crop_box = (
            max(0, left - padding),
            max(0, top - padding),
            min(image.width, right + padding),
            min(image.height, bottom + padding),
        )
        save_options = {"dpi": image_dpi} if image_dpi is not None else {}
        image.crop(crop_box).save(path, **save_options)


def _save_figure(figure, path: Path, dpi: int) -> None:
    figure.savefig(
        path,
        dpi=dpi,
        bbox_inches="tight",
        # Preserve artists that touch an axes edge before the pixel-level crop.
        pad_inches=0.05,
        facecolor="white",
    )
    plt.close(figure)
    _crop_image(path, dpi)


def render_shapes(
    xml_path: Path,
    output_dir: Path,
    *,
    figure_type: str = "fretboard",
    orientation: str = "auto",
    text: str = "function",
    target_root: str | None = None,
    dpi: int = 300,
    tab: bool = False,
    show_title: bool = False,
) -> list[Path]:
    """Render every explicitly defined shape in ``xml_path``.

    Returns the paths of the generated PNG files.
    """

    xml_path = Path(xml_path)
    output_dir = Path(output_dir)

    if not xml_path.is_file():
        raise FileNotFoundError(f"XML file not found: {xml_path}")
    if target_root is not None and target_root not in Finger.NOTES:
        valid_roots = ", ".join(Finger.NOTES)
        raise ValueError(f"Unknown root {target_root!r}. Valid roots: {valid_roots}")
    if figure_type not in {"fretboard", "score", "both"}:
        raise ValueError("figure_type must be 'fretboard', 'score', or 'both'")
    if orientation not in {"auto", "horizontal", "vertical"}:
        raise ValueError("orientation must be 'auto', 'horizontal', or 'vertical'")
    if text not in TEXT_MODES:
        raise ValueError(f"Unknown text mode: {text}")
    if dpi < 1:
        raise ValueError("dpi must be greater than zero")

    song = Song(str(xml_path))
    records = list(_iter_shapes(song))
    if not records:
        raise ValueError(f"No shapes were found in {xml_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    horizontal_drawer = DrawShape()
    vertical_drawer = DrawShape()
    draw_score = None
    if figure_type in {"score", "both"}:
        _register_music_font()
        draw_score = DrawScore()

    generated: list[Path] = []
    for index, record in enumerate(records, start=1):
        shape = copy.deepcopy(record.shape)
        root = record.root
        if target_root is not None and target_root != record.root:
            interval = shape.get_interval(record.root, target_root)
            shape.transpose(interval)
            root = target_root

        label = f"{root} {record.harmony_type} — {record.shape_id}"
        shape_name = label if show_title else None

        if figure_type in {"fretboard", "both"}:
            use_vertical = orientation == "vertical" or (
                orientation == "auto" and record.kind == "chord"
            )
            if use_vertical:
                figure = vertical_drawer.draw_vertical(
                    shape,
                    text=TEXT_MODES[text],
                    shape_name=shape_name,
                    return_fig=True,
                )
            else:
                figure = horizontal_drawer.draw(
                    shape,
                    text=TEXT_MODES[text],
                    shape_name=shape_name,
                    return_fig=True,
                )

            path = output_dir / _output_name(index, record, root, "fretboard")
            _save_figure(figure, path, dpi)
            generated.append(path)

        if figure_type in {"score", "both"}:
            assert draw_score is not None
            figure = draw_score.draw(
                shape,
                text=TEXT_MODES[text],
                fingering=text == "finger",
                shape_name=shape_name,
                return_fig=True,
                tab=tab,
            )
            path = output_dir / _output_name(index, record, root, "score")
            _save_figure(figure, path, dpi)
            generated.append(path)

    return generated


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render every shape defined in a PyFretboard SongXML file."
    )
    parser.add_argument("xml_file", type=Path, help="SongXML input file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output directory (default: <xml-name>_rendered)",
    )
    parser.add_argument(
        "--render",
        choices=("fretboard", "score", "both"),
        default="fretboard",
        help="figure type to generate (default: fretboard)",
    )
    parser.add_argument(
        "--orientation",
        choices=("auto", "horizontal", "vertical"),
        default="auto",
        help="fretboard orientation; auto uses vertical chords and horizontal scales",
    )
    parser.add_argument(
        "--text",
        choices=tuple(TEXT_MODES),
        default="function",
        help="text displayed inside notes (default: function)",
    )
    parser.add_argument(
        "--root",
        dest="target_root",
        help="transpose every shape to this root, for example G, Bb, or F#",
    )
    parser.add_argument(
        "--dpi", type=int, default=300, help="output resolution (default: 300)"
    )
    parser.add_argument(
        "--tab",
        action="store_true",
        help="include guitar tablature when rendering scores",
    )
    parser.add_argument(
        "--title",
        action="store_true",
        help="display the chord or scale name above each fretboard",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    output_dir = args.output or Path(f"{args.xml_file.stem}_rendered")

    try:
        generated = render_shapes(
            args.xml_file,
            output_dir,
            figure_type=args.render,
            orientation=args.orientation,
            text=args.text,
            target_root=args.target_root,
            dpi=args.dpi,
            tab=args.tab,
            show_title=args.title,
        )
    except (OSError, ValueError) as error:
        parser.error(str(error))

    print(f"Generated {len(generated)} figure(s) in {output_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
