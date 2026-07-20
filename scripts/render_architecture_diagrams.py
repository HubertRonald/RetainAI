#!/usr/bin/env python3
"""Render polished RetainAI architecture diagrams with official AWS/GCP assets.

The selected cloud service icons are downloaded separately from the official
vendor icon packages. This renderer keeps those images unmodified and embeds
copies into self-contained SVG and PNG outputs.
"""

from __future__ import annotations

import argparse
import base64
import html
import io
import math
import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError as exc:  # pragma: no cover - explicit operator guidance
    raise SystemExit(
        "Pillow is required. Activate the project virtual environment and run: "
        "python -m pip install 'Pillow>=10,<13'"
    ) from exc


COLORS = {
    "ink": "#111827",
    "muted": "#64748B",
    "line": "#475569",
    "soft_line": "#CBD5E1",
    "canvas": "#F8FAFC",
    "white": "#FFFFFF",
    "gcp": "#4285F4",
    "gcp_soft": "#EFF6FF",
    "aws": "#FF9900",
    "aws_soft": "#FFF7ED",
    "green": "#16A34A",
    "green_soft": "#F0FDF4",
    "purple": "#8B5CF6",
    "purple_soft": "#FAF5FF",
    "red": "#EF4444",
    "red_soft": "#FEF2F2",
    "amber": "#CA8A04",
    "amber_soft": "#FEFCE8",
    "slate": "#64748B",
    "slate_soft": "#F1F5F9",
    "blue": "#2563EB",
    "blue_soft": "#EFF6FF",
    "orange": "#F97316",
    "orange_soft": "#FFF7ED",
    "teal": "#0F766E",
    "teal_soft": "#F0FDFA",
}


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[index : index + 2], 16) for index in (0, 2, 4))


def data_uri(path: Path) -> str:
    content = path.read_bytes()
    mime = "image/svg+xml" if path.suffix.lower() == ".svg" else "image/png"
    return f"data:{mime};base64,{base64.b64encode(content).decode('ascii')}"


def font_path(bold: bool = False) -> str:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]

    for candidate in candidates:
        if Path(candidate).is_file():
            return candidate

    return candidates[0]


@dataclass
class TextElement:
    x: float
    y: float
    text: str
    size: int
    color: str
    bold: bool = False
    anchor: str = "start"
    max_width: float | None = None
    line_height: float | None = None


@dataclass
class RectElement:
    x: float
    y: float
    width: float
    height: float
    fill: str
    stroke: str
    radius: float = 24
    stroke_width: float = 2
    dashed: bool = False
    shadow: bool = False


@dataclass
class LineElement:
    points: list[tuple[float, float]]
    color: str = COLORS["line"]
    width: float = 3
    dashed: bool = False
    arrow: bool = True
    label: str | None = None
    label_x: float | None = None
    label_y: float | None = None


@dataclass
class ImageElement:
    x: float
    y: float
    width: float
    height: float
    path: Path


@dataclass
class CircleElement:
    cx: float
    cy: float
    radius: float
    fill: str
    stroke: str = "none"
    stroke_width: float = 0


@dataclass
class Card:
    x: float
    y: float
    width: float
    height: float
    title: str
    subtitle: str = ""
    icon: Path | None = None
    abbreviation: str | None = None
    accent: str = COLORS["blue"]
    fill: str = COLORS["white"]
    dashed: bool = False
    status: str | None = None

    @property
    def left(self) -> tuple[float, float]:
        return self.x, self.y + self.height / 2

    @property
    def right(self) -> tuple[float, float]:
        return self.x + self.width, self.y + self.height / 2

    @property
    def top(self) -> tuple[float, float]:
        return self.x + self.width / 2, self.y

    @property
    def bottom(self) -> tuple[float, float]:
        return self.x + self.width / 2, self.y + self.height


