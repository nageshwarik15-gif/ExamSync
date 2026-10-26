
import streamlit as st
import pandas as pd
from datetime import date, timedelta

import database as db
from scheduler import generate_timetable

# Page configuration
st.set_page_config(
    page_title="ExamSync",
    page_icon="📚",
    layout="wide"
)

# ---------------- PROFESSIONAL DASHBOARD STYLING ----------------

st.markdown("""
<style>
    .stApp {
        background-color: #f4f7fb;
    }

    [data-testid="stSidebar"] {
        background-color: #14213d;
    }

    [data-testid="stSidebar"] {
        background-color: #14213d !important;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #ffffff !important;
    }

    [data-testid="stBaseButton-secondary"],
    [data-testid="stDownloadButton"] button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
    }

    [data-testid="stBaseButton-secondary"] *,
    [data-testid="stDownloadButton"] button * {
        color: #ffffff !important;
    }

    [data-testid="stDataFrame"] {
        background-color: #ffffff !important;
        border: 1px solid #dbe3ef !important;
        border-radius: 10px !important;
    }

    [data-testid="stDataFrame"] iframe {
        background-color: #ffffff !important;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3,
    [data-testid="stHeader"],
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {
        color: #14213d !important;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #f4f7fb;
    }

    [data-testid="stDataFrame"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        overflow: hidden;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: #14213d !important;
    }

    [data-testid="stMarkdownContainer"] p {
        color: #334155;
    }

    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.06);
    }

    [data-testid="stDataFrame"] {
        background-color: #ffffff;
        border-radius: 10px;
    }

    div.stButton > button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.55rem 1rem;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background-color: #1d4ed8;
        color: white;
        border: none;
    }

    hr {
        border-color: #dbe3ef;
    }

    /* Improve form inputs and dropdowns */
    [data-testid="stSelectbox"] label,
    [data-testid="stTextInput"] label,
    [data-testid="stNumberInput"] label {
        color: #14213d !important;
        font-weight: 600 !important;
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #14213d !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] * {
        color: #14213d !important;
    }

    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input {
        background-color: #ffffff !important;
        color: #14213d !important;
    }

    /* Make form and download buttons readable */
    [data-testid="stFormSubmitButton"] button,
    [data-testid="stDownloadButton"] button,
    div.stButton > button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 9px !important;
        font-weight: 600 !important;
        padding: 0.6rem 1rem !important;
    }

    [data-testid="stFormSubmitButton"] button *,
    [data-testid="stDownloadButton"] button *,
    div.stButton > button * {
        color: #ffffff !important;
    }

    [data-testid="stFormSubmitButton"] button:hover,
    [data-testid="stDownloadButton"] button:hover,
    div.stButton > button:hover {
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
    }


    /* Improve table readability and spacing */
    [data-testid="stDataFrame"] {
        background-color: #ffffff !important;
        border: 1px solid #dbe3ef !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    [data-testid="stDataFrame"] canvas {
        border-radius: 10px;
    }

    /* Make table containers consistent */
    [data-testid="stTable"] {
        background-color: #ffffff !important;
        color: #14213d !important;
        border-radius: 10px !important;
    }

    [data-testid="stTable"] th {
        background-color: #e8eef7 !important;
        color: #14213d !important;
        text-align: left !important;
    }

    [data-testid="stTable"] td {
        background-color: #ffffff !important;
        color: #334155 !important;
    }


    /* Make charts match the light dashboard */
    [data-testid="stVegaLiteChart"],
    [data-testid="stArrowVegaLiteChart"],
    [data-testid="stVegaLiteChart"] > div {
        background-color: #ffffff !important;
        border-radius: 12px !important;
    }

    [data-testid="stVegaLiteChart"] canvas,
    [data-testid="stVegaLiteChart"] svg {
        background-color: #ffffff !important;
    }

    /* Improve metric cards */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1px solid #dbe3ef !important;
        border-radius: 14px !important;
        padding: 20px !important;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.06);
    }


    /* Light theme: dropdowns, date inputs and time-slot controls */
    [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    [data-testid="stMultiSelect"] [data-baseweb="select"] > div,
    [data-testid="stDateInput"] input,
    [data-testid="stTimeInput"] input,
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input {
        background-color: #ffffff !important;
        color: #14213d !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }

    [data-testid="stSelectbox"] [data-baseweb="select"] *,
    [data-testid="stMultiSelect"] [data-baseweb="select"] *,
    [data-testid="stDateInput"] input,
    [data-testid="stDateInput"] button,
    [data-testid="stTimeInput"] input {
        color: #14213d !important;
    }

    [data-testid="stMultiSelect"] [data-baseweb="tag"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
    }

    [data-baseweb="popover"],
    [data-baseweb="menu"],
    [role="listbox"] {
        background-color: #ffffff !important;
        color: #14213d !important;
    }


    /* FIX: Streamlit dropdowns and their option menus */
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background: #ffffff !important;
        color: #14213d !important;
        border: 1px solid #cbd5e1 !important;
    }

    [data-testid="stSelectbox"] [data-baseweb="select"] input {
        color: #14213d !important;
        -webkit-text-fill-color: #14213d !important;
    }

    [data-baseweb="popover"] [role="listbox"],
    [data-baseweb="popover"] ul,
    [data-baseweb="menu"] {
        background-color: #ffffff !important;
    }

    [data-baseweb="popover"] [role="option"],
    [data-baseweb="popover"] li,
    [data-baseweb="menu"] li {
        background-color: #ffffff !important;
        color: #14213d !important;
    }

    [data-baseweb="popover"] [role="option"] *,
    [data-baseweb="popover"] li *,
    [data-baseweb="menu"] li * {
        color: #14213d !important;
        -webkit-text-fill-color: #14213d !important;
    }

    [data-baseweb="popover"] [role="option"]:hover,
    [data-baseweb="popover"] li:hover {
        background-color: #e8eef7 !important;
        color: #14213d !important;
    }

    /* FIX: Date and time input fields */
    [data-testid="stDateInput"] input,
    [data-testid="stTimeInput"] input {
        background-color: #ffffff !important;
        color: #14213d !important;
        -webkit-text-fill-color: #14213d !important;
        border: 1px solid #cbd5e1 !important;
    }


    /* Strong light styling for Streamlit Base Web select controls */
    [data-testid="stSelectbox"] [data-baseweb="select"] > div,
    [data-testid="stMultiSelect"] [data-baseweb="select"] > div {
        background: #ffffff !important;
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        color: #14213d !important;
        box-shadow: none !important;
    }

    [data-testid="stSelectbox"] [data-baseweb="select"] *,
    [data-testid="stMultiSelect"] [data-baseweb="select"] * {
        color: #14213d !important;
        -webkit-text-fill-color: #14213d !important;
    }

    /* Dropdown popup and option text */
    [data-baseweb="popover"] > div,
    [data-baseweb="popover"] [data-baseweb="menu"],
    [data-baseweb="popover"] [role="listbox"],
    [data-baseweb="popover"] ul {
        background: #ffffff !important;
        background-color: #ffffff !important;
    }

    [data-baseweb="popover"] [role="option"],
    [data-baseweb="popover"] [role="option"] *,
    [data-baseweb="popover"] li,
    [data-baseweb="popover"] li * {
        background-color: #ffffff !important;
        color: #14213d !important;
        -webkit-text-fill-color: #14213d !important;
        opacity: 1 !important;
    }

    [data-baseweb="popover"] [role="option"]:hover,
    [data-baseweb="popover"] [role="option"]:hover * {
        background-color: #e8eef7 !important;
        color: #14213d !important;
        -webkit-text-fill-color: #14213d !important;
    }

    /* Date fields */
    [data-testid="stDateInput"] input {
        background: #ffffff !important;
        color: #14213d !important;
        -webkit-text-fill-color: #14213d !important;
        border: 1px solid #cbd5e1 !important;
    }


/* Fix dropdown menu: white background with readable dark text */
div[data-baseweb="popover"],
div[data-baseweb="popover"] *,
ul[role="listbox"],
ul[role="listbox"] *,
li[role="option"],
li[role="option"] * {
    background-color: #ffffff !important;
    color: #14213d !important;
    -webkit-text-fill-color: #14213d !important;
    opacity: 1 !important;
}

li[role="option"]:hover {
    background-color: #e8efff !important;
    color: #14213d !important;
    -webkit-text-fill-color: #14213d !important;
}


/* Fix React Aria dropdown option readability */
.react-aria-ListBox,
.react-aria-ListBoxItem,
.react-aria-Popover,
.react-aria-ListBoxItem *,
[role="listbox"],
[role="option"],
[role="option"] * {
    color: #14213d !important;
    -webkit-text-fill-color: #14213d !important;
}

.react-aria-ListBox,
.react-aria-Popover,
[role="listbox"],
[role="option"] {
    background-color: #ffffff !important;
}

.react-aria-ListBoxItem:hover,
[role="option"]:hover {
    background-color: #e8eef7 !important;
    color: #14213d !important;
    -webkit-text-fill-color: #14213d !important;
}

/* ExamSync: White dropdown controls with black text */
.react-aria-ComboBox [role="group"] {
    background-color: #ffffff !important;
    color: #000000 !important;
    border: 1px solid #cbd5e1 !important;
}

.react-aria-ComboBox input {
    background-color: transparent !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

.react-aria-ComboBox button {
    background-color: #ffffff !important;
    color: #000000 !important;
}

.react-aria-ComboBox button svg {
    color: #000000 !important;
    fill: #000000 !important;
}

.react-aria-ComboBox [role="option"],
.react-aria-ComboBox [role="option"] *,
.react-aria-ListBox,
.react-aria-ListBoxItem,
[role="listbox"],
[role="option"] {
    background-color: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

.react-aria-ComboBox [role="option"]:hover,
.react-aria-ListBoxItem:hover,
[role="option"]:hover {
    background-color: #e8eef7 !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

/* ExamSync: Light date and time input styling */
[data-testid="stDateInput"] input,
[data-testid="stTimeInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background-color: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    border-color: #cbd5e1 !important;
    color-scheme: light !important;
}

[data-testid="stDateInput"] [data-baseweb="input"] > div,
[data-testid="stTimeInput"] [data-baseweb="input"] > div,
[data-testid="stTextInput"] [data-baseweb="input"] > div,
[data-testid="stNumberInput"] [data-baseweb="input"] > div {
    background-color: #ffffff !important;
    color: #000000 !important;
    border-color: #cbd5e1 !important;
}

[data-testid="stDateInput"] button,
[data-testid="stTimeInput"] button {
    background-color: #ffffff !important;
    color: #000000 !important;
}

[data-testid="stDateInput"] button svg,
[data-testid="stTimeInput"] button svg {
    color: #000000 !important;
    fill: #000000 !important;
}

[data-testid="stDateInput"] label,
[data-testid="stTimeInput"] label,
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label {
    color: #14213d !important;
}

/* ExamSync: Force date fields to white with black text */
[data-testid="stDateInput"],
[data-testid="stDateInput"] > div,
[data-testid="stDateInput"] div,
[data-testid="stDateInput"] [data-baseweb="input"],
[data-testid="stDateInput"] [data-baseweb="input"] > div {
    background-color: #ffffff !important;
    color: #000000 !important;
    border-color: #cbd5e1 !important;
}

[data-testid="stDateInput"] input {
    background-color: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    color-scheme: light !important;
}

[data-testid="stDateInput"] button {
    background-color: #ffffff !important;
    color: #000000 !important;
}

[data-testid="stDateInput"] button svg {
    color: #000000 !important;
    fill: #000000 !important;
}

[data-testid="stDateInput"] label {
    color: #14213d !important;
}

/* ExamSync: Fix React Aria date picker text and calendar */
[data-testid="stDateInput"] .react-aria-DateSegment,
[data-testid="stDateInput"] .react-aria-DateSegment *,
[data-testid="stDateInput"] [data-rac] {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

.react-aria-Popover,
.react-aria-Popover .react-aria-Calendar,
.react-aria-Calendar,
.react-aria-CalendarGrid,
.react-aria-CalendarHeader {
    background-color: #ffffff !important;
    color: #000000 !important;
}

.react-aria-Calendar button,
.react-aria-Calendar button *,
.react-aria-CalendarGrid button,
.react-aria-CalendarGrid button * {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

.react-aria-Calendar button:hover,
.react-aria-CalendarGrid button:hover {
    background-color: #e8eef7 !important;
}


/* ExamSync: Professional blue time-slot chips */
[data-testid="stMultiSelect"] [data-baseweb="tag"],
[data-baseweb="tag"] {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border: 1px solid #2563EB !important;
    border-radius: 8px !important;
}

[data-testid="stMultiSelect"] [data-baseweb="tag"] *,
[data-baseweb="tag"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

[data-testid="stMultiSelect"] [data-baseweb="tag"] svg,
[data-baseweb="tag"] svg {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}

[data-testid="stMultiSelect"] [data-baseweb="tag"] button,
[data-baseweb="tag"] button {
    background-color: transparent !important;
    border: none !important;
}


/* ExamSync: Professional blue time-slot chips */
[data-testid="stMultiSelect"] [data-baseweb="tag"],
[data-baseweb="tag"] {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border: 1px solid #2563EB !important;
    border-radius: 8px !important;
}

[data-testid="stMultiSelect"] [data-baseweb="tag"] *,
[data-baseweb="tag"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

[data-testid="stMultiSelect"] [data-baseweb="tag"] svg,
[data-baseweb="tag"] svg {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}

[data-testid="stMultiSelect"] [data-baseweb="tag"] button,
[data-baseweb="tag"] button {
    background-color: transparent !important;
    border: none !important;
}


/* ExamSync: Professional blue time-slot chips */
[data-testid="stMultiSelect"] [data-baseweb="tag"],
[data-baseweb="tag"] {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    border: 1px solid #2563EB !important;
    border-radius: 8px !important;
}

[data-testid="stMultiSelect"] [data-baseweb="tag"] *,
[data-baseweb="tag"] * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

[data-testid="stMultiSelect"] [data-baseweb="tag"] svg,
[data-baseweb="tag"] svg {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}

[data-testid="stMultiSelect"] [data-baseweb="tag"] button,
[data-baseweb="tag"] button {
    background-color: transparent !important;
    border: none !important;
}


    /* ExamSync: Royal blue examination time-slot chips */
    [data-testid="stMultiSelectTagsContainer"] [data-tag=""] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: 1px solid #1D4ED8 !important;
        border-radius: 8px !important;
    }

    [data-testid="stMultiSelectTagsContainer"] [data-tag=""] span {
        color: #FFFFFF !important;
    }

    [data-testid="stMultiSelectTagsContainer"] [data-tag=""] button {
        color: #FFFFFF !important;
    }


    /* ===== ExamSync: Light Blue Professional Theme ===== */

    /* Main application background */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background-color: #F4F8FE !important;
        color: #172B4D !important;
    }

    /* Top header */
    header[data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        border-bottom: 1px solid #E2EAF5 !important;
    }

    [data-testid="stToolbar"] {
        background-color: transparent !important;
    }

    /* Light blue navigation sidebar */
    section[data-testid="stSidebar"] {
        background-color: #EDF4FF !important;
        border-right: 1px solid #DCE8F8 !important;
    }

    section[data-testid="stSidebar"] > div {
        background-color: #EDF4FF !important;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] {
        color: #243B60 !important;
    }

    /* Navigation radio options */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        background-color: transparent !important;
        border-radius: 10px !important;
        padding: 8px 10px !important;
        transition: background-color 0.2s ease !important;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background-color: #DCEAFF !important;
    }

    /* Main headings */
    .stApp h1,
    .stApp h2,
    .stApp h3 {
        color: #142B52 !important;
    }

    /* Supporting text */
    .stApp [data-testid="stCaptionContainer"] {
        color: #647895 !important;
    }

    /* Dashboard metric cards */
    [data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E0EAF7 !important;
        border-radius: 16px !important;
        padding: 20px !important;
        box-shadow: 0 4px 16px rgba(31, 73, 125, 0.07) !important;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] p {
        color: #536987 !important;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] div {
        color: #173565 !important;
    }

    /* Forms, tables and containers */
    [data-testid="stForm"],
    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        border-color: #DFE9F6 !important;
        border-radius: 12px !important;
    }

    /* Input fields and dropdowns */
    .stApp input,
    .stApp textarea {
        background-color: #FFFFFF !important;
        color: #172B4D !important;
        border-color: #CCD9EC !important;
    }

    /* Buttons */
    .stApp button[kind="primary"],
    .stApp button[data-testid="stBaseButton-primary"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 9px !important;
    }

    .stApp button[kind="primary"]:hover,
    .stApp button[data-testid="stBaseButton-primary"]:hover {
        background-color: #1D4ED8 !important;
    }

    /* Preserve royal blue examination time-slot chips */
    [data-testid="stMultiSelectTagsContainer"] [data-tag=""] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: 1px solid #1D4ED8 !important;
        border-radius: 9px !important;
    }

    [data-testid="stMultiSelectTagsContainer"] [data-tag=""] span,
    [data-testid="stMultiSelectTagsContainer"] [data-tag=""] button {
        color: #FFFFFF !important;
    }

    /* Subtle section separators */
    .stApp hr {
        border-color: #DFE9F6 !important;
    }


    /* ===== Refined ExamSync Navigation ===== */

    /* Remove the default radio circles */
    section[data-testid="stSidebar"] [data-testid="stRadio"] input {
        accent-color: #2563EB !important;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child {
        display: none !important;
    }

    /* Make navigation options clean and readable */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        background-color: transparent !important;
        border-radius: 10px !important;
        padding: 10px 12px !important;
        margin-bottom: 4px !important;
        color: #243B60 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label p,
    section[data-testid="stSidebar"] [data-testid="stRadio"] label span {
        color: #243B60 !important;
    }

    /* Improve supporting text contrast */
    .stApp [data-testid="stCaptionContainer"],
    .stApp [data-testid="stCaptionContainer"] p {
        color: #647895 !important;
        opacity: 1 !important;
    }

    /* Refined dashboard card labels */
    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] p {
        color: #536987 !important;
        font-weight: 500 !important;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] div {
        color: #173565 !important;
    }


    /* ===== ExamSync Navigation: Exact Streamlit Selectors ===== */

    /* Each navigation item */
    section[data-testid="stSidebar"] [data-testid="stRadioOption"] {
        display: block !important;
        background: transparent !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 12px !important;
        margin: 4px 0 !important;
        cursor: pointer !important;
        transition: background-color 0.2s ease !important;
    }

    /* Remove the custom black radio indicator */
    section[data-testid="stSidebar"] [data-testid="stRadioOption"] > div > div:first-child {
        display: none !important;
    }

    /* Keep labels readable */
    section[data-testid="stSidebar"] [data-testid="stRadioOption"] p {
        color: #243B60 !important;
        font-weight: 500 !important;
        margin: 0 !important;
    }

    /* Hover highlight */
    section[data-testid="stSidebar"] [data-testid="stRadioOption"]:hover {
        background-color: #DCEAFF !important;
    }

    /* Selected navigation item */
    section[data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"] {
        background-color: #D6E7FF !important;
        border-left: 4px solid #2563EB !important;
        padding-left: 8px !important;
    }

    section[data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"] p {
        color: #1D4ED8 !important;
        font-weight: 700 !important;
    }


/* ===== ExamSync Dashboard Card Refinement ===== */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #FFFFFF 0%, #F8FBFF 100%) !important;
    border: 1px solid #D9E7FA !important;
    border-radius: 16px !important;
    padding: 22px 20px !important;
    box-shadow: 0 5px 18px rgba(37, 99, 235, 0.08) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 22px rgba(37, 99, 235, 0.13) !important;
}

[data-testid="stMetricLabel"] p {
    color: #536987 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #173565 !important;
    font-size: 30px !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize database
db.init_db()

# Application heading
st.title("📚 ExamSync")
st.subheader("Smart University Examination Timetable Generator")

st.write(
    "Generate examination timetables automatically while "
    "preventing clashes between subjects with common students."
)

# Sidebar navigation
menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Manage Students",
        "Manage Subjects",
        "Student Enrollment",
        "Generate Timetable",
        "View Timetable"
    ]
)

# ---------------- DASHBOARD ----------------

if menu == "Dashboard":

    st.header("📊 Dashboard")
    st.caption("Overview of students, subjects, enrollments, and examinations.")

    students = db.get_students()
    subjects = db.get_subjects()
    enrollments = db.get_enrollments()
    schedule = db.get_schedule()

    # Summary cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👨‍🎓 Total Students", len(students))
    col2.metric("📚 Total Subjects", len(subjects))
    col3.metric("📊 Total Enrollments", len(enrollments))
    col4.metric("📅 Scheduled Exams", len(schedule))

    st.divider()

    # Subject overview
    st.subheader("📚 Subject Overview")

    if subjects:
        subject_df = pd.DataFrame(
            subjects,
            columns=["Subject ID", "Subject Code", "Subject Name"]
        )

        st.table(subject_df[["Subject Code", "Subject Name"]])
    else:
        st.info("No subjects added yet.")

    # Enrollment chart
    st.subheader("📈 Student Enrollment by Subject")

    if subjects and enrollments:
        subject_names = {s[0]: f"{s[1]} - {s[2]}" for s in subjects}
        enrollment_counts = {}

        for student_id, subject_id in enrollments:
            if subject_id in subject_names:
                name = subject_names[subject_id]
                enrollment_counts[name] = enrollment_counts.get(name, 0) + 1

        if enrollment_counts:
            import plotly.express as px

            chart_df = pd.DataFrame(
                list(enrollment_counts.items()),
                columns=["Subject", "Students Enrolled"]
            )

            fig = px.bar(
                chart_df,
                x="Subject",
                y="Students Enrolled",
                text="Students Enrolled",
                color_discrete_sequence=["#3b82f6"]
            )

            fig.update_layout(
                height=480,
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                font=dict(
                    color="#14213d",
                    size=13
                ),
                xaxis=dict(
                    title="Subject",
                    tickangle=-25,
                    tickfont=dict(color="#14213d", size=12),
                    title_font=dict(color="#14213d"),
                    showgrid=False,
                    automargin=True
                ),
                yaxis=dict(
                    title="Number of Students",
                    tickfont=dict(color="#14213d", size=12),
                    title_font=dict(color="#14213d"),
                    gridcolor="#e2e8f0",
                    rangemode="tozero",
                    dtick=2
                ),
                margin=dict(l=65, r=25, t=35, b=130)
            )

            fig.update_traces(
                textposition="outside",
                textfont=dict(color="#14213d", size=13)
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No enrollment data available.")
    else:
        st.info("Enroll students in subjects to display the chart.")


    # Timetable preview
    st.subheader("\U0001F5D3\uFE0F Examination Timetable Preview")

    if schedule:
        schedule_df = pd.DataFrame(
            schedule,
            columns=["Subject Code", "Subject Name", "Exam Date", "Time Slot"]
        )

        schedule_df = schedule_df.sort_values(["Exam Date", "Time Slot"])

        st.table(schedule_df)
    else:
        st.info("Generate an examination timetable to see it here.")

    st.divider()

    # Project features
    st.subheader("\u2728 ExamSync Features")

    feature1, feature2, feature3 = st.columns(3)

    with feature1:
        st.markdown("### \U0001F393 Student Management")
        st.write("Register students using their ERP numbers.")

    with feature2:
        st.markdown("### \U0001F4DA Subject Management")
        st.write("Maintain subject codes and names.")

    with feature3:
        st.markdown("### \U0001F9E0 Smart Scheduling")
        st.write("Generate examination timetables with clash prevention.")

# ---------------- STUDENT MANAGEMENT ----------------

elif menu == "Manage Students":

    st.header("👨‍🎓 Manage Students")

    with st.form("student_form", clear_on_submit=True):

        name = st.text_input("Student Name")
        roll = st.text_input("ERP Number")

        submitted = st.form_submit_button("Add Student")

        if submitted:

            if not name.strip() or not roll.strip():
                st.error("Please enter the student name and ERP Number.")

            else:
                try:
                    db.add_student(name, roll)
                    st.success("Student added successfully!")
                    st.rerun()

                except Exception as e:
                    st.error(f"Could not add student: {e}")

    st.subheader("Registered Students")

    students = db.get_students()

    if students:
        df = pd.DataFrame(
            students,
            columns=["Student ID", "Student Name", "ERP Number"]
        )

        st.table(df)

    else:
        st.info("No students have been added yet.")

# ---------------- SUBJECT MANAGEMENT ----------------

elif menu == "Manage Subjects":

    st.header("📚 Manage Subjects")

    with st.form("subject_form", clear_on_submit=True):

        code = st.text_input("Subject Code")
        name = st.text_input("Subject Name")

        submitted = st.form_submit_button("Add Subject")

        if submitted:

            if not code.strip() or not name.strip():
                st.error("Please enter the subject code and name.")

            else:
                try:
                    db.add_subject(code, name)
                    st.success("Subject added successfully!")
                    st.rerun()

                except Exception as e:
                    st.error(f"Could not add subject: {e}")

    st.subheader("Available Subjects")

    subjects = db.get_subjects()

    if subjects:
        df = pd.DataFrame(
            subjects,
            columns=["Subject ID", "Subject Code", "Subject Name"]
        )

        st.table(df)

    else:
        st.info("No subjects have been added yet.")

# ---------------- STUDENT ENROLLMENT ----------------

elif menu == "Student Enrollment":

    st.header("📖 Student Subject Enrollment")

    students = db.get_students()
    subjects = db.get_subjects()
    enrollments = db.get_enrollments()

    if not students or not subjects:

        st.warning(
            "Please add students and subjects before creating enrollments."
        )

    else:

        student_options = {
            f"{s[2]} - {s[1]}": s[0]
            for s in students
        }

        subject_options = {
            f"{s[1]} - {s[2]}": s[0]
            for s in subjects
        }

        with st.form("enrollment_form"):

            selected_student = st.selectbox(
                "Select Student",
                list(student_options.keys())
            )

            selected_subject = st.selectbox(
                "Select Subject",
                list(subject_options.keys())
            )

            submitted = st.form_submit_button("Enroll Student")

            if submitted:

                student_id = student_options[selected_student]
                subject_id = subject_options[selected_subject]

                if (student_id, subject_id) in enrollments:

                    st.warning(
                        "This student is already enrolled in this subject."
                    )

                else:

                    try:
                        db.enroll_student(student_id, subject_id)
                        st.success("Enrollment completed successfully!")
                        st.rerun()

                    except Exception as e:
                        st.error(f"Enrollment failed: {e}")

    st.subheader("Current Enrollments")

    students = db.get_students()
    subjects = db.get_subjects()
    enrollments = db.get_enrollments()

    student_map = {s[0]: s for s in students}
    subject_map = {s[0]: s for s in subjects}

    rows = []

    for student_id, subject_id in enrollments:

        if student_id in student_map and subject_id in subject_map:

            student = student_map[student_id]
            subject = subject_map[subject_id]

            rows.append({
                "ERP Number": student[2],
                "Student Name": student[1],
                "Subject Code": subject[1],
                "Subject Name": subject[2]
            })

    if rows:

        st.table(pd.DataFrame(rows))

    else:
        st.info("No student enrollments available.")

# ---------------- TIMETABLE GENERATION ----------------

elif menu == "Generate Timetable":

    st.header("📅 Examination Timetable")

    subjects = db.get_subjects()
    enrollments = db.get_enrollments()

    if not subjects:

        st.warning("Please add subjects before generating the timetable.")

    else:

        st.write(
            "Choose the examination dates and daily time slots. "
            "ExamSync will prevent subjects sharing students "
            "from being scheduled simultaneously."
        )

        with st.form("schedule_form"):

            start_date = st.date_input(
                "Examination Start Date",
                value=date.today() + timedelta(days=7)
            )

            end_date = st.date_input(
                "Examination End Date",
                value=date.today() + timedelta(days=14)
            )

            selected_slots = st.multiselect(
                "Daily Examination Time Slots",
                [
                    "09:30 AM - 12:30 PM",
                    "09:45 AM - 10:45 AM",
                    "11:00 AM - 12:00 PM",
                    "02:00 PM - 05:00 PM",
                    "02:00 PM - 03:00 PM",
                    "04:00 PM - 05:00 PM"
                ],
                default=[
                    "09:30 AM - 12:30 PM",
                    "02:00 PM - 05:00 PM"
                ]
            )

            submitted = st.form_submit_button("Generate Timetable")

            if submitted:

                if end_date < start_date:

                    st.error(
                        "The end date must be on or after the start date."
                    )

                elif not selected_slots:

                    st.error("Please select at least one time slot.")

                else:

                    exam_dates = []
                    current_date = start_date

                    while current_date <= end_date:

                        exam_dates.append(current_date.isoformat())

                        current_date += timedelta(days=1)

                    try:

                        timetable = generate_timetable(
                            subjects,
                            enrollments,
                            exam_dates,
                            selected_slots
                        )

                        db.save_schedule(timetable)

                        st.success(
                            f"Timetable generated successfully for "
                            f"{len(timetable)} subjects!"
                        )

                        st.rerun()

                    except ValueError as e:

                        st.error(str(e))

                    except Exception as e:

                        st.error(f"An unexpected error occurred: {e}")

# ---------------- VIEW TIMETABLE ----------------

elif menu == "View Timetable":

    st.header("📅 Examination Timetable")

    schedule = db.get_schedule()

    if schedule:

        df = pd.DataFrame(
            schedule,
            columns=[
                "Subject Code",
                "Subject Name",
                "Exam Date",
                "Time Slot"
            ]
        )

        st.table(df)


        csv_data = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Timetable as CSV",
            data=csv_data,
            file_name="ExamSync_Timetable.csv",
            mime="text/csv"
        )

        # Download timetable as PDF
        from io import BytesIO
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle,
        )

        pdf_buffer = BytesIO()

        pdf_doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=landscape(A4),
        )

        styles = getSampleStyleSheet()

        elements = [
            Paragraph("ExamSync - Examination Timetable", styles["Title"]),
            Spacer(1, 20),
        ]

        pdf_table_data = [df.columns.tolist()] + df.astype(str).values.tolist()

        pdf_table = Table(
            pdf_table_data,
            repeatRows=1,
            hAlign="CENTER",
        )

        pdf_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#174A7E")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                    colors.white,
                    colors.HexColor("#EAF2F8"),
                ]),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ])
        )

        elements.append(pdf_table)
        pdf_doc.build(elements)

        st.download_button(
            label="📄 Download Timetable as PDF",
            data=pdf_buffer.getvalue(),
            file_name="ExamSync_Timetable.pdf",
            mime="application/pdf",
        )
        st.subheader("🔍 Examination Clash Detection Report")

        clashes = []
        student_enrollments = db.get_enrollments()
        all_subjects = db.get_subjects()

        subject_codes = {subject[0]: subject[1] for subject in all_subjects}
        subject_names = {subject[0]: subject[2] for subject in all_subjects}

        # Schedule rows contain: subject code, subject name, exam date, time slot.
        schedule_lookup = {
            row[0]: (str(row[2]), str(row[3]))
            for row in schedule
        }

        student_subjects = {}
        for student_id, subject_id in student_enrollments:
            student_subjects.setdefault(student_id, set()).add(subject_id)

        for student_id, subject_ids in student_subjects.items():
            scheduled_subject_ids = [
                subject_id
                for subject_id in subject_ids
                if subject_codes.get(subject_id) in schedule_lookup
            ]

            for i in range(len(scheduled_subject_ids)):
                for j in range(i + 1, len(scheduled_subject_ids)):
                    subject_a = scheduled_subject_ids[i]
                    subject_b = scheduled_subject_ids[j]

                    code_a = subject_codes.get(subject_a)
                    code_b = subject_codes.get(subject_b)
                    date_a, time_a = schedule_lookup[code_a]
                    date_b, time_b = schedule_lookup[code_b]

                    if date_a == date_b and time_a == time_b:
                        clashes.append({
                            "Student ID": student_id,
                            "Subject 1": f"{code_a} - {subject_names.get(subject_a, '')}",
                            "Subject 2": f"{code_b} - {subject_names.get(subject_b, '')}",
                            "Exam Date": date_a,
                            "Time Slot": time_a,
                        })

        if clashes:
            st.error(f"Found {len(clashes)} examination clash(es).")
            st.dataframe(pd.DataFrame(clashes), use_container_width=True, hide_index=True)
        else:
            st.success("\u2705 No examination clashes detected for enrolled students.")

    else:

        st.info(
            "No timetable has been generated yet. "
            "Open Generate Timetable to create one."
        )

