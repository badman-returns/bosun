"""A small diagram builder for the bosun docs.

Each diagram script describes boxes, panels, arrows, notes and a legend in canvas
coordinates. save() writes two files next to the script: an .excalidraw file that
you can open at https://excalidraw.com, and an .svg file that GitHub shows in the
README. Edit the .py script and run it again. Do not edit the outputs by hand.

Colours tell "when": each arrow, note and legend row has a phase number.
  0 problem   1 start   2 you   3 agents   4 the gate and the PR
"""
import json
import os
from html import escape

PHASE = {0: "#c2255c", 1: "#495057", 2: "#1971c2", 3: "#6741d9", 4: "#2f9e44"}
KIND = {  # fill, stroke, title colour
    "plain": ("#ffffff", "#343a40", "#1e1e1e"),
    "agent": ("#f3f0ff", "#6741d9", "#6741d9"),
    "store_hot": ("#fff9db", "#f08c00", "#f08c00"),
    "store_cold": ("#d3f9d8", "#2f9e44", "#2f9e44"),
    "panel": ("#f8f9fa", "#343a40", "#1e1e1e"),
}
INK, MUTED = "#1e1e1e", "#868e96"
FONT = "Inter, Segoe UI, system-ui, -apple-system, sans-serif"


class Shape:
    def __init__(self, x, y, w, h, cursor):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.cursor = cursor  # top of the next body text

    @property
    def right(self):
        return self.x + self.w

    @property
    def bottom(self):
        return self.y + self.h


