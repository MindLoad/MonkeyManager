"""
Styles for Qwidget elements
"""

root_style = """
    QWidget#bar_top {background:#fff;border-bottom:1px solid #c6c6c6;}
    QLabel#logo {background:#4797ce;border-bottom:1px solid #00365c;}
    QWidget#bar_menu {background:#00365c;}
    QWidget#bar_key {background:#eaeaea;}
    QLineEdit#pass_input {border:none;font:bold 12px Arial;color:#636363;border-left:1px solid #c6c6c6;
    border-bottom:1px solid #c6c6c6;padding:0 30px;}
    QToolButton#add_new {font:bold 12px Arial;color:#6089a6;border:none;padding:0 30px;border-left:1px solid #c6c6c6;}
    QPushButton#menu_button {background:#00365c;color:#9bb0bf;border:none;font:bold 13px Arial;}
    QRadioButton#child-element {font:bold 10px Arial;color:#757575;padding:2px 8px 2px 4px;}
    QRadioButton#child-element::checked {background:#4797ce;border-radius:10px;color:#fff;}
    QRadioButton#child-element::indicator {width:0;}
    QToolButton#refresh {border:none;}
    QTableWidget {border: 1px solid #c6c6c6; font:bold 11px Arial; color: #8e8e8e;}
    QHeaderView::section {border-top: 0px solid #8a8a8a; border-left: 0px solid #8a8a8a;
        border-right: 0px solid #d9d9d9; border-bottom: 1px solid #ccc; font: bold 12px Arial; background:#fff;
        height:45px; color:#325d7c;padding-left:20px;}
    QHeaderView::up-arrow {image: url(:/header-up);width:18px;height:18px;}
    QHeaderView::down-arrow {image: url(:/header-down);width:18px;height:18px;}
    QTableView::item {border-bottom: 1px solid #ccc;padding-left:20px;}
    QTableView::item:selected {background:#f2faff; color:#578dc9;}
    QScrollBar:horizontal {border: none; background: #a5c8ed; height: 3px;}
    QScrollBar::handle:horizontal {max-width: 0; background: #4797ce;}
    QScrollBar:vertical {border: none; background: #a5c8ed; width: 4px;}
    QScrollBar::handle:vertical {max-height: 0; background: #4797ce;}
    QLabel#search_result {font:12px Arial;color:#646464;}
"""

search_field_style = """
    border-radius:23px; background:#fff; border:1px solid #c6c6c6; padding:0 30px;font:13px Arial;color:#636363;
    background-image: url(:/search); background-repeat: no-repeat; background-position: left;
"""
