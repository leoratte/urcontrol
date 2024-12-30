# Copyright (C) 2013 Riverbank Computing Limited.
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

"""PySide6 port of the widgets/layouts/dynamiclayouts example from Qt v5.x"""

from PySide6.QtCore import Qt, QSize, Signal, Slot
from PySide6.QtWidgets import (QApplication, QDialog, QLayout, QGridLayout,
                               QMessageBox, QGroupBox, QSpinBox, QSlider, QPushButton,
                               QProgressBar, QDial, QDialogButtonBox, QWidget,
                               QComboBox, QLabel, QVBoxLayout, QHBoxLayout)
from PySide6.QtGui import QPalette, QColor


def slider2dB(pos):
    if pos == 0:
        label = "-∞"
    elif pos > 0 and pos <= 13:
        # -74B to -50dB (step size: 2)
        val = -74 + ((pos - 1) * 2)
        label = f"{val}"
    elif pos > 13 and pos <= 43:
        # -50dB to -20dB (step size: 1)
        val = -50 + (pos - 13)
        label = f"{val}"
    elif pos > 43 and pos <= 63:
        # -52dB to -10dB (step size: 0.5)
        val = -20 + ((pos - 43) * 0.5)
        label = f"{val}"
    else:
        # -10dB to 6dB (step size: 0.25)
        val = -10 + ((pos - 63) * 0.25)
        label = f"{val}"

    return label


class Send(QWidget):
    @Slot()
    def dial(self, pos):
        label = slider2dB(pos)

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


class Channel(QWidget):
    def __init__(self, channel_no):
        super().__init__()

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

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

        self.setLayout(vlayout)


class Fader(QWidget):
    @Slot()
    def slide(self, pos):
        label = slider2dB(pos)

        self.val_label.setText(label)


    def __init__(self, channel_no):
        super().__init__()

        layout = QVBoxLayout()

        slider = QSlider()
        slider.setRange(0, 127)

        self.val_label = QLabel("-∞")
        name_label = QLabel(f"Input {channel_no}")

        layout.addWidget(slider)
        layout.addWidget(self.val_label)
        layout.addWidget(name_label)

        layout.setAlignment(slider, Qt.AlignCenter)
        layout.setAlignment(self.val_label, Qt.AlignCenter)
        layout.setAlignment(name_label, Qt.AlignCenter)

        self.setLayout(layout)

        slider.valueChanged.connect(self.slide)

class Dialog(QDialog):
    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout()
        main_layout.addWidget(Channel(1))
        main_layout.addWidget(Channel(2))
        main_layout.addWidget(Channel(3))
        main_layout.addWidget(Channel(4))
        main_layout.addWidget(Channel(5))
        main_layout.addWidget(Channel(6))

        self._main_layout = main_layout
        self.setLayout(self._main_layout)

        self.setWindowTitle("Dynamic Layouts")


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

    app = QApplication(sys.argv)
    enable_dark_mode(app)

    dialog = Dialog()
    dialog.exec()