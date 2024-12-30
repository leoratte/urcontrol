# Copyright (C) 2013 Riverbank Computing Limited.
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

"""PySide6 port of the widgets/layouts/dynamiclayouts example from Qt v5.x"""

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (QApplication, QDialog, QLayout, QGridLayout,
                               QMessageBox, QGroupBox, QSpinBox, QSlider, QPushButton,
                               QProgressBar, QDial, QDialogButtonBox, QWidget,
                               QComboBox, QLabel, QVBoxLayout, QHBoxLayout)


class Channel(QWidget):
    def __init__(self):
        super().__init__()

        hlayout = QHBoxLayout()

        mbutton = QPushButton("M")
        sbutton = QPushButton("S")

        mbutton.setFixedWidth(20)
        sbutton.setFixedWidth(20)

        hlayout.addWidget(mbutton)
        hlayout.addWidget(sbutton)

        self.setLayout(hlayout)

        # TODO: add mute
        # TODO: add solo
        # TODO: add send


class Fader(QWidget):
    def __init__(self, channel):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(Channel())
        layout.addWidget(QSlider())
        layout.addWidget(QLabel("-∞"))
        layout.addWidget(QLabel(f"Input {channel}"))

        self.setLayout(layout)

class Dialog(QDialog):
    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout()
        main_layout.addWidget(Fader(1))
        main_layout.addWidget(Fader(2))
        main_layout.addWidget(Fader(3))
        main_layout.addWidget(Fader(4))
        main_layout.addWidget(Fader(5))
        main_layout.addWidget(Fader(6))

        self._main_layout = main_layout
        self.setLayout(self._main_layout)

        self.setWindowTitle("Dynamic Layouts")

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.exec()