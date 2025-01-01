from __future__ import annotations

"""PySide6 port of the widgets/layouts/dynamiclayouts example from Qt v5.x"""

from PySide6.QtCore import Qt, QSize, Signal, Slot
from PySide6.QtWidgets import (QApplication, QDialog, QLayout, QGridLayout,
                               QMessageBox, QGroupBox, QSpinBox, QSlider, QPushButton,
                               QProgressBar, QDial, QDialogButtonBox, QWidget,
                               QComboBox, QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem,
                               QSizePolicy)
from PySide6.QtGui import QPalette, QColor


import utils
import argparse
from URxxx.ur44c import *
from URxxx.params import *
from test.ur44c_mock import *

ur44c = None


WHITE = QColor(255, 255, 255)
BUTTON = WHITE
BUTTON_SET = QColor(255, 136, 0)
VERY_DARK = QColor(53, 53, 53)
SUPER_DARK = QColor(42, 42, 42)
DARK = QColor(66, 66, 66)
RED = QColor(255, 0, 0)
HIGHLIGHT = QColor(142, 45, 197).lighter()


class Send(QWidget):
    category = UR44C_Params_Mixer
    parameter = "InputReverbSend"
    channel_no = 0

    @Slot()
    def dial(self, pos):
        if not ur44c.SetParameterByName(self.category, self.parameter, pos, self.channel_no):
            exit(1)

        label = utils.slider2dB(pos)

        self.val_label.setText(label)


    def __init__(self, channel_no):
        super().__init__()

        self.channel_no = channel_no

        val = ur44c.GetParameterByName(self.category, self.parameter, self.channel_no)
        if val == None:
            exit(1)

        layout = QVBoxLayout()

        dialer = QDial()
        dialer.setRange(0, 127)
        dialer.setFixedSize(60, 60)
        dialer.setValue(val)

        self.val_label = QLabel(utils.slider2dB(val))
        name_label = QLabel(f"Input {channel_no}")

        layout.addWidget(dialer)
        layout.addWidget(self.val_label)

        layout.setAlignment(dialer, Qt.AlignCenter)
        layout.setAlignment(self.val_label, Qt.AlignCenter)

        self.setLayout(layout)

        dialer.valueChanged.connect(self.dial)



class Pan(QWidget):
    category = UR44C_Params_Mixer
    parameter = "InputMix1Pan"
    channel_no = 0

    @Slot()
    def dial(self, pos):
        if not ur44c.SetParameterByName(self.category, self.parameter, pos, self.channel_no):
            exit(1)

        self.label.setText(utils.pan2Label(pos))

    def __init__(self, channel_no):
        super().__init__()

        self.channel_no = channel_no

        val = ur44c.GetParameterByName(self.category, self.parameter, self.channel_no)
        if val == None:
            exit(1)

        self.label = QLabel(utils.pan2Label(val))

        dial = QDial()
        dial.valueChanged.connect(self.dial)
        dial.setRange(-16, 16)
        dial.setFixedSize(60, 60)
        dial.setValue(val)

        vlayout = QVBoxLayout()
        vlayout.addWidget(dial)
        vlayout.addWidget(self.label)

        vlayout.setAlignment(dial, Qt.AlignCenter)
        vlayout.setAlignment(self.label, Qt.AlignCenter)

        self.setLayout(vlayout)


class Fader(QWidget):
    category = UR44C_Params_Mixer
    parameter = "Dummy"
    channel_no = 0

    @Slot()
    def slide(self, pos):
        if not ur44c.SetParameterByName(self.category, self.parameter, pos, self.channel_no):
            exit(1)

        label = utils.slider2dB(pos)

        self.val_label.setText(label)


    def __init__(self, channel_no, parameter="InputMix1Volume"):
        super().__init__()

        self.channel_no = channel_no
        self.parameter = parameter

        val = ur44c.GetParameterByName(self.category, self.parameter, self.channel_no)
        if val == None:
            exit(1)

        layout = QVBoxLayout()

        slider = QSlider()
        slider.setRange(0, 127)
        slider.setValue(val)

        self.val_label = QLabel(utils.slider2dB(val))

        layout.addWidget(slider)
        layout.addWidget(self.val_label)

        layout.setAlignment(slider, Qt.AlignCenter)
        layout.setAlignment(self.val_label, Qt.AlignCenter)

        self.setLayout(layout)

        slider.valueChanged.connect(self.slide)


class Button(QPushButton):
    category = UR44C_Params_Mixer
    parameter = "Dummy"
    channel_no = 0
    state = False
    colors = (WHITE, HIGHLIGHT)

    def update_font(self):
        palette = self.palette()
        palette.setColor(self.foregroundRole(), self.colors[self.state])
        self.setPalette(palette)
        self.repaint()


    def toggle(self):
        self.state = not self.state
        self.update_font()


    @Slot()
    def click(self):
        self.toggle()

        if not ur44c.SetParameterByName(self.category, self.parameter, self.state, self.channel_no):
            exit(1)


    def __init__(self, text, channel_no, parameter):
        super().__init__(text)

        self.channel_no = channel_no
        self.parameter = parameter

        val = ur44c.GetParameterByName(self.category, self.parameter, self.channel_no)
        if val < 0 or val > 1:
            exit(1)

        self.state = bool(val)

        self.update_font()

        self.clicked.connect(self.click)


class Mute(Button):
    colors = (HIGHLIGHT, WHITE)

    def __init__(self, channel_no, parameter):
        super().__init__("M", channel_no, parameter)


class Solo(Button):
    def __init__(self, channel_no, parameter):
        super().__init__("S", channel_no, parameter)


