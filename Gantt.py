import datetime
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont
import os

# HINWEIS: Dieses Skript benötigt die Pillow-Bibliothek.
# Führen Sie im Terminal aus: pip install Pillow

# --- Hilfsfunktion zum Finden von Schriften ---
def find_font(font_names):
    """Sucht nach einer Schriftart in gängigen Systemverzeichnissen."""
    font_paths = [
        "C:/Windows/Fonts/",                # Windows
        "/usr/share/fonts/truetype/dejavu/", # Linux (Debian/Ubuntu)
        "/System/Library/Fonts/Supplemental/", # macOS
        "/Library/Fonts/"                    # macOS
    ]
    for path in font_paths:
        for font_name in font_names:
            font_file = os.path.join(path, font_name)
            if os.path.exists(font_file):
                return font_file
    return None

# --- Konfiguration ---
# Schriften
# Sucht automatisch nach einer passenden Schriftart, die Umlaute unterstützt.
FONT_REGULAR_PATH = find_font(["arial.ttf", "DejaVuSans.ttf"])
FONT_BOLD_PATH = find_font(["arialbd.ttf", "DejaVuSans-Bold.ttf"])
FONT_ITALIC_PATH = find_font(["ariali.ttf", "DejaVuSans-Oblique.ttf"])

if FONT_REGULAR_PATH:
    print(f"Schriftart '{os.path.basename(FONT_REGULAR_PATH)}' wird verwendet.")
    FONT_BOLD = ImageFont.truetype(FONT_BOLD_PATH or FONT_REGULAR_PATH, 14)
    FONT_REGULAR = ImageFont.truetype(FONT_REGULAR_PATH, 12)
    FONT_ITALIC = ImageFont.truetype(FONT_ITALIC_PATH or FONT_REGULAR_PATH, 12)
    FONT_CHART_HEADER = ImageFont.truetype(FONT_REGULAR_PATH, 11)
    FONT_CHART_WEEK = ImageFont.truetype(FONT_REGULAR_PATH, 9)
else:
    print("Warnung: Keine passende Schriftart gefunden, die Umlaute unterstützt. Verwende Standard-Schriftart.")
    print("Umlaute werden möglicherweise nicht korrekt dargestellt.")
    FONT_BOLD = ImageFont.load_default()
    FONT_REGULAR = ImageFont.load_default()
    FONT_ITALIC = FONT_REGULAR
    FONT_CHART_HEADER = ImageFont.load_default()
    FONT_CHART_WEEK = ImageFont.load_default()


# Farben
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREY_LIGHT = (240, 240, 240)
COLOR_GREY_MEDIUM = (200, 200, 200)
COLOR_BLUE_PRIMARY = (54, 162, 235)
COLOR_BLUE_DARK = (40, 120, 180) # Farbe für den Fortschrittsbalken
COLOR_HEADER_BG = (230, 230, 230)
COLOR_RED_MILESTONE = (255, 99, 132)

# Layout
TOTAL_IMAGE_WIDTH = 1800
PADDING = 20
TABLE_WIDTH = 440 # Breite an die entfernte Spalte angepasst
HEADER_HEIGHT = 40
ROW_HEIGHT = 30
SPACE_BETWEEN = 0
MILESTONE_SIZE = 8 # Größe der Raute
TEXT_AREA_WIDTH = 50 # Platz für den Erfüllungsgrad-Text neben den Balken

