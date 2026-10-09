import sqlite3
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import (QPixmap, QPainter, QColor, QFont, QFontMetrics, QLinearGradient, QPen, QBrush, QPainterPath)
from Cards.paths import resource_path

CARD_WIDTH, CARD_HEIGHT = 360, 460
PIXMAP_WIDTH, PIXMAP_HEIGHT = 141, 181
_cards = None
_cache = {}


def _load_cards():
    global _cards
    if _cards is None:
        conn = sqlite3.connect(resource_path("../Database/cards.db"))
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, card_name, rating, pos, PAC, SHO, PAS, DRI, DEF, PHY FROM all_cards"
        ).fetchall()
        conn.close()
        _cards = {r["id"]: dict(r) for r in rows}
    return _cards


def _palette(rating):
    if rating >= 82:
        return "#f7e27c", "#b9870f", "#fff3b0", "#2e1f03"
    if rating >= 75:
        return "#f3dc7a", "#d2a62f", "#fbefb4", "#35260a"
    return "#e6d08a", "#c4a24a", "#f1e3ae", "#3b2a08"


def _shield():
    m = 12
    p = QPainterPath()
    p.moveTo(m + 50, m)
    p.lineTo(CARD_WIDTH - m - 50, m)
    p.quadTo(CARD_WIDTH - m, m, CARD_WIDTH - m, m + 50)
    p.lineTo(CARD_WIDTH - m, CARD_HEIGHT - 120)
    p.quadTo(CARD_WIDTH - m, CARD_HEIGHT - 60, CARD_WIDTH / 2, CARD_HEIGHT - m)
    p.quadTo(m, CARD_HEIGHT - 60, m, CARD_HEIGHT - 120)
    p.lineTo(m, m + 50)
    p.quadTo(m, m, m + 50, m)
    p.closeSubpath()
    return p


def _fit_font(text, max_width, start=34, minimum=16):
    size = start
    while size > minimum:
        font = QFont("Arial")
        font.setPixelSize(size)
        font.setBold(True)
        if QFontMetrics(font).horizontalAdvance(text) <= max_width:
            return font
        size -= 1
    font = QFont("Arial")
    font.setPixelSize(minimum)
    font.setBold(True)
    return font


def _draw_text(p, text, rect, font, color, align):
    p.setFont(font)
    p.setPen(QColor(color))
    p.drawText(rect, align, text)


def _draw_card(card):
    top, bottom, border, text = _palette(card["rating"])
    pm = QPixmap(PIXMAP_WIDTH, PIXMAP_HEIGHT)
    pm.fill(Qt.transparent)

    p = QPainter(pm)
    p.scale(PIXMAP_WIDTH / CARD_WIDTH, PIXMAP_HEIGHT / CARD_HEIGHT)
    p.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

    grad = QLinearGradient(0, 0, 0, CARD_HEIGHT)
    grad.setColorAt(0, QColor(top))
    grad.setColorAt(1, QColor(bottom))
    shape = _shield()
    p.setBrush(QBrush(grad))
    p.setPen(QPen(QColor(border), 6))
    p.drawPath(shape)

    p.save()
    p.setClipPath(shape)
    p.setPen(Qt.NoPen)
    p.setBrush(QColor(0, 0, 0, 45))
    p.drawEllipse(QRectF(195, 90, 80, 80))
    p.drawEllipse(QRectF(160, 175, 150, 130))
    p.restore()

    big = QFont("Arial"); big.setPixelSize(70); big.setBold(True)
    mid = QFont("Arial"); mid.setPixelSize(30); mid.setBold(True)
    _draw_text(p, str(card["rating"]), QRectF(40, 50, 130, 80), big, text, Qt.AlignLeft | Qt.AlignVCenter)
    _draw_text(p, card["pos"], QRectF(40, 128, 130, 36), mid, text, Qt.AlignLeft | Qt.AlignVCenter)

    name = card["card_name"]
    _draw_text(p, name, QRectF(40, 262, CARD_WIDTH - 80, 44),
               _fit_font(name, CARD_WIDTH - 90), text, Qt.AlignCenter)

    p.setPen(QPen(QColor(text), 2))
    p.drawLine(70, 312, CARD_WIDTH - 70, 312)

    val_font = QFont("Arial"); val_font.setPixelSize(26); val_font.setBold(True)
    lab_font = QFont("Arial"); lab_font.setPixelSize(22)
    columns = [
        [("PAC", card["PAC"]), ("SHO", card["SHO"]), ("PAS", card["PAS"])],
        [("DRI", card["DRI"]), ("DEF", card["DEF"]), ("PHY", card["PHY"])],
    ]
    for c, stats in enumerate(columns):
        x = 60 + c * 125
        for r, (label, value) in enumerate(stats):
            y = 322 + r * 31
            _draw_text(p, str(value), QRectF(x, y, 45, 30), val_font, text, Qt.AlignRight | Qt.AlignVCenter)
            _draw_text(p, label, QRectF(x + 52, y, 60, 30), lab_font, text, Qt.AlignLeft | Qt.AlignVCenter)

    p.end()
    return pm

def _draw_empty():
    pm = QPixmap(PIXMAP_WIDTH, PIXMAP_HEIGHT)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.scale(PIXMAP_WIDTH / CARD_WIDTH, PIXMAP_HEIGHT / CARD_HEIGHT)
    p.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

    shape = _shield()
    p.setBrush(QColor(70, 70, 70))
    pen = QPen(QColor(150, 150, 150), 6)
    pen.setStyle(Qt.DashLine)
    p.setPen(pen)
    p.drawPath(shape)

    font = QFont("Arial")
    font.setPixelSize(110)
    font.setBold(True)
    p.setFont(font)
    p.setPen(QColor(150, 150, 150))
    p.drawText(QRectF(0, 0, CARD_WIDTH, CARD_HEIGHT - 40), Qt.AlignCenter, "?")
    p.end()
    return pm


def render_card(key):
    if key in _cache:
        return _cache[key]
    card = None
    if isinstance(key, str) and key.startswith("card:"):
        try:
            card = _load_cards().get(int(key.split(":", 1)[1]))
        except ValueError:
            card = None
    if card is None:
        pm = _draw_empty()
    else:
        pm = _draw_card(card)
    _cache[key] = pm
    return pm