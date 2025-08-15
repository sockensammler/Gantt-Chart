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
FONT_REGULAR_PATH = find_font(["arial.ttf", "DejaVuSans.ttf"])
FONT_BOLD_PATH = find_font(["arialbd.ttf", "DejaVuSans-Bold.ttf"])
FONT_ITALIC_PATH = find_font(["ariali.ttf", "DejaVuSans-Oblique.ttf"])

if FONT_REGULAR_PATH:
    print(f"Schriftart '{os.path.basename(FONT_REGULAR_PATH)}' wird verwendet.")
    FONT_BOLD = ImageFont.truetype(FONT_BOLD_PATH or FONT_REGULAR_PATH, 14)
    FONT_REGULAR = ImageFont.truetype(FONT_REGULAR_PATH, 12)
    FONT_ITALIC = ImageFont.truetype(FONT_ITALIC_PATH or FONT_REGULAR_PATH, 12)
    FONT_CHART_HEADER_BOLD = ImageFont.truetype(FONT_BOLD_PATH or FONT_REGULAR_PATH, 11)
    FONT_CHART_WEEK_BOLD = ImageFont.truetype(FONT_BOLD_PATH or FONT_REGULAR_PATH, 9)
    FONT_LEGEND = ImageFont.truetype(FONT_REGULAR_PATH, 11)
else:
    print("Warnung: Keine passende Schriftart gefunden, die Umlaute unterstützt. Verwende Standard-Schriftart.")
    FONT_BOLD = ImageFont.load_default()
    FONT_REGULAR = ImageFont.load_default()
    FONT_ITALIC = FONT_REGULAR
    FONT_CHART_HEADER_BOLD = FONT_BOLD
    FONT_CHART_WEEK_BOLD = FONT_BOLD
    FONT_LEGEND = ImageFont.load_default()

# Farben
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREY_LIGHT = (240, 240, 240)
COLOR_GREY_DARK = (225, 225, 225) # Für abwechselnde Zeilen
COLOR_GREY_MEDIUM = (200, 200, 200)
COLOR_BLUE_PRIMARY = (54, 162, 235)
COLOR_BLUE_DARK = (40, 120, 180)
COLOR_HEADER_BG = (230, 230, 230)
COLOR_CATEGORY_BG = (200, 200, 200)
COLOR_RED_MILESTONE = (255, 99, 132)
COLOR_YELLOW_PHASE = (255, 221, 0)

# Layout
TOTAL_IMAGE_WIDTH = 1800
PADDING = 20
HEADER_AREA_HEIGHT = 80 # NEU: Platz für den oberen Header
TABLE_WIDTH = 440
HEADER_HEIGHT = 40
ROW_HEIGHT = 30
SPACE_BETWEEN = 0
MILESTONE_SIZE = 8
TEXT_AREA_WIDTH = 50

# --- 1. Daten definieren ---
tasks_data = [
    {'name': 'Kick-off Meeting', 'category': 'Klärungsphase', 'start': datetime.date(2025, 9, 1), 'end': datetime.date(2025, 9, 1), 'completion': 100},
    {'name': 'Anforderungsanalyse & Spezifikation', 'category': 'Klärungsphase', 'start': datetime.date(2025, 9, 2), 'end': datetime.date(2025, 9, 8), 'completion': 100},
    {'name': 'Mechanische Design', 'category': 'Entwicklungsphase', 'start': datetime.date(2025, 9, 9), 'end': datetime.date(2025, 9, 19), 'completion': 75},
    {'name': 'Elektrisches Design', 'category': 'Entwicklungsphase', 'start': datetime.date(2025, 9, 22), 'end': datetime.date(2025, 9, 23), 'completion': 0},
    {'name': 'SPS Automatisierung', 'category': 'Entwicklungsphase', 'start': datetime.date(2025, 9, 24), 'end': datetime.date(2025, 10, 10), 'completion': 40},
    {'name': 'Testphase', 'category': 'Entwicklungsphase', 'start': datetime.date(2025, 9, 24), 'end': datetime.date(2025, 10, 15), 'completion': 25},
    {'name': 'Nacharbeiten', 'category': 'Testphase', 'start': datetime.date(2025, 10, 16), 'end': datetime.date(2025, 10, 24), 'completion': 0},
    {'name': 'Einbau bei Krones', 'category': 'Testphase', 'start': datetime.date(2025, 10, 27), 'end': datetime.date(2025, 10, 27), 'completion': 0}
]