class Diagram:
    def __init__(self, title, subtitle):
        self.rects, self.paths, self.texts = [], [], []
        self.text(60, 40, title, 28, INK, bold=True)
        self.text(60, 84, subtitle, 15, MUTED, bold=True)

    # ---- primitives
    def text(self, x, y, s, size=13, color=INK, bold=False):
        """Text whose top-left corner is (x, y). Lines split on newline."""
        self.texts.append((x, y, s.split("\n"), size, color, bold))
        return y + len(s.split("\n")) * size * 1.25

    def _rect(self, x, y, w, h, fill, stroke, dashed=False):
        self.rects.append((x, y, w, h, fill, stroke, dashed))

    # ---- shapes
    def box(self, x, y, w, h, title, sub=None, kind="plain"):
        fill, stroke, ink = KIND[kind]
        self._rect(x, y, w, h, fill, stroke)
        self.text(x + 22, y + 20, title, 16, ink, bold=True)
        if sub:
            self.text(x + 22, y + 50, sub, 13, MUTED)
            return Shape(x, y, w, h, y + 82)
        return Shape(x, y, w, h, y + 58)

    def panel(self, x, y, w, h, title):
        return self.box(x, y, w, h, title, kind="panel")

    def body(self, shape, s, dy=0, size=13):
        shape.cursor = self.text(shape.x + 22, shape.cursor + dy, s, size, INK)

    def note(self, x, y, w, s, phase=1):
        lines = s.split("\n")
        self._rect(x, y, w, 24 + 15 * len(lines), "#e7f5ff", PHASE[phase], dashed=True)
        self.text(x + 18, y + 12, s, 12, PHASE[phase])

    def legend(self, x, y, w, title, items):
        self._rect(x, y, w, 56 + 60.25 * len(items), "#ffffff", "#dee2e6")
        self.text(x + 24, y + 22, title, 16, INK, bold=True)
        for i, (phase, label, desc) in enumerate(items):
            top = y + 66 + i * 60.25
            self.text(x + 24, top, f"{phase}     {label}", 13, PHASE[phase])
            self.text(x + 24, top + 24, desc, 13, INK)

    # ---- arrows
    def _label(self, x, y, s, size, phase, above):
        n = len(s.split("\n"))
        top = y - 10 - n * size * 1.25 if above else y + 10
        self.text(x, top, s, size, PHASE[phase])

    def arrow_h(self, a, b, y, label=None, phase=1, above=True):
        x1, x2 = (a.right + 4, b.x - 4) if a.x < b.x else (a.x - 4, b.right + 4)
        self.paths.append(([(x1, y), (x2, y)], PHASE[phase]))
        if label:
            self._label(min(x1, x2) + 8, y, label, 13, phase, above)

    def arrow_v(self, a, b, x, label=None, phase=1):
        y1, y2 = (a.bottom + 4, b.y - 4) if a.y < b.y else (a.y - 4, b.bottom + 4)
        self.paths.append(([(x, y1), (x, y2)], PHASE[phase]))
        if label:
            self.text(x + 22, (y1 + y2) / 2 - 7.5, label, 12, PHASE[phase])

    def arrow_path(self, points, phase=1, label=None, label_at=None):
        self.paths.append((points, PHASE[phase]))
        if label:
            self.text(label_at[0], label_at[1], label, 12, PHASE[phase])

    # ---- output
    def _bounds(self):
        xs, ys = [], []
        for x, y, w, h, *_ in self.rects:
            xs += [x, x + w]
            ys += [y, y + h]
        for pts, _ in self.paths:
            xs += [p[0] for p in pts]
            ys += [p[1] for p in pts]
        for x, y, lines, size, *_ in self.texts:
            xs += [x, x + max(len(line) for line in lines) * size * 0.55]
            ys += [y, y + len(lines) * size * 1.25]
        return min(xs) - 40, max(xs) + 40, max(ys) + 40

    def svg(self):
        x0, x1, h = self._bounds()
        w = x1 - x0
        out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:g}" height="{h:g}" '
               f'viewBox="{x0:g} 0 {w:g} {h:g}" font-family="{FONT}">',
               f'<rect x="{x0:g}" y="0" width="{w:g}" height="{h:g}" fill="#ffffff"/>', "<defs>"]
        for c in sorted({c for _, c in self.paths}):
            out.append(f'<marker id="a{c[1:]}" markerWidth="9" markerHeight="7" refX="8" refY="3.5" '
                       f'orient="auto"><polygon points="0 0, 9 3.5, 0 7" fill="{c}"/></marker>')
        out.append("</defs>")
        for x, y, rw, rh, fill, stroke, dashed in self.rects:
            dash = ' stroke-dasharray="8 6"' if dashed else ""
            out.append(f'<rect x="{x:g}" y="{y:g}" width="{rw:g}" height="{rh:g}" rx="10" fill="{fill}" '
                       f'stroke="{stroke}" stroke-width="1.5"{dash}/>')
        for pts, c in self.paths:
            d = " L ".join(f"{px:g} {py:g}" for px, py in pts)
            out.append(f'<path d="M {d}" fill="none" stroke="{c}" stroke-width="2" '
                       f'stroke-linejoin="round" marker-end="url(#a{c[1:]})"/>')
        for x, y, lines, size, color, bold in self.texts:
            out.append(f'<text x="{x:g}" y="{y + size * 0.95:g}" font-size="{size}" '
                       f'font-weight="{600 if bold else 400}" fill="{color}" xml:space="preserve">')
            for i, line in enumerate(lines):
                out.append(f'<tspan x="{x:g}" dy="{0 if i == 0 else size * 1.25:g}">{escape(line) or "&#160;"}</tspan>')
            out.append("</text>")
        out.append("</svg>")
        return "\n".join(out) + "\n"

    def excalidraw(self):
        els = []

        def base(kind, x, y, w, h, stroke, fill="transparent"):
            els.append({
                "id": f"e{len(els):03d}", "type": kind, "x": x, "y": y, "width": w, "height": h,
                "angle": 0, "strokeColor": stroke, "backgroundColor": fill, "fillStyle": "solid",
                "strokeWidth": 1.5, "strokeStyle": "solid", "roughness": 0, "opacity": 100,
                "groupIds": [], "frameId": None, "roundness": None, "seed": len(els) + 1,
                "version": 1, "versionNonce": len(els) + 1, "isDeleted": False,
                "boundElements": None, "updated": 1, "link": None, "locked": False,
            })
            return els[-1]

        for x, y, w, h, fill, stroke, dashed in self.rects:
            e = base("rectangle", x, y, w, h, stroke, fill)
            e["roundness"] = {"type": 3}
            if dashed:
                e["strokeStyle"] = "dashed"
        for pts, c in self.paths:
            (sx, sy) = pts[0]
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            e = base("arrow", sx, sy, max(xs) - min(xs), max(ys) - min(ys), c)
            e.update(strokeWidth=2, points=[[px - sx, py - sy] for px, py in pts],
                     startArrowhead=None, endArrowhead="arrow", startBinding=None, endBinding=None)
        for x, y, lines, size, color, _ in self.texts:
            s = "\n".join(lines)
            e = base("text", x, y, max(len(line) for line in lines) * size * 0.55,
                     len(lines) * size * 1.25, color)
            e.update(text=s, originalText=s, fontSize=size, fontFamily=2, textAlign="left",
                     verticalAlign="top", containerId=None, lineHeight=1.25, autoResize=True)
        return {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com",
                "elements": els, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
                "files": {}}

    def save(self, path):
        """Write <name>.excalidraw and <name>.svg."""
        stem = os.path.splitext(path)[0]
        with open(stem + ".excalidraw", "w", encoding="utf-8") as f:
            json.dump(self.excalidraw(), f, indent=2)
            f.write("\n")
        with open(stem + ".svg", "w", encoding="utf-8") as f:
            f.write(self.svg())