# --- 1. Daten definieren ---
tasks_data = [
    {'name': 'Kick-off Meeting', 'start': datetime.date(2025, 9, 1), 'duration': 1, 'completion': 100},
    {'name': 'Anforderungsanalyse', 'start': datetime.date(2025, 9, 2), 'duration': 7, 'completion': 100},
    {'name': 'Design-Entwurf', 'start': datetime.date(2025, 9, 9), 'duration': 11, 'completion': 75},
    {'name': 'Design-Abnahme', 'start': datetime.date(2025, 9, 22), 'duration': 2, 'completion': 0},
    {'name': 'Frontend-Entwicklung', 'start': datetime.date(2025, 9, 24), 'duration': 17, 'completion': 40},
    {'name': 'Backend-Entwicklung', 'start': datetime.date(2025, 9, 24), 'duration': 22, 'completion': 25},
    {'name': 'Testing & QA', 'start': datetime.date(2025, 10, 16), 'duration': 9, 'completion': 0},
    {'name': 'Go-Live', 'start': datetime.date(2025, 10, 27), 'duration': 1, 'completion': 0}
]

milestones_data = [
    {'name': 'Design finalisiert', 'date': datetime.date(2025, 9, 23)},
    {'name': 'Alpha-Version fertig', 'date': datetime.date(2025, 10, 15)}
]

# Daten für die Verarbeitung vorbereiten
project_items = []
for task in tasks_data:
    task['type'] = 'task'
    task['end'] = task['start'] + timedelta(days=task['duration'] - 1)
    project_items.append(task)

for milestone in milestones_data:
    milestone['type'] = 'milestone'
    milestone['start'] = milestone['date'] # Für die Sortierung
    project_items.append(milestone)

# Alle Einträge nach Startdatum sortieren
project_items.sort(key=lambda x: x['start'])


# --- 2. Bilddimensionen berechnen ---
project_start_date = min(item['start'] for item in project_items)
project_end_date = max(item.get('end', item['start']) for item in project_items)
project_duration_days = (project_end_date - project_start_date).days + 1

CHART_WIDTH = TOTAL_IMAGE_WIDTH - (PADDING * 2 + TABLE_WIDTH + SPACE_BETWEEN + TEXT_AREA_WIDTH)
if CHART_WIDTH < 200:
    CHART_WIDTH = 200
    print("Warnung: TOTAL_IMAGE_WIDTH ist sehr klein. Der Chart wird auf 200px Breite begrenzt.")

pixels_per_day = CHART_WIDTH / project_duration_days

IMG_HEIGHT = PADDING * 2 + HEADER_HEIGHT + len(project_items) * ROW_HEIGHT
IMG_WIDTH = TOTAL_IMAGE_WIDTH

# --- 3. Bild-Leinwand erstellen ---
image = Image.new('RGB', (int(IMG_WIDTH), IMG_HEIGHT), COLOR_WHITE)
draw = ImageDraw.Draw(image)

# --- 4. Tabelle zeichnen ---
table_x, table_y = PADDING, PADDING
col1_x, col2_x, col3_x = table_x, table_x + 230, table_x + 340

# Tabellenüberschrift
draw.rectangle([table_x, table_y, table_x + TABLE_WIDTH, table_y + HEADER_HEIGHT], fill=COLOR_HEADER_BG)
draw.text((col1_x + 5, table_y + 12), "Aufgabe / Meilenstein", font=FONT_BOLD, fill=COLOR_BLACK)
draw.text((col2_x + 5, table_y + 12), "Start", font=FONT_BOLD, fill=COLOR_BLACK)
draw.text((col3_x + 5, table_y + 12), "Ende", font=FONT_BOLD, fill=COLOR_BLACK)

# Tabellenzeilen
current_y = table_y + HEADER_HEIGHT
for item in project_items:
    draw.rectangle([table_x, current_y, table_x + TABLE_WIDTH, current_y + ROW_HEIGHT], outline=COLOR_GREY_MEDIUM)
    if item['type'] == 'task':
        draw.text((col1_x + 5, current_y + 8), item['name'], font=FONT_REGULAR, fill=COLOR_BLACK)
        draw.text((col2_x + 5, current_y + 8), item['start'].strftime('%d.%m.%Y'), font=FONT_REGULAR, fill=COLOR_BLACK)
        draw.text((col3_x + 5, current_y + 8), item['end'].strftime('%d.%m.%Y'), font=FONT_REGULAR, fill=COLOR_BLACK)
    elif item['type'] == 'milestone':
        draw.text((col1_x + 5, current_y + 8), item['name'], font=FONT_ITALIC, fill=COLOR_BLACK)
        draw.text((col2_x + 5, current_y + 8), item['date'].strftime('%d.%m.%Y'), font=FONT_REGULAR, fill=COLOR_BLACK)
    current_y += ROW_HEIGHT