milestones_data = [
    {'name': 'Auftragseingang', 'category': 'Klärungsphase', 'date': datetime.date(2025, 8, 25)},
    {'name': 'Bestätigung der Spezifikation durch Krones', 'category': 'Klärungsphase', 'date': datetime.date(2025, 9, 9)},
    {'name': 'Design finalisiert', 'category': 'Entwicklungsphase', 'date': datetime.date(2025, 9, 23)},
    {'name': 'Lieferbereitschaft', 'category': 'Entwicklungsphase', 'date': datetime.date(2025, 10, 15)}
]

# Daten für die Verarbeitung vorbereiten und gruppieren
all_items = []
for task in tasks_data:
    task['type'] = 'task'
    # Dauer aus Start- und Enddatum berechnen
    task['duration'] = (task['end'] - task['start']).days + 1
    all_items.append(task)

for milestone in milestones_data:
    milestone['type'] = 'milestone'
    milestone['start'] = milestone['date']
    all_items.append(milestone)

# Nach Kategorien gruppieren
categorized_items = {}
category_order = []
for item in all_items:
    category = item.get('category', 'Sonstiges')
    if category not in categorized_items:
        categorized_items[category] = []
        category_order.append(category)
    categorized_items[category].append(item)

# Einträge innerhalb jeder Kategorie nach Datum sortieren
for category in categorized_items:
    categorized_items[category].sort(key=lambda x: x['start'])

# --- 2. Bilddimensionen berechnen ---
project_start_date = min(item['start'] for item in all_items)
project_end_date = max(item.get('end', item['start']) for item in all_items)
project_duration_days = (project_end_date - project_start_date).days + 1

CHART_WIDTH = TOTAL_IMAGE_WIDTH - (PADDING * 2 + TABLE_WIDTH + SPACE_BETWEEN + TEXT_AREA_WIDTH)
pixels_per_day = CHART_WIDTH / project_duration_days

IMG_HEIGHT = PADDING * 2 + HEADER_AREA_HEIGHT + HEADER_HEIGHT + (len(all_items) + len(category_order)) * ROW_HEIGHT
IMG_WIDTH = TOTAL_IMAGE_WIDTH

# --- 3. Bild-Leinwand erstellen ---
image = Image.new('RGB', (int(IMG_WIDTH), IMG_HEIGHT), COLOR_WHITE)
draw = ImageDraw.Draw(image)

# --- Header-Bereich zeichnen ---
header_y = PADDING

# Oben Links: Projektinfo
draw.text((PADDING, header_y + 10), "Projekt: Website Relaunch", font=FONT_BOLD, fill=COLOR_BLACK)
draw.text((PADDING, header_y + 35), f"Datum: {datetime.date.today().strftime('%d.%m.%Y')}", font=FONT_REGULAR, fill=COLOR_BLACK)

# Oben Rechts: Logo
try:
    logo = Image.open("logo.png")
    logo_aspect_ratio = logo.width / logo.height
    logo_height = 60
    logo_width = int(logo_height * logo_aspect_ratio)
    logo = logo.resize((logo_width, logo_height))
    logo_x = IMG_WIDTH - PADDING - logo_width
    logo_y = header_y + 5
    image.paste(logo, (logo_x, logo_y), logo)
except FileNotFoundError:
    print("logo.png nicht gefunden. Logo wird nicht angezeigt.")

# Oben Mitte: Legende
legend_x = IMG_WIDTH / 2 - 180
legend_y = header_y + 15
legend_item_height = 20
box_size = 12

# Legende: Phase
draw.rectangle([legend_x, legend_y, legend_x + box_size, legend_y + box_size], fill=COLOR_YELLOW_PHASE, outline=COLOR_BLACK)
draw.text((legend_x + box_size + 5, legend_y - 2), "Phase", font=FONT_LEGEND, fill=COLOR_BLACK)

