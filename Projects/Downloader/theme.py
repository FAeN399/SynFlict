"""
Theme definition for the Reddit Media Downloader GUI.
Defines colors, styles and common UI elements.
"""

# Main color scheme - using darker purple as requested
PRIMARY_COLOR = "#7B1FA2"  # Darker Purple
SECONDARY_COLOR = "#FFB300"  # Slightly darker Yellow
BACKGROUND_COLOR = "#F5F5F5"  # Light gray background
SURFACE_COLOR = "#FFFFFF"  # White for cards and surfaces
TEXT_PRIMARY_COLOR = "#212121"  # Dark text
TEXT_SECONDARY_COLOR = "#757575"  # Secondary text
BORDER_DIVIDER_COLOR = "#BDBDBD"  # Dividers
ERROR_COLOR = "#F44336"  # Error red
SUCCESS_COLOR = "#4CAF50"  # Success green
WARNING_COLOR = "#FF9800"  # Warning orange

# Dark theme
DARK_BACKGROUND_COLOR = "#121212"
DARK_SURFACE_COLOR = "#1E1E1E"
DARK_TEXT_PRIMARY_COLOR = "#FFFFFF"
DARK_TEXT_SECONDARY_COLOR = "#B0B0B0"
DARK_BORDER_DIVIDER_COLOR = "#333333"

# Typography
FONT_FAMILY = "Inter, 'Segoe UI', Roboto, Arial, sans-serif"
FONT_SIZE_SMALL = 9
FONT_SIZE_NORMAL = 10
FONT_SIZE_LARGE = 12
FONT_SIZE_XLARGE = 14

# Spacing
SPACING_TINY = 4
SPACING_SMALL = 8
SPACING_MEDIUM = 12
SPACING_LARGE = 16
SPACING_XLARGE = 24

# Border radius
BORDER_RADIUS_SMALL = 4
BORDER_RADIUS_MEDIUM = 6
BORDER_RADIUS_LARGE = 8

# Icon paths
ICON_PATH = "icons/"

