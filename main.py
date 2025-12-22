from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sqlite3
import os

DB_NAME = "store_v2.db"

def db_path():
    # For Android, keep db in app user data directory
    return os.path.join(App.get_running_app().user_data_dir, DB_NAME)

def init_db():
    conn = sqlite3.connect(db_path())
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        unit TEXT,
        description TEXT,
        unit_price REAL,
        selling_price REAL,
        income_price REAL,
        quantity INTEGER,
        category TEXT,
        expiry_date TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        description TEXT,
        qty INTEGER,
        price_each REAL,
        total REAL,
        payment REAL,
        change REAL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

class SellingScreen(Screen):
    pass

class MaintenanceScreen(Screen):
    pass

class ReportScreen(Screen):
    pass

class Root(ScreenManager):
    pass

KV = """
Root:
    SellingScreen:
        name: "selling"
    MaintenanceScreen:
        name: "maintenance"
    ReportScreen:
        name: "report"

<SellingScreen>:
    BoxLayout:
        orientation: "vertical"
        Label:
            text: "SELLING"
            font_size: "24sp"
        Button:
            text: "Go to Maintenance"
            on_release: app.root.current = "maintenance"

<MaintenanceScreen>:
    BoxLayout:
        orientation: "vertical"
        Label:
            text: "MAINTENANCE"
            font_size: "24sp"
        Button:
            text: "Go to Report"
            on_release: app.root.current = "report"

<ReportScreen>:
    BoxLayout:
        orientation: "vertical"
        Label:
            text: "REPORT"
            font_size: "24sp"
        Button:
            text: "Back to Selling"
            on_release: app.root.current = "selling"
"""

class POSApp(App):
    def build(self):
        Builder.load_string(KV)
        root = Builder.load_string(KV)
        return root

    def on_start(self):
        init_db()

if __name__ == "__main__":
    POSApp().run()
