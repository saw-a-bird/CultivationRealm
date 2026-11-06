
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
from collections import defaultdict
from PIL import Image, ImageDraw
import time
import random
import json
import os
import sys
import re

import ctypes
import pystray

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

BG = "#10131D"
PANEL = "#1A2030"
PANEL_ALT = "#222A3D"
BORDER = "#303A52"
TEXT = "#E8EAF2"
MUTED = "#929BB2"
PURPLE = "#A78BFA"
GOLD = "#F5C66A"
GREEN = "#65D6A0"
RED = "#F08080"
BLUE = "#79B8F5"

# --------- SMALL REWARDS
def get_cultivation_session_reward(elapsed):
    # Duration-based XP rewards
    if elapsed < 60:
        xp_reward = 0
    elif elapsed < 600:
        xp_reward = 1
    elif elapsed < 1500:
        xp_reward = 2
    elif elapsed < 3000:
        xp_reward = 4
    elif elapsed < 5400:
        xp_reward = 7
    else:
        xp_reward = 10
    return xp_reward

# daily_bonus = min(11, 5 + (self.getting_started_streak - 1)) # starts at 5 to 11XP max

# ---------------- CULTIVATION / XP SYSTEM ----------------

REALMS = [
    (0, 1, "MORTAL", "You are but an ordinary mortal.",
    "No power. No foundation. Only the potential to begin.", 50),

    (2, 5, "THE PATH OF INITIATION", "Your journey begins here.",
        "Every cultivator must overcome the resistance of beginning.", 150),

    (6, 12, "BODY REFINEMENT", "Forge discipline. Strengthen your foundation.",
        "Greatness begins with a foundation that cannot be shaken.", 250),

    (13, 20, "QI CONDENSATION", "Gather your energy. Begin true cultivation.",
        "Turn scattered effort into focused power.", 500),

    (21, 30, "FOUNDATION ESTABLISHMENT", "Build the foundation of your future.",
        "A strong foundation carries you beyond ordinary limits.", 800),

    (31, 40, "GOLDEN CORE", "Condense your power. Become extraordinary.",
        "Your hard work is taking a solid form.", 1200),

    (41, 50, "NASCENT SOUL", "Your spirit rises beyond its former limits.",
        "Your will is becoming stronger than resistance.", 1800),

    (51, 60, "SOUL TRANSFORMATION", "Transform your very existence.",
        "You are no longer who you were when you began.", 2500),

    (61, 70, "VOID REFINEMENT", "Refine the void. Break worldly limitations.",
        "Even the impossible becomes another obstacle to overcome.", 3500),

    (71, 80, "BODY INTEGRATION", "Unite body, mind, and spirit.",
        "Every part of you moves with a single purpose.", 5000),

    (81, 90, "GREAT ASCENSION", "Stand at the threshold of immortality.",
        "The summit is closer than it has ever been.", 7000),

    (91, 100, "TRUE IMMORTAL", "Step beyond the limits of mortality.",
        "Your journey has entered a new plane of existence.", 10000),

    (101, 110, "IMMORTAL KING", "Rule over your own immortal domain.",
        "Your presence commands respect.", 15000),

    (111, 120, "IMMORTAL EMPEROR", "Your name shakes the heavens.",
        "Few can stand where you now stand.", 22000),

    (121, 130, "DAO ANCESTOR", "Comprehend the origin of all things.",
        "You are approaching the source of the path itself.", 35000),

    (131, float("inf"), "FANG YUAN", "Beyond the Dao. Beyond the heavens.",
        "There are no limits left to inherit.", 50000),
]

# ---------------- QUOTES -------------------------

HEADER_QUOTES = [
    "CONSISTENCY  •  DISCIPLINE  •  PROGRESS  •  MASTERY",
    "XP rewards effort. Streaks reward consistency. Realms reward long-term dedication.",
    "Motivation gets you started. Consistency keeps you moving.",
    "Be patient with the process, but relentless with your commitment."
]

# --------------- LEVEL UP MESSAGES ------------------

LEVEL_UP_MESSAGES = [
    "No more excuses. Your next sequence awaits!",
    "Another breakthrough! Keep ascending!",
    "The pathway to greatness is paved with consistency!",
    "Even a demigod started as a mere mortal!",
    "One step closer to becoming a legend!",
    "Your cultivation has improved. Keep going!",
    "The heavens have witnessed your progress!",
    "Another day, another opportunity to defy fate!",
    "Keep grinding. Your future self will thank you!",
    "A true cultivator never wastes a breakthrough!",
    "Your Dao is becoming clearer!",
    "Even immortality requires patience!",
    "You're slowly becoming the monster you once feared!",
    "The journey to the peak never ends!",
    "Your legend won't write itself!",
    "A little closer to transcending mortality!",
    "Every action is an investment in your future!",
    "Keep going. The heavens are not your limit!",
]


# -------------- REVIEW RESPONSES --------------------

REVIEW_RESPONSES = {
    "YES!": [
        "That's what I'm talking about! You crushed it! 🎉",
        "Mission accomplished! Be proud of yourself!",
        "You set a goal and delivered. Excellent work!",
        "Procrastination never stood a chance!",
        "Another victory! Your legend grows!",
        "Even Klein would approve of this level of preparation!",
        "The Fool's honor is maintained. Excellent work!",
        "Today, you were the protagonist of your own story!",
        "You have successfully advanced your sequence!",
        "Not even the Nightmare Spell could stop you today!",
        "Sunny would be proud. Maybe. He'd probably still complain.",
        "A flawless execution. Even Fang Yuan would acknowledge that!",
        "You have taken another step toward immortality!",
        "Your perseverance rivals that of a true Sword God!",
        "The heavens have witnessed your dedication!",
        "You've earned your share of good karma today!",
        "Another fate-defying achievement!",
        "Your future self just gained a powerful ally!",
        "You didn't wait for an opportunity. You created one!",
        "The world belongs to those who take action!",
    ],

    "PARTIALLY": [
        "Good progress! Even a demigod wasn't born overnight!",
        "Not a complete victory, but your sequence has advanced!",
        "Every small step brings you closer to the peak!",
        "Even Sunny needs more than one attempt!",
        "The path of cultivation is never easy. Keep going!",
        "A minor setback in the grand scheme of things!",
        "Fang Yuan wouldn't waste time regretting this. Neither should you!",
        "Your progress may be slow, but your Dao remains yours!",
        "One step forward is better than remaining stagnant!",
        "Not bad! Your next breakthrough is within reach!",
        "Even the strongest cultivators need time to recover!",
        "The Nightmare Spell is cruel, but so is your determination!",
        "You're gathering experience. Use it wisely!",
        "The road to the peak is paved with imperfect victories!",
        "A partial success is still a success. Build upon it!",
        "Your story isn't over. This is just another chapter!",
    ],

    "NOT YET": [
        "Don't panic. Even Klein had to survive some ridiculous situations!",
        "The Fool's journey wasn't completed in a single day!",
        "Even Sunny has suffered worse setbacks. Probably.",
        "You have encountered a Nightmare. Now learn from it!",
        "Fang Yuan wouldn't waste time crying over a failed attempt!",
        "A true cultivator doesn't abandon their Dao after one setback!",
        "The heavens may oppose you, but your journey continues!",
        "You failed today. Don't let it become your Sequence 0!",
        "Even a Sword God needs time to sharpen his blade!",
        "Your story has encountered a difficult arc. Keep reading!",
        "Not every chapter can be a victory. Keep turning the pages!",
        "The Nightmare Spell has claimed today's victory. Take revenge tomorrow!",
        "Even the strongest characters have their lowest moments!",
        "Don't let temporary circumstances dictate your destiny!",
        "Fang Yuan would call this a minor inconvenience!",
        "The road to immortality is paved with countless failures!",
        "You can still become the protagonist of your own story!",
        "One failed session won't destroy your entire cultivation!",
        "Your enemies are getting stronger. So should you!",
        "Regroup, recover, and return stronger!",
    ]
}


# -------------- MAIN CLASS --------------------

class FocusTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Cultivation Realm")

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        self.project_menu_open = False

        window_w = min(900, max(700, screen_w - 50))
        window_h = min(600, max(480, screen_h - 100))

        pos_x = max(0, (screen_w - window_w) // 2)
        pos_y = max(0, (screen_h - window_h) // 2)

        self.root.geometry(f"{window_w}x{window_h}+{pos_x}+{pos_y}")
        self.root.minsize(min(700, window_w), min(480, window_h))
        self.root.resizable(True, True)

        self.root.configure(bg="#171923")
        self.root.overrideredirect(True)
        self.build_custom_titlebar()
        self.build_tray_icon()
        # self.root.bind("<Map>", self.restore_custom_titlebar)
        # print("OK")

        self.duration = 0
        self.start_time = None
        self.end_time = None
        self.running = False
        self.session_finished = False

        self.history = []
        self.mission_board = []
        self.projects = {"General": []}
        self.active_project = "General"
        self.last_getting_started = None
        self.getting_started_streak = 0
        self.after_id = None

        self.xp = 0
        self.level = 0
        self.total_completed_bounties = 0

        if getattr(sys, "frozen", False):
            app_folder = os.path.dirname(sys.executable)
        else:
            app_folder = os.path.dirname(os.path.abspath(__file__))

        self.data_file = os.path.join(app_folder, "cultivation_data.json")

        self.load_data()
        self.setup_styles()
        self.build_main()
        self.update_xp_display()

        # print("OK2.5")
        # self.selected_mission = None
        self.render_mission_board()
        self.render_mission_log()

        # print("OK3")

        self.build_overlay()
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

        self.show_window()
        # print("OK4")

    # region ---------------- STYLES -------------------
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Cultivation.TNotebook",
            background=BG,
            borderwidth=0
        )
        style.configure(
            "Cultivation.TNotebook.Tab",
            background=PANEL,
            foreground=MUTED,
            padding=(18, 9),
            font=("Segoe UI", 9, "bold")
        )
        style.map(
            "Cultivation.TNotebook.Tab",
            background=[("selected", PANEL_ALT)],
            foreground=[("selected", GOLD)]
        )

        style.configure(
            "XP.Horizontal.TProgressbar",
            troughcolor="#252a3a",
            background="#d9a441",
            bordercolor="#252a3a",
            lightcolor="#d9a441",
            darkcolor="#d9a441",
            thickness=9
        )

        style.configure(
            "Timer.Horizontal.TProgressbar",
            troughcolor="#303448",
            background="#8b7cff",
            bordercolor="#202435",
            lightcolor="#8b7cff",
            darkcolor="#8b7cff",
            thickness=7
        )

        self.colors = {
            "background": "#11131d",
            "panel": "#1b1f2e",
            "input": "#252a3a",
            "purple": "#7668e8",
            "purple_hover": "#897df5",
            "gold": "#e5b85c",
            "text": "#f0f0f5",
            "muted": "#969caf",
            "green": "#65cb91",
            "red": "#c44755",
            "border": "#30364b"
        }

        style.configure(
            "Mission.Vertical.TScrollbar",
            background="#393d54",
            troughcolor="#171923",
            bordercolor="#171923",
            arrowcolor="#aab0c0",
            darkcolor="#393d54",
            lightcolor="#393d54"
        )

        style.map(
            "Mission.Vertical.TScrollbar",
            background=[
                # ("active", "#7668e8"),
                ("!active", "#393d54")
            ]
        )

        style.configure(
            "Project.TCombobox",
            fieldbackground=PANEL_ALT,
            background=PANEL_ALT,
            foreground=GOLD,
            arrowcolor=GOLD,
            bordercolor=PANEL_ALT,
            lightcolor=PANEL_ALT,
            darkcolor=PANEL_ALT,
            padding=(8, 6),
            font=("Segoe UI", 9, "bold")
        )

        style.map(
            "Project.TCombobox",
            fieldbackground=[("readonly", PANEL_ALT)],
            foreground=[("readonly", GOLD)],
            selectbackground=[("readonly", PANEL_ALT)],
            selectforeground=[("readonly", GOLD)],
            background=[("active", PANEL)]
        )

    def animate_header_sparkle(self):
        colors = [
            "#8C713E",
            "#C49A50",
            "#E5B85C",
            "#FFE6A3",
            "#E5B85C",
            "#C49A50"
        ]

        if not self.root.winfo_exists():
            return

        step = getattr(self, "_sparkle_step", 0)
        self.header_sparkle.config(fg=colors[step])
        self._sparkle_step = (step + 1) % len(colors)
        self.root.after(180, self.animate_header_sparkle)

    def pulse_reset_border(self, reset_btn):
        colors = [
            "#997a45",
            "#b99a63",
            "#d6b778",
            "#f0d49a",
            "#d6b778",
            "#b99a63"
        ]

        index = 0

        def pulse():
            nonlocal index

            if not reset_btn.winfo_exists():
                return

            reset_btn.configure(fg=colors[index])
            index = (index + 1) % len(colors)

            reset_btn.after(120, pulse)

        pulse()
   
    def effect_shake(self, popup: tk.Toplevel, width, height):
        original_x = (popup.winfo_screenwidth() - width) // 2
        original_y = (popup.winfo_screenheight() - height) // 2

        def shake(step=0):
            if not popup.winfo_exists() or step >= 10:
                return

            offset = random.randint(-6, 6)

            popup.geometry(
                f"+{original_x + offset}+{original_y + offset}"
            )

            popup.after(35, lambda: shake(step + 1))
        popup.after(100, shake)

    # endregion
    
    # region ---------------- TITLE BAR ----------------

    def build_custom_titlebar(self):

        titlebar = tk.Frame(
            self.root,
            bg="#211D35",
            height=38
        )
        titlebar.pack(fill="x")
        titlebar.pack_propagate(False)

        # Left section
        left = tk.Frame(titlebar, bg="#211D35")
        left.pack(side="left", fill="y", padx=12)

        self.header_sparkle = tk.Label(
            left,
            text="✦",
            fg="#E5B85C",
            bg="#211D35",
            font=("Segoe UI", 13, "bold")
        )

        self.header_sparkle.pack(side="left", padx=(0, 7))
        self.animate_header_sparkle()

        tk.Label(
            left,
            text="CULTIVATION REALM",
            font=("Segoe UI", 9, "bold"),
            fg="#D8C9FF",
            bg="#211D35"
        ).pack(side="left")

        # Window controls
        controls = tk.Frame(titlebar, bg="#211D35")
        controls.pack(side="right", fill="y")

        def make_button(text, command, hover, width=4):
            btn = tk.Button(
                controls,
                text=text,
                command=command,
                bg="#211D35",
                fg="#D8D5E5",
                activebackground=hover,
                activeforeground="white",
                relief="flat",
                bd=0,
                width=width,
                font=("Segoe UI", 10),
                cursor="hand2"
            )
            btn.pack(side="left", fill="y")

            btn.bind(
                "<Enter>",
                lambda e: btn.config(bg=hover)
            )
            btn.bind(
                "<Leave>",
                lambda e: btn.config(bg="#211D35")
            )

            return btn

        make_button("—", self.minimize_window, "#39334D")
        make_button("□", self.toggle_maximize, "#39334D")
        make_button("✕", self.close_app, "#B94B5A")

        # Window dragging
        def start_move(event):
            self._drag_x = event.x_root - self.root.winfo_x()
            self._drag_y = event.y_root - self.root.winfo_y()

        def move_window(event):
            x = event.x_root - self._drag_x
            y = event.y_root - self._drag_y

            self.root.geometry(f"+{x}+{y}")

        for widget in (titlebar, left):
            widget.bind("<Button-1>", start_move)
            widget.bind("<B1-Motion>", move_window)
    
    def minimize_window(self):
        self.root.withdraw()
        self.tray_icon.visible = True
        
        if not self.running:
            return

        self.overlay.deiconify()
        self.overlay.lift()

    def show_window(self, event=None):
        self.root.deiconify()
        self.root.state("zoomed")
        self.root.lift()
        self.root.focus_force()
        self.root.overrideredirect(True)
        self.tray_icon.visible = True
        
        if self.running:
            self.status_label.config(
                text="Session still running. Keep going!"
            )

    def toggle_maximize(self):
        if not hasattr(self, "is_maximized"):
            self.is_maximized = False

        if self.is_maximized:
            self.root.state("normal")
            self.root.geometry(self.normal_geometry)
            self.is_maximized = False

        else:
            self.normal_geometry = self.root.geometry()
            self.root.state("zoomed")
            self.is_maximized = True
 
    def restore_custom_titlebar(self, event=None):
        if self.root.winfo_exists():
            self.root.after(
                100,
                lambda: self.root.overrideredirect(True)
                if self.root.winfo_exists() else None
            )
   
    def create_tray_image(self):

        image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        gold = "#E5B85C"

        # Four-point sparkle
        points = [
            (32, 3),
            (39, 24),
            (61, 32),
            (39, 40),
            (32, 61),
            (25, 40),
            (3, 32),
            (25, 24)
        ]

        draw.polygon(points, fill=gold)

        return image
 
    def build_tray_icon(self):
        image = self.create_tray_image()

        menu = pystray.Menu(
            pystray.MenuItem(
                "Open Cultivation Realm",
                lambda icon, item: self.root.after(0, self.show_window),
                default=True
            ),
            pystray.MenuItem(
                "Exit",
                lambda icon, item: self.root.after(0, self.close_app)
            )
        )

        self.tray_icon = pystray.Icon(
            "Cultivation Realm",
            image,
            "Cultivation Realm",
            menu
        )

        # Make the icon visible after initialization
        def setup(icon):
            icon.visible = True

        self.tray_icon.run_detached(setup=setup)
  
    def close_app(self):
        if self.after_id:
            self.root.after_cancel(self.after_id)

        self.save_data()
        self.tray_icon.stop()
        self.root.destroy()
    
    # endregion

    # region ---------------- MAIN WINDOW ----------------

    def build_main(self):
        """Build a compact cultivation dashboard with a tabbed layout and bounty board."""

        # ---------- PALETTE ----------
        self.root.configure(bg=BG)
        self.root.minsize(760, 560)

        # ---------- HELPERS ----------
        def make_card(parent, title, subtitle=None):
            card = tk.Frame(
                parent,
                bg=PANEL,
                highlightbackground=BORDER,
                highlightthickness=1
            )
            heading = tk.Frame(card, bg=PANEL)
            heading.pack(fill="x", padx=12, pady=(10, 5))

            tk.Label(
                heading,
                text=title.upper(),
                bg=PANEL,
                fg=GOLD,
                font=("Segoe UI", 9, "bold")
            ).pack(anchor="w")

            if subtitle:
                tk.Label(
                    heading,
                    text=subtitle,
                    bg=PANEL,
                    fg=MUTED,
                    font=("Segoe UI", 8)
                ).pack(anchor="w", pady=(2, 0))

            content = tk.Frame(card, bg=PANEL)
            content.pack(fill="both", expand=True, padx=12, pady=(4, 12))
            return card, content

        def make_button(parent, label, command, bg=PURPLE, fg = "#11131A", compact=False):
            return tk.Button(
                parent,
                text=label,
                command=command,
                bg=bg,
                fg=fg,
                activebackground=TEXT,
                activeforeground=BG,
                relief="flat",
                bd=0,
                cursor="hand2",
                font=("Segoe UI", 8 if compact else 9, "bold"),
                padx=10 if compact else 14,
                pady=5 if compact else 8
            )

        def add_hover(widget, normal, hover):
            widget.bind("<Enter>", lambda e: widget.configure(bg=hover))
            widget.bind("<Leave>", lambda e: widget.configure(bg=normal))

        # ---------- HEADER ----------
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=18, pady=(12, 8))

        # Quote Label Header
        quote_label = tk.Label(
            header,
            text=HEADER_QUOTES[0],
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 8, "bold"),
            cursor="hand2"
        )

        quote_label.pack(side="right", pady=(8, 0))
        def change_quote(event=None):
            current = quote_label.cget("text")

            try:
                index = HEADER_QUOTES.index(current)
                next_index = (index + 1) % len(HEADER_QUOTES)
            except ValueError:
                next_index = 0

            quote_label.config(text=HEADER_QUOTES[next_index])

        def reset_quote(event=None):
            quote_label.config(text=HEADER_QUOTES[0])

        quote_label.bind("<Button-1>", change_quote)
        quote_label.bind("<Button-3>", reset_quote)


        # ---------- NOTEBOOK ----------
        notebook = ttk.Notebook(
            self.root,
            style="Cultivation.TNotebook"
        )
        notebook.pack(fill="both", expand=True, padx=14, pady=(0, 10))

        dashboard_tab = tk.Frame(notebook, bg=BG)
        bounty_tab = tk.Frame(notebook, bg=BG)
        chronicle_tab = tk.Frame(notebook, bg=BG)

        notebook.add(dashboard_tab, text="  ✦ DASHBOARD  ")
        notebook.add(bounty_tab, text="  ⚔ BOUNTY BOARD  ")
        notebook.add(chronicle_tab, text="  📜 CHRONICLE  ")

        # ==========================================================
        # region DASHBOARD TAB
        # ==========================================================
        dashboard_tab.columnconfigure(0, weight=1)
        dashboard_tab.columnconfigure(1, weight=1)
        dashboard_tab.rowconfigure(0, weight=1)

        left = tk.Frame(dashboard_tab, bg=BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(8, 5), pady=8)

        right = tk.Frame(dashboard_tab, bg=BG)
        right.grid(row=0, column=1, sticky="nsew", padx=(5, 8), pady=8)

        # Cultivation rank
        rank_card, rank_content = make_card(
            left, "Cultivation Realm", "Your current path to mastery"
        )
        rank_card.pack(fill="x", pady=(0, 8))

        self.rank_label = tk.Label(
            rank_content,
            text="Novice Cultivator",
            bg=PANEL,
            fg=PURPLE,
            font=("Segoe UI", 16, "bold")
        )
        self.rank_label.pack(anchor="w")

        self.level_label = tk.Label(
            rank_content,
            text="LEVEL 0",
            bg=PANEL,
            fg=TEXT,
            font=("Segoe UI", 9, "bold")
        )
        self.level_label.pack(anchor="w", pady=(3, 0))

        # Realm description
        self.rank_description = tk.Label(
            rank_content,
            text="You are but an ordinary mortal.",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 8),
            anchor="w"
        )
        self.rank_description.pack(fill="x", pady=(3, 10))

        # XP + percentage
        xp_header = tk.Frame(rank_content, bg=PANEL)
        xp_header.pack(fill="x")

        self.xp_label = tk.Label(
            xp_header,
            text="5 / 50 XP",
            bg=PANEL,
            fg=GOLD,
            font=("Segoe UI", 10, "bold")
        )
        self.xp_label.pack(side="left")

        self.xp_percentage_label = tk.Label(
            xp_header,
            text="10%",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 8)
        )
        self.xp_percentage_label.pack(side="right")

        # Progress bar styling
        style = ttk.Style()

        style.configure(
            "Cultivation.Horizontal.TProgressbar",
            troughcolor="#303548",
            background=PURPLE,
            bordercolor="#303548",
            lightcolor=PURPLE,
            darkcolor=PURPLE,
            thickness=9
        )

        self.xp_progress = ttk.Progressbar(
            rank_content,
            orient="horizontal",
            mode="determinate",
            maximum=100,
            style="Cultivation.Horizontal.TProgressbar"
        )
        self.xp_progress.pack(fill="x", pady=(5, 4))

        # Remaining XP
        self.total_xp_label = tk.Label(
            rank_content,
            text="45 XP to next level",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 8)
        )
        self.total_xp_label.pack(anchor="w")

        # Separator
        tk.Frame(
            rank_content,
            bg=BORDER,
            height=1
        ).pack(fill="x", pady=(10, 8))

        # Next breakthrough
        self.next_realm_label = tk.Label(
            rank_content,
            text="✦  NEXT BREAKTHROUGH: THE PATH OF INITIATION",
            bg=PANEL,
            fg=GOLD,
            font=("Segoe UI", 9, "bold"),
            anchor="w",
            justify="left"
        )
        self.next_realm_label.pack(fill="x")

        # region DAILY STREAK & LIFETIME XP

        stats_frame = tk.Frame(left, bg=BG)
        stats_frame.pack(fill="x", pady=(0, 8))

        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(2, weight=1)

        # DAILY STREAK
        streak_card, streak_content = make_card(
            stats_frame, "Daily Streak", "Consistency"
        )
        streak_card.grid(row=0, column=0, sticky="nsew", padx=(0, 4))

        self.dashboard_streak_card = tk.Label(
            streak_content,
            text=f"🔥  {self.getting_started_streak} "
                f"{'day' if self.getting_started_streak == 1 else 'days'}",
            bg=PANEL,
            fg=GOLD,
            font=("Segoe UI", 17, "bold")
        )
        
        self.dashboard_streak_card.pack(anchor="w")

        # LIFETIME XP
        lifetime_card, lifetime_content = make_card(
            stats_frame, "Lifetime XP", "Total earned"
        )
        lifetime_card.grid(row=0, column=1, sticky="nsew", padx=(4, 0))

        self.dashboard_xp_card = tk.Label(
            lifetime_content,
            text=f"✦  {self.xp} XP",
            bg=PANEL,
            fg=GOLD,
            font=("Segoe UI", 17, "bold")
        )
        
        self.dashboard_xp_card.pack(anchor="w")

        # TOTAL BOUNTIES
        total_bounties_card, total_bounties_content = make_card(
            stats_frame, "Bounties Completed", "Total victories"
        )
        total_bounties_card.grid(row=0, column=2, sticky="nsew", padx=(4, 0))

        self.dashboard_bounty_card = tk.Label(
            total_bounties_content,
            text=f"⚔  {self.total_completed_bounties} "
                f"{'Bounty' if self.total_completed_bounties == 1 else 'Bounties'}",
            bg=PANEL,
            fg=GOLD,
            font=("Segoe UI", 17, "bold")
        )

        self.dashboard_bounty_card.pack(anchor="w")

        # endregion

        # region ---------- COMPACT MISSION CREATION ----------
        task_card, task_content = make_card(
            left, "New Bounty", "Prepare your next cultivation session"
        )
        task_card.pack(fill="x", pady=(0, 8))

        # Mission name
        tk.Label(
            task_content,
            text="BOUNTY NAME",
            bg=PANEL, fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        self.task_var = getattr(self, "task_var", tk.StringVar())

        self.task_entry = tk.Entry(
            task_content,
            textvariable=self.task_var,
            bg=PANEL_ALT, fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=("Segoe UI", 9)
        )
        self.task_entry.pack(fill="x", pady=(3, 8), ipady=4)

        # Duration and reward side by side
        fields = tk.Frame(task_content, bg=PANEL)
        fields.pack(fill="x")

        fields.columnconfigure(0, weight=1)
        fields.columnconfigure(1, weight=1)

        # Duration
        duration_frame = tk.Frame(fields, bg=PANEL)
        duration_frame.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        tk.Label(
            duration_frame,
            text="DURATION (MIN)",
            bg=PANEL, fg=MUTED,
            font=("Segoe UI", 7, "bold")
        ).pack(anchor="w")

        self.minutes_var = getattr(
            self, "minutes_var", tk.StringVar(value="25")
        )

        self.minutes_entry = tk.Entry(
            duration_frame,
            textvariable=self.minutes_var,
            bg=PANEL_ALT, fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=("Segoe UI", 9)
        )
        self.minutes_entry.pack(fill="x", pady=(3, 0), ipady=4)

        # XP reward
        reward_frame = tk.Frame(fields, bg=PANEL)
        reward_frame.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        tk.Label(
            reward_frame,
            text="XP REWARD",
            bg=PANEL, fg=GOLD,
            font=("Segoe UI", 7, "bold")
        ).pack(anchor="w")

        self.reward_var = getattr(
            self, "reward_var", tk.StringVar(value="50")
        )

        self.reward_entry = tk.Entry(
            reward_frame,
            textvariable=self.reward_var,
            bg=PANEL_ALT, fg=GOLD,
            insertbackground=TEXT,
            relief="flat",
            font=("Segoe UI", 9)
        )
        self.reward_entry.pack(fill="x", pady=(3, 0), ipady=4)

        # Daily checkbox and quick duration presets
        bottom_row = tk.Frame(task_content, bg=PANEL)
        bottom_row.pack(fill="x", pady=(7, 0))

        self.daily_var = getattr(
            self, "daily_var", tk.BooleanVar(value=False)
        )

        daily_check = tk.Checkbutton(
            bottom_row,
            text="♻ Daily",
            variable=self.daily_var,
            bg=PANEL,
            fg=GREEN,
            activebackground=PANEL,
            activeforeground=GREEN,
            selectcolor=PANEL_ALT,
            font=("Segoe UI", 8, "bold"),
            padx=0,
            pady=0,
            cursor="hand2"
        )
        daily_check.pack(side="left")

        presets = tk.Frame(bottom_row, bg=PANEL)
        presets.pack(side="right")

        for duration in (25, 45, 60, 90):
            btn = make_button(
                presets,
                str(duration),
                lambda d=duration: self.minutes_var.set(str(d)),
                bg=PANEL_ALT,
                compact=True
            )
            btn.configure(
                fg=TEXT,
                padx=7,
                pady=3,
                font=("Segoe UI", 7, "bold")
            )
            btn.pack(side="left", padx=(3, 0))

        # Post bounty
        make_button(
            task_content,
            "✦ POST BOUNTY",
            self.add_mission,
            GOLD,
            compact=True
        ).pack(fill="x", pady=(9, 0))
        
        # endregion 

        # region Mission controls
        
        control_card, control_content = make_card(
            right, "Cultivation", "Choose your path and begin your training"
        ) #"Focus begins with a single decision"
        control_card.pack(fill="x", pady=(0, 8))

        duration_frame = tk.Frame(control_content, bg=PANEL)
        duration_frame.pack(fill="x", pady=(10, 8))

        tk.Label(
            duration_frame,
            text="CULTIVATION DURATION (MIN)",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        self.control_minutes_var = getattr(
            self, "control_minutes_var", tk.StringVar(value="25")
        )

        self.control_minutes_entry = tk.Entry(
            duration_frame,
            textvariable=self.control_minutes_var,
            bg=PANEL_ALT,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=("Segoe UI", 9)
        )
        self.control_minutes_entry.pack(
            fill="x", pady=(3, 5), ipady=4
        )

        # Quick duration presets
        duration_presets = tk.Frame(duration_frame, bg=PANEL)
        duration_presets.pack(fill="x")

        for duration in (5, 10, 25, 30, 45):
            btn = make_button(
                duration_presets,
                f"{duration}m",
                lambda d=duration: self.control_minutes_var.set(str(d)),
                bg=PANEL_ALT,
                compact=True
            )
            btn.configure(
                fg=TEXT,
                padx=7,
                pady=3,
                font=("Segoe UI", 7, "bold")
            )
            btn.pack(side="left", expand=True, fill="x", padx=2)
            
        self.start_button = make_button(
            control_content, "▶  BEGIN CULTIVATION",
            self.start_session, GREEN
        )
        self.start_button.pack(fill="x", pady=(10, 6))

        self.stop_button = make_button(
            control_content, "■  END CULTIVATION",
            self.stop_session, RED
        )
        self.stop_button.pack(fill="x", pady=(0, 6))

        self.hide_button = make_button(
            control_content, "MINIMIZE",
            self.minimize_window,
            PANEL_ALT
        )
        self.hide_button.configure(fg=TEXT)
        self.hide_button.pack(fill="x")

        # endregion

        # region Status footer
        self.status_label = tk.Label(
            dashboard_tab,
            text="✦  Your cultivation journey awaits.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 8)
        )
        self.status_label.grid(
            row=1, column=0, columnspan=2,
            sticky="w", padx=12, pady=(0, 8)
        )

        # endregion
        
        # endregion

        # ==========================================================
        # region BOUNTY BOARD TAB
        # ==========================================================
        bounty_tab.rowconfigure(1, weight=1)
        bounty_tab.columnconfigure(0, weight=1)

        bounty_header = tk.Frame(bounty_tab, bg=BG)
        bounty_header.grid(row=0, column=0, sticky="ew", padx=12, pady=10)

        tk.Label(
            bounty_header,
            text="THE BOUNTY BOARD",
            bg=BG,
            fg=GOLD,
            font=("Segoe UI", 15, "bold")
        ).pack(anchor="w")

        tk.Label(
            bounty_header,
            text="Accept missions. Complete them. Claim your rewards.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 8)
        ).pack(anchor="w", pady=(3, 0))

        board = tk.Frame(bounty_tab, bg=BG)
        board.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 8))

        for col in range(3):
            board.columnconfigure(col, weight=1)
        board.rowconfigure(0, weight=1)

        self.mission_rows = {}

        status_columns = [
            ("CURRENT", PURPLE),
            ("COMPLETED", GREEN),
            ("POSTPONED", GOLD)
        ]

        self.mission_canvases = {}
        for col, (status, accent) in enumerate(status_columns):
            column = tk.Frame(
                board,
                bg=PANEL,
                highlightbackground=BORDER,
                highlightthickness=1
            )
            column.grid(
                row=0, column=col, sticky="nsew",
                padx=4, pady=4
            )

            top = tk.Frame(column, bg=PANEL)
            top.pack(fill="x", padx=9, pady=9)

            tk.Label(
                top,
                text=status,
                bg=PANEL,
                fg=accent,
                font=("Segoe UI", 9, "bold")
            ).pack(side="left")

            # Scrollable mission area
            scroll_container = tk.Frame(column, bg=PANEL)
            scroll_container.pack(
                fill="both", expand=True, padx=7, pady=(0, 8)
            )

            mission_canvas = tk.Canvas(
                scroll_container,
                bg=PANEL,
                highlightthickness=0
            )
            mission_canvas.pack(side="left", fill="both", expand=True)

            mission_scrollbar = ttk.Scrollbar(
                scroll_container,
                orient="vertical",
                command=mission_canvas.yview,
                style="Mission.Vertical.TScrollbar"
            )
            mission_scrollbar.pack(side="right", fill="y")

            mission_canvas.configure(
                yscrollcommand=mission_scrollbar.set
            )

            # Frame that actually lives inside the Canvas
            mission_content = tk.Frame(mission_canvas, bg=PANEL)

            # When creating each mission canvas:
            self.mission_canvases[status.lower()] = mission_canvas
            mission_window = mission_canvas.create_window(
                (0, 0),
                window=mission_content,
                anchor="nw"
            )

            # Update scroll region when content changes
            mission_content.bind(
                "<Configure>",
                lambda event: mission_canvas.configure(
                    scrollregion=mission_canvas.bbox("all")
                )
            )

            # Keep embedded Frame as wide as Canvas
            mission_canvas.bind(
                "<Configure>",
                lambda event: mission_canvas.itemconfigure(
                    mission_window, width=event.width
                )
            )

            mission_inner = tk.Frame(mission_canvas, bg=PANEL)
            mission_window = mission_canvas.create_window(
                (0, 0),
                window=mission_inner,
                anchor="nw"
            )

            self.scroll_on_wheel(mission_canvas, mission_inner) # MISSION BOARD

            def update_scrollbar(event=None, canvas=mission_canvas,
                                inner=mission_inner, scrollbar=mission_scrollbar):

                canvas.configure(scrollregion=canvas.bbox("all"))

                content_height = inner.winfo_reqheight()
                visible_height = canvas.winfo_height()

                if content_height > visible_height:
                    if not scrollbar.winfo_ismapped():
                        scrollbar.pack(side="right", fill="y")
                else:
                    scrollbar.pack_forget()

            mission_inner.bind(
                "<Configure>",
                update_scrollbar
            )

            mission_canvas.bind(
                "<Configure>",
                lambda e, c=mission_canvas, w=mission_window:
                    (
                        c.itemconfigure(w, width=e.width),
                        update_scrollbar()
                    )
            )

            self.mission_rows[status.lower()] = mission_inner


        # Project and mission actions
        actions = tk.Frame(bounty_tab, bg=BG)
        actions.grid(row=2, column=0, sticky="ew", padx=12, pady=(4, 12))

        self.project_var = tk.StringVar(value=self.active_project)
        self.project_picker = tk.Frame(
            actions,
            bg="#222A3D",
            highlightbackground="#303A52",
            highlightthickness=1,
            cursor="hand2"
        )

        self.project_picker.pack(side="left", padx=(0, 6))

        self.project_label = tk.Label(
            self.project_picker,
            textvariable=self.project_var,
            bg="#222A3D",
            fg="#E8EAF2",
            font=("Segoe UI", 9),
            padx=10,
            pady=6,
            cursor="hand2"
        )
        self.project_label.pack(side="left")
        self.project_arrow = tk.Label(
            self.project_picker,
            text="▾",
            bg="#222A3D",
            fg="#929BB2",
            font=("Segoe UI Symbol", 10),
            padx=9,
            pady=5,
            cursor="hand2"
        )
        self.project_arrow.pack(side="left")

        # Click handling
        for widget in (
            self.project_picker,
            self.project_label,
            self.project_arrow
        ):
            widget.bind("<Button-1>", self.render_show_project_menu)

            widget.bind(
                "<Enter>",
                lambda e: self.project_picker.config(bg="#303A52")
            )

            widget.bind(
                "<Leave>",
                lambda e: self.project_picker.config(bg="#222A3D")
            )

        make_button(
            actions, "+ SECT", self.render_add_project_popup,
            PANEL, fg=TEXT, compact=True
        ).pack(side="left", padx=3)

        make_button(
            actions, "EDIT NOTES", self.render_edit_mission_markdown_popup,
            PANEL, fg=TEXT, compact=True
        ).pack(side="left", padx=3)

        # endregion

        # ==========================================================
        # region CHRONICLE TAB
        # ==========================================================
        chronicle_tab.rowconfigure(0, weight=1)
        chronicle_tab.columnconfigure(0, weight=1)

        chronicle_card, chronicle_content = make_card(
            chronicle_tab,
            "Cultivation Chronicle",
            "A record of your completed sessions and progress"
        )

        chronicle_card.grid(
            row=0, column=0, sticky="nsew",
            padx=12, pady=12
        )

        # Header action button
        reset_border =  tk.Frame(
            chronicle_card,
            bg="#b99a63",
            padx=2,
            pady=2
        )

        reset_border.place(relx=0.99, y=12, anchor="ne")

        # Actual button
        reset_btn = tk.Button(
            reset_border,
            text="✦  RESET CULTIVATION",
            font=("Georgia", 9, "bold"),
            bg="#171923",
            fg="#b99a63",
            activebackground="#292536",
            activeforeground="#e5c58b",
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            padx=14,
            pady=7,
            command=self.confirm_reset_cultivation
        )

        reset_btn.pack()

        # Subtle hover effect
        def on_reset_enter(event):
            reset_btn.configure(
                bg="#242638",
                fg="#e6c98e",
                highlightbackground="#b99a63"
            )

        def on_reset_leave(event):
            reset_btn.configure(
                bg="#171923",
                fg="#b99a63",
                highlightbackground="#665337"
            )

        reset_btn.bind("<Enter>", on_reset_enter)
        reset_btn.bind("<Leave>", on_reset_leave)
        self.pulse_reset_border(reset_btn)
        
        chronicle_content.pack_propagate(False)

        log_frame = tk.Frame(chronicle_content, bg=PANEL)
        log_frame.pack(fill="both", expand=True)

        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)

        self.log_canvas = tk.Canvas(
            log_frame,
            bg=PANEL,
            highlightthickness=0
        )
        self.log_canvas.grid(row=0, column=0, sticky="nsew")
        self.log_inner = tk.Frame(
            self.log_canvas,
            bg=PANEL
        )

        self.log_window = self.log_canvas.create_window(
            (0, 0),
            window=self.log_inner,
            anchor="nw"
        )

        def resize_log(event):
            self.log_canvas.itemconfigure(
                self.log_window,
                width=event.width,
                height=max(
                    event.height,
                    self.log_inner.winfo_reqheight()
                )
            )

        self.log_canvas.bind("<Configure>", resize_log)

        self.log_inner.bind(
            "<Configure>",
            lambda e: self.log_canvas.configure(
                scrollregion=self.log_canvas.bbox("all")
            )
        )

        # endregion
        # ---------- ANIMATION ----------
        self._accent_animation_id = None

        def animate_accent():
            try:
                if not self.root.winfo_exists():
                    return
                current = self.rank_label.cget("fg")
                next_color = GOLD if current == PURPLE else PURPLE
                self.rank_label.configure(fg=next_color)
                self._accent_animation_id = self.root.after(
                    900, animate_accent
                )
            except tk.TclError:
                return

        animate_accent()

        # ---------- INITIAL REFRESH ----------
        self.update_xp_display()
        # self.refresh_missions()

    def render_mission_board(self, reset=False):
        self.refresh_project_picker()
        today_str = date.today().isoformat()
        scroll_positions = {}

        for status, container in self.mission_rows.items():
            canvas = self.mission_canvases[status]
            if not reset:
                scroll_positions[status] = canvas.yview()[0]
            else:
                scroll_positions[status] = 0
        
        # Clear columns
        for container in self.mission_rows.values():
            for child in container.winfo_children():
                child.destroy()

        missions = self.current_missions()
        grouped = {
            "current": [],
            "completed": [],
            "postponed": []
        }

        for item in missions:
            status = item.get("status", "current").lower()

            if status not in grouped:
                status = "current"

            is_daily = item.get("is_daily", False)
            last_done = item.get("last_done_date")
            streak = item.get("streak_count", 0)

            done_today = (
                is_daily and last_done == today_str
            )

            if done_today:
                status = "completed"

            grouped[status].append(item)

        # Render columns
        for status, container in self.mission_rows.items():
            status_missions = grouped[status]

            if not status_missions:
                tk.Label(
                    container,
                    text="No bounties here",
                    bg="#1A2030",
                    fg="#929BB2",
                    font=("Segoe UI", 8, "italic")
                ).pack(pady=12)
                continue

            for item in status_missions:
                is_daily = item.get("is_daily", False)
                last_done = item.get("last_done_date")
                streak = item.get("streak_count", 0)

                done_today = (
                    is_daily and last_done == today_str
                )

                # Card
                card = tk.Frame(
                    container,
                    bg="#222A3D",
                    highlightbackground=(
                        "#65D6A0" if done_today
                        else "#8B72DC" if is_daily
                        else "#303A52"
                    ),
                    highlightthickness=1
                )
                card.pack(fill="x", pady=4)

                # Mission header
                header = tk.Frame(card, bg="#222A3D")
                header.pack(fill="x", padx=8, pady=(7, 3))

                tk.Label(
                    header,
                    text=item.get("task"),
                    bg="#222A3D",
                    fg="#E8EAF2",
                    font=("Segoe UI", 9, "bold"),
                    anchor="w",
                    wraplength=170,
                    justify="left"
                ).pack(side="left", fill="x", expand=True)

                # Mission type badge
                if is_daily:
                    badge_text = "♻ DAILY"
                    badge_bg = "#244D43"
                    badge_fg = "#65D6A0"
                else:
                    badge_text = "◆ STANDARD"
                    badge_bg = "#293B5B"
                    badge_fg = "#91B9FF"

                tk.Label(
                    header,
                    text=badge_text,
                    bg=badge_bg,
                    fg=badge_fg,
                    font=("Segoe UI", 7, "bold"),
                    padx=6,
                    pady=3
                ).pack(side="right", padx=(4, 0))

                # Divider
                tk.Frame(
                    card,
                    bg="#354057",
                    height=1
                ).pack(fill="x", padx=8, pady=3)

                # Duration and reward
                details = tk.Frame(card, bg="#222A3D")
                details.pack(fill="x", padx=8, pady=3)

                tk.Label(
                    details,
                    text=f"◷ {item.get('duration', 45)} min",
                    bg="#222A3D",
                    fg="#AAB0C0",
                    font=("Segoe UI", 8)
                ).pack(side="left")

                tk.Label(
                    details,
                    text=f"✦ {item.get('reward_xp', 0)} XP",
                    bg="#222A3D",
                    fg="#F5C66A",
                    font=("Segoe UI", 8, "bold")
                ).pack(side="right")

                # Daily streak section
                if is_daily:
                    streak_frame = tk.Frame(
                        card,
                        bg="#302B43",
                        highlightbackground="#51446F",
                        highlightthickness=1
                    )
                    streak_frame.pack(
                        fill="x",
                        padx=7,
                        pady=(5, 4)
                    )

                    # Streak header
                    streak_header = tk.Frame(
                        streak_frame,
                        bg="#302B43"
                    )
                    streak_header.pack(
                        fill="x",
                        padx=7,
                        pady=(5, 2)
                    )

                    tk.Label(
                        streak_header,
                        text="🔥 CULTIVATION STREAK",
                        bg="#302B43",
                        fg="#F5C66A",
                        font=("Segoe UI", 7, "bold")
                    ).pack(side="left")

                    tk.Label(
                        streak_header,
                        text=f"{streak} DAYS",
                        bg="#51412E",
                        fg="#F5D98A",
                        font=("Segoe UI", 7, "bold"),
                        padx=6,
                        pady=2
                    ).pack(side="right")

                    # Last completion status
                    if done_today:
                        completion_text = "✓ COMPLETED TODAY"
                        completion_color = "#65D6A0"
                        completion_bg = "#1E493B"
                    else:
                        completion_text = "○ AVAILABLE TODAY"
                        completion_color = "#BDB5D5"
                        completion_bg = "#39334D"

                    tk.Label(
                        streak_frame,
                        text=completion_text,
                        bg=completion_bg,
                        fg=completion_color,
                        font=("Segoe UI", 8, "bold"),
                        anchor="w",
                        padx=7,
                        pady=5
                    ).pack(fill="x", padx=6, pady=(2, 5))

                    # Last done date
                    last_done_text = (
                        f"Last completed: {last_done}"
                        if last_done
                        else "Last completed: Never"
                    )

                    tk.Label(
                        streak_frame,
                        text=last_done_text,
                        bg="#302B43",
                        fg="#65D6A0" if done_today else "#929BB2",
                        font=("Segoe UI", 7),
                        anchor="w"
                    ).pack(fill="x", padx=7, pady=(0, 6))

                # Normal completed mission date
                elif status == "completed":
                    completed_date = item.get(
                        "completed_date", "Unknown"
                    )

                    tk.Label(
                        card,
                        text=f"✓ Completed: {completed_date}",
                        bg="#222A3D",
                        fg="#65D6A0",
                        font=("Segoe UI", 7),
                        anchor="w"
                    ).pack(fill="x", padx=8, pady=4)

                # Action buttons
                buttons = tk.Frame(card, bg="#222A3D")
                buttons.pack(fill="x", padx=5, pady=(5, 7))

                if status == "current":
                    tk.Button(
                        buttons,
                        text="COMPLETE",
                        command=lambda m=item: self.change_mission_status(
                            m, "completed"
                        ),
                        bg="#65D6A0",
                        fg="#10131D",
                        relief="flat",
                        cursor="hand2",
                        font=("Segoe UI", 7, "bold"),
                        padx=7,
                        pady=3
                    ).pack(side="left", padx=2)

                    tk.Button(
                        buttons,
                        text="POSTPONE",
                        command=lambda m=item: self.change_mission_status(
                            m, "postponed"
                        ),
                        bg="#F5C66A",
                        fg="#10131D",
                        relief="flat",
                        cursor="hand2",
                        font=("Segoe UI", 7, "bold"),
                        padx=7,
                        pady=3
                    ).pack(side="left", padx=2)
                else:
                    if done_today:
                        tk.Label(
                            buttons,
                            text="✦ BOUNTY CLAIMED",
                            bg="#222A3D",
                            fg="#65D6A0",
                            font=("Segoe UI", 7, "bold")
                        ).pack(side="left", padx=3)

                        # Undo today's daily completion
                        tk.Button(
                            buttons,
                            text="↶ UNDO COMPLETION",
                            command=lambda m=item: self.undo_daily_completion(m),
                            bg="#D69A65",
                            fg="#10131D",
                            relief="flat",
                            cursor="hand2",
                            font=("Segoe UI", 7, "bold"),
                            padx=7,
                            pady=3
                        ).pack(side="left", padx=2)
                    else:
                        tk.Button(
                            buttons,
                            text="RESTORE",
                            command=lambda m=item: self.change_mission_status(
                                m, "current"
                            ),
                            bg="#A78BFA",
                            fg="#10131D",
                            relief="flat",
                            cursor="hand2",
                            font=("Segoe UI", 7, "bold"),
                            padx=7,
                            pady=3
                        ).pack(side="left", padx=2)
                
                # Reset streak only when there is a streak
                if is_daily and streak > 0:
                    tk.Button(
                        buttons,
                        text="RESET STREAK",
                        command=lambda m=item: self.reset_daily_streak(m, done_today),
                        bg="#F57D6A",
                        fg="#10131D",
                        relief="flat",
                        cursor="hand2",
                        font=("Segoe UI", 7, "bold"),
                        padx=7,
                        pady=3
                    ).pack(side="left", padx=2)

                tk.Button(
                    buttons,
                    text="✕ DELETE",
                    command=lambda m=item: self.confirm_remove_mission(m),
                    bg="#E87979",
                    fg="#10131D",
                    relief="flat",
                    cursor="hand2",
                    font=("Segoe UI", 7, "bold"),
                    padx=7,
                    pady=3
                ).pack(side="right", padx=2)

        def restore_scroll():
            for status, position in scroll_positions.items():
                canvas = self.mission_canvases[status]
                canvas.update_idletasks()
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.yview_moveto(position)

        self.root.after_idle(restore_scroll)

    def render_mission_log(self):
        for child in self.log_inner.winfo_children():
            child.destroy()

        # ==============================
        # DAILY DISCIPLINE SUMMARY
        # ==============================
        today = datetime.now().date()

        today_entries = [
            entry for entry in self.history
            if isinstance(entry, dict)
            and str(entry.get("date")).startswith(today.isoformat())
        ]

        latest_bounties = {}

        for entry in sorted(
            (e for e in self.history if isinstance(e, dict)),
            key=lambda e: str(e.get("date", ""))
        ):
            project = entry.get("project")

            if project is not None:
                latest_bounties[project] = entry

        today_bounties = sum(
            1 for entry in latest_bounties.values()
            if entry.get("status") == "COMPLETED"
            and str(entry.get("date", "")).startswith(today.isoformat())
        )

        today_sessions = sum(
            1 for entry in today_entries
            if entry.get("project") is None and entry.get("xp") > 0
        )

        today_focused = 0

        for entry in today_entries:
            duration = entry.get("duration", 0)

            if isinstance(duration, str):
                minutes, _, seconds = duration.partition("m ")
                today_focused += int(minutes or 0) + (
                    int(seconds.replace("s", "") or 0) / 60
                )
            else:
                today_focused += int(duration or 0)
                
        today_xp = sum(
            int(entry.get("xp", 0))
            for entry in today_entries
            if str(entry.get("xp", 0)).isdigit()
        )

        summary = tk.Frame(
            self.log_inner,
            bg="#242638",
            highlightbackground="#393d54",
            highlightthickness=1
        )
        summary.pack(fill="x", padx=2, pady=(2, 12))

        tk.Label(
            summary,
            text="DAILY DISCIPLINE",
            font=("Segoe UI", 9, "bold"),
            fg="#f0f0f5",
            bg="#242638"
        ).pack(anchor="w", padx=12, pady=(10, 2))

        stats = tk.Frame(summary, bg="#242638")
        stats.pack(fill="x", padx=12, pady=(2, 10))

        for value, subtitle, color in (
            (f"{today_xp} XP", "EARNED TODAY", GOLD),
            (str(today_bounties), "BOUNTIES COMPLETED", PURPLE),
            (f"{int(today_focused)}m", "FOCUSED TODAY", "#6CCE91"),
            (str(today_sessions), "CULTIVATION SESSIONS (≥ 1 MIN)", GREEN)
        ):
            frame = tk.Frame(stats, bg="#242638")
            frame.pack(side="left", padx=(0, 25))

            tk.Label(
                frame, text=value,
                font=("Segoe UI", 13, "bold"),
                fg=color, bg="#242638"
            ).pack(anchor="w")

            tk.Label(
                frame, text=subtitle,
                font=("Segoe UI", 7),
                fg=MUTED, bg="#242638"
            ).pack(anchor="w")
        # ==============================
        # SEPARATOR
        # ==============================
        tk.Frame(
            self.log_inner,
            bg="#393d54",
            height=1
        ).pack(fill="x", padx=4, pady=(0, 10))

        # ==============================
        # MISSION HISTORY CONTAINER
        # ==============================
        history_container = tk.Frame(
            self.log_inner,
            bg="#171a27"
        )
        history_container.pack(
            fill="both",
            expand=True,
            padx=2,
            pady=(0, 2)
        )

       # Header stays fixed
        header_frame = tk.Frame(
            history_container,
            bg="#171a27"
        )
        header_frame.pack(fill="x", padx=8, pady=(4, 8))

        tk.Label(
            header_frame,
            text="CULTIVATION HISTORY",
            font=("Segoe UI", 9, "bold"),
            fg="#f0f0f5",
            bg="#171a27"
        ).pack(side="left")

        clear_log_btn = tk.Button(
            header_frame,
            text="Clear History",
            font=("Segoe UI", 8, "bold"),
            fg="#ff8b8b",
            bg="#292333",
            activeforeground="#ffffff",
            activebackground="#a83246",
            relief="flat",
            bd=0,
            padx=12,
            pady=4,
            cursor="hand2",
            command=self.confirm_clear_history
        )
        clear_log_btn.pack(side="right")

        # ==============================
        # SCROLLABLE MISSION LIST
        # ==============================
        list_frame = tk.Frame(history_container, bg="#171a27")
        list_frame.pack(fill="both", expand=True)

        mission_canvas = tk.Canvas(
            list_frame,
            bg="#171a27",
            highlightthickness=0
        )

        mission_scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=mission_canvas.yview,
            style="Mission.Vertical.TScrollbar"
        )

        mission_canvas.configure(yscrollcommand=mission_scrollbar.set)

        mission_scrollbar.pack(side="right", fill="y")
        mission_canvas.pack(side="left", fill="both", expand=True)

        # Frame that holds the actual mission items
        mission_inner = tk.Frame(mission_canvas, bg="#171a27")
        mission_window = mission_canvas.create_window(
            (0, 0),
            window=mission_inner,
            anchor="nw"
        )

        def update_scroll_region(event=None):
            mission_canvas.configure(
                scrollregion=mission_canvas.bbox("all")
            )

        mission_inner.bind("<Configure>", update_scroll_region)

        mission_canvas.bind(
            "<Configure>",
            lambda event: mission_canvas.itemconfigure(
                mission_window, width=event.width
            )
        )

        self.scroll_on_wheel(mission_canvas, mission_inner) # MISSION LOG

        mission_list = tk.Frame(mission_canvas, bg="#171a27")

        mission_window = mission_canvas.create_window(
            (0, 0),
            window=mission_list,
            anchor="nw"
        )

        mission_canvas.bind(
            "<Configure>",
            lambda e: mission_canvas.itemconfigure(
                mission_window,
                width=e.width
            )
        )

        mission_list.bind(
            "<Configure>",
            lambda e: mission_canvas.configure(
                scrollregion=mission_canvas.bbox("all")
            )
        )

        # ==============================
        # EMPTY HISTORY
        # ==============================
        if not self.history:
            tk.Label(
                mission_list,
                text=f"Your chronicle is empty. {"\nComplete your first bounty to leave a mark." if self.level == 0 else ""}",
                font=("Segoe UI", 9, "italic"),
                fg="#969caf",
                bg="#171a27",
                justify="center"
            ).pack(fill="both", expand=True, pady=20)

            return

        # ==============================
        # MISSION LIST
        # ==============================
        for entry in self.history:
            status = str(entry.get("status"))
            accent = {
                "COMPLETED": "#65cb91",
                "BONUS": "#ff8ccf",
                "SKIPPED": "#696969",
                "PARTIALLY COMPLETED": "#e5b85c"
            }.get(status, "#e5b85c")

            card = tk.Frame(
                mission_list,
                bg="#242638",
                highlightbackground="#393d54",
                highlightthickness=1
            )
            card.pack(fill="x", padx=2, pady=3)

            top = tk.Frame(card, bg="#242638")
            top.pack(fill="x", padx=10, pady=(8, 5))

            mission_type = str(entry.get("type", "GENERAL")).upper()

            # Project badge
            if entry.get("project") is not None:
                tk.Label(
                    top,
                    text=f" {entry.get('project')} ",
                    font=("Segoe UI", 7, "bold"),
                    fg="#fff39a",
                    bg="#393052",
                    padx=5,
                    pady=3
                ).pack(side="left", padx=(0, 7))

            # Task title
            if entry.get("task") is not None:
                if mission_type != "SESSION":
                    tk.Label(
                        top,
                        text="Task: ",
                        font=("Segoe UI", 9),
                        fg="#9298aa",
                        bg="#242638"
                    ).pack(side="left")

                tk.Label(
                    top,
                    text=entry.get("task"),
                    font=("Segoe UI", 9, "bold"),
                    fg="#f0f0f5",
                    bg="#242638",
                    anchor="w",
                    wraplength=380,
                    justify="left"
                ).pack(side="left", fill="x", expand=True)

            # Date and duration
            duration = entry.get("duration", 0)

            duration_text = (
                f"{duration}m" if duration >= 1
                else None
            ) if type(duration) == int else duration

            tk.Label(
                top,
                text=f"{entry.get('date', '—')}  ·  {duration_text}" if duration_text is not None else f"{entry.get('date', '—')}",
                font=("Segoe UI", 7),
                fg="#aab0c0",
                bg="#242638"
            ).pack(side="right", padx=(6, 0))

            # Bottom information row
            details = tk.Frame(card, bg="#242638")
            details.pack(fill="x", padx=10, pady=(2, 8))

            # Mission type
            tk.Label(
                details,
                text=f" {mission_type} ",
                font=("Segoe UI", 7, "bold"),
                fg="#b99aff",
                bg="#393052",
                padx=4,
                pady=2
            ).pack(side="left", padx=(0, 7))

            # Status badge
            tk.Label(
                details,
                text=f"  ✦ {status.replace('_', ' ')}  ",
                font=("Segoe UI", 7, "bold"),
                fg=accent,
                bg="#303348",
                padx=5,
                pady=3
            ).pack(side="left")

            # XP label
            xp = entry.get('xp', 0)
            tk.Label(
                details,
                text=f"✧  {"" if xp < 0 else "+" if xp > 0 else ""}{xp} XP",
                font=("Segoe UI", 8, "bold"),
                fg="#65cb91" if xp >= 0 else "#e57a5c",
                bg="#303348",
                padx=8,
                pady=3
            ).pack(side="right")

    def render_show_project_menu(self, event=None):
        if self.project_menu_open:
            self.project_menu.destroy()
            self.project_menu_open = False
            return
        
        self.project_menu_open = True

        projects = self.project_picker["values"] if hasattr(
            self.project_picker, "values"
        ) else getattr(self, "projects", [])

        self.project_menu = tk.Toplevel(self.root)
        self.project_menu.overrideredirect(True)
        self.project_menu.configure(bg="#303A52")

        # Position below picker
        self.project_menu.update_idletasks()

        x = self.project_picker.winfo_rootx()
        picker_y = self.project_picker.winfo_rooty()
        picker_height = self.project_picker.winfo_height()

        menu_height = self.project_menu.winfo_reqheight()

        screen_height = self.root.winfo_screenheight()

        gap = 30

        space_below = screen_height - (picker_y + picker_height)
        space_above = picker_y

        if space_below >= menu_height + gap:
            # Open downward
            y = picker_y + picker_height + gap

        elif space_above >= menu_height + gap:
            # Open upward
            y = picker_y - menu_height - gap

        else:
            # Not enough room: prioritize keeping the picker visible
            y = max(0, min(
                picker_y - menu_height - gap,
                screen_height - menu_height
            ))

        self.project_menu.geometry(f"+{x}+{y}")

        container = tk.Frame(
            self.project_menu,
            bg="#1A2030",
            highlightbackground="#303A52",
            highlightthickness=1
        )
        container.pack()

        for project in projects:

            selected = project == self.project_var.get()

            item = tk.Label(
                container,
                text=f"{'✦  ' if selected else '    '}{project}",
                bg="#222A3D" if selected else "#1A2030",
                fg="#A78BFA" if selected else "#E8EAF2",
                font=("Segoe UI", 9),
                anchor="w",
                padx=12,
                pady=8,
                width=19,
                cursor="hand2"
            )
            item.pack(fill="x")

            def select_project(value=project):
                self.project_menu_open = False
                self.project_menu.destroy()
                if self.project_var.get() != value:
                    self.project_var.set(value)
                    self.change_project()

            item.bind(
                "<Button-1>",
                lambda e, value=project: select_project(value)
            )

            item.bind(
                "<Enter>",
                lambda e, w=item: w.config(bg="#303A52")
            )

            item.bind(
                "<Leave>",
                lambda e, w=item, s=selected: w.config(
                    bg="#222A3D" if s else "#1A2030"
                )
            )

        def close_project_menu(event=None):

            if not self.project_menu_open:
                return

            # Identify the widget currently under the mouse
            clicked_widget = self.root.winfo_containing(
                self.root.winfo_pointerx(),
                self.root.winfo_pointery()
            )

            # Ignore clicks on the project picker
            if clicked_widget in (
                self.project_picker,
                self.project_label,
                self.project_arrow
            ):
                return

            self.project_menu_open = False
            self.project_menu.destroy()

        self.project_menu.bind(
            "<FocusOut>",
            lambda e: close_project_menu(e)
        )

        self.project_menu.focus_force()
    
    # endregion 

    # region ---------------- POPUPS ----------------

    def render_edit_mission_markdown_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title(f"Quest Scroll Editor — {self.active_project}")

        width, height = 880, 900
        x = (popup.winfo_screenwidth() - width) // 2
        y = (popup.winfo_screenheight() - height) // 2
        popup.geometry(f"{width}x{height}+{x}+{y}")

        popup.configure(bg="#171923")
        popup.transient(self.root)
        popup.grab_set()

        tk.Label(
            popup,
            text="EDIT QUEST SCROLLS",
            bg="#171923",
            fg="#e5b85c",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=16, pady=(14, 4))

        tk.Label(
            popup,
            text=(
                "Format:\n"
                "- Mission | 30m | 50xp | daily | current | 3 | 2026-11-03 | 2026-11-04\n\n"
                "Fields: name | duration | reward | daily | status | streak | previous_done_date | last_done_date\n"
                "Status: current, completed, postponed\n"
                "Use none if the mission has no last completion date or no previous completion date (for streaks)."
            ),
            bg="#171923",
            fg="#aab0c0",
            font=("Segoe UI", 9),
            justify="left"
        ).pack(anchor="w", padx=16, pady=(0, 10))

        editor_frame = tk.Frame(popup, bg="#171923")
        editor_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 10)
        )

        editor_scrollbar = ttk.Scrollbar(
            editor_frame,
            orient="vertical",
            style="Mission.Vertical.TScrollbar"
        )
        editor_scrollbar.pack(side="right", fill="y")

        editor = tk.Text(
            editor_frame,
            wrap="word",
            bg="#202435",
            fg="#f0f0f5",
            insertbackground="white",
            relief="flat",
            font=("Consolas", 10),
            padx=12,
            pady=12,
            yscrollcommand=editor_scrollbar.set
        )

        editor_scrollbar.config(command=editor.yview)
        self.scroll_on_wheel(editor) # MARKDOWN EDITOR

        editor.pack(fill="both", expand=True)

        old_missions = defaultdict(list)

        for project, missions in self.projects.items():
            for mission in missions:
                key = mission.get("task", "").strip().casefold()
                old_missions[(project, key)].append(mission.copy())

        lines = []

        for project, missions in self.projects.items():
            lines.append(f"# {project}")
            lines.append("")

            for mission in missions:
                task = mission.get("task", "Untitled quest")
                duration = mission.get("duration", 45)
                reward = mission.get("reward_xp", 0)
                daily = "daily" if mission.get("is_daily", False) else "not_daily"
                status = mission.get("status", "current")
                streak = mission.get("streak_count", 0)
                previous_done = mission.get("previous_done_date") or "none"
                last_done = mission.get("last_done_date") or "none"

                lines.append(
                    f"- {task} | {duration}m | {reward}xp | "
                    f"{daily} | {status} | {streak} | {previous_done} | {last_done}"
                )

            lines.append("")

        editor.insert("1.0", "\n".join(lines))

        def apply_markdown():
            parsed_projects = {}
            current_project = None

            try:
                for raw in editor.get("1.0", "end-1c").splitlines():
                    line = raw.strip()

                    if not line:
                        continue

                    if line.startswith("#"):
                        current_project = line.lstrip("#").strip()

                        if current_project:
                            parsed_projects.setdefault(current_project, [])

                        continue

                    if current_project is None:
                        raise ValueError(
                            "Add a project heading using # Project Name."
                        )

                    if line.startswith(("- ", "* ")):
                        line = line[2:].strip()

                    parts = [part.strip() for part in line.split("|")]

                    task = parts[0] if parts else ""

                    if not task:
                        continue

                    duration = 45
                    reward = 0
                    is_daily = False
                    status = "current"
                    streak = 0
                    previous_done = None
                    last_done = None

                    duration_found = False
                    streak_found = False

                    for i, field in enumerate(parts[1:]):
                        field_lower = field.lower()

                        if field_lower == "daily":
                            is_daily = True

                        elif field_lower == "not_daily":
                            is_daily = False

                        elif field_lower in ("current", "completed", "postponed"):
                            status = field_lower

                        elif field_lower == "none":
                            last_done = None

                        elif "xp" in field_lower:
                            digits = "".join(ch for ch in field if ch.isdigit())
                            reward = int(digits) if digits else 0

                        elif field_lower.endswith("m") or field.isdigit():
                            digits = "".join(ch for ch in field if ch.isdigit())

                            if digits:
                                number = int(digits)

                                if not duration_found:
                                    duration = number
                                    duration_found = True
                                elif not streak_found:
                                    streak = number
                                    streak_found = True

                        elif "-" in field and len(field) == 10:
                            if i == 5: 
                                previous_done = date.fromisoformat(field).isoformat()

                            elif i == 6:
                                last_done = date.fromisoformat(field).isoformat()

                            # print(i, date.fromisoformat(field).isoformat())


                    if not 1 <= duration <= 1440:
                        raise ValueError(
                            f"Invalid duration for mission: {task} - {duration}"
                        )

                    if reward < 0:
                        raise ValueError(
                            f"Invalid XP reward for mission: {task} - {reward}"
                        )

                    if streak < 0:
                        raise ValueError(
                            f"Streak cannot be negative: {task}"
                        )

                    key = (current_project, task.casefold())
                    previous = (
                        old_missions[key].pop(0)
                        if old_missions[key]
                        else {}
                    )

                    mission = {
                        **previous,
                        "task": task,
                        "duration": duration,
                        "reward_xp": reward,
                        "is_daily": is_daily,
                        "status": status,
                        "streak_count": streak,
                        "reclaimable": True,
                        "previous_done_date": previous_done,
                        "last_done_date": last_done,
                        "completed_date": previous.get("completed_date")
                    }
                    # print(mission)

                    parsed_projects[current_project].append(mission)

                if not parsed_projects:
                    raise ValueError(
                        "You need at least one project and mission."
                    )

                for project, missions in parsed_projects.items():
                    if not missions:
                        raise ValueError(
                            f"Project '{project}' needs at least one mission."
                        )

            except (ValueError, TypeError) as error:
                messagebox.showerror(
                    "Quest Scroll Error",
                    str(error),
                    parent=popup
                )
                return

            self.projects = parsed_projects

            if self.active_project not in self.projects:
                self.active_project = next(iter(self.projects))

            # self.selected_mission = None
            self.refresh_project_picker()
            self.render_mission_board()
            self.save_data()

            popup.destroy()

            self.status_label.config(
                text="✦ Quest scrolls successfully updated."
            )

        tk.Button(
            popup,
            text="SAVE QUEST SCROLLS",
            command=apply_markdown,
            bg="#7668e8",
            fg="white",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(pady=(0, 13), ipadx=15, ipady=7)
    
    def render_level_up_popup(self, breakthrough=False):
        bg = "#171923"
        gold = "#e8bb69"
        purple = "#b9a3ff"

        popup = tk.Toplevel(self.root)
        popup.title(
            "REALM BREAKTHROUGH!" if breakthrough else "LEVEL UP!"
        )

        width = 610 if breakthrough else 480
        height = 520 if breakthrough else 370
        popup_container = self.create_custom_titlebar(
            popup,  
            bg=bg,
            start_hidden=True
        )

        message = random.choice(LEVEL_UP_MESSAGES)
        realm = self.get_realm()

        # Sparkle background
        canvas = tk.Canvas(
            popup_container,
            bg=bg,
            highlightthickness=0
        )
        canvas.place(relwidth=1, relheight=1)

        sparkles = []

        def create_sparkles():
            if not popup.winfo_exists():
                return

            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()

            if canvas_width <= 1 or canvas_height <= 1:
                popup_container.after(50, create_sparkles)
                return

            for _ in range(70):
                x = random.randint(5, canvas_width - 5)
                y = random.randint(5, canvas_height - 5)
                size = random.randint(2, 5)

                sparkle = canvas.create_text(
                    x, y,
                    text=random.choice(["✦", "✧", "·", "⋆"]),
                    fill=random.choice([gold, purple, "#ffffff"]),
                    font=("Segoe UI", size + 7)
                )

                sparkles.append({
                    "id": sparkle,
                    "x": x,
                    "y": y,
                    "speed": random.uniform(0.3, 1.5)
                })

            animate_sparkles()

        def animate_sparkles():
            if not popup.winfo_exists():
                return

            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()

            for particle in sparkles:
                particle["y"] -= particle["speed"]

                if particle["y"] < 0:
                    particle["y"] = canvas_height
                    particle["x"] = random.randint(5, max(5, canvas_width - 5))

                canvas.coords(
                    particle["id"],
                    particle["x"],
                    particle["y"]
                )

            popup_container.after(45, animate_sparkles)

        popup_container.after(100, create_sparkles)

        animate_sparkles()

        # Main content
        content = tk.Frame(popup_container, bg=bg)
        content.place(relx=0.5, rely=0.5, anchor="center")

        title_text = (
            "REALM BREAKTHROUGH!"
            if breakthrough else "LEVEL UP!"
        )

        title = tk.Label(
            content,
            text=title_text,
            font=("Segoe UI", 21 if breakthrough else 25, "bold"),
            fg=gold,
            bg=bg
        )
        title.pack(pady=(8, 10))

        # Golden glow pulse
        glow_colors = [
            "#8f6b32",
            "#bd914b",
            "#e8bb69",
            "#fff0b3",
            "#e8bb69",
            "#bd914b"
        ]

        pulse_index = [0]

        def pulse_title():
            if not popup.winfo_exists():
                return

            title.config(
                fg=glow_colors[pulse_index[0]]
            )

            pulse_index[0] = (
                pulse_index[0] + 1
            ) % len(glow_colors)

            popup_container.after(180, pulse_title)

        pulse_title()

        tk.Label(
            content,
            text=f"LEVEL {self.level}",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg=bg
        ).pack(pady=(0, 5))

        if breakthrough:
            tk.Label(
                content,
                text=realm["name"],
                font=("Segoe UI", 13, "bold"),
                fg=purple,
                bg=bg,
                wraplength=350
            ).pack(pady=(0, 6))

            tk.Label(
                content,
                text="✧ A NEW REALM HAS BEEN UNLOCKED ✧",
                font=("Segoe UI", 8, "bold"),
                fg=gold,
                bg=bg
            ).pack(pady=(0, 5))

        # Typewriter dialogue
        dialogue = tk.Label(
            content,
            text="",
            font=("Segoe UI", 10),
            fg="#aab0c0",
            bg=bg,
            wraplength=340,
            justify="center"
        )
        dialogue.pack(pady=(7, 17))

        def type_message(index=0):
            if not popup.winfo_exists():
                return

            dialogue.config(text=message[:index])

            if index <= len(message):
                popup_container.after(
                    35,
                    lambda: type_message(index + 1)
                )
            else:
                show_button()

        def show_button():
            if not popup.winfo_exists():
                return

            button.pack(pady=(4, 5))

        button = tk.Button(
            content,
            text="CONTINUE CULTIVATING",
            command=popup.destroy,
            font=("Segoe UI", 10, "bold"),
            bg="#6c63ff",
            fg="white",
            activebackground="#8179ff",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=22,
            pady=10
        )

        popup_container.after(400, type_message)

        # Dramatic breakthrough screen shake
        if breakthrough:
            self.effect_shake(popup, width, height)

        self.adjust_popup_dimensions(popup, size=(width, height), with_lift=True)

    def render_streak_continues_popup(self, bonus, on_continue):
        popup = tk.Toplevel(self.root)
        popup.title("Daily Cultivation")

        popup_container = self.create_custom_titlebar(
            popup, 
            bg="#100f20",
            start_hidden=True
        )

        canvas = tk.Canvas(
            popup_container,
            width=540,
            height=490,
            bg="#100f20",
            highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)

        center_x = 270

        canvas.create_text(
            center_x, 38,
            text="✦  HEAVENLY NOTIFICATION  ✦",
            fill="#bda8ff",
            font=("Segoe UI", 10, "bold")
        )

        ring = canvas.create_oval(
            center_x - 75, 90,
            center_x + 75, 240,
            outline="#6e55b5",
            width=3
        )

        inner = canvas.create_oval(
            center_x - 60, 105,
            center_x + 60, 225,
            outline="#d9b75f",
            width=2
        )

        canvas.create_text(
            center_x, 160,
            text="✧",
            fill="#f5d98a",
            font=("Segoe UI Symbol", 55, "bold"),
            tags="emblem"
        )

        canvas.create_text(
            center_x, 300,
            text="STREAK CONTINUES!",
            fill="#f5d98a",
            font=("Segoe UI", 21, "bold")
        )

        canvas.create_text(
            center_x, 342,
            text=f"DAY {self.getting_started_streak}",
            fill="#ffffff",
            font=("Segoe UI", 18, "bold")
        )

        canvas.create_text(
            center_x, 380,
            text="Your Dao Heart remains unshaken.",
            fill="#bdb5d5",
            font=("Segoe UI", 10)
        )

        canvas.create_text(
            center_x-5, 425,
            text=f"+{bonus} XP",
            fill="#f5d98a",
            font=("Segoe UI", 24, "bold")
        )

        # Floating particles
        particles = []
        random.seed()

        for _ in range(40):
            px = random.randint(15, 525)
            py = random.randint(50, 460)
            size = random.choice((2, 3, 4))

            dot = canvas.create_oval(
                px, py, px + size, py + size,
                fill=random.choice(
                    ("#f5d98a", "#a58aff", "#ffffff")
                ),
                outline=""
            )

            particles.append((
                dot,
                random.uniform(0.7, 2.2),
                random.uniform(-0.7, 0.7)
            ))

        finished = {"value": False}

        def proceed():
            if finished["value"]:
                return

            finished["value"] = True

            try:
                popup.grab_release()
                popup.destroy()
            except tk.TclError:
                pass

            on_continue()

        tk.Button(
            popup_container,
            text="BEGIN CULTIVATION  →",
            command=proceed,
            font=("Segoe UI", 10, "bold"),
            bg="#6c55b5",
            fg="white",
            activebackground="#8b72dc",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=22,
            pady=9
        ).place(relx=0.5, rely=0.91, anchor="center")

        popup.protocol("WM_DELETE_WINDOW", proceed)

        phase = {"n": 0}

        def animate():
            if finished["value"]:
                return

            phase["n"] += 1
            n = phase["n"]

            pulse = 5 + (n % 24)

            canvas.coords(
                ring,
                center_x - 75 - pulse,
                165 - 75 - pulse,
                center_x + 75 + pulse,
                165 + 75 + pulse
            )

            canvas.itemconfigure(
                ring,
                outline="#%02x%02x%02x" % (
                    min(255, 105 + (n % 12) * 8),
                    min(255, 75 + (n % 12) * 7),
                    190
                )
            )

            for dot, speed, drift in particles:
                coords = canvas.coords(dot)

                if coords:
                    nx = coords[0] + drift
                    ny = coords[1] - speed

                    if ny < 45:
                        ny = 470
                        nx = random.randint(15, 525)

                    canvas.coords(
                        dot,
                        nx, ny,
                        nx + 3, ny + 3
                    )

            popup_container.after(45, animate)

        animate()

        self.adjust_popup_dimensions(popup, size= (540, 620), with_lift=True)
 
    def render_missed_streak_popup(self, streak : int):
        popup = tk.Toplevel(self.root)
        popup.title("Daily Cultivation")
        popup_container = self.create_custom_titlebar(
            popup, 
            bg="#100f20", 
            start_hidden=True
        )

        canvas = tk.Canvas(
            popup_container,
            width=540,
            height=550,
            bg="#100f20",
            highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)

        # Heavenly notification
        canvas.create_text(
            270, 42,
            text="✦  HEAVENLY WARNING  ✦",
            fill="#bda8ff",
            font=("Segoe UI", 11, "bold")
        )

        # Magical rings
        ring = canvas.create_oval(
            190, 85, 350, 245,
            outline="#a45d79",
            width=3
        )

        canvas.create_oval(
            207, 102, 333, 228,
            outline="#d9b75f",
            width=2
        )

        canvas.create_text(
            270, 150,
            text="⚠",
            fill="#f5d98a",
            font=("Segoe UI Symbol", 55, "bold")
        )

        # Main message
        text_y_loc = 310
        canvas.create_text(
            270, text_y_loc,
            text="STREAK BROKEN!",
            fill="#f5d98a",
            font=("Segoe UI", 24, "bold")
        )

        canvas.create_text(
            270, text_y_loc+45,
            text=f"Your previous streak: {streak} day(s)",
            fill="#ffffff",
            font=("Segoe UI", 13, "bold")
        )

        canvas.create_text(
            270, text_y_loc+85,
            text="Your Dao Heart has missed a day.",
            fill="#bdb5d5",
            font=("Segoe UI", 11)
        )

        canvas.create_text(
            270, text_y_loc+117,
            text="Will you preserve your path or begin anew?",
            fill="#bdb5d5",
            font=("Segoe UI", 10)
        )

        # Magical particles
        particles = []

        for _ in range(42):
            px = random.randint(15, 540)
            py = random.randint(45, 560)
            size = random.choice((2, 3, 4))

            dot = canvas.create_oval(
                px, py,
                px + size, py + size,
                fill=random.choice(
                    ("#f5d98a", "#a58aff", "#ffffff")
                ),
                outline=""
            )

            particles.append((
                dot,
                random.uniform(0.5, 1.8),
                random.uniform(-0.6, 0.6)
            ))

        finished = {"value": False}

        def close_popup():
            if finished["value"]:
                return

            finished["value"] = True

            try:
                popup.grab_release()
                popup.destroy()
            except tk.TclError:
                pass

        result = {"choice": None}

        def use_grace():
            result["choice"] = "grace"
            close_popup()

        def reset_streak():
            result["choice"] = "reset"
            close_popup()

        # Grace button
        # Button container
        button_frame = tk.Frame(popup_container, bg="#100f20")
        button_frame.place(
            relx=0.5,
            rely=0.85,
            anchor="center"
        )

        # Grace button
        tk.Button(
            button_frame,
            text="✦  USE GRACE DAY",
            command=use_grace,
            font=("Segoe UI", 11, "bold"),
            bg="#6c55b5",
            fg="white",
            activebackground="#8b72dc",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            width=28
        ).pack(pady=(0, 12))

        # Reset button
        tk.Button(
            button_frame,
            text="RESET STREAK",
            command=reset_streak,
            font=("Segoe UI", 10, "bold"),
            bg="#30243e",
            fg="#f5d98a",
            activebackground="#493653",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            width=28
        ).pack()

        # Prevent accidental dismissal
        popup.protocol("WM_DELETE_WINDOW", lambda: None)

        # Animation
        phase = {"n": 0}

        def animate():
            if finished["value"]:
                return

            phase["n"] += 1
            n = phase["n"]

            pulse = 5 + (n % 24)

            canvas.coords(
                ring,
                270 - 80 - pulse,
                165 - 80 - pulse,
                270 + 80 + pulse,
                165 + 80 + pulse
            )

            canvas.itemconfigure(
                ring,
                outline="#%02x%02x%02x" % (
                    min(255, 105 + (n % 12) * 8),
                    min(255, 75 + (n % 12) * 7),
                    190
                )
            )

            for dot, speed, drift in particles:
                coords = canvas.coords(dot)

                if coords:
                    nx = coords[0] + drift
                    ny = coords[1] - speed

                    if ny < 40:
                        ny = 450
                        nx = random.randint(15, 525)

                    canvas.coords(
                        dot,
                        nx, ny,
                        nx + 3, ny + 3
                    )

            popup_container.after(45, animate)

        animate()

        self.adjust_popup_dimensions(popup, size=(540, 690), with_lift=True)
        popup.wait_window()
        return result["choice"]
    
    def render_inspection_report_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Cultivation Complete")
        width, height = 700, 575
        mwidth, mheight = 700, 310

        BG = "#171923"
        PANEL = "#222738"
        BORDER = "#34394b"
        GOLD = "#F5C66A"
        PURPLE = "#A78BFA"
        MUTED = "#9CA9C5"
        GREEN = "#6cce91"

        # Calculate session duration
        elapsed = (
            min(self.duration, int(time.monotonic() - self.start_time))
            if self.start_time is not None else 0
        )

        minutes, seconds = divmod(elapsed, 60)

        focus_time = (
            f"{minutes} min" if seconds < 30
            else f"{minutes} min {seconds}s"
        )

        # Duration-based XP rewards
        XP_REWARD = get_cultivation_session_reward(elapsed)
        
        # Custom title bar
        popup_container = self.create_custom_titlebar(
            popup,
            start_hidden=True
        )

        # Main heading
        tk.Label(
            popup_container,
            text="✦  CULTIVATION COMPLETE  ✦",
            font=("Segoe UI", 19, "bold"),
            fg=GOLD,
            bg=BG
        ).pack(pady=(22, 5))

        tk.Label(
            popup_container,
            text="Your efforts have strengthened your Dao." if elapsed > 60 else
            "Your cultivation was too brief to earn XP. Try again!",
            font=("Segoe UI", 9),
            fg=MUTED,
            bg=BG
        ).pack(pady=(0, 18))

        # Session statistics
        stats = tk.Frame(popup_container, bg=BG)
        stats.pack(fill="x", padx=35, pady=(0, 18))

        stats.grid_columnconfigure(0, weight=1)
        stats.grid_columnconfigure(1, weight=1)

        def create_stat(parent, title, value, color):
            card = tk.Frame(
                parent,
                bg=PANEL,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            tk.Label(
                card,
                text=title.upper(),
                font=("Segoe UI", 8, "bold"),
                fg=MUTED,
                bg=PANEL
            ).pack(anchor="w", padx=12, pady=(10, 3))

            tk.Label(
                card,
                text=value,
                font=("Segoe UI", 17, "bold"),
                fg=color,
                bg=PANEL
            ).pack(anchor="w", padx=12, pady=(0, 10))

            return card

        create_stat(
            stats,
            "Focus time",
            focus_time,
            PURPLE
        ).grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        create_stat(
            stats,
            "XP reward",
            f"+{XP_REWARD} XP",
            GOLD
        ).grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        # Question
        tk.Label(
            popup_container,
            text="How did your cultivation go?",
            font=("Segoe UI", 12, "bold"),
            fg="white",
            bg=BG
        ).pack(pady=(0, 3))

        tk.Label(
            popup_container,
            text="Choose an honest assessment of your work.",
            font=("Segoe UI", 8),
            fg=MUTED,
            bg=BG
        ).pack(pady=(0, 12))

        # Response colors
        colors = {
            "YES!": GREEN,
            "PARTIALLY": GOLD,
            "NOT YET": "#8b9df5"
        }

        descriptions = {
            "YES!": "I accomplished my goal",
            "PARTIALLY": "I made progress",
            "NOT YET": "I'll try again"
        }

        def respond(choice):
            duration = f"{minutes}m {seconds}s"
            message = random.choice(REVIEW_RESPONSES[choice])

            self.record_history(
                title="Session finished.",
                status={
                    "YES!": "COMPLETED",
                    "PARTIALLY": "PARTIALLY COMPLETED",
                    "NOT YET": "SKIPPED"
                }[choice],
                history_type="Session",
                duration=duration,
                project=None,
                xp_reward=XP_REWARD
            )

            # Clear previous content
            for widget in popup_container.winfo_children():
                widget.destroy()

            popup.update_idletasks()
            self.center_geometry(popup, (mwidth, mheight))

            # Completion screen
            tk.Label(
                popup_container,
                text="✦  CULTIVATION COMPLETE  ✦",
                font=("Segoe UI", 17, "bold"),
                fg=GOLD,
                bg=BG
            ).pack(pady=(35, 12))

            tk.Label(
                popup_container,
                text=message,
                font=("Segoe UI", 10),
                fg=MUTED,
                bg=BG,
                wraplength=400,
                justify="center"
            ).pack(padx=25, pady=12)

            tk.Button(
                popup_container,
                text="CONTINUE",
                command=popup.destroy,
                bg=PANEL,
                fg=GOLD,
                activebackground="#34394b",
                activeforeground=GOLD,
                relief="flat",
                font=("Segoe UI", 10, "bold"),
                cursor="hand2",
                bd=0
            ).pack(pady=(18, 25), ipadx=30, ipady=8)
            self.overlay.withdraw()

        # Response buttons
        buttons = tk.Frame(popup_container, bg=BG)
        buttons.pack(fill="x", padx=35, pady=(0, 20))

        for choice in REVIEW_RESPONSES:
            button = tk.Button(
                buttons,
                text=f"{choice}   ·   {descriptions[choice]}",
                font=("Segoe UI", 9, "bold"),
                bg=PANEL,
                fg=colors[choice],
                activebackground=colors[choice],
                activeforeground=BG,
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda c=choice: respond(c),
                anchor="w",
                padx=15
            )

            button.pack(fill="x", pady=3, ipady=7)

        self.adjust_popup_dimensions(
            popup,
            size=(width, height),
            with_lift=True
        )

    def render_add_project_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Found a New Sect")
        
        # Custom draggable title bar
        popup_container = self.create_custom_titlebar(
            popup, 
            fixed_size=(340, 200), 
            start_hidden=True
        )

        tk.Label(popup_container, text="NAME YOUR SECT", bg="#171923", fg="#e5b85c", font=("Segoe UI", 10, "bold")).pack(pady=(18, 8))

        name_var = tk.StringVar()
        entry = tk.Entry(popup_container, textvariable=name_var, bg="#252a3a", fg="white", insertbackground="white", relief="flat", font=("Segoe UI", 10))
        entry.pack(fill="x", padx=22, ipady=7)

        def create():
            name = name_var.get().strip()
            if not name:
                return
            
            self.create_project(name)
            popup.destroy()

        tk.Button(popup_container, text="CREATE SECT", command=create, bg="#7668e8", fg="white", relief="flat", font=("Segoe UI", 9, "bold")).pack(pady=12, ipadx=12, ipady=5)

        entry.focus_set()
        self.adjust_popup_dimensions(popup, (340, 200), with_lift=True)

    def render_restart_cultivation_popup(self, on_confirm):
        bg = "#100f20"
        gold = "#e8bb69"
        purple = "#b9a3ff"

        popup = tk.Toplevel(self.root)
        
        # Custom title bar
        popup_container = self.create_custom_titlebar(
            popup=popup, 
            bg=bg,
            start_hidden = True
        )

        # Background canvas
        canvas = tk.Canvas(
            popup_container,
            bg=bg,
            highlightthickness=0
        )
        canvas.place(relwidth=1, relheight=1)

        # Content
        content = tk.Frame(popup_container, bg=bg)
        content.place(relx=0.5, rely=0.47, anchor="center")

        # Magical warning symbol
        icon = tk.Label(
            content,
            text="⚠",
            bg=bg,
            fg=gold,
            font=("Segoe UI Symbol", 48, "bold")
        )
        icon.pack(pady=(8, 2))

        # Dramatic title
        title = tk.Label(
            content,
            text="RESTART CULTIVATION",
            bg=bg,
            fg=gold,
            font=("Segoe UI", 19, "bold")
        )
        title.pack(pady=(5, 12))

        # Subtitle
        tk.Label(
            content,
            text="THE PATH OF CULTIVATION WILL BE RESET",
            bg=bg,
            fg=purple,
            font=("Segoe UI", 8, "bold")
        ).pack(pady=(0, 15))

        # Description
        tk.Label(
            content,
            text=(
                "Are you certain you wish to abandon your current path?\n\n"
                "Your cultivation progress will begin anew.\n"
                "Your achievements may be lost permanently, and your daily bounty streaks will be reset. However, the status of your regular bounties will remain unchanged."
            ),
            bg=bg,
            fg="#bdb5d5",
            font=("Segoe UI", 9),
            justify="center",
            wraplength=500
        ).pack(padx=20, pady=5)

        # Warning message
        tk.Label(
            content,
            text="✧ THERE IS NO TURNING BACK ✧",
            bg=bg,
            fg="#d17b8b",
            font=("Segoe UI", 9, "bold")
        ).pack(pady=(15, 18))

        # Buttons
        button_frame = tk.Frame(content, bg=bg)
        button_frame.pack(pady=(0, 10))

        def confirm_restart():
            self.close_custom_popup(popup)
            on_confirm()

        tk.Button(
            button_frame,
            text="⚔  RESTART CULTIVATION",
            command=confirm_restart,
            font=("Segoe UI", 9, "bold"),
            bg="#8e354b",
            fg="white",
            activebackground="#b44760",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10
        ).pack(side="left", padx=6)

        tk.Button(
            button_frame,
            text="CANCEL",
            command=lambda: self.close_custom_popup(popup),
            font=("Segoe UI", 9, "bold"),
            bg="#292638",
            fg="#b9a3ff",
            activebackground="#403653",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10
        ).pack(side="left", padx=6)

        # Pulsating title
        glow_colors = [
            "#98733d",
            "#bd914b",
            "#e8bb69",
            "#fff0b3",
            "#e8bb69",
            "#bd914b"
        ]

        pulse_index = [0]

        def pulse_title():
            if not popup.winfo_exists():
                return

            title.config(fg=glow_colors[pulse_index[0]])

            pulse_index[0] = (
                pulse_index[0] + 1
            ) % len(glow_colors)

            popup_container.after(180, pulse_title)

        # Floating magical particles
        particles = []

        def create_particles():
            if not popup.winfo_exists():
                return

            w = canvas.winfo_width()
            h = canvas.winfo_height()

            if w <= 1 or h <= 1:
                popup_container.after(50, create_particles)
                return

            for _ in range(55):
                px = random.randint(5, w - 5)
                py = random.randint(35, h - 5)

                particle = canvas.create_text(
                    px,
                    py,
                    text=random.choice(["✦", "✧", "·", "⋆"]),
                    fill=random.choice([
                        gold,
                        purple,
                        "#ffffff",
                        "#8e354b"
                    ]),
                    font=("Segoe UI", random.randint(9, 15))
                )

                particles.append({
                    "id": particle,
                    "x": px,
                    "y": py,
                    "speed": random.uniform(0.3, 1.3),
                    "drift": random.uniform(-0.4, 0.4)
                })

            animate_particles()

        def animate_particles():
            if not popup.winfo_exists():
                return

            h = canvas.winfo_height()
            w = canvas.winfo_width()

            for p in particles:
                p["y"] -= p["speed"]
                p["x"] += p["drift"]

                if p["y"] < 32:
                    p["y"] = h
                    p["x"] = random.randint(5, max(5, w - 5))

                canvas.coords(
                    p["id"],
                    p["x"],
                    p["y"]
                )

            popup_container.after(45, animate_particles)

        # Keyboard shortcuts
        popup.bind(
            "<Escape>",
            lambda e: self.close_custom_popup(popup)
        )

        # Calculate DPI-aware dimensions
        popup.update_idletasks()
        width, height = max(680, popup.winfo_reqwidth()), max(620, popup.winfo_reqheight())
        self.adjust_popup_dimensions(popup, (width, height), with_lift=True)

        # Start animations
        pulse_title()
        popup.after(100, create_particles)

        # Display popup
        popup.wait_window()

    def render_message_popup(self, title, description):
        popup = tk.Toplevel(self.root)

        # Custom draggable title bar
        popup_container = self.create_custom_titlebar(
            popup, 
            start_hidden=True
        )

        # Icon
        tk.Label(
            popup_container,
            text="✦",
            bg="#171923",
            fg="#E5B85C",
            font=("Segoe UI", 25, "bold")
        ).pack(pady=(15, 2))

        # Title
        tk.Label(
            popup_container,
            text=title,
            bg="#171923",
            fg="#E5B85C",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=(0, 8))

        # Description
        tk.Label(
            popup_container,
            text=description,
            bg="#171923",
            fg="#B8BED0",
            font=("Segoe UI", 9),
            justify="center",
            wraplength=350
        ).pack(padx=25, pady=5)

        # Understood button
        tk.Button(
            popup_container,
            text="UNDERSTOOD",
            command=lambda: self.close_custom_popup(popup),
            bg="#7668E8",
            fg="white",
            activebackground="#897CF0",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=25,
            pady=7
        ).pack(pady=(15, 20))

        # Keyboard shortcuts
        popup.bind(
            "<Return>",
            lambda e: self.close_custom_popup(popup)
        )
        popup.bind(
            "<Escape>",
            lambda e: self.close_custom_popup(popup)
        )

        # Calculate actual dimensions (DPI-aware)
        popup.update_idletasks()
        width, height = max(420, popup.winfo_reqwidth()), popup.winfo_reqheight()
        self.adjust_popup_dimensions(popup, size=(width, height), with_lift=True)

    def render_confirmation_popup(self, title, description, on_confirm, highlight_text=None, highlight_text_color= None):
        popup = tk.Toplevel(self.root)

        # Create generic title bar
        popup_container = self.create_custom_titlebar(
            popup, 
            start_hidden=True, 
            is_dialog=True
        )

        # Icon
        tk.Label(
            popup_container,
            text="?",
            bg="#171923",
            fg="#E5B85C",
            font=("Segoe UI", 25, "bold")
        ).pack(pady=(15, 2))

        # Title
        tk.Label(
            popup_container,
            text=title,
            bg="#171923",
            fg="#E5B85C",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=(0, 8))

        # Description
        desc_frame = tk.Frame(popup_container, bg="#171923")
        desc_frame.pack(padx=20, pady=5)
        desc_frame.pack_propagate(True)

        desc_text = tk.Text(
            desc_frame,
            bg="#171923",
            fg="#B8BED0",
            font=("Segoe UI", 9),
            wrap="word",
            height=1,
            width=48,
            relief="flat",
            bd=0,
            highlightthickness=0,
            cursor="arrow",
            spacing1=3,
            spacing3=3
        )

        desc_text.tag_configure("normal", foreground="#B8BED0")

        # Normalize arguments into tuples
        highlights = (
            (highlight_text,) if isinstance(highlight_text, str)
            else highlight_text or ()
        )

        colors = (
            (highlight_text_color,) if isinstance(highlight_text_color, str)
            else highlight_text_color or ()
        )

        # Replace placeholders with their corresponding highlights
        for i, text in enumerate(highlights):
            color = colors[i] if i < len(colors) else "#E5B85C"
            desc_text.tag_configure(
                f"highlight_{i}",
                foreground=color,
                font=("Segoe UI", 9, "bold"),
                justify="center"
            )

        # Build placeholder lookup
        highlight_map = {
            f"{{t{i + 1}}}": (text, f"highlight_{i}")
            for i, text in enumerate(highlights)
        }

        # Insert description while preserving formatting
        pattern = re.compile(
            "|".join(re.escape(p) for p in highlight_map)
        ) if highlight_map else None

        parts = pattern.split(description) if pattern else [description]
        matches = pattern.findall(description) if pattern else []

        for i, part in enumerate(parts):
            desc_text.insert("end", part, "normal")

            if i < len(matches):
                text, tag = highlight_map[matches[i]]
                desc_text.insert("end", text, tag)

        # Configure description widget first
        desc_text.configure(
            width=48,
            wrap="word"
        )

        # Pack the widget
        desc_text.pack(fill="x", padx=10, pady=5)

        # Establish the popup's layout
        popup.update_idletasks()

        # Buttons
        button_frame = tk.Frame(popup_container, bg="#171923")
        button_frame.pack(pady=(15, 20))

        def confirm():
            popup.destroy()
            on_confirm()

        tk.Button(
            button_frame,
            text="YES",
            command=confirm,
            bg="#7668E8",
            fg="white",
            activebackground="#897CF0",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=25,
            pady=7
        ).pack(side="left", padx=7)

        tk.Button(
            button_frame,
            text="CANCEL",
            command=lambda: self.close_custom_popup(popup),
            bg="#292D3D",
            fg="#B8BED0",
            activebackground="#393F52",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=25,
            pady=7
        ).pack(side="left", padx=7)

        popup.bind("<Return>", lambda e: confirm())
        popup.bind("<Escape>", lambda e: self.close_custom_popup(popup))

        # Adjusting description height
        popup.update_idletasks()
        
        top, bottom = desc_text.yview()
        visible_height = desc_text.winfo_height()

        if bottom < 1.0:
            real_height = visible_height / (bottom - top)
        else:
            real_height = visible_height

        line_height = desc_text.dlineinfo("1.0")[3]
        required_lines = round(real_height / line_height)
        desc_text.configure(height=required_lines+1 if required_lines > 1 else 1)
        popup.update_idletasks()
        
        # Calculate dimensions
        width, height = max(440, popup.winfo_reqwidth()), popup.winfo_reqheight()
        self.adjust_popup_dimensions(popup, (width, height), with_lift=True)

        popup.wait_window()

    # endregion
 
    # region ---------------- FLOATING OVERLAY ----------------
 
    def build_overlay(self):
        self.overlay = tk.Toplevel(self.root)
        self.overlay.overrideredirect(True)
        self.overlay.attributes("-topmost", True)
        self.overlay.configure(bg="#d9b75f")

        self.position_overlay()

        self.overlay_frame = tk.Frame(
            self.overlay,
            bg="#171525",
            highlightbackground="#6c55b5",
            highlightthickness=1,
            cursor="hand2"
        )
        self.overlay_frame.pack(
            fill="both", expand=True, padx=1, pady=1
        )

        # Header
        header = tk.Frame(
            self.overlay_frame,
            bg="#171525"
        )
        header.pack(fill="x", padx=11, pady=(7, 0))

        self.overlay_title = tk.Label(
            header,
            text="✦ FOCUS MODE",
            font=("Segoe UI", 8, "bold"),
            fg="#bda8ff",
            bg="#171525",
            cursor="hand2"
        )
        self.overlay_title.pack(side="left")

        self.focus_indicator = tk.Label(
            header,
            text="● ACTIVE",
            font=("Segoe UI", 7, "bold"),
            fg="#8ed6a5",
            bg="#171525",
            padx=2
        )
        self.focus_indicator.pack(side="right")

        # Timer
        self.timer_label = tk.Label(
            self.overlay_frame,
            text="45:00",
            font=("Segoe UI", 22, "bold"),
            fg="#f5d98a",
            bg="#171525",
            bd=0,
            highlightthickness=0,
            cursor="hand2"
        )
        self.timer_label.pack(pady=(0, 0))
        self.timer_label.place(relx=0.5, y=25, anchor="n")
        header.lift()

        # Progress
        progress_frame = tk.Frame(
            self.overlay_frame,
            bg="#171525",
            height=12
        )

        progress_frame.pack(
            fill="x",
            padx=13,
            pady=(0, 18)
        )
        progress_frame.place(x=13, y=100, relwidth=1, width=-26)
        progress_frame.pack_propagate(False)

        self.progress_bg = tk.Frame(
            progress_frame,
            bg="#49415e",
            height=8
        )
        self.progress_bg.pack(fill="both", expand=True)

        self.progress_fill = tk.Frame(
            self.progress_bg,
            bg="#f5d98a",
            width=120
        )
        self.progress_fill.place(
            relx=0,
            rely=0,
            relheight=1,
            relwidth=0.65
        )
        # Click anywhere to open main window
        for widget in (
            self.overlay,
            self.overlay_frame,
            header,
            self.overlay_title,
            self.timer_label,
            self.focus_indicator
        ):
            widget.bind("<Button-1>", self.show_window)

        self.overlay.withdraw()

    def position_overlay(self):
        self.overlay.update_idletasks()

        width, height = 320, 130

        screen_width = self.overlay.winfo_screenwidth()
        screen_height = self.overlay.winfo_screenheight()

        x = screen_width - width - 20
        y = screen_height - height - 65

        self.overlay.geometry(f"{width}x{height}+{x}+{y}")
        self.overlay.update_idletasks()

        # if hasattr(self, "progress"):
        #     print("Overlay:", self.overlay.winfo_geometry())
        #     print("Progress:", self.progress.winfo_rooty())
        #     print("Progress height:", self.progress.winfo_height())
        #     print("Overlay bottom:", 
        #         self.overlay.winfo_rooty() + self.overlay.winfo_height())

    def update_overlay_progress(self, value):
        value = max(0, min(100, value))

        self.progress_value = value

        self.progress_fill.place(
            relx=0,
            rely=0,
            relheight=1,
            relwidth=value / 100
        )

    # endregion

    # region ---------------- GENERIC FUNCTIONS --------

    def is_inside_widget(self, widget, parent):
        while widget:
            if widget == parent:
                return True
            widget = getattr(widget, "master", None)

        return False
    
    def scroll_on_wheel(self, scrollable, container=None):
        def on_mousewheel(event):
            target = event.widget

            # Let Text widgets scroll themselves
            while target is not None:
                if isinstance(target, tk.Text):
                    first, last = target.yview()
                    if first <= 0 and last >= 1:
                        return "break"
                    break
                target = target.master
            else:
                target = scrollable
                first, last = target.yview()

                if first <= 0 and last >= 1:
                    return "break"

            if event.num == 4:
                direction = -1
            elif event.num == 5:
                direction = 1
            else:
                direction = -1 if event.delta > 0 else 1

            target.yview_scroll(direction, "units")
            return "break"

        def bind_wheel(event):
            scrollable.bind_all("<MouseWheel>", on_mousewheel)
            scrollable.bind_all("<Button-4>", on_mousewheel)
            scrollable.bind_all("<Button-5>", on_mousewheel)

        def unbind_wheel(event):
            scrollable.unbind_all("<MouseWheel>")
            scrollable.unbind_all("<Button-4>")
            scrollable.unbind_all("<Button-5>")

        widgets = [scrollable]
        if container is not None:
            widgets.append(container)

        def bind_recursive(widget):
            widget.bind("<Enter>", bind_wheel, add="+")
            widget.bind("<Leave>", unbind_wheel, add="+")
            for child in widget.winfo_children():
                bind_recursive(child)

        for widget in widgets:
            bind_recursive(widget)

        if container is not None:
            container.bind(
                "<Map>",
                lambda event: bind_recursive(container),
                add="+"
            )

    # endregion

    # region ---------------- FUNCTIONS ----------------

    # region Dashboard

    def get_realm(self, level=None):
        level = self.level if level is None else level
        for low, high, name, description, subtitle, requirement in REALMS:
            if low <= level <= high:
                return {
                    "name": name,
                    "description": description,
                    "subtitle": subtitle,
                    "xp_required": requirement
                }
        return {
            "name": "TRANSCENDENCE",
            "description": "Beyond the Dao. Beyond the heavens.",
            "subtitle": "There are no limits left to inherit.",
            "xp_required": 3000
        }

    def update_xp_display(self):
        current_xp, requirement = self.calculate_progression()
        realm = self.get_realm()

        # Current realm
        self.rank_label.config(text=realm["name"].upper())
        self.level_label.config(text=f"LEVEL {self.level}")
        self.rank_description.config(text=realm["description"])

        # XP progress
        percentage = (
            min(100, current_xp / requirement * 100)
            if requirement > 0 else 100
        )

        remaining = max(0, requirement - current_xp)

        self.xp_label.config(
            text=f"{current_xp:,} / {requirement:,} XP"
        )

        self.xp_percentage_label.config(
            text=f"{percentage:.0f}%"
        )

        self.xp_progress.configure(
            maximum=max(1, requirement)
        )
        self.xp_progress["value"] = current_xp

        self.total_xp_label.config(
            text=f"{remaining:,} XP to next level"
        )

        # Next cultivation realm
        realms = REALMS

        current_index = next(
            (
                i for i, r in enumerate(realms)
                if r[2] == realm["name"]
            ),
            -1
        )

        if current_index >= 0 and current_index + 1 < len(realms):
            next_realm = realms[current_index + 1]
            self.next_realm_label.config(
                text=f"✨  NEXT BREAKTHROUGH: {next_realm[2].upper()}"
            )
        else:
            self.next_realm_label.config(
                text="✨  HIGHEST CULTIVATION REALM ACHIEVED"
            )

        # Dashboard statistics
        self.dashboard_streak_card.config(
            text=f"🔥  {self.getting_started_streak} "
                f"{'day' if self.getting_started_streak == 1 else 'days'}",
        )

        self.dashboard_xp_card.config(
            text=f"✦  {self.xp} XP"
        )

        self.dashboard_bounty_card.config(
            text=f"⚔  {self.total_completed_bounties} "
                f"{'Bounty' if self.total_completed_bounties == 1 else 'Bounties'}"
        )

    def award_xp(self, amount):
        old_level = self.level
        old_realm = self.get_realm(old_level)["name"]

        self.xp += amount

        # Level down when XP becomes negative.
        while self.xp < 0 and self.level > 0:
            self.level -= 1

            # Carry the XP deficit into the previous level.
            previous_requirement = self.get_realm(self.level)["xp_required"]
            self.xp += previous_requirement

        # Never go below level 0 or negative XP.
        if self.level == 0 and self.xp < 0:
            self.xp = 0

        self.update_xp_display()

        new_realm = self.get_realm()["name"]

        if self.level > old_level:
            if new_realm != old_realm:
                self.render_level_up_popup(breakthrough=True)
            else:
                self.render_level_up_popup()

        elif self.level < old_level:
            self.status_label.config(
                text="▼ You lost a level! Your cultivation has declined."
            )
    
    # endregion

    # region Sects
    
    def create_project(self, name):
        if name not in self.projects:
            self.projects[name] = []

        self.active_project = name
        self.refresh_project_picker()
        self.render_mission_board()
        self.save_data()

    def change_project(self):
        self.active_project = self.project_var.get()
        # self.selected_mission = None
        self.render_mission_board(reset=True)

    def refresh_project_picker(self):
        if self.active_project not in self.projects:
            self.active_project = next(iter(self.projects), "General")
            self.projects.setdefault(self.active_project, [])

        self.project_var.set(self.active_project)

        # Update custom picker display
        self.project_label.config(
            text=self.active_project
        )

    # endregion

    # region Bounties

    def current_missions(self): # get current missions
        return self.projects.setdefault(self.active_project, [])
    
    def change_mission_status(self, mission, new_status):
        today = date.today()
        today_str = today.isoformat()

        is_daily = mission.get("is_daily", False)
        reward = int(mission.get("reward_xp", 0))

        # ---------- COMPLETE MISSION ----------
        if new_status == "completed":
            if is_daily:
                last_done = mission.get("last_done_date")
                streak = mission.get("streak_count", 0)

                if last_done == today_str:
                    self.render_message_popup(
                        title="BOUNTY ALREADY CLAIMED",
                        description="This daily bounty has already been\ncompleted for today.",
                    )
                    return

                if last_done:
                    try:
                        previous_date = date.fromisoformat(last_done)
                        days_missed = (today - previous_date).days

                    except ValueError:
                        days_missed = 0

                    if days_missed > 1: # if more than 1 day is missed, it means the streak is broken
                        choice = self.render_missed_streak_popup(
                            streak
                        )

                        if choice == "grace":
                            # Preserve existing streak
                            streak += 1
                            pass

                        # elif choice == "reset":
                        else:
                            streak = 1

                    else:
                        streak += 1

                else:
                    streak = 1

                mission["streak_count"] = streak
                mission["previous_done_date"] =  mission["last_done_date"]
                mission["last_done_date"] = today_str
                mission["status"] = "current"

            else:
                if mission.get("status") == "completed":
                    return

                mission["status"] = "completed"
                mission["completed_date"] = today_str
                self.total_completed_bounties += 1

            # Record completion
            self.record_history(
                mission.get("task"),
                status="COMPLETED",
                history_type=("Streak " if is_daily else "")+"Bounty",
                project=self.active_project,
                duration=mission.get("duration"),
                xp_reward=reward
            )

            self.update_xp_display()
            self.status_label.config(
                text=(
                    f"✦ Daily bounty mission completed! +{reward} XP "
                    f"| Streak: {mission['streak_count']}"
                    if is_daily
                    else f"✦ Bounty mission completed! +{reward} XP"
                )
            )

        # ---------- POSTPONE / RESTORE ----------
        elif new_status in ("postponed", "current"):
            if is_daily and mission.get("last_done_date") == today_str:
                messagebox.showinfo(
                    "Daily Bounty",
                    "Today's daily mission is already complete."
                )
                return

            if (
                not is_daily
                and mission.get("status") == "completed"
                and new_status == "current"
            ):
                if mission.get("reclaimable", True) == False:
                    reward = 0
                
                mission["completed_date"] = None
                mission["reclaimable"] = True
                self.total_completed_bounties -= 1

                self.record_history(
                    mission.get('task'),
                    status="RECLAIMED",
                    history_type="Bounty",
                    project=self.active_project,
                    duration=mission.get("duration"),
                    xp_reward=-reward # Reverse XP
                )


            mission["status"] = new_status

        # ---------- SAVE AND REFRESH ----------
        self.save_data()
        self.render_mission_board()

    def undo_daily_completion(self, mission):
        today_str = date.today().isoformat()

        if mission.get("last_done_date") != today_str:
            return

        mission["last_done_date"] = mission["previous_done_date"]
        mission["streak_count"] = max(
            0, mission.get("streak_count", 0) - 1
        )
        self.total_completed_bounties -= 1

        self.record_history(
            mission.get('task'),
            status="RECLAIMED",
            history_type="Streak Bounty",
            project=self.active_project,
            duration=mission.get("duration"),
            xp_reward=-int(mission.get("reward_xp", 0))
        )

        self.render_mission_board()

    def reset_daily_streak(self, mission, done_today):
        mission["previous_done_date"] = None
        mission["last_done_date"] = None
        mission["streak_count"] = 0

        if done_today:
            self.total_completed_bounties -= 1
            self.record_history(
                mission.get('task'),
                status="RECLAIMED",
                history_type="Streak Bounty",
                project=self.active_project,
                duration=mission.get("duration"),
                xp_reward=-int(mission.get("reward_xp", 0))
            )
        else:
            self.save_data()

        self.render_mission_board()
        
    def add_mission(self):
        task = self.task_var.get().strip()

        try:
            if len(task) > 40:
                raise ValueError
        except ValueError:
            self.status_label.config(
                text="Bounty name length can't exceed 40 words!"
            )
            return
        
        try:
            duration = int(float(self.minutes_var.get()))
            if duration <= 0 or duration > 1440:
                raise ValueError
        except ValueError:
            self.status_label.config(
                text="Set a duration between 1 and 1440 minutes."
            )
            return

        if not task:
            self.status_label.config(
                text="Give your quest a name first."
            )
            return
        
        mission = {
            "task": task,
            "duration": duration,
            "reward_xp":  int(float(self.reward_var.get())),
            "is_daily": self.daily_var.get(),
            "status": "current",
            "streak_count": 0,
            "previous_done_date": None,
            "last_done_date": None,
            "completed_date": None
        }

        self.current_missions().append(mission)

        # self.selected_mission = len(self.current_missions()) - 1

        self.save_data()
        self.render_mission_board()

        self.task_var.set("")
        self.minutes_var.set("25")
        self.daily_var.set(False)

        self.status_label.config(
            text="✦ New bounty successfully posted!"
        )

    def confirm_remove_mission(self, mission):
        def remove_mission():
            missions = self.current_missions()

            if mission not in missions:
                return

            missions.remove(mission)

            if hasattr(self, "save_data"):
                self.save_data()

            self.render_mission_board()

        task_name = mission.get("task", "Unknown Bounty")

        self.render_confirmation_popup(
            "ABANDON BOUNTY",
            f"Do you wish to relinquish '{{t1}}' Bounty?\n\n"
            "This bounty will be struck from your journal, and its contract will be voided.",
            remove_mission,
            highlight_text=task_name,
            highlight_text_color="#CFA34B"
        )
            
    # endregion

    # endregion
    
    # region ---------------- TIMER LOGIC ----------------

    def start_session(self):
        try:
            minutes = float(self.control_minutes_var.get())
            if not 0 < minutes <= 1440:
                raise ValueError
            seconds = int(minutes * 60)
        except ValueError:
            self.status_label.config(text="Enter a duration between 0 and 1440 minutes.")
            return

        if self.running:
            return

        self.duration = seconds
        bonus = self.award_getting_started_bonus()
        if self.getting_started_streak >= 2 and bonus:
            self.render_streak_continues_popup(bonus, self._begin_session)
        else:
            self._begin_session()

    def _begin_session(self):
        if self.running:
            return
        
        self.start_time = time.monotonic()
        self.end_time = self.start_time + self.duration
        self.running = True
        self.session_finished = False
    
        self.timer_label.config(font=("Segoe UI", 29, "bold"))
        self.progress_value = 0
        self.stop_button.config(state="normal")
        self.start_button.config(state="disabled")
        self.status_label.config(text="Session in progress...")
        self.overlay_title.config(text="CULTIVATION IN PROGRESS...")
        self.overlay.deiconify()
        self.position_overlay()
        self.root.withdraw()
        self.update_timer()
 
    def update_timer(self):
        if not self.running:
            return

        remaining = max(0, int(self.end_time - time.monotonic()))
        elapsed = min(self.duration, self.duration - remaining)

        minutes, seconds = divmod(remaining, 60)

        self.timer_label.config(
            text=f"{minutes:02d}:{seconds:02d}"
        )

        percent = elapsed / self.duration * 100
        self.update_overlay_progress(percent)

        if remaining <= 0:
            self.finish_session()
            return

        self.after_id = self.root.after(200, self.update_timer)
        
    def finish_session(self):
        self.running = False
        self.session_finished = True

        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
        self.overlay.withdraw()

        self.timer_label.config(text="TIME'S UP!")
        self.timer_label.config(font=("Segoe UI", 20, "bold"))
        self.overlay_title.config(text="MISSION ACCOMPLISHED")
        self.update_overlay_progress(100)

        self.stop_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.status_label.config(text="Session completed!")

        self.root.deiconify()
        self.root.lift()

        self.render_inspection_report_popup()
        
    def stop_session(self):
        if not self.running:
            return

        self.running = False
        self.overlay.withdraw()

        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.timer_label.config(
            text="STOPPED",
            font=("Segoe UI", 22, "bold")
        )
        self.overlay_title.config(text="SESSION ENDED")

        self.stop_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.status_label.config(text="Session stopped.")

        self.root.deiconify()
        self.root.lift()

        self.render_inspection_report_popup()

    def calculate_progression(self):
        remaining_xp = max(0, int(self.xp))
        level = 0

        while True:
            requirement = self.get_realm(level)["xp_required"]
            if remaining_xp < requirement:
                break
            remaining_xp -= requirement
            level += 1

        self.level = level
        return remaining_xp, self.get_realm(level)["xp_required"]

    def award_getting_started_bonus(self):
        today = datetime.now().date()
        today_text = today.isoformat()

        if self.last_getting_started == today_text:
            return 0

        try:
            previous = datetime.strptime(
                self.last_getting_started, "%Y-%m-%d"
            ).date() if self.last_getting_started else None
        except ValueError:
            previous = None

        # Determine streak
        if previous:
            days_missed = (today - previous).days

            if days_missed == 1:
                self.getting_started_streak = min(
                    7, self.getting_started_streak + 1
                )

            elif days_missed > 1:
                # Show missed streak popup
                choice = self.render_missed_streak_popup(
                    self.getting_started_streak
                )

                if choice == "grace":
                    self.getting_started_streak += 1
                    # Preserve existing streak
                    pass

                elif choice == "reset":
                    self.getting_started_streak = 1

                else:
                    return 0

            else:
                return 0

        else:
            self.getting_started_streak = 1

        # Calculate bonus
        bonus = min(
            11,
            5 + (self.getting_started_streak - 1)
        )

        self.last_getting_started = today_text

        self.record_history(
            title=f"Getting started bonus · Day {self.getting_started_streak} streak!", 
            status="BONUS", 
            history_type="Session", 
            duration=0,
            project=None,
            xp_reward= bonus
        )
    
        self.status_label.config(
            text=(
                f"Getting started bonus: +{bonus} XP "
                f"· Day {self.getting_started_streak} streak!"
            )
        )

        return bonus
    
    # endregion

    # region ---------------- SAVE / LOAD ------------
        
    def save_data(self):
        data = {
            "xp": self.xp,
            "total_completed_bounties": self.total_completed_bounties,
            "level": self.level,
            "history": self.history,
            "projects": self.projects,
            "active_project": self.active_project,
            "last_getting_started": self.last_getting_started,
            "getting_started_streak": self.getting_started_streak
        }

        try:
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except OSError as error:
            print(f"Could not save progress: {error}")


    def load_data(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.xp = max(0, int(data.get("xp", 0)))
            self.total_completed_bounties = max(0, int(data.get("total_completed_bounties", 0)))
            self.calculate_progression()

            saved_projects = data.get("projects")
            if isinstance(saved_projects, dict):
                self.projects = {}
                for project, missions in saved_projects.items():
                    if isinstance(missions, list):
                        self.projects[str(project)] = [({"task": m, "duration": 45} if isinstance(m, str) else m) for m in missions if isinstance(m, (str, dict))]
            else:
                old_board = data.get("mission_board", [])
                if isinstance(old_board, list):
                    self.projects = {"General": [({"task": m, "duration": 45} if isinstance(m, str) else m) for m in old_board if isinstance(m, (str, dict))]}
            self.active_project = data.get("active_project", next(iter(self.projects), "General"))
            self.last_getting_started = data.get("last_getting_started")
            self.getting_started_streak = max(0, int(data.get("getting_started_streak", 0)))

            saved_history = data.get("history", [])
            if isinstance(saved_history, list):
                self.history = [
                    entry for entry in saved_history
                    if isinstance(entry, (str, dict))
                ]

        except FileNotFoundError:
            pass
        except (json.JSONDecodeError, ValueError, TypeError, OSError):
            print("Could not load saved progress.")

    # endregion
    
    # region ---------------- TITLE BAR FOR POPUPS -----
    
    def center_geometry(self, popup : tk.Toplevel, size):
        width, height = size
        x = (popup.winfo_screenwidth() - width) // 2
        y = (popup.winfo_screenheight() - height) // 2
        popup.geometry(f"{width}x{height}+{x}+{y}")
        
    def adjust_popup_dimensions(self, popup : tk.Toplevel, size, with_lift=False):
        popup.update_idletasks()
        self.center_geometry(popup, size)

        if with_lift:
            popup.deiconify()
            popup.lift()

        popup.focus_force()

    def create_custom_titlebar(
        self, 
        popup : tk.Toplevel, 
        fixed_size = None, 
        is_dialog = True, 
        with_title_bar = True,
        bg = "#171923",
        start_hidden = False
    ):

        popup.overrideredirect(True)
        popup.resizable(False, False)
        popup.attributes("-topmost", True)
        popup.configure(bg=bg)

        if start_hidden: popup.withdraw()
        if is_dialog: popup.grab_set()

        if fixed_size is not None:
            self.center_geometry(popup, fixed_size)

        # Outer border
        outer_border = tk.Frame(
            popup,
            bg="#5B4A27",
            bd=0
        )
        outer_border.pack(fill="both", expand=True, padx=2, pady=2)

        if with_title_bar:
            title_bar = tk.Frame(outer_border, bg="#222638", height=32)
            title_bar.pack(fill="x")
            title_bar.pack_propagate(False)

            tk.Label(
                title_bar,
                text="✦  ",
                bg="#222638",
                fg="#E5B85C",
                font=("Segoe UI", 8, "bold")
            ).pack(side="left", padx=12)

            close_btn = tk.Button(
                title_bar,
                text="×",
                command=lambda: self.close_custom_popup(popup),
                bg="#222638",
                fg="#B8BED0",
                activebackground="#A83246",
                activeforeground="white",
                relief="flat",
                bd=0,
                font=("Segoe UI", 13, "bold"),
                cursor="hand2"
            )
            close_btn.pack(side="right", padx=8)

            # Drag functionality
            def start_move(event):
                popup._drag_x = event.x_root - popup.winfo_x()
                popup._drag_y = event.y_root - popup.winfo_y()

            def do_move(event):
                x = event.x_root - popup._drag_x
                y = event.y_root - popup._drag_y
                popup.geometry(f"+{x}+{y}")

            title_bar.bind("<Button-1>", start_move)
            title_bar.bind("<B1-Motion>", do_move)

            for widget in title_bar.winfo_children():
                if isinstance(widget, tk.Button):
                    continue

                widget.bind("<Button-1>", start_move)
                widget.bind("<B1-Motion>", do_move)

        # Inner border
        popup_container = tk.Frame(
            outer_border,
            bd=0
        )
        popup_container.pack(fill="both", expand=True, padx=1, pady=1)
        popup_container.configure(bg=bg)

        # Custom title bar
        return popup_container

    def close_custom_popup(self, popup):
        try:
            popup.grab_release()
        except tk.TclError:
            pass

        popup.destroy()

    # endregion

    # region ---------------- HISTORY ----------------

    def record_history(self, title, history_type, status, duration, project, xp_reward):
        if type(duration) == "int":
            duration = f"{duration}m"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        if xp_reward:
            self.award_xp(xp_reward)

        record = {
            "date": timestamp,
            "task": title,
            "duration": duration,
            "type": history_type,
            "project": project,
            "status": status,
            "xp": xp_reward
        }

        self.history.insert(0, record)
        self.save_data()
        self.render_mission_log()

    def confirm_reset_cultivation(self):
        def on_confirm():
            self.level = 0
            self.xp = 0
            self.total_completed_bounties = 0
            self.getting_started_streak = 0
            self.last_getting_started = None
            self.history.clear()

            new_completed_bounty_count = 0
            for rows in self.projects.values():
                 for row in rows:
                    if row["status"] == "completed" and row["is_daily"] == False:
                        new_completed_bounty_count += 1 
                        row["reclaimable"] = False # XP of these bounties cannot be reclaimed
                    else:
                        row.update({
                            "status": "current",
                            "streak_count": 0,
                            "last_done_date": None,
                            "previous_done_date": None
                        })

            self.save_data()
            self.render_mission_log()
            self.render_mission_board()
            self.update_xp_display()
        
        if self.running:
            self.render_message_popup(
                title="SESSION IS RUNNING",
                description="Stop the currently running session before performing this action!",
            )
        else:
            self.render_restart_cultivation_popup(on_confirm)

    def confirm_clear_history(self):
        def clear_history():
            self.history.clear()
            self.render_mission_log()
            self.save_data()
            
        self.render_confirmation_popup(
            "CLEAR CULTIVATION HISTORY?",
            "Are you sure you want to clear all cultivation history?",
            clear_history
        )


    # endregion

if __name__ == "__main__":
    root = tk.Tk()
    app = FocusTimer(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.close_app()