# Legende: Aufgabe
draw.rectangle([legend_x, legend_y + legend_item_height, legend_x + box_size, legend_y + legend_item_height + box_size], fill=COLOR_BLUE_PRIMARY, outline=COLOR_BLACK)
draw.rectangle([legend_x, legend_y + legend_item_height, legend_x + box_size/2, legend_y + legend_item_height + box_size], fill=COLOR_BLUE_DARK) # Fortschritt andeuten
draw.text((legend_x + box_size + 5, legend_y + legend_item_height - 2), "Aufgabe mit Fortschritt", font=FONT_LEGEND, fill=COLOR_BLACK)

# Legende: Meilenstein
points = [(legend_x + box_size/2, legend_y + 2*legend_item_height), (legend_x + box_size, legend_y + 2*legend_item_height + box_size/2),
          (legend_x + box_size/2, legend_y + 2*legend_item_height + box_size), (legend_x, legend_y + 2*legend_item_height + box_size/2)]
draw.polygon(points, fill=COLOR_RED_MILESTONE, outline=COLOR_BLACK)
draw.text((legend_x + box_size + 5, legend_y + 2*legend_item_height - 2), "Meilenstein", font=FONT_LEGEND, fill=COLOR_BLACK)


# --- 4. Tabelle und Diagramm-Hintergrund zeichnen ---
table_y = PADDING + HEADER_AREA_HEIGHT
table_x = PADDING
chart_x = table_x + TABLE_WIDTH + SPACE_BETWEEN
chart_y = table_y

# Globale Überschriften
draw.rectangle([table_x, table_y, table_x + TABLE_WIDTH, table_y + HEADER_HEIGHT], fill=COLOR_HEADER_BG)
draw.text((table_x + 5, table_y + 12), "Aufgabe / Meilenstein", font=FONT_BOLD, fill=COLOR_BLACK)
draw.text((table_x + 230, table_y + 12), "Start", font=FONT_BOLD, fill=COLOR_BLACK)
draw.text((table_x + 340, table_y + 12), "Ende", font=FONT_BOLD, fill=COLOR_BLACK)

# KORREKTUR: Hintergrund für Chart-Kopfzeile
draw.rectangle([chart_x, chart_y, chart_x + CHART_WIDTH + TEXT_AREA_WIDTH, chart_y + HEADER_HEIGHT], fill=COLOR_HEADER_BG)

# Zeitachsen-Überschriften (Monat und KW)
current_date = project_start_date
while current_date <= project_end_date:
    if current_date.day == 1:
        month_start_x = chart_x + ((current_date - project_start_date).days * pixels_per_day)
        draw.text((month_start_x + 5, chart_y + 5), current_date.strftime('%B %Y'), font=FONT_CHART_HEADER_BOLD, fill=COLOR_BLACK)
    if current_date.weekday() == 0:
        line_x = chart_x + ((current_date - project_start_date).days * pixels_per_day)
        week_num = current_date.isocalendar()[1]
        draw.text((line_x + 3, chart_y + 25), f"KW{week_num}", font=FONT_CHART_WEEK_BOLD, fill=COLOR_BLACK)
    current_date += timedelta(days=1)

# Kategorien und Einträge durchlaufen
current_y = table_y + HEADER_HEIGHT
category_index = 0
for category_name in category_order:
    category_items = categorized_items[category_name]
    
    # Kategorie-Überschrift in der Tabelle
    draw.rectangle([table_x, current_y, table_x + TABLE_WIDTH, current_y + ROW_HEIGHT], fill=COLOR_CATEGORY_BG)
    draw.text((table_x + 5, current_y + 8), category_name, font=FONT_BOLD, fill=COLOR_BLACK)
    
    # Phasen-Balken im Diagramm zeichnen
    phase_start_date = min(item['start'] for item in category_items)
    phase_end_date = max(item.get('end', item['start']) for item in category_items)
    phase_duration_days = (phase_end_date - phase_start_date).days + 1
    
    start_offset = (phase_start_date - project_start_date).days * pixels_per_day
    bar_width = phase_duration_days * pixels_per_day
    bar_x = chart_x + start_offset
    draw.rectangle([bar_x, current_y + 5, bar_x + bar_width, current_y + ROW_HEIGHT - 5], fill=COLOR_YELLOW_PHASE, outline=COLOR_BLACK)
    
    # Hintergrund für die Zeilen der Kategorie im Chart
    bg_color = COLOR_GREY_LIGHT if category_index % 2 == 0 else COLOR_GREY_DARK
    chart_bg_y_start = current_y + ROW_HEIGHT
    chart_bg_y_end = chart_bg_y_start + len(category_items) * ROW_HEIGHT
    draw.rectangle([chart_x, chart_bg_y_start, chart_x + CHART_WIDTH + TEXT_AREA_WIDTH, chart_bg_y_end], fill=bg_color)
    
    current_y += ROW_HEIGHT
    
    # Einträge der Kategorie zeichnen
    for item in category_items:
        # Tabellenzeile
        draw.rectangle([table_x, current_y, table_x + TABLE_WIDTH, current_y + ROW_HEIGHT], outline=COLOR_GREY_MEDIUM)
        if item['type'] == 'task':
            draw.text((table_x + 5, current_y + 8), item['name'], font=FONT_REGULAR, fill=COLOR_BLACK)
            draw.text((table_x + 230, current_y + 8), item['start'].strftime('%d.%m.%Y'), font=FONT_REGULAR, fill=COLOR_BLACK)
            draw.text((table_x + 340, current_y + 8), item['end'].strftime('%d.%m.%Y'), font=FONT_REGULAR, fill=COLOR_BLACK)
            
            # Aufgabenbalken im Chart
            start_offset = (item['start'] - project_start_date).days * pixels_per_day
            bar_width = item['duration'] * pixels_per_day
            bar_x = chart_x + start_offset
            draw.rectangle([bar_x, current_y + 5, bar_x + bar_width, current_y + ROW_HEIGHT - 5], fill=COLOR_BLUE_PRIMARY, outline=COLOR_BLACK)
            
            completion_width = bar_width * (item.get('completion', 0) / 100)
            if completion_width > 0:
                draw.rectangle([bar_x, current_y + 5, bar_x + completion_width, current_y + ROW_HEIGHT - 5], fill=COLOR_BLUE_DARK)
            
            draw.text((bar_x + bar_width + 5, current_y + 8), f"{item.get('completion', 0)}%", font=FONT_REGULAR, fill=COLOR_BLACK)

        elif item['type'] == 'milestone':
            draw.text((table_x + 5, current_y + 8), item['name'], font=FONT_ITALIC, fill=COLOR_BLACK)
            draw.text((table_x + 230, current_y + 8), item['date'].strftime('%d.%m.%Y'), font=FONT_REGULAR, fill=COLOR_BLACK)
            
            # Meilenstein-Raute im Chart
            offset = (item['date'] - project_start_date).days * pixels_per_day
            center_x = chart_x + offset
            center_y = current_y + (ROW_HEIGHT / 2)
            points = [(center_x, center_y - MILESTONE_SIZE), (center_x + MILESTONE_SIZE, center_y),
                      (center_x, center_y + MILESTONE_SIZE), (center_x - MILESTONE_SIZE, center_y)]
            draw.polygon(points, fill=COLOR_RED_MILESTONE, outline=COLOR_BLACK)
            
        current_y += ROW_HEIGHT
    category_index += 1

# --- 5. Vordergründige Wochenlinien zeichnen (gestrichelt) ---
current_date = project_start_date
while current_date <= project_end_date:
    if current_date.weekday() == 0: # Montag
        line_x = chart_x + ((current_date - project_start_date).days * pixels_per_day)
        line_y_start = chart_y + HEADER_HEIGHT
        line_y_end = IMG_HEIGHT - PADDING
        
        # Gestrichelte Linie manuell zeichnen
        for y in range(line_y_start, line_y_end, 10): # 10 = Strichlänge + Lücke
            draw.line([(line_x, y), (line_x, y + 5)], fill=COLOR_GREY_MEDIUM, width=1) # 5 = Strichlänge
            
    current_date += timedelta(days=1)

# --- 6. Bild speichern ---
output_filename = "projektplan.png"
image.save(output_filename)

print(f"Gantt-Diagramm mit Tabelle wurde erfolgreich als '{output_filename}' gespeichert.")