# --- 5. Gantt-Diagramm zeichnen ---
chart_x = table_x + TABLE_WIDTH + SPACE_BETWEEN
chart_y = table_y

# Chart-Hintergrund und Zeitachse
draw.rectangle([chart_x, chart_y, chart_x + CHART_WIDTH + TEXT_AREA_WIDTH, IMG_HEIGHT - PADDING], fill=COLOR_GREY_LIGHT)

current_date = project_start_date
while current_date <= project_end_date:
    if current_date.day == 1:
        month_start_x = chart_x + ((current_date - project_start_date).days * pixels_per_day)
        draw.text((month_start_x + 5, chart_y + 5), current_date.strftime('%B %Y'), font=FONT_CHART_HEADER, fill=COLOR_BLACK)
    if current_date.weekday() == 0:
        line_x = chart_x + ((current_date - project_start_date).days * pixels_per_day)
        draw.line([(line_x, chart_y + HEADER_HEIGHT), (line_x, IMG_HEIGHT - PADDING)], fill=COLOR_GREY_MEDIUM, width=1)
        week_num = current_date.isocalendar()[1]
        draw.text((line_x + 3, chart_y + 25), f"KW{week_num}", font=FONT_CHART_WEEK, fill=COLOR_BLACK)
    current_date += timedelta(days=1)

# Chart-Elemente (Balken und Rauten)
current_y = chart_y + HEADER_HEIGHT
for item in project_items:
    if item['type'] == 'task':
        start_offset_days = (item['start'] - project_start_date).days
        bar_x = chart_x + (start_offset_days * pixels_per_day)
        bar_width = item['duration'] * pixels_per_day
        bar_y_top = current_y + 5
        bar_y_bottom = current_y + ROW_HEIGHT - 5
        
        # Haupt-Balken zeichnen
        draw.rectangle([bar_x, bar_y_top, bar_x + bar_width, bar_y_bottom], fill=COLOR_BLUE_PRIMARY, outline=COLOR_BLACK)
        
        # Fortschrittsbalken darüber zeichnen
        completion_width = bar_width * (item.get('completion', 0) / 100)
        if completion_width > 0:
            draw.rectangle(
                [bar_x, bar_y_top, bar_x + completion_width, bar_y_bottom],
                fill=COLOR_BLUE_DARK
            )
        
        # Erfüllungsgrad-Text neben den Balken schreiben
        text_x = bar_x + bar_width + 5
        text_y = current_y + 8
        draw.text((text_x, text_y), f"{item.get('completion', 0)}%", font=FONT_REGULAR, fill=COLOR_BLACK)

    elif item['type'] == 'milestone':
        date_offset_days = (item['date'] - project_start_date).days
        center_x = chart_x + (date_offset_days * pixels_per_day)
        center_y = current_y + (ROW_HEIGHT / 2)
        
        points = [
            (center_x, center_y - MILESTONE_SIZE),
            (center_x + MILESTONE_SIZE, center_y),
            (center_x, center_y + MILESTONE_SIZE),
            (center_x - MILESTONE_SIZE, center_y)
        ]
        draw.polygon(points, fill=COLOR_RED_MILESTONE, outline=COLOR_BLACK)

    current_y += ROW_HEIGHT

# --- 6. Bild speichern ---
output_filename = "projektplan.png"
image.save(output_filename)

print(f"Gantt-Diagramm mit Tabelle wurde erfolgreich als '{output_filename}' gespeichert.")
