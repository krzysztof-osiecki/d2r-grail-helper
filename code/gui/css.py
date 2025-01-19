# i dont know how to make it properly at the moment, so just put stylesheet away so i dont see it

def get_application_stylesheet():
    return """
            QWidget {
                background-color: #2E2E2E;  /* Dark grey background */
                color: #F0F0F0;  /* Light greyish/white text */
                border-radius: 5px; 
            }
                           
            QTableWidget {
                background-color: #2E2E2E;  /* Dark background for table */
                color: #F0F0F0;              /* White text color */
                border: 1px solid #333;      /* Border around the table */
                gridline-color: #444;        /* Gridline color between cells */
                font-size: 14px;             /* Font size */
                font-family: Arial, sans-serif;  /* Font style */
                border-radius: 10px;          /* Rounded corners for the whole table */
                padding: 5px;
            }

            QTableWidget::item {
                background-color: #444444;  /* Background color for table items */
                color: #F0F0F0;              /* Text color */
                border: 1px solid #333;      /* Border around each cell */
                padding: 5px;                /* Padding inside cells */
                border-radius: 5px;          /* Rounded corners for cells */
            }

            QTableWidget::item:selected {
                background-color: #888888;  /* Background color for selected item */
                color: white;               /* Text color for selected item */
            }

            QHeaderView::section {
                background-color: #333333;  /* Background color for headers */
                color: #F0F0F0;              /* Text color for headers */
                padding: 10px;               /* Padding inside headers */
                font-weight: bold;           /* Make header text bold */
                border: 1px solid #444;      /* Border around headers */
            }

            QHeaderView::section:horizontal {
                border-bottom: 2px solid #444; /* Bottom border for horizontal headers */
            }

            QHeaderView::section:vertical {
                border-right: 2px solid #444;  /* Right border for vertical headers */
            }

            /* Modern Scrollbar Styles */
            QScrollBar:horizontal, QScrollBar:vertical {
                background-color: #2E2E2E; /* Background of scrollbar */
                border: none;              /* Remove border */
                height: 12px;              /* Height for horizontal scrollbar */
                width: 12px;               /* Width for vertical scrollbar */
                border-radius: 6px;        /* Rounded corners for scrollbar */
            }

            QScrollBar::handle:horizontal, QScrollBar::handle:vertical {
                background-color: #555555;  /* Handle color */
                border-radius: 6px;         /* Rounded handle */
            }

            QScrollBar::handle:horizontal:hover, QScrollBar::handle:vertical:hover {
                background-color: #888888;  /* Hover effect for the scrollbar handle */
            }

            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;               /* Remove arrows */
                background: none;
            }

            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal,
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;           /* Remove background of scroll area */
            }

            /* Style for the corner header (the one where row and column meet) */
            QTableCornerButton::section {
                background-color: #333333;  /* Same background as other headers */
                border: none;               /* No border */
                color: #F0F0F0;              /* White text */
            }
            
            QTableWidget {
                background-color: #2E2E2E;  /* Dark background for table */
                color: #F0F0F0;              /* White text color */
                border: 1px solid #333;      /* Border around the table */
                gridline-color: #444;        /* Gridline color between cells */
                font-size: 14px;             /* Font size */
                font-family: Arial, sans-serif;  /* Font style */
            }

            QTableWidget::item {
                background-color: #444444;  /* Background color for table items */
                color: #F0F0F0;              /* Text color */
                border: 1px solid #333;      /* Border around each cell */
                padding: 5px;                /* Padding inside cells */
                border-radius: 5px;          /* Rounded corners for cells */
            }

            QTableWidget::item:selected {
                background-color: #888888;  /* Background color for selected item */
                color: white;               /* Text color for selected item */
            }

            QHeaderView::section {
                background-color: #333333;  /* Background color for headers */
                color: #F0F0F0;              /* Text color for headers */
                padding: 10px;               /* Padding inside headers */
                font-weight: bold;           /* Make header text bold */
                border: 1px solid #444;      /* Border around headers */
            }

            QHeaderView::section:horizontal {
                border-bottom: 2px solid #444; /* Bottom border for horizontal headers */
            }

            QHeaderView::section:vertical {
                border-right: 2px solid #444;  /* Right border for vertical headers */
            }
                                       
            QTabWidget {
                background-color: #2E2E2E;  /* Dark grey background for the tab widget */
                border: 1px solid #333;     /* Border around the tab widget */
            }

            QTabBar::tab {
                background-color: #444444;  /* Default background for tabs */
                color: #F0F0F0;              /* Text color */
                padding: 10px;               /* Padding inside tabs */
                margin-right: 2px;           /* Space between tabs */
                border: 1px solid #333;      /* Border around each tab */
                border-radius: 5px;          /* Rounded corners for tabs */
            }

            QTabBar::tab:selected {
                background-color: #888888;  /* Selected tab background color */
                color: white;               /* Text color for selected tab */
                font-weight: bold;          /* Make selected tab text bold */
            }

            QTabBar::tab:hover {
                background-color: #555555;  /* Hover effect for tabs */
            }

            QTabWidget::pane {
                border: none;  /* Remove border around the tab content */
            }
        """