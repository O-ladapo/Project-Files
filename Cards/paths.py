import os, sys
from PyQt5 import QtGui

def base_dir():
    return getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))

def resource_path(rel):
    return os.path.join(base_dir(), rel)

def card_pixmap(key):
    from Cards.card_renderer import render_card
    return render_card(key)