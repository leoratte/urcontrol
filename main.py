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

        vlayout.addWidget(QDial())
        vlayout.addLayout(hlayout)
        vlayout.addWidget(Fader(channel_no))


        self.setLayout(vlayout)

        # TODO: add mute
        # TODO: add solo
        # TODO: add send


class Fader(QWidget):
    def __init__(self, channel_no):
        super().__init__()

        layout = QVBoxLayout()

        slider = QSlider()
        slider.setRange(0, 127)

        val_label = QLabel("-∞")
        name_label = QLabel(f"Input {channel_no}")

        layout.addWidget(slider)
        layout.addWidget(val_label)
        layout.addWidget(name_label)

        layout.setAlignment(slider, Qt.AlignCenter)
        layout.setAlignment(val_label, Qt.AlignCenter)
        layout.setAlignment(name_label, Qt.AlignCenter)
        
        self.setLayout(layout)

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

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.exec()