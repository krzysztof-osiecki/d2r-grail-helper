# i dont know how to make it properly at the moment, so just put stylesheet away so i dont see it
# it is currenty maintained by chatgpt ;)

def get_application_stylesheet():
    base_color = "#2E2E2E"
    text_color = "#F0F0F0"
    border_color = "#333333"
    hover_color = "#555555"
    active_color = "#666666"
    highlight_color = "#888888"
    selected_color = "#66afe9"
    font_size = "16px"
    border_radius = "5px"
    padding = "5px"

    return f"""
        /* Global Styles */
        QWidget {{
            background-color: {base_color};
            color: {text_color};
            font-size: {font_size};
        }}

        /* QLineEdit Styles */
        QLineEdit {{
            color: white;
            border: 1px solid {border_color};
            border-radius: {border_radius};
            padding: {padding} 10px;
            font-size: {font_size};
        }}
        QLineEdit:hover {{
            background-color: {hover_color};
            border-color: {active_color};
        }}
        QLineEdit:focus {{
            border: 1px solid {selected_color};
            background-color: {active_color};
        }}

        /* QPushButton Styles */
        QPushButton {{
            background-color: {hover_color};
            color: white;
            border: 1px solid {border_color};
            border-radius: {border_radius};
            padding: 10px 20px;
            font-size: {font_size};
        }}
        QPushButton:hover {{
            background-color: {active_color};
            border-color: {highlight_color};
        }}
        QPushButton:pressed {{
            background-color: {border_color};
            border-color: {hover_color};
        }}

        /* QTableWidget Styles */
        QTableWidget {{
            background-color: {base_color};
            color: {text_color};
            border: 1px solid {border_color};
            gridline-color: {hover_color};
            font-size: 14px;
            font-family: Arial, sans-serif;
            border-radius: {border_radius};
            padding: {padding};
        }}
        QTableWidget::item {{
            background-color: {hover_color};
            color: {text_color};
            border: 1px solid {border_color};
            padding: {padding};
            border-radius: {border_radius};
        }}
        QTableWidget::item:selected {{
            background-color: {highlight_color};
            color: white;
        }}

        /* QHeaderView Styles */
        QHeaderView::section {{
            background-color: {border_color};
            color: {text_color};
            padding: 10px;
            font-weight: bold;
            border: 1px solid {hover_color};
        }}
        QHeaderView::section:horizontal {{
            border-bottom: 2px solid {hover_color};
        }}
        QHeaderView::section:vertical {{
            border-right: 2px solid {hover_color};
        }}

        /* QScrollBar Styles */
        QScrollBar:horizontal, QScrollBar:vertical {{
            background-color: {base_color};
            border: none;
            height: 12px;
            width: 12px;
            border-radius: 6px;
        }}
        QScrollBar::handle:horizontal, QScrollBar::handle:vertical {{
            background-color: {hover_color};
            border-radius: 6px;
        }}
        QScrollBar::handle:horizontal:hover, QScrollBar::handle:vertical:hover {{
            background-color: {highlight_color};
        }}
        QScrollBar::add-line, QScrollBar::sub-line,
        QScrollBar::add-page, QScrollBar::sub-page {{
            background: none;
            border: none;
        }}

        /* QTabWidget Styles */
        QTabWidget {{
            background-color: {base_color};
            border: 1px solid {border_color};
        }}
        QTabBar::tab {{
            background-color: {hover_color};
            color: {text_color};
            padding: 10px;
            margin-right: 2px;
            border: 1px solid {border_color};
            border-radius: {border_radius};
        }}
        QTabBar::tab:selected {{
            background-color: {highlight_color};
            color: white;
            font-weight: bold;
        }}
        QTabBar::tab:hover {{
            background-color: {active_color};
        }}
        QTabWidget::pane {{
            border: none;
        }}

        /* QTableCornerButton Styles */
        QTableCornerButton::section {{
            background-color: {border_color};
            color: {text_color};
            border: none;
        }}
    """