# Style sheets
def get_style_sheet(dark_mode=False):
    """Get the appropriate stylesheet based on theme."""
    # Determine colors based on theme
    if dark_mode:
        bg = DARK_BACKGROUND_COLOR
        surface = DARK_SURFACE_COLOR
        text_primary = DARK_TEXT_PRIMARY_COLOR
        text_secondary = DARK_TEXT_SECONDARY_COLOR
        border = DARK_BORDER_DIVIDER_COLOR
        button_bg = SECONDARY_COLOR
        button_text = DARK_BACKGROUND_COLOR
        button_hover_bg = "#E6A100" # Darker yellow
        input_bg = DARK_SURFACE_COLOR
        input_border = DARK_BORDER_DIVIDER_COLOR
    else:
        bg = BACKGROUND_COLOR
        surface = SURFACE_COLOR
        text_primary = TEXT_PRIMARY_COLOR
        text_secondary = TEXT_SECONDARY_COLOR
        border = BORDER_DIVIDER_COLOR
        button_bg = PRIMARY_COLOR
        button_text = "#FFFFFF"
        button_hover_bg = "#6A1B9A" # Darker purple
        input_bg = SURFACE_COLOR
        input_border = BORDER_DIVIDER_COLOR
        
    return f"""
    /* Global Styles */
    QWidget {{
        background-color: {bg};
        color: {text_primary};
        font-family: {FONT_FAMILY};
        font-size: {FONT_SIZE_NORMAL}pt;
    }}
    
    QMainWindow, QDialog {{
        background-color: {bg};
    }}
    
    /* Form Controls */
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
        background-color: {input_bg};
        color: {text_primary};
        border: 1px solid {input_border};
        border-radius: {BORDER_RADIUS_SMALL}px;
        padding: {SPACING_SMALL}px;
        selection-background-color: {button_bg};
    }}
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
        border: 2px solid {button_bg};
    }}
    
    /* Buttons */
    QPushButton {{
        background-color: {button_bg};
        color: {button_text};
        border: none;
        border-radius: {BORDER_RADIUS_MEDIUM}px;
        padding: {SPACING_SMALL}px {SPACING_MEDIUM}px;
        font-weight: bold;
        min-height: 28px;
    }}
    
    QPushButton:hover {{
        background-color: {button_hover_bg};
    }}
    
    QPushButton:pressed {{
        background-color: {button_bg};
        padding-top: {SPACING_SMALL+1}px;
    }}
    
    QPushButton:disabled {{
        background-color: {text_secondary};
        color: {bg};
    }}
    
    /* Secondary Button Style */
    QPushButton[flat="true"] {{
        background-color: transparent;
        color: {button_bg};
        border: 1px solid {button_bg};
    }}
    
    QPushButton[flat="true"]:hover {{
        background-color: rgba(123, 31, 162, 0.1);
    }}
    
    /* Progress Bars */
    QProgressBar {{
        border: 1px solid {border};
        border-radius: {BORDER_RADIUS_SMALL}px;
        background-color: {surface};
        color: {text_primary};
        text-align: center;
    }}
    
    QProgressBar::chunk {{
        background-color: {button_bg};
        border-radius: {BORDER_RADIUS_SMALL-1}px;
    }}
    
    /* Tabs */
    QTabWidget::pane {{
        border: 1px solid {border};
        border-radius: {BORDER_RADIUS_SMALL}px;
        top: -1px;
    }}
    
    QTabBar::tab {{
        background-color: {surface};
        color: {text_primary};
        border: 1px solid {border};
        border-bottom: none;
        border-top-left-radius: {BORDER_RADIUS_SMALL}px;
        border-top-right-radius: {BORDER_RADIUS_SMALL}px;
        padding: {SPACING_SMALL}px {SPACING_MEDIUM}px;
        margin-right: 2px;
    }}
    
    QTabBar::tab:selected {{
        background-color: {button_bg};
        color: {button_text};
    }}
    
    QTabBar::tab:hover:!selected {{
        background-color: rgba(123, 31, 162, 0.1);
    }}
    
    /* Group Boxes */
    QGroupBox {{
        border: 1px solid {border};
        border-radius: {BORDER_RADIUS_MEDIUM}px;
        margin-top: 1.5ex;
        font-weight: bold;
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: {SPACING_MEDIUM}px;
        padding: 0 {SPACING_SMALL}px;
        color: {text_primary};
    }}
    
    /* List & Table Widgets */
    QListWidget, QTableWidget, QTreeWidget {{
        background-color: {surface};
        border: 1px solid {border};
        border-radius: {BORDER_RADIUS_SMALL}px;
        alternate-background-color: rgba(123, 31, 162, 0.05);
    }}
    
    QListWidget::item, QTableWidget::item, QTreeWidget::item {{
        padding: {SPACING_SMALL}px;
    }}
    
    QListWidget::item:selected, QTableWidget::item:selected, QTreeWidget::item:selected {{
        background-color: {button_bg};
        color: {button_text};
    }}
    
    QHeaderView::section {{
        background-color: {button_bg};
        color: {button_text};
        padding: {SPACING_SMALL}px;
        border: none;
    }}
    
    /* Scroll Bars */
    QScrollBar:vertical {{
        border: none;
        background-color: {surface};
        width: 12px;
        margin: 12px 0 12px 0;
        border-radius: {BORDER_RADIUS_SMALL}px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {button_bg};
        min-height: 30px;
        border-radius: {BORDER_RADIUS_SMALL}px;
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        border: none;
        background: none;
        height: 12px;
    }}
    
    QScrollBar:horizontal {{
        border: none;
        background-color: {surface};
        height: 12px;
        margin: 0 12px 0 12px;
        border-radius: {BORDER_RADIUS_SMALL}px;
    }}
    
    QScrollBar::handle:horizontal {{
        background-color: {button_bg};
        min-width: 30px;
        border-radius: {BORDER_RADIUS_SMALL}px;
    }}
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        border: none;
        background: none;
        width: 12px;
    }}
    
    /* Check Boxes */
    QCheckBox {{
        spacing: {SPACING_SMALL}px;
    }}
    
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 1px solid {border};
        border-radius: {BORDER_RADIUS_SMALL}px;
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {button_bg};
        border: 1px solid {button_bg};
    }}
    
    /* Radio Buttons */
    QRadioButton {{
        spacing: {SPACING_SMALL}px;
    }}
    
    QRadioButton::indicator {{
        width: 18px;
        height: 18px;
        border: 1px solid {border};
        border-radius: 9px;
    }}
    
    QRadioButton::indicator:checked {{
        background-color: {button_bg};
        border: 1px solid {button_bg};
    }}
    
    /* Status Bar */
    QStatusBar {{
        background-color: {surface};
        color: {text_primary};
        border-top: 1px solid {border};
    }}
    
    /* Tool Tip */
    QToolTip {{
        background-color: {button_bg};
        color: {button_text};
        border: none;
        border-radius: {BORDER_RADIUS_SMALL}px;
        padding: {SPACING_SMALL}px;
    }}
    
    /* Custom Widget Styles */
    #headerLabel {{
        font-size: {FONT_SIZE_LARGE}pt;
        font-weight: bold;
        color: {button_bg};
    }}
    
    #subHeaderLabel {{
        font-size: {FONT_SIZE_NORMAL}pt;
        color: {text_secondary};
    }}
    
    #cardWidget {{
        background-color: {surface};
        border: 1px solid {border};
        border-radius: {BORDER_RADIUS_MEDIUM}px;
    }}
    
    #searchButton, #downloadButton {{
        min-width: 120px;
        min-height: 32px;
    }}
    
    #warningLabel {{
        color: {WARNING_COLOR};
        font-weight: bold;
    }}
    
    #errorLabel {{
        color: {ERROR_COLOR};
        font-weight: bold;
    }}
    
    #successLabel {{
        color: {SUCCESS_COLOR};
        font-weight: bold;
    }}
    """

# Helper functions for creating styled widgets
def style_button(button, primary=True, icon_path=None):
    """Apply styling to a button."""
    if primary:
        button.setObjectName("primaryButton")
    else:
        button.setFlat(True)
    
    if icon_path:
        button.setIcon(QIcon(icon_path))
    
    return button

def style_header_label(label):
    """Style a label as a section header."""
    label.setObjectName("headerLabel")
    return label

def style_warning_label(label):
    """Style a label as a warning text."""
    label.setObjectName("warningLabel")
    return label

def style_success_label(label):
    """Style a label as a success text."""
    label.setObjectName("successLabel")
    return label

def style_error_label(label):
    """Style a label as an error text."""
    label.setObjectName("errorLabel")
    return label

def style_card(widget):
    """Style a widget as a card."""
    widget.setObjectName("cardWidget")
    return widget