class Input(QWidget):
    def __init__(self, channel_no):
        super().__init__()

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        name_label = QLabel(f"Input {channel_no+1}")
        mbutton = Mute(channel_no, "InputMix1Mute")
        sbutton = Solo(channel_no, "InputMix1Solo")

        mbutton.setFixedWidth(20)
        sbutton.setFixedWidth(20)

        hlayout.addWidget(mbutton)
        hlayout.addWidget(sbutton)

        vlayout.addWidget(Send(channel_no))
        vlayout.addWidget(Pan(channel_no))
        vlayout.addLayout(hlayout)
        vlayout.addWidget(Fader(channel_no, "InputMix1Volume"))
        vlayout.addWidget(name_label)
        vlayout.setAlignment(name_label, Qt.AlignCenter)

        self.setLayout(vlayout)


class DAWInput(QWidget):
    def __init__(self):
        super().__init__()

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        name_label = QLabel(f"DAW")
        spacer = QSpacerItem(50, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
        mbutton = Mute(0, "DAWMix1Mute")
        sbutton = Solo(0, "DAWMix1Solo")

        mbutton.setFixedWidth(20)
        sbutton.setFixedWidth(20)

        hlayout.addWidget(mbutton)
        hlayout.addWidget(sbutton)

        vlayout.addItem(spacer)
        vlayout.addWidget(Pan(0))
        vlayout.addLayout(hlayout)
        vlayout.addWidget(Fader(0, "DAWMix1Volume"))
        vlayout.addWidget(name_label)
        vlayout.setAlignment(name_label, Qt.AlignCenter)

        self.setLayout(vlayout)


class MusicInput(QWidget):
    def __init__(self):
        super().__init__()

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        spacer = QSpacerItem(50, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
        name_label = QLabel(f"Music")
        mbutton = Mute(0, "MusicMix1Mute")
        sbutton = Solo(0, "MusicMix1Solo")

        mbutton.setFixedWidth(20)
        sbutton.setFixedWidth(20)

        hlayout.addWidget(mbutton)
        hlayout.addWidget(sbutton)

        vlayout.addItem(spacer)
        vlayout.addWidget(Pan(0))
        vlayout.addLayout(hlayout)
        vlayout.addWidget(Fader(0, "MusicMix1Volume"))
        vlayout.addWidget(name_label)
        vlayout.setAlignment(name_label, Qt.AlignCenter)

        self.setLayout(vlayout)


class VoiceInput(QWidget):
    def __init__(self):
        super().__init__()

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        name_label = QLabel(f"Voice")
        spacer = QSpacerItem(50, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)
        mbutton = Mute(1, "MusicMix1Mute")
        sbutton = Solo(1, "MusicMix1Solo")

        mbutton.setFixedWidth(20)
        sbutton.setFixedWidth(20)

        hlayout.addWidget(mbutton)
        hlayout.addWidget(sbutton)

        vlayout.addItem(spacer)
        vlayout.addWidget(Pan(0))
        vlayout.addLayout(hlayout)
        vlayout.addWidget(Fader(1, "MusicMix1Volume"))
        vlayout.addWidget(name_label)
        vlayout.setAlignment(name_label, Qt.AlignCenter)

        self.setLayout(vlayout)


class Dialog(QDialog):
    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout()
        main_layout.addWidget(Input(0))
        main_layout.addWidget(Input(1))
        main_layout.addWidget(Input(2))
        main_layout.addWidget(Input(3))
        main_layout.addWidget(Input(4))
        main_layout.addWidget(Input(5))
        main_layout.addWidget(DAWInput())
        main_layout.addWidget(MusicInput())
        main_layout.addWidget(VoiceInput())

        self._main_layout = main_layout
        self.setLayout(self._main_layout)

        self.setWindowTitle("URcontrol")


def enable_dark_mode(app):
    dark_palette = QPalette()

    # Set dark background
    dark_palette.setColor(QPalette.Window, VERY_DARK)
    dark_palette.setColor(QPalette.WindowText, WHITE)
    dark_palette.setColor(QPalette.Base, SUPER_DARK)
    dark_palette.setColor(QPalette.AlternateBase, DARK)
    dark_palette.setColor(QPalette.ToolTipBase, WHITE)
    dark_palette.setColor(QPalette.ToolTipText, WHITE)
    dark_palette.setColor(QPalette.Text, WHITE)
    dark_palette.setColor(QPalette.Button, VERY_DARK)
    dark_palette.setColor(QPalette.ButtonText, BUTTON)
    dark_palette.setColor(QPalette.BrightText, RED)

    # Highlight colors
    dark_palette.setColor(QPalette.Highlight, HIGHLIGHT)
    dark_palette.setColor(QPalette.HighlightedText, WHITE)

    # Set the palette
    app.setPalette(dark_palette)


if __name__ == '__main__':
    import sys

    formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=45)
    parser = argparse.ArgumentParser(description='GUI to control UR44C by MIDI', formatter_class=formatter)

    parser.add_argument('--midi-in', '-mi', action='store', help='Input MIDI port', metavar='PORT', default='')
    parser.add_argument('--midi-out', '-mo', action='store', help='Output MIDI port', metavar='PORT', default='')
    parser.add_argument('--get-midi-ports', '-m', action='store_true', help='Show MIDI ports in system')
    parser.add_argument('--test', '-t', action='store_true', help='Run in test mode (no physical device required)')

    args = parser.parse_args()

    if args.get_midi_ports:
        utils.print_midi_ports()
        exit(0)

    if args.test:
        ur44c = UR44C_mock()
    else:
        midi_in, midi_out = utils.open_midi_ports(args.midi_in, args.midi_out)
        ur44c = UR44C(midi_in, midi_out)

    app = QApplication(sys.argv)
    enable_dark_mode(app)

    dialog = Dialog()
    dialog.exec()