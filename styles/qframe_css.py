"""
Styles for QFrame elements
"""

add_new_key_style = """
    QFrame#AddFrame {background:#eaeaea;}
    QPushButton#close {border:none;}
    QLineEdit#field {border-radius:20px;background:#fff;border:1px solid #b7b7b7;padding:0 30px;font:13px Arial;
    color:#808080;}
    QPushButton#save {font: 14px Arial;color:#fff;background:#4797ce;border:none;}
    QComboBox {font: 15px Arial;color:#808080;padding-left:10px;border: 1px solid #b7b7b7;background:#fff;height:28px;}
    QComboBox::drop-down {subcontrol-origin:padding;subcontrol-position: top right;width:20px;
    border-top-right-radius:3px;border-bottom-right-radius:3px;}
    QComboBox::down-arrow {image: url(:/down);padding-right:8px;}
    QComboBox QAbstractItemView {background:#fff;padding:7px 5px 7px 5px;font:15px Arial;color:#808080;}
    QComboBox QAbstractItemView::item {padding:4px;}
    QRadioButton#child-element {font:bold 10px Arial;color:#646464;padding:2px 6px 3px 0;}
    QRadioButton#child-element::checked {background:#4797ce;border-radius:10px;color:#fff;}
    QRadioButton#child-element::indicator {width:0;}
"""