@dataclass
class Scene:
    width: int
    height: int
    title: str
    subtitle: str
    elements: list[object] = field(default_factory=list)
    cards: list[Card] = field(default_factory=list)

    def add_text(self, *args, **kwargs) -> None:
        self.elements.append(TextElement(*args, **kwargs))

    def add_rect(self, *args, **kwargs) -> None:
        self.elements.append(RectElement(*args, **kwargs))

    def add_line(self, *args, **kwargs) -> None:
        self.elements.append(LineElement(*args, **kwargs))

    def add_image(self, *args, **kwargs) -> None:
        self.elements.append(ImageElement(*args, **kwargs))

    def add_circle(self, *args, **kwargs) -> None:
        self.elements.append(CircleElement(*args, **kwargs))

    def add_zone(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        title: str,
        subtitle: str,
        fill: str,
        stroke: str,
        dashed: bool = False,
        badge: str | None = None,
    ) -> None:
        self.add_rect(
            x,
            y,
            width,
            height,
            fill,
            stroke,
            radius=32,
            stroke_width=2.5,
            dashed=dashed,
            shadow=False,
        )
        self.add_text(x + 30, y + 34, title, 24, COLORS["ink"], bold=True)
        self.add_text(x + 30, y + 68, subtitle, 16, COLORS["muted"])

        if badge:
            badge_width = max(118, len(badge) * 11 + 30)
            self.add_rect(
                x + width - badge_width - 22,
                y + 18,
                badge_width,
                40,
                COLORS["white"],
                stroke,
                radius=20,
                stroke_width=1.5,
                dashed=dashed,
            )
            self.add_text(
                x + width - badge_width / 2 - 22,
                y + 45,
                badge,
                14,
                stroke,
                bold=True,
                anchor="middle",
            )

    def add_card(self, card: Card) -> Card:
        self.cards.append(card)
        self.add_rect(
            card.x,
            card.y,
            card.width,
            card.height,
            card.fill,
            card.accent,
            radius=24,
            stroke_width=2.5,
            dashed=card.dashed,
            shadow=True,
        )

        icon_box = min(card.height - 32, 92)
        icon_x = card.x + 18
        icon_y = card.y + (card.height - icon_box) / 2

        icon_fill = COLORS["white"] if card.icon else card.accent
        icon_stroke = card.accent
        icon_stroke_width = 1.5 if card.icon else 0

        self.add_rect(
            icon_x,
            icon_y,
            icon_box,
            icon_box,
            icon_fill,
            icon_stroke,
            radius=20,
            stroke_width=icon_stroke_width,
        )

        if card.icon:
            padding = 13
            self.add_image(
                icon_x + padding,
                icon_y + padding,
                icon_box - 2 * padding,
                icon_box - 2 * padding,
                card.icon,
            )
        else:
            abbreviation = card.abbreviation or card.title[:3].upper()
            self.add_text(
                icon_x + icon_box / 2,
                icon_y + icon_box / 2 + 9,
                abbreviation,
                22,
                COLORS["white"],
                bold=True,
                anchor="middle",
            )

        text_x = icon_x + icon_box + 18
        self.add_text(
            text_x,
            card.y + 40,
            card.title,
            20,
            COLORS["ink"],
            bold=True,
            max_width=card.width - (text_x - card.x) - 18,
            line_height=25,
        )

        if card.subtitle:
            self.add_text(
                text_x,
                card.y + 74,
                card.subtitle,
                14,
                COLORS["muted"],
                max_width=card.width - (text_x - card.x) - 18,
                line_height=20,
            )

        if card.status:
            status_color = COLORS["green"] if not card.dashed else COLORS["purple"]
            status_fill = COLORS["green_soft"] if not card.dashed else COLORS["purple_soft"]
            badge_width = max(90, len(card.status) * 8.5 + 24)
            self.add_rect(
                card.x + card.width - badge_width - 12,
                card.y + card.height - 32,
                badge_width,
                22,
                status_fill,
                status_color,
                radius=11,
                stroke_width=1,
                dashed=card.dashed,
            )
            self.add_text(
                card.x + card.width - badge_width / 2 - 12,
                card.y + card.height - 16,
                card.status,
                11,
                status_color,
                bold=True,
                anchor="middle",
            )

        return card

    def connect(
        self,
        start: tuple[float, float],
        end: tuple[float, float],
        *,
        label: str | None = None,
        dashed: bool = False,
        color: str = COLORS["line"],
        width: float = 3,
        bend: str = "auto",
    ) -> None:
        sx, sy = start
        ex, ey = end

        if bend == "straight" or abs(sy - ey) < 8 or abs(sx - ex) < 8:
            points = [start, end]
        elif bend == "vertical-first":
            middle_y = (sy + ey) / 2
            points = [start, (sx, middle_y), (ex, middle_y), end]
        else:
            middle_x = (sx + ex) / 2
            points = [start, (middle_x, sy), (middle_x, ey), end]

        label_x = sum(point[0] for point in points) / len(points)
        label_y = sum(point[1] for point in points) / len(points) - 12

        self.add_line(
            points,
            color=color,
            width=width,
            dashed=dashed,
            arrow=True,
            label=label,
            label_x=label_x,
            label_y=label_y,
        )

    def add_header_badge(self, text: str, color: str, fill: str) -> None:
        width = max(200, len(text) * 12 + 36)
        x = self.width - width - 56
        y = 46
        self.add_rect(x, y, width, 44, fill, color, radius=22, stroke_width=1.8)
        self.add_text(x + width / 2, y + 29, text, 15, color, bold=True, anchor="middle")

    def add_legend(self, y: float) -> None:
        self.add_line([(70, y), (145, y)], color=COLORS["line"], width=3, arrow=False)
        self.add_text(160, y + 6, "Implemented / deployed", 14, COLORS["muted"])
        self.add_line(
            [(410, y), (485, y)],
            color=COLORS["purple"],
            width=3,
            dashed=True,
            arrow=False,
        )
        self.add_text(500, y + 6, "Planned / disabled", 14, COLORS["muted"])
        self.add_text(
            self.width - 70,
            y + 6,
            "RetainAI · Hubert Ronald",
            13,
            COLORS["muted"],
            anchor="end",
        )

    def _wrapped_lines(self, element: TextElement) -> list[str]:
        if not element.max_width:
            return element.text.split("\n")

        average_char_width = max(6, element.size * 0.56)
        max_chars = max(5, int(element.max_width / average_char_width))
        lines: list[str] = []

        for paragraph in element.text.split("\n"):
            wrapped = textwrap.wrap(
                paragraph,
                width=max_chars,
                break_long_words=False,
                replace_whitespace=False,
            )
            lines.extend(wrapped or [""])

        return lines

    def save_svg(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        marker_id = "arrowhead"
        shadow_id = "cardShadow"

        chunks = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">',
            "<defs>",
            f'<marker id="{marker_id}" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L12,6 L0,12 z" fill="{COLORS["line"]}"/></marker>',
            f'<filter id="{shadow_id}" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="7" stdDeviation="8" flood-color="#0F172A" flood-opacity="0.12"/></filter>',
            "</defs>",
            f'<rect width="100%" height="100%" fill="{COLORS["canvas"]}"/>',
            f'<text x="56" y="68" font-family="Inter,Arial,sans-serif" font-size="34" font-weight="700" fill="{COLORS["ink"]}">{html.escape(self.title)}</text>',
            f'<text x="56" y="101" font-family="Inter,Arial,sans-serif" font-size="17" fill="{COLORS["muted"]}">{html.escape(self.subtitle)}</text>',
        ]

        for element in self.elements:
            if isinstance(element, RectElement):
                dash = ' stroke-dasharray="10 8"' if element.dashed else ""
                shadow = f' filter="url(#{shadow_id})"' if element.shadow else ""
                chunks.append(
                    f'<rect x="{element.x}" y="{element.y}" width="{element.width}" height="{element.height}" rx="{element.radius}" fill="{element.fill}" stroke="{element.stroke}" stroke-width="{element.stroke_width}"{dash}{shadow}/>'
                )
            elif isinstance(element, CircleElement):
                chunks.append(
                    f'<circle cx="{element.cx}" cy="{element.cy}" r="{element.radius}" fill="{element.fill}" stroke="{element.stroke}" stroke-width="{element.stroke_width}"/>'
                )
            elif isinstance(element, ImageElement):
                chunks.append(
                    f'<image x="{element.x}" y="{element.y}" width="{element.width}" height="{element.height}" href="{data_uri(element.path)}" preserveAspectRatio="xMidYMid meet"/>'
                )
            elif isinstance(element, TextElement):
                lines = self._wrapped_lines(element)
                line_height = element.line_height or element.size * 1.28
                anchor = {"start": "start", "middle": "middle", "end": "end"}[element.anchor]
                weight = "700" if element.bold else "400"
                chunks.append(
                    f'<text x="{element.x}" y="{element.y}" text-anchor="{anchor}" font-family="Inter,Arial,sans-serif" font-size="{element.size}" font-weight="{weight}" fill="{element.color}">'
                )
                for index, line in enumerate(lines):
                    dy = 0 if index == 0 else line_height
                    chunks.append(
                        f'<tspan x="{element.x}" dy="{dy}">{html.escape(line)}</tspan>'
                    )
                chunks.append("</text>")
            elif isinstance(element, LineElement):
                points = " ".join(f"{x},{y}" for x, y in element.points)
                dash = ' stroke-dasharray="10 8"' if element.dashed else ""
                marker = f' marker-end="url(#{marker_id})"' if element.arrow else ""
                chunks.append(
                    f'<polyline points="{points}" fill="none" stroke="{element.color}" stroke-width="{element.width}" stroke-linecap="round" stroke-linejoin="round"{dash}{marker}/>'
                )
                if element.label:
                    label_x = element.label_x or 0
                    label_y = element.label_y or 0
                    label_width = max(120, len(element.label) * 8.5 + 24)
                    chunks.append(
                        f'<rect x="{label_x - label_width / 2}" y="{label_y - 18}" width="{label_width}" height="30" rx="15" fill="#FFFFFF" stroke="{COLORS["soft_line"]}" stroke-width="1"/>'
                    )
                    chunks.append(
                        f'<text x="{label_x}" y="{label_y + 2}" text-anchor="middle" font-family="Inter,Arial,sans-serif" font-size="12" font-weight="600" fill="{COLORS["muted"]}">{html.escape(element.label)}</text>'
                    )

        chunks.append("</svg>")
        path.write_text("\n".join(chunks) + "\n", encoding="utf-8")

    def save_png(self, path: Path, scale: float = 1.0) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        width = int(self.width * scale)
        height = int(self.height * scale)
        image = Image.new("RGBA", (width, height), hex_to_rgb(COLORS["canvas"]) + (255,))
        draw = ImageDraw.Draw(image)

        def xy(value: float) -> int:
            return int(round(value * scale))

        fonts: dict[tuple[int, bool], ImageFont.FreeTypeFont | ImageFont.ImageFont] = {}

        def get_font(size: int, bold: bool = False):
            key = (size, bold)
            if key not in fonts:
                try:
                    fonts[key] = ImageFont.truetype(font_path(bold), xy(size))
                except OSError:
                    fonts[key] = ImageFont.load_default()
            return fonts[key]

        draw.text((xy(56), xy(42)), self.title, fill=COLORS["ink"], font=get_font(34, True))
        draw.text((xy(56), xy(82)), self.subtitle, fill=COLORS["muted"], font=get_font(17))

        for element in self.elements:
            if isinstance(element, RectElement):
                box = (
                    xy(element.x),
                    xy(element.y),
                    xy(element.x + element.width),
                    xy(element.y + element.height),
                )
                if element.shadow:
                    shadow_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
                    shadow_draw = ImageDraw.Draw(shadow_layer)
                    shadow_box = (
                        box[0],
                        box[1] + xy(6),
                        box[2],
                        box[3] + xy(6),
                    )
                    shadow_draw.rounded_rectangle(
                        shadow_box,
                        radius=xy(element.radius),
                        fill=(15, 23, 42, 28),
                    )
                    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(xy(7)))
                    image.alpha_composite(shadow_layer)
                    draw = ImageDraw.Draw(image)

                draw.rounded_rectangle(
                    box,
                    radius=xy(element.radius),
                    fill=element.fill,
                    outline=None if element.dashed else element.stroke,
                    width=max(1, xy(element.stroke_width)),
                )
                if element.dashed:
                    self._draw_dashed_rounded_rect(
                        draw,
                        box,
                        xy(element.radius),
                        element.stroke,
                        max(1, xy(element.stroke_width)),
                    )
            elif isinstance(element, CircleElement):
                box = (
                    xy(element.cx - element.radius),
                    xy(element.cy - element.radius),
                    xy(element.cx + element.radius),
                    xy(element.cy + element.radius),
                )
                draw.ellipse(
                    box,
                    fill=element.fill,
                    outline=None if element.stroke == "none" else element.stroke,
                    width=max(1, xy(element.stroke_width)),
                )
            elif isinstance(element, ImageElement):
                icon = self._load_icon(element.path, xy(element.width), xy(element.height))
                image.alpha_composite(icon, (xy(element.x), xy(element.y)))
                draw = ImageDraw.Draw(image)
            elif isinstance(element, TextElement):
                lines = self._wrapped_lines(element)
                font = get_font(element.size, element.bold)
                line_height = xy(element.line_height or element.size * 1.28)
                current_y = xy(element.y - element.size)
                for line in lines:
                    bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = bbox[2] - bbox[0]
                    x = xy(element.x)
                    if element.anchor == "middle":
                        x -= text_width // 2
                    elif element.anchor == "end":
                        x -= text_width
                    draw.text((x, current_y), line, fill=element.color, font=font)
                    current_y += line_height
            elif isinstance(element, LineElement):
                points = [(xy(x), xy(y)) for x, y in element.points]
                if element.dashed:
                    self._draw_dashed_polyline(
                        draw,
                        points,
                        element.color,
                        max(1, xy(element.width)),
                    )
                else:
                    draw.line(
                        points,
                        fill=element.color,
                        width=max(1, xy(element.width)),
                        joint="curve",
                    )
                if element.arrow and len(points) >= 2:
                    self._draw_arrowhead(
                        draw,
                        points[-2],
                        points[-1],
                        element.color,
                        xy(11),
                    )
                if element.label:
                    label_x = xy(element.label_x or 0)
                    label_y = xy(element.label_y or 0)
                    font = get_font(12, True)
                    bbox = draw.textbbox((0, 0), element.label, font=font)
                    text_width = bbox[2] - bbox[0]
                    label_width = max(xy(120), text_width + xy(24))
                    draw.rounded_rectangle(
                        (
                            label_x - label_width // 2,
                            label_y - xy(18),
                            label_x + label_width // 2,
                            label_y + xy(12),
                        ),
                        radius=xy(15),
                        fill=COLORS["white"],
                        outline=COLORS["soft_line"],
                        width=1,
                    )
                    draw.text(
                        (label_x - text_width // 2, label_y - xy(11)),
                        element.label,
                        fill=COLORS["muted"],
                        font=font,
                    )

        image.convert("RGB").save(path, format="PNG", optimize=True)

    @staticmethod
    def _load_icon(path: Path, width: int, height: int) -> Image.Image:
        if path.suffix.lower() == ".svg":
            try:
                import cairosvg
            except ImportError as exc:
                raise RuntimeError(
                    f"SVG icon {path} requires CairoSVG. Prefer PNG vendor assets or "
                    "install 'cairosvg'."
                ) from exc
            payload = cairosvg.svg2png(
                bytestring=path.read_bytes(),
                output_width=width,
                output_height=height,
            )
            source = Image.open(io.BytesIO(payload)).convert("RGBA")
        else:
            source = Image.open(path).convert("RGBA")

        source.thumbnail((width, height), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        canvas.alpha_composite(
            source,
            ((width - source.width) // 2, (height - source.height) // 2),
        )
        return canvas

    @staticmethod
    def _draw_arrowhead(
        draw: ImageDraw.ImageDraw,
        start: tuple[int, int],
        end: tuple[int, int],
        color: str,
        size: int,
    ) -> None:
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.hypot(dx, dy) or 1
        ux, uy = dx / length, dy / length
        px, py = -uy, ux
        base_x = end[0] - ux * size
        base_y = end[1] - uy * size
        points = [
            end,
            (int(base_x + px * size * 0.55), int(base_y + py * size * 0.55)),
            (int(base_x - px * size * 0.55), int(base_y - py * size * 0.55)),
        ]
        draw.polygon(points, fill=color)

    @staticmethod
    def _draw_dashed_polyline(
        draw: ImageDraw.ImageDraw,
        points: Sequence[tuple[int, int]],
        color: str,
        width: int,
        dash: int = 13,
        gap: int = 9,
    ) -> None:
        for first, second in zip(points, points[1:]):
            dx = second[0] - first[0]
            dy = second[1] - first[1]
            length = math.hypot(dx, dy)
            if length == 0:
                continue
            ux, uy = dx / length, dy / length
            position = 0.0
            while position < length:
                end_position = min(position + dash, length)
                draw.line(
                    (
                        first[0] + ux * position,
                        first[1] + uy * position,
                        first[0] + ux * end_position,
                        first[1] + uy * end_position,
                    ),
                    fill=color,
                    width=width,
                )
                position += dash + gap

    @staticmethod
    def _draw_dashed_rounded_rect(
        draw: ImageDraw.ImageDraw,
        box: tuple[int, int, int, int],
        radius: int,
        color: str,
        width: int,
    ) -> None:
        # A clean dashed approximation is preferable to a fully solid future card.
        x1, y1, x2, y2 = box
        dash, gap = 14, 9
        for start in range(x1 + radius, x2 - radius, dash + gap):
            draw.line((start, y1, min(start + dash, x2 - radius), y1), fill=color, width=width)
            draw.line((start, y2, min(start + dash, x2 - radius), y2), fill=color, width=width)
        for start in range(y1 + radius, y2 - radius, dash + gap):
            draw.line((x1, start, x1, min(start + dash, y2 - radius)), fill=color, width=width)
            draw.line((x2, start, x2, min(start + dash, y2 - radius)), fill=color, width=width)
        # Corner arcs remain solid but short; visually they read as a dashed outline.
        draw.arc((x1, y1, x1 + 2 * radius, y1 + 2 * radius), 180, 270, fill=color, width=width)
        draw.arc((x2 - 2 * radius, y1, x2, y1 + 2 * radius), 270, 360, fill=color, width=width)
        draw.arc((x1, y2 - 2 * radius, x1 + 2 * radius, y2), 90, 180, fill=color, width=width)
        draw.arc((x2 - 2 * radius, y2 - 2 * radius, x2, y2), 0, 90, fill=color, width=width)


class Icons:
    def __init__(self, vendor_root: Path):
        self.vendor_root = vendor_root
        self._map: dict[str, Path] = {}
        for vendor in ("aws", "gcp"):
            directory = vendor_root / vendor
            if not directory.exists():
                continue
            for path in directory.iterdir():
                if path.suffix.lower() not in {".png", ".svg"}:
                    continue
                self._map[f"{vendor}:{path.stem}"] = path

    def get(self, key: str) -> Path:
        try:
            return self._map[key]
        except KeyError as exc:
            available = ", ".join(sorted(self._map))
            raise RuntimeError(
                f"Required architecture icon {key!r} is missing. "
                f"Run scripts/download_architecture_assets.sh first. "
                f"Available: {available}"
            ) from exc


# ---------------------------------------------------------------------------
# Diagram builders
# ---------------------------------------------------------------------------


def decision_intelligence(icons: Icons) -> Scene:
    scene = Scene(
        2500,
        1500,
        "RetainAI Decision Intelligence Platform",
        "End-to-end ML, survival analysis, explainability, MLOps, decision experience, and bounded AI guidance",
    )
    scene.add_header_badge("PRODUCT ARCHITECTURE", COLORS["blue"], COLORS["blue_soft"])

    zones = [
        (50, 145, 430, 1170, "1 · Data Foundation", "Evidence starts with reproducible data", COLORS["green_soft"], COLORS["green"]),
        (510, 145, 430, 1170, "2 · Predictive Intelligence", "Risk and time-to-event models", COLORS["orange_soft"], COLORS["orange"]),
        (970, 145, 430, 1170, "3 · Explainable Intelligence", "Drivers, artifacts, and model context", COLORS["amber_soft"], COLORS["amber"]),
        (1430, 145, 470, 1170, "4 · Decision Experience", "Controlled API and dashboard", COLORS["blue_soft"], COLORS["blue"]),
        (1930, 145, 520, 1170, "5 · Advisor Evolution", "Provider-neutral and disabled by default", COLORS["purple_soft"], COLORS["purple"]),
    ]
    for zone in zones:
        scene.add_zone(*zone)

    source = scene.add_card(Card(90, 275, 350, 145, "Employee data", "Kaggle benchmark or governed HR sources", abbreviation="DATA", accent=COLORS["green"], status="current"))
    quality = scene.add_card(Card(90, 495, 350, 145, "EDA and quality", "Schema, missingness, leakage, cohort checks", abbreviation="EDA", accent=COLORS["green"], status="current"))
    features = scene.add_card(Card(90, 715, 350, 145, "Feature datasets", "Processed, train, validation, and test", abbreviation="FX", accent=COLORS["green"], status="current"))
    scene.connect(source.bottom, quality.top)
    scene.connect(quality.bottom, features.top)

    clf = scene.add_card(Card(550, 310, 350, 155, "Attrition classification", "Logistic regression · Random Forest · XGBoost", abbreviation="ML", accent=COLORS["orange"], status="current"))
    survival = scene.add_card(Card(550, 625, 350, 155, "Survival analysis", "Retention curves and time-to-event behavior", abbreviation="TTE", accent=COLORS["orange"], status="current"))
    evaluation = scene.add_card(Card(550, 940, 350, 155, "Evaluation", "Calibration, thresholds, temporal and subgroup checks", abbreviation="EV", accent=COLORS["orange"], status="current"))
    scene.connect(features.right, clf.left)
    scene.connect(features.right, survival.left, bend="auto")
    scene.connect(clf.bottom, evaluation.top)
    scene.connect(survival.bottom, evaluation.top)

    shap = scene.add_card(Card(1010, 300, 350, 155, "SHAP explainability", "Global importance and local feature drivers", abbreviation="SHAP", accent=COLORS["amber"], status="current"))
    mlflow = scene.add_card(Card(1010, 620, 350, 155, "Experiment tracking", "MLflow runs, parameters, metrics, and models", abbreviation="MLF", accent=COLORS["amber"], status="current"))
    evidence = scene.add_card(Card(1010, 940, 350, 155, "Evidence artifacts", "Model cards, reports, explanation payloads", abbreviation="DOC", accent=COLORS["amber"], status="current"))
    scene.connect(clf.right, shap.left)
    scene.connect(survival.right, shap.left)
    scene.connect(evaluation.right, mlflow.left)
    scene.connect(shap.bottom, evidence.top)
    scene.connect(mlflow.bottom, evidence.top)

    api = scene.add_card(Card(1470, 315, 390, 165, "Prediction and explanation API", "AWS Lambda container behind API Gateway", icon=icons.get("aws:lambda"), accent=COLORS["aws"], status="deployed"))
    dashboard = scene.add_card(Card(1470, 640, 390, 165, "Decision dashboard", "Streamlit on Google Cloud Run", icon=icons.get("gcp:cloud-run"), accent=COLORS["gcp"], status="deployed"))
    reports = scene.add_card(Card(1470, 965, 390, 165, "Validation reports", "Evidence, limitations, performance, and drift status", abbreviation="REP", accent=COLORS["blue"], dashed=True, status="v0.5"))
    scene.connect(shap.right, api.left)
    scene.connect(evidence.right, api.left)
    scene.connect(api.bottom, dashboard.top)
    scene.connect(evidence.right, dashboard.left)
    scene.connect(dashboard.bottom, reports.top, dashed=True, color=COLORS["purple"])

    pack = scene.add_card(Card(1970, 285, 440, 150, "Evidence context pack", "Drivers, cohorts, model cards, and responsible-use notes", abbreviation="CTX", accent=COLORS["purple"], dashed=True, status="planned"))
    advisor = scene.add_card(Card(1970, 560, 440, 165, "Retention Advisor", "Quota, policy, retrieval, localization, and provider routing", abbreviation="AI", accent=COLORS["purple"], dashed=True, status="planned"))
    bedrock = scene.add_card(Card(1970, 840, 205, 155, "Amazon Bedrock", "AWS adapter", icon=icons.get("aws:bedrock"), accent=COLORS["teal"], dashed=True, status="disabled"))
    gemini = scene.add_card(Card(2205, 840, 205, 155, "Google Gemini", "GCP adapter", abbreviation="GEM", accent=COLORS["gcp"], dashed=True, status="disabled"))
    monitoring = scene.add_card(Card(1970, 1070, 440, 140, "Monitoring and drift", "Data quality, predictions, and model performance", abbreviation="MON", accent=COLORS["purple"], dashed=True, status="v0.5"))
    scene.connect(evidence.right, pack.left, dashed=True, color=COLORS["purple"])
    scene.connect(pack.bottom, advisor.top, dashed=True, color=COLORS["purple"])
    scene.connect(advisor.bottom, bedrock.top, dashed=True, color=COLORS["purple"])
    scene.connect(advisor.bottom, gemini.top, dashed=True, color=COLORS["purple"])
    scene.connect(reports.right, monitoring.left, dashed=True, color=COLORS["purple"])
    scene.add_legend(1390)
    return scene


def multicloud_runtime(icons: Icons) -> Scene:
    scene = Scene(
        2700,
        1520,
        "RetainAI v0.4 — Deployed Multi-Cloud Runtime",
        "Public GCP dashboard, controlled AWS backend, branded HTTPS, bounded scaling, authentication, quota, and observability",
    )
    scene.add_header_badge("DEPLOYED · v0.4", COLORS["green"], COLORS["green_soft"])

    scene.add_zone(300, 150, 1010, 1080, "Google Cloud · Dashboard Plane", "Public product experience and server-side secret boundary", COLORS["gcp_soft"], COLORS["gcp"], badge="us-east4")
    scene.add_zone(1390, 150, 1260, 1080, "AWS · Backend Plane", "Authentication, quota, prediction, explanation, and logging", COLORS["aws_soft"], COLORS["aws"], badge="us-east-1")

    user = scene.add_card(Card(45, 490, 215, 180, "Users", "Browser", abbreviation="USER", accent=COLORS["ink"], status="public"))
    domain = scene.add_card(Card(360, 285, 390, 155, "retainai.hubertronald.dev", "Managed HTTPS · direct Cloud Run mapping", abbreviation="DNS", accent=COLORS["gcp"], status="live"))
    cloudrun = scene.add_card(Card(815, 470, 420, 185, "Cloud Run dashboard", "Streamlit · scale-to-zero · max 1", icon=icons.get("gcp:cloud-run"), accent=COLORS["gcp"], status="deployed"))
    secret = scene.add_card(Card(360, 700, 390, 165, "Secret Manager", "Backend bearer token remains server-side", icon=icons.get("gcp:secret-manager"), accent=COLORS["gcp"], status="active"))
    gar = scene.add_card(Card(815, 845, 420, 165, "Artifact Registry", "Immutable dashboard container images", icon=icons.get("gcp:artifact-registry"), accent=COLORS["gcp"], status="active"))

    cert = scene.add_card(Card(1460, 250, 360, 160, "API custom domain + ACM", "api.retainai.hubertronald.dev", icon=icons.get("aws:certificate-manager"), accent=COLORS["red"], status="live"))
    gateway = scene.add_card(Card(1890, 250, 360, 160, "API Gateway HTTP API", "Regional branded entry point", icon=icons.get("aws:api-gateway"), accent=COLORS["purple"], status="deployed"))
    guard = scene.add_card(Card(1460, 520, 360, 175, "Auth and quota guard", "Constant-time bearer validation before protected work", abbreviation="AUTH", accent=COLORS["red"], status="active"))
    lamb = scene.add_card(Card(1890, 500, 360, 195, "Lambda container backend", "Prediction · survival · explainability · routing", icon=icons.get("aws:lambda"), accent=COLORS["aws"], status="deployed"))
    ddb = scene.add_card(Card(1460, 815, 360, 165, "DynamoDB quota", "3 requests per bounded window", icon=icons.get("aws:dynamodb"), accent=COLORS["purple"], status="active"))
    watch = scene.add_card(Card(1890, 815, 360, 165, "CloudWatch", "Logs and operational metrics", icon=icons.get("aws:cloudwatch"), accent=COLORS["red"], status="active"))
    ecr = scene.add_card(Card(2320, 500, 285, 175, "Amazon ECR", "Lambda images", icon=icons.get("aws:ecr"), accent=COLORS["aws"], status="active"))
    bedrock = scene.add_card(Card(2320, 815, 285, 165, "Amazon Bedrock", "Advisor adapter", icon=icons.get("aws:bedrock"), accent=COLORS["teal"], dashed=True, status="disabled"))

    terraform = scene.add_card(Card(760, 1080, 570, 120, "Terraform infrastructure", "infra/gcp-terraform · domains · IAM · secrets · service", abbreviation="TF", accent=COLORS["slate"], status="active"))
    terraform_aws = scene.add_card(Card(1700, 1080, 570, 120, "Terraform infrastructure", "infra/aws-terraform · API · Lambda · ACM · DynamoDB", abbreviation="TF", accent=COLORS["slate"], status="active"))

    scene.connect(user.right, domain.left, label="HTTPS")
    scene.connect(domain.right, cloudrun.left)
    scene.connect(secret.right, cloudrun.left, label="secret reference")
    scene.connect(gar.top, cloudrun.bottom, label="image")
    scene.connect(cloudrun.right, cert.left, label="server-side HTTPS + bearer", color=COLORS["red"], width=4)
    scene.connect(cert.right, gateway.left)
    scene.connect(gateway.bottom, lamb.top, label="invoke")
    scene.connect(guard.right, lamb.left, label="authorized context", color=COLORS["red"])
    scene.connect(lamb.left, guard.right, label="validate", color=COLORS["red"])
    scene.connect(lamb.bottom, ddb.top, label="quota")
    scene.connect(lamb.bottom, watch.top, label="logs")
    scene.connect(ecr.left, lamb.right, label="container image")
    scene.connect(lamb.bottom, bedrock.top, dashed=True, color=COLORS["purple"], label="provider routing")
    scene.connect(terraform.top, cloudrun.bottom, label="IaC")
    scene.connect(terraform_aws.top, lamb.bottom, label="IaC")

    scene.add_text(345, 1038, "Application image delivery is separate from Terraform infrastructure delivery.", 15, COLORS["muted"])
    scene.add_text(1450, 1038, "No Route 53 · No CloudFront · No load balancer", 15, COLORS["muted"], bold=True)
    scene.add_legend(1400)
    return scene


def data_evidence_pipeline(icons: Icons) -> Scene:
    scene = Scene(
        2700,
        1840,
        "RetainAI — Data, Model, Evidence, and Advisor Evolution",
        "Current analytical foundation in solid styling; cloud data, monitoring, retrieval, and advisor capabilities in dashed styling",
    )
    scene.add_header_badge("CURRENT + EVOLUTION", COLORS["purple"], COLORS["purple_soft"])

    scene.add_zone(50, 145, 820, 1450, "Current Data Foundation", "Reproducible analytical path", COLORS["green_soft"], COLORS["green"])
    scene.add_zone(910, 145, 820, 1450, "Current Model and Evidence Layer", "Prediction, survival, explainability, and artifacts", COLORS["amber_soft"], COLORS["amber"])
    scene.add_zone(1770, 145, 880, 1450, "Planned Cloud Knowledge Layer", "Data lake, monitoring, vector retrieval, and advisor", COLORS["purple_soft"], COLORS["purple"], dashed=True)

    kaggle = scene.add_card(Card(90, 260, 340, 140, "IBM HR benchmark", "Kaggle or governed data source", abbreviation="CSV", accent=COLORS["green"], status="current"))
    raw = scene.add_card(Card(480, 260, 340, 140, "Local raw zone", "Source data unchanged", abbreviation="RAW", accent=COLORS["green"], status="current"))
    quality = scene.add_card(Card(90, 515, 340, 150, "Quality and EDA", "Schema, nulls, duplicates, leakage, cohorts", abbreviation="EDA", accent=COLORS["green"], status="current"))
    processed = scene.add_card(Card(480, 515, 340, 150, "Processed data", "Typed and reproducible transformations", abbreviation="PROC", accent=COLORS["green"], status="current"))
    split = scene.add_card(Card(285, 785, 340, 150, "Train · validation · test", "Versioned feature datasets", abbreviation="SPLIT", accent=COLORS["green"], status="current"))
    scene.connect(kaggle.right, raw.left)
    scene.connect(raw.bottom, processed.top)
    scene.connect(kaggle.bottom, quality.top)
    scene.connect(quality.right, processed.left)
    scene.connect(processed.bottom, split.top)

    clf = scene.add_card(Card(950, 255, 340, 150, "Attrition classification", "Risk estimation", abbreviation="ML", accent=COLORS["orange"], status="current"))
    surv = scene.add_card(Card(1350, 255, 340, 150, "Survival analysis", "Time-to-event behavior", abbreviation="TTE", accent=COLORS["orange"], status="current"))
    shap = scene.add_card(Card(950, 535, 340, 150, "SHAP evidence", "Global and local drivers", abbreviation="SHAP", accent=COLORS["amber"], status="current"))
    eval_card = scene.add_card(Card(1350, 535, 340, 150, "Evaluation reports", "Metrics, calibration, limitations", abbreviation="EV", accent=COLORS["amber"], status="current"))
    mlflow = scene.add_card(Card(950, 815, 340, 150, "MLflow registry", "Runs, parameters, metrics, models", abbreviation="MLF", accent=COLORS["amber"], status="current"))
    docs = scene.add_card(Card(1350, 815, 340, 150, "Evidence documents", "Model cards, summaries, policies", abbreviation="DOC", accent=COLORS["amber"], status="current"))
    dashboard = scene.add_card(Card(1145, 1110, 350, 160, "Dashboard and API", "Reviewable prediction and explanation experience", icon=icons.get("gcp:cloud-run"), accent=COLORS["gcp"], status="deployed"))
    scene.connect(split.right, clf.left)
    scene.connect(split.right, surv.left)
    scene.connect(clf.bottom, shap.top)
    scene.connect(surv.bottom, eval_card.top)
    scene.connect(shap.bottom, mlflow.top)
    scene.connect(eval_card.bottom, docs.top)
    scene.connect(mlflow.right, docs.left)
    scene.connect(docs.bottom, dashboard.top)

    s3 = scene.add_card(Card(1810, 235, 370, 160, "Amazon S3 data lake", "raw · staging · analytics · features", icon=icons.get("aws:s3"), accent=COLORS["green"], dashed=True, status="planned"))
    monitor = scene.add_card(Card(2230, 235, 370, 160, "Monitoring and drift", "Data quality · predictions · performance", abbreviation="MON", accent=COLORS["purple"], dashed=True, status="v0.5"))
    evidence_docs = scene.add_card(Card(1810, 535, 370, 160, "RAG evidence corpus", "Drivers, cohorts, model cards, responsible use", abbreviation="DOC", accent=COLORS["purple"], dashed=True, status="planned"))
    vector = scene.add_card(Card(2230, 535, 370, 160, "Vector connectors", "FAISS + S3 or S3 Vectors / Bedrock KB", abbreviation="VEC", accent=COLORS["purple"], dashed=True, status="planned"))
    advisor = scene.add_card(Card(1810, 835, 370, 175, "Retention Advisor", "Retrieval, policy, quota, locale, provider routing", abbreviation="AI", accent=COLORS["purple"], dashed=True, status="planned"))
    bedrock = scene.add_card(Card(2230, 835, 175, 160, "Bedrock", "AWS adapter", icon=icons.get("aws:bedrock"), accent=COLORS["teal"], dashed=True, status="disabled"))
    gemini = scene.add_card(Card(2425, 835, 175, 160, "Gemini", "GCP adapter", abbreviation="GEM", accent=COLORS["gcp"], dashed=True, status="disabled"))
    validation = scene.add_card(Card(2015, 1160, 370, 160, "Validation dashboard", "Dataset · model · window · drift · limitations", abbreviation="REP", accent=COLORS["purple"], dashed=True, status="v0.5"))
    scene.connect(raw.right, s3.left, dashed=True, color=COLORS["purple"], label="controlled sync")
    scene.connect(split.right, s3.left, dashed=True, color=COLORS["purple"])
    scene.connect(s3.right, monitor.left, dashed=True, color=COLORS["purple"])
    scene.connect(docs.right, evidence_docs.left, dashed=True, color=COLORS["purple"], label="structured evidence")
    scene.connect(evidence_docs.right, vector.left, dashed=True, color=COLORS["purple"])
    scene.connect(vector.bottom, advisor.top, dashed=True, color=COLORS["purple"], label="retrieved context")
    scene.connect(advisor.right, bedrock.left, dashed=True, color=COLORS["purple"])
    scene.connect(advisor.right, gemini.left, dashed=True, color=COLORS["purple"])
    scene.connect(monitor.bottom, validation.top, dashed=True, color=COLORS["purple"])
    scene.add_text(1795, 1400, "Evidence before generation", 24, COLORS["purple"], bold=True)
    scene.add_text(1795, 1440, "Raw SHAP arrays are transformed into bounded, reviewable documents before retrieval or provider calls.", 16, COLORS["muted"], max_width=760, line_height=22)
    scene.add_legend(1730)
    return scene


def delivery_architecture(icons: Icons) -> Scene:
    scene = Scene(
        2700,
        1510,
        "RetainAI — Application and Infrastructure Delivery",
        "Current scripts and Terraform contracts remain the source of truth; GitHub Actions will orchestrate them with short-lived identity",
    )
    scene.add_header_badge("DELIVERY ARCHITECTURE", COLORS["slate"], COLORS["slate_soft"])

    scene.add_zone(60, 160, 1260, 1080, "Application Delivery", "Build, publish, and deploy immutable application revisions", COLORS["blue_soft"], COLORS["blue"])
    scene.add_zone(1380, 160, 1260, 1080, "Infrastructure Delivery", "Plan, review, and apply cloud resource changes", COLORS["green_soft"], COLORS["green"])

    operator = scene.add_card(Card(110, 300, 300, 145, "Maintainer", "Local DevContainer or controlled workflow", abbreviation="DEV", accent=COLORS["ink"], status="current"))
    tests = scene.add_card(Card(470, 300, 300, 145, "Tests and validation", "Unit, security, container, and contract checks", abbreviation="TEST", accent=COLORS["blue"], status="current"))
    build = scene.add_card(Card(830, 300, 390, 145, "Versioned release scripts", "Docker build and immutable image tags", abbreviation="SH", accent=COLORS["blue"], status="active"))
    gar = scene.add_card(Card(150, 610, 340, 160, "Artifact Registry", "Dashboard image", icon=icons.get("gcp:artifact-registry"), accent=COLORS["gcp"], status="active"))
    ecr = scene.add_card(Card(520, 610, 340, 160, "Amazon ECR", "Lambda image", icon=icons.get("aws:ecr"), accent=COLORS["aws"], status="active"))
    cloudrun = scene.add_card(Card(150, 905, 340, 160, "Cloud Run revision", "Application deploy only · max 1", icon=icons.get("gcp:cloud-run"), accent=COLORS["gcp"], status="deployed"))
    lamb = scene.add_card(Card(520, 905, 340, 160, "Lambda image update", "Application deploy only", icon=icons.get("aws:lambda"), accent=COLORS["aws"], status="deployed"))
    actions = scene.add_card(Card(900, 690, 330, 180, "GitHub Actions", "workflow_dispatch · main guard · immutable tags", abbreviation="GHA", accent=COLORS["purple"], dashed=True, status="next"))
    scene.connect(operator.right, tests.left)
    scene.connect(tests.right, build.left)
    scene.connect(build.bottom, gar.top)
    scene.connect(build.bottom, ecr.top)
    scene.connect(gar.bottom, cloudrun.top)
    scene.connect(ecr.bottom, lamb.top)
    scene.connect(actions.left, build.right, dashed=True, color=COLORS["purple"], label="reuse scripts")

    code = scene.add_card(Card(1430, 300, 300, 145, "Terraform code", "infra/gcp-terraform · infra/aws-terraform", abbreviation="TF", accent=COLORS["slate"], status="active"))
    fmt = scene.add_card(Card(1790, 300, 300, 145, "fmt and validate", "Static configuration checks", abbreviation="CHK", accent=COLORS["green"], status="current"))
    plan = scene.add_card(Card(2150, 300, 390, 145, "Saved Terraform plan", "Explicit artifact for review", abbreviation="PLAN", accent=COLORS["green"], status="current"))
    review = scene.add_card(Card(1430, 610, 340, 165, "Human plan review", "Reject unexpected deletion or replacement", abbreviation="REV", accent=COLORS["amber"], status="required"))
    apply = scene.add_card(Card(1810, 610, 340, 165, "Apply reviewed plan", "No implicit infrastructure changes", abbreviation="APPLY", accent=COLORS["green"], status="controlled"))
    gcp = scene.add_card(Card(1430, 920, 340, 160, "GCP resources", "Cloud Run · domains · IAM · secrets", abbreviation="GCP", accent=COLORS["gcp"], status="managed"))
    aws = scene.add_card(Card(1810, 920, 340, 160, "AWS resources", "API Gateway · Lambda · ACM · DynamoDB", abbreviation="AWS", accent=COLORS["aws"], status="managed"))
    oidc = scene.add_card(Card(2190, 610, 350, 165, "Short-lived identity", "AWS OIDC · GCP Workload Identity Federation", abbreviation="OIDC", accent=COLORS["purple"], dashed=True, status="next"))
    scene.connect(code.right, fmt.left)
    scene.connect(fmt.right, plan.left)
    scene.connect(plan.bottom, review.top)
    scene.connect(review.right, apply.left)
    scene.connect(apply.bottom, gcp.top)
    scene.connect(apply.bottom, aws.top)
    scene.connect(oidc.left, apply.right, dashed=True, color=COLORS["purple"], label="approved automation")
    scene.add_text(85, 1155, "Application delivery never runs Terraform.", 18, COLORS["blue"], bold=True)
    scene.add_text(1410, 1155, "Infrastructure delivery never changes images as a side effect.", 18, COLORS["green"], bold=True)
    scene.add_legend(1400)
    return scene


def runtime_sequence(icons: Icons) -> Scene:
    scene = Scene(
        2800,
        1630,
        "RetainAI — Runtime Request Sequence",
        "Authentication and quota precede protected work; the optional advisor branch remains disabled until evidence and provider controls are enabled",
    )
    scene.add_header_badge("RUNTIME SEQUENCE", COLORS["red"], COLORS["red_soft"])

    x_positions = [90, 480, 900, 1320, 1740, 2160, 2500]
    cards = [
        scene.add_card(Card(x_positions[0], 180, 300, 150, "User and browser", "Public product entry", abbreviation="USER", accent=COLORS["ink"], status="public")),
        scene.add_card(Card(x_positions[1], 180, 330, 150, "Cloud Run dashboard", "Server-side application", icon=icons.get("gcp:cloud-run"), accent=COLORS["gcp"], status="deployed")),
        scene.add_card(Card(x_positions[2], 180, 330, 150, "Secret Manager", "Backend token", icon=icons.get("gcp:secret-manager"), accent=COLORS["gcp"], status="active")),
        scene.add_card(Card(x_positions[3], 180, 330, 150, "API Gateway", "Branded HTTPS entry", icon=icons.get("aws:api-gateway"), accent=COLORS["purple"], status="deployed")),
        scene.add_card(Card(x_positions[4], 180, 330, 150, "Lambda backend", "Controlled orchestration", icon=icons.get("aws:lambda"), accent=COLORS["aws"], status="deployed")),
        scene.add_card(Card(x_positions[5], 180, 300, 150, "Auth and quota", "Bearer + DynamoDB", icon=icons.get("aws:dynamodb"), accent=COLORS["red"], status="active")),
        scene.add_card(Card(x_positions[6], 180, 240, 150, "AI adapter", "Gemini / Bedrock", icon=icons.get("aws:bedrock"), accent=COLORS["purple"], dashed=True, status="disabled")),
    ]

    lane_top = 375
    lane_bottom = 1410
    for card in cards:
        x = card.x + card.width / 2
        scene.add_line([(x, lane_top), (x, lane_bottom)], color=COLORS["soft_line"], width=2, dashed=True, arrow=False)

    steps = [
        (1, cards[0].right, cards[1].left, 440, "Open retainai.hubertronald.dev", False),
        (2, cards[1].right, cards[2].left, 535, "Read token server-side", False),
        (3, cards[2].left, cards[1].right, 625, "Return secret value", False),
        (4, cards[1].right, cards[3].left, 735, "HTTPS + bearer token", False),
        (5, cards[3].right, cards[4].left, 835, "Invoke Lambda", False),
        (6, cards[4].right, cards[5].left, 945, "Validate auth and quota", False),
        (7, cards[5].left, cards[4].right, 1040, "Authorized context", False),
        (8, cards[4].right, cards[6].left, 1160, "Optional evidence-grounded advisor", True),
        (9, cards[4].left, cards[3].right, 1280, "Structured prediction and explanation", False),
        (10, cards[3].left, cards[1].right, 1370, "HTTPS response", False),
    ]

    for number, start, end, y, label, dashed in steps:
        sx = start[0]
        ex = end[0]
        color = COLORS["purple"] if dashed else COLORS["line"]
        scene.add_circle(sx, y, 18, COLORS["white"], color, 2)
        scene.add_text(sx, y + 6, str(number), 12, color, bold=True, anchor="middle")
        scene.add_line(
            [(sx + 22, y), (ex - 14 if ex > sx else ex + 14, y)],
            color=color,
            width=3,
            dashed=dashed,
            arrow=True,
            label=label,
            label_x=(sx + ex) / 2,
            label_y=y - 16,
        )

    scene.add_rect(1680, 1085, 1040, 145, COLORS["purple_soft"], COLORS["purple"], radius=24, stroke_width=2, dashed=True)
    scene.add_text(1710, 1125, "Optional provider branch — disabled in v0.4", 21, COLORS["purple"], bold=True)
    scene.add_text(1710, 1165, "No AI call occurs before authentication, quota, evidence assembly, schema validation, and explicit provider enablement.", 15, COLORS["muted"], max_width=940, line_height=22)
    scene.add_legend(1525)
    return scene


BUILDERS = {
    "decision-intelligence": decision_intelligence,
    "multicloud-runtime-v0-4": multicloud_runtime,
    "data-model-evidence-pipeline": data_evidence_pipeline,
    "delivery-architecture": delivery_architecture,
    "runtime-sequence": runtime_sequence,
}

OUTPUTS = {
    "decision-intelligence": "figs/retainai_decision_intelligence_architecture",
    "multicloud-runtime-v0-4": "figs/architecture/retainai_multicloud_runtime_v0_4",
    "data-model-evidence-pipeline": "figs/architecture/retainai_data_model_evidence_pipeline",
    "delivery-architecture": "figs/architecture/retainai_delivery_architecture",
    "runtime-sequence": "figs/architecture/retainai_runtime_sequence",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--diagram", choices=["all", *BUILDERS], default="all")
    parser.add_argument("--png-scale", type=float, default=1.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.root.resolve()
    vendor_root = root / "docs/architecture/assets/vendor"
    icons = Icons(vendor_root)

    selected = list(BUILDERS) if args.diagram == "all" else [args.diagram]

    for name in selected:
        scene = BUILDERS[name](icons)
        base = root / OUTPUTS[name]
        svg_path = base.with_suffix(".svg")
        png_path = base.with_suffix(".png")
        scene.save_svg(svg_path)
        scene.save_png(png_path, scale=args.png_scale)
        print(f"Rendered {svg_path}")
        print(f"Rendered {png_path}")


if __name__ == "__main__":
    main()
