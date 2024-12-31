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
from ur44c import *

ur44c = None


class Send(QWidget):
    @Slot()
    def dial(self, pos):
        label = utils.slider2dB(pos)

        self.val_label.setText(label)


    def __init__(self, channel_no):
        super().__init__()

        layout = QVBoxLayout()

        dialer = QDial()
        dialer.setRange(0, 127)
        dialer.setFixedSize(60, 60)

        self.val_label = QLabel("-∞")
        name_label = QLabel(f"Input {channel_no}")

        layout.addWidget(dialer)
        layout.addWidget(self.val_label)

        layout.setAlignment(dialer, Qt.AlignCenter)
        layout.setAlignment(self.val_label, Qt.AlignCenter)

        self.setLayout(layout)

        dialer.valueChanged.connect(self.dial)



class Pan(QWidget):
    @Slot()
    def dial(self, pos):
        if pos < 0:
            self.label.setText(f"L{-pos}")
        elif pos == 0:
            self.label.setText("C")
        if pos > 0:
            self.label.setText(f"R{pos}")


    def __init__(self, channel_no):
        super().__init__()

        vlayout = QVBoxLayout()

        dial = QDial()
        dial.valueChanged.connect(self.dial)
        dial.setRange(-16, 16)
        dial.setFixedSize(60, 60)


        self.label = QLabel("C")

        vlayout.addWidget(dial)
        vlayout.addWidget(self.label)

        vlayout.setAlignment(dial, Qt.AlignCenter)
        vlayout.setAlignment(self.label, Qt.AlignCenter)

        self.setLayout(vlayout)


class Fader(QWidget):
    category = UR44C_Params_Mixer
    parameter = "InputMix1Volume"
    channel_no = 0

    @Slot()
    def slide(self, pos):
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


class Input(QWidget):
    def __init__(self, channel_no):
        super().__init__()

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        name_label = QLabel(f"Input {channel_no+1}")
        mbutton = QPushButton("M")
        sbutton = QPushButton("S")

        mbutton.setFixedWidth(20)
        sbutton.setFixedWidth(20)

        hlayout.addWidget(mbutton)
        hlayout.addWidget(sbutton)

        vlayout.addWidget(Send(channel_no))
        vlayout.addWidget(Pan(channel_no))
        vlayout.addLayout(hlayout)
        vlayout.addWidget(Fader(channel_no))
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
        mbutton = QPushButton("M")
        sbutton = QPushButton("S")

        mbutton.setFixedWidth(20)
        sbutton.setFixedWidth(20)

        hlayout.addWidget(mbutton)
        hlayout.addWidget(sbutton)

        vlayout.addItem(spacer)
        vlayout.addWidget(Pan(0))
        vlayout.addLayout(hlayout)
        vlayout.addWidget(Fader(0))
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
        mbutton = QPushButton("M")
        sbutton = QPushButton("S")

        mbutton.setFixedWidth(20)
        sbutton.setFixedWidth(20)

        hlayout.addWidget(mbutton)
        hlayout.addWidget(sbutton)

        vlayout.addItem(spacer)
        vlayout.addWidget(Pan(0))
        vlayout.addLayout(hlayout)
        vlayout.addWidget(Fader(0))
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
        mbutton = QPushButton("M")
        sbutton = QPushButton("S")

        mbutton.setFixedWidth(20)
        sbutton.setFixedWidth(20)

        hlayout.addWidget(mbutton)
        hlayout.addWidget(sbutton)

        vlayout.addItem(spacer)
        vlayout.addWidget(Pan(0))
        vlayout.addLayout(hlayout)
        vlayout.addWidget(Fader(0))
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
    dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Base, QColor(42, 42, 42))
    dark_palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))

    # Highlight colors
    dark_palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
    dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

    # Set the palette
    app.setPalette(dark_palette)


if __name__ == '__main__':
    import sys

    formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=45)
    parser = argparse.ArgumentParser(description='GUI to control UR44C by MIDI', formatter_class=formatter)

    parser.add_argument('--midi-in', '-mi', action='store', help='Input MIDI port', metavar='PORT', default='')
    parser.add_argument('--midi-out', '-mo', action='store', help='Output MIDI port', metavar='PORT', default='')
    parser.add_argument('--get-midi-ports', '-m', action='store_true', help='Show MIDI ports in system')

    args = parser.parse_args()

    if args.get_midi_ports:
        utils.print_midi_ports()
        exit(0)

    midi_in, midi_out = utils.open_midi_ports(args.midi_in, args.midi_out)

    ur44c = UR44C(midi_in, midi_out)

    app = QApplication(sys.argv)
    enable_dark_mode(app)

    dialog = Dialog()
    dialog.exec()