
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
from collections import defaultdict
import time
import random
import json
import os
import sys
import re
import tkinter.font as tkfont
import math
import ctypes
import pystray
from AssetHandler import AssetHandler, StarIconColors, ASSET_TYPES
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageTk

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
DEEP_MUTED = "#B1A9DC"
PURPLE = "#A78BFA"
BRIGHT_PURPLE="#D2C9E3"
WHITE_GOLD = "#F0E6C6"
GOLD = "#F5C66A"
GREEN = "#65D6A0"
RED = "#F08080"
BLUE = "#79B8F5"

PULSE_GOLD_RECYCLE = [
    "#997a45",
    "#b99a63",
    "#d6b778",
    "#f0d49a",
    "#d6b778",
    "#b99a63"
]

GLOW_MIN_INTENSITY = 0.3   # Minimum glow (0.0 - 1.0)
GLOW_MAX_INTENSITY = 1.00   # Maximum glow (0.0 - 1.0)
GLOW_CHANGE_SPEED = 0.1   # Higher = faster breathing
GLOW_UPDATE_MS = 10         # Animation refresh interval
GLOW_SCALE = 2

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

    (2, 5, "THE PATH OF INITIATION", "Your journey begins here.", # THE PATH OF INITIATION
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

# -------------- TUTORIALS ---------------------------

TUTORIALS_DICT = {
    "onboarding": False,
    "bountyboard": False,
    "chronicles": False,
    "minimize": False,
    "first_session": False,
    "bounty_creation": False,
    "sect_creation": False,
    "markdown_editor": False
}

TUTORIAL_MESSAGES = {
    "onboarding": {
        "title": "Welcome, Cultivator!",
        "description": (
            "Your cultivation journey begins here!\n\n"
            "Establish your own Sects to organize your goals, "
            "take on Bounties to challenge yourself, and earn XP "
            "with every achievement.\n\n"
            "Forge your own path, grow stronger with each step, "
            "and build your legacy. Your journey to greatness "
            "starts now. Are you ready?"
        ),
        "wrapsize": 500
    },
    "bountyboard": {
        "title": "The Bounty Board",
        "description": (
            "Create your own Sects and add Bounties to them. "
            "Track their progress, mark them as completed or postponed, "
            "and keep an eye on your daily streaks."
        ),
        "wrapsize": 500
    },
    "chronicles": {
        "title": "Your Chronicles",
        "description": (
            "Look back on your cultivation journey. "
            "Your completed sessions and past achievements "
            "are recorded here."
        ),
        "wrapsize": 500
    },
    "minimize": {
        "title": "System Tray",
        "description": (
            "Minimizing the app doesn't close it! It simply "
            "hides it while keeping it running in the background.\n\n"
            "Look for the app's icon near your computer's clock. "
            "Double-click it whenever you want to open the app again!"
        ),
        "wrapsize": 450
    },
    "first_session": {
        "title": "Cultivation Overlay",
        "description": (
            "While a cultivation session is running, "
            "you can click the overlay (in the bottom-right section of the screen) to open "
            "the main application again."
        ),
        "wrapsize": 500
    },
    "bounty_creation": {
        "title": "✦ Your First Bounty!",
        "description": (
            "Congratulations! You've created your first Bounty. "
            "Your cultivation journey is officially underway!\n\n"
            "Looking for your next challenge? Check the "
            "recommended Bounties on the right side of your "
            "Dashboard and start a cultivation session with "
            "just one click.\n\n"
            "Keep going, complete your Bounties, and grow stronger!"
        ),
        "wrapsize": 500
    },
    "sect_creation": {
        "title": "✦ Your First Sect!",
        "description": (
            "Congratulations! You've established your first Sect. "
            "Your cultivation journey is taking shape!\n\n"
            "Sects help you organize your Bounties into different "
            "groups, making it easier to manage your goals and "
            "keep track of your progress.\n\n"
            "Build your Sect, take on challenges, and forge your legacy!"
        ),
        "wrapsize": 500
    },
    "markdown_editor": {
        "title": "✦ The Art of Quick Formatting!",
        "description": (
            "Want to create or edit multiple Bounties at once?\n\n"
            "Meet your Markdown Editor! Use its simple text-based "
            "format to organize your Bounties and import them all "
            "in one go.\n\n"
            "Just follow the example provided, and let the app "
            "handle the rest!"
        ),
        "wrapsize": 600
    }
}

# -------------- MAIN CLASS --------------------

class CultivationRealmMain:
    def __init__(self, root):
        self.root = root
        self.root.title("Cultivation Realm")

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

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

        self._mission_virtual = {}
        self._current_popups = []

        self.tutorials = TUTORIALS_DICT
        self.duration = 0
        self.start_time = None
        self.end_time = None
        self.running = False
        self.session_finished = False
        self.chosen_bounty = None

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

        self.setup_data_folder()
        self.load_data()
        self.setup_styles()
        self.build_main()

        self.schedule_update("dashboard", "ui_render_dashboard_xp_display")
        self.schedule_update("dashboard", "ui_update_next_cultivation_display")
        self.schedule_update("board", "render_mission_board")
        self.schedule_update("history", "render_mission_log")

        # print("OK3")

        self.build_overlay()
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

        self.show_window()
        # print("OK4")
        

    # region ---------------- UPDATE SCHEDULER ---------

    def schedule_update(self, tab_name, update_name, args=None):
        args = args or {}
        tab_index = self.tab_names[tab_name]
        current_tab_index = self.notebook.index(self.notebook.select())

        if current_tab_index == tab_index:
            getattr(self, update_name)(**args)
        else:
            self.pending_display_updates.setdefault(
                tab_index, {}
            )[update_name] = args

    def _process_display_updates(self, event=None):
        current_tab_index = self.notebook.index(self.notebook.select())
        
        # update UI
        updates = self.pending_display_updates.pop(current_tab_index, {})

        for update_name, args in updates.items():
            getattr(self, update_name)(**args)
            
        self.check_tutorial_popups(current_tab_index)

    def check_tutorial_popups(self, current_tab_index=None):
        current_tab_index = current_tab_index or  self.notebook.index(self.notebook.select())
        tutorial_map = {
            0: "onboarding",
            1: "bountyboard",
            2: "chronicles"
        }

        tutorial_key = tutorial_map.get(current_tab_index)

        if tutorial_key and tutorial_key not in self.visited_tutorial_tabs:
            self.visited_tutorial_tabs.add(tutorial_key)
            self.check_tutorial(tutorial_key)

    # endregion

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

    def pulse_reset_button(self, reset_btn):
        index = 0

        def pulse():
            nonlocal index

            if not reset_btn.winfo_exists():
                return

            current_tab_index = self.notebook.index(self.notebook.select())
            if current_tab_index == 2:
                reset_btn.update_text_color(PULSE_GOLD_RECYCLE[index])
                index = (index + 1) % len(PULSE_GOLD_RECYCLE)

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

    def pulse_label(self, label, popup_container, speed = 180):
        index = 0

        def pulse():
            nonlocal index
            if not label.winfo_exists():
                return

            label.config(fg=PULSE_GOLD_RECYCLE[index])
            index = (index + 1) % len(PULSE_GOLD_RECYCLE)

            popup_container.after(speed, pulse)

        pulse()

    def create_rank_glow(self, parent, text, bg, fg, font):
        self._rank_text = text
        self._rank_bg = bg
        self._rank_fg = fg
        self._rank_phase = 0.0
        scale = GLOW_SCALE

        tk_font = tkfont.Font(font=font)

        size = abs(int(tk_font.actual("size")))
        weight = tk_font.actual("weight")

        FONTS_DIR = AssetHandler._get_assets_path(ASSET_TYPES.FONTS)

        font_path = FONTS_DIR / (
            "georgiab.ttf" if weight == "bold" else "georgia.ttf"
        )

        self._rank_pil_font = ImageFont.truetype(
            str(font_path),
            size * scale
        )

        bbox = self._rank_pil_font.getbbox(text)

        pad_left = 18 * scale
        pad_right = 18 * scale
        pad_top = 18 * scale
        pad_bottom = 18 * scale

        width = bbox[2] - bbox[0] + pad_left + pad_right
        height = bbox[3] - bbox[1] + pad_top + pad_bottom

        self._rank_image_size = (
            (width + scale - 1) // scale,
            (height + scale - 1) // scale
        )

        # Create text mask
        mask = Image.new("L", (width, height), 0)

        draw = ImageDraw.Draw(mask)
        draw.text(
            (pad_left - bbox[0], pad_top - bbox[1]),
            text,
            font=self._rank_pil_font,
            fill=255
        )

        # Two genuinely blurred glow layers
        self._rank_wide_glow = mask.filter(
            ImageFilter.GaussianBlur(12 * scale)
        )

        self._rank_tight_glow = mask.filter(
            ImageFilter.GaussianBlur(5 * scale)
        )

        self._rank_text_mask = mask

        self.rank_glow_canvas = tk.Canvas(
            parent,
            width=self._rank_image_size[0],
            height=self._rank_image_size[1],
            bg=bg,
            bd=0,
            highlightthickness=0
        )

        self.rank_glow_canvas.pack(anchor="w", padx=(0, 0))

        self._rank_canvas_image = self.rank_glow_canvas.create_image(
            0, 0, anchor="nw"
        )

    def pulse_rank_label(self):

        try:
            if not self.root.winfo_exists():
                return

            if not self.rank_glow_canvas.winfo_exists():
                return

            colors = PULSE_GOLD_RECYCLE

            # Smooth palette interpolation
            self._rank_phase = (
                self._rank_phase + GLOW_CHANGE_SPEED
            ) % len(colors)

            index = int(self._rank_phase)
            fraction = self._rank_phase - index

            c1 = colors[index]
            c2 = colors[(index + 1) % len(colors)]

            rgb1 = tuple(
                int(c1[i:i+2], 16) for i in (1, 3, 5)
            )
            rgb2 = tuple(
                int(c2[i:i+2], 16) for i in (1, 3, 5)
            )

            glow_rgb = tuple(
                int(a + (b - a) * fraction)
                for a, b in zip(rgb1, rgb2)
            )

            # Breathing intensity
            breathing = (
                0.5 + 0.5 * math.sin(
                    self._rank_phase * math.pi / 3
                )
            )

            intensity = (
                GLOW_MIN_INTENSITY
                + (GLOW_MAX_INTENSITY - GLOW_MIN_INTENSITY)
                * breathing
            )

            def make_glow(mask, strength):
                alpha = mask.point(
                    lambda p: int(p * strength * intensity)
                )

                layer = Image.new(
                    "RGBA", mask.size, (*glow_rgb, 0)
                )
                layer.putalpha(alpha)
                return layer

            # Composite the actual blurred aura
            image = Image.new(
                "RGBA",
                self._rank_text_mask.size,
                self._rank_bg
            )

            wide = make_glow(self._rank_wide_glow, 0.65)
            tight = make_glow(self._rank_tight_glow, 0.85)

            image = Image.alpha_composite(image, wide)
            image = Image.alpha_composite(image, tight)

            # Sharp foreground text
            foreground = Image.new(
                "RGBA",
                self._rank_text_mask.size,
                self._rank_fg
            )
            foreground.putalpha(self._rank_text_mask)

            image = Image.alpha_composite(image, foreground)

            # High-quality downsampling
            image = image.resize(
                self._rank_image_size,
                Image.Resampling.LANCZOS
            )

            self._rank_photo = ImageTk.PhotoImage(image)

            self.rank_glow_canvas.itemconfigure(
                self._rank_canvas_image,
                image=self._rank_photo
            )

            self.root.after(GLOW_UPDATE_MS, self.pulse_rank_label)

        except tk.TclError:
            return

    def set_rank_text(self, new_text):
        try:
            if not self.rank_glow_canvas.winfo_exists():
                return

            self._rank_text = new_text

            # Recreate the text mask
            bbox = self._rank_pil_font.getbbox(new_text)

            scale = GLOW_SCALE
            
            pad_left = 18 * scale
            pad_right = 18 * scale
            pad_top = 18 * scale
            pad_bottom = 18 * scale

            width = bbox[2] - bbox[0] + pad_left + pad_right
            height = bbox[3] - bbox[1] + pad_top + pad_bottom

            mask = Image.new("L", (width, height), 0)

            draw = ImageDraw.Draw(mask)
            draw.text(
                (pad_left - bbox[0], pad_top - bbox[1]),
                new_text,
                font=self._rank_pil_font,
                fill=255
            )

            # Update all glow assets
            self._rank_wide_glow = mask.filter(
                ImageFilter.GaussianBlur(12 * scale)
            )

            self._rank_tight_glow = mask.filter(
                ImageFilter.GaussianBlur(5 * scale)
            )

            self._rank_text_mask = mask

            # Cropping
            crop_box = self._rank_wide_glow.point(
                lambda p: 255 if p > 2 else 0
            ).getbbox()

            if crop_box:
                self._rank_text_mask = self._rank_text_mask.crop(crop_box)
                self._rank_wide_glow = self._rank_wide_glow.crop(crop_box)
                self._rank_tight_glow = self._rank_tight_glow.crop(crop_box)

            # Calculate dimensions AFTER cropping
            self._rank_image_size = (
                (self._rank_text_mask.width + scale - 1) // scale,
                (self._rank_text_mask.height + scale - 1) // scale
            )

            # Create Canvas
            self.rank_glow_canvas.configure(
                width=self._rank_image_size[0],
                height=self._rank_image_size[1],
            )

            # Keep animation phase unchanged
            # Next pulse_rank_label() renders the new text

        except tk.TclError:
            return
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
        
        self.check_tutorial("minimize")
        if not self.running:
            return

        self.overlay.deiconify()
        self.overlay.lift()
    
    def show_window(self, event=None):
        self.root.deiconify()
        self.root.overrideredirect(True)
        self.root.state("zoomed")

        # Find the latest popup that still exists
        target = next(
            (popup for popup in reversed(self._current_popups)
            if popup.winfo_exists()),
            self.root
        )

        target.attributes("-topmost", True)
        target.lift()
        target.focus_force()

        if target == self.root: target.attributes("-topmost", False)

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

    def bring_window_to_front(self):
        if self.root.state() == "iconic":
            return

        self.root.lift()
        self.root.focus_force()

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

        # ---------- HEADER ----------
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=18, pady=(12, 8))

        # ==========================================================
        # region Main Frame Setup
        # ==========================================================

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
        self.notebook = ttk.Notebook(
            self.root,
            style="Cultivation.TNotebook"
        )
        self.notebook.pack(fill="both", expand=True, padx=14, pady=(0, 10))

        dashboard_tab = tk.Frame(self.notebook, bg=BG)
        bounty_tab = tk.Frame(self.notebook, bg=BG)
        chronicle_tab = tk.Frame(self.notebook, bg=BG)

        self.notebook.add(dashboard_tab, text="  🏠 DASHBOARD  ")
        self.notebook.add(bounty_tab, text="  ⚔ BOUNTY BOARD  ")
        self.notebook.add(chronicle_tab, text="  📜 CHRONICLE  ")
        
        self.tab_names = {
            "dashboard": 0,
            "board": 1,
            "history": 2
        }

        self.pending_display_updates = {}

        self.notebook.bind(
            "<<NotebookTabChanged>>",
            self._process_display_updates
        )
        
        # Show onboarding when Dashboard is first opened
        self.root.after(100, lambda: self.check_tutorial_popups())
        
        # Track tutorials already triggered this session
        self.visited_tutorial_tabs = set()


        # endregion

        # ==========================================================
        # region DASHBOARD TAB
        # ==========================================================
        dashboard_tab.columnconfigure(0, weight=6, uniform="dashboard")
        dashboard_tab.columnconfigure(1, weight=4, uniform="dashboard")
        dashboard_tab.rowconfigure(0, weight=1)
        dashboard_tab.rowconfigure(1, weight=0, minsize=30)

        left = tk.Frame(dashboard_tab, bg=BG)
        left.grid(
            row=0, column=0,
            sticky="nsew",
            padx=(8, 5),
            pady=(8, 0)
        )

        right = tk.Frame(dashboard_tab, bg=BG)
        right.grid(
            row=0, column=1,
            sticky="nsew",
            padx=(5, 8),
            pady=(8, 0)
        )

        # Cultivation rank
        rank_card, rank_content = self.make_card(
            left, "Cultivation Realm", None, title_color="#9A85BA", icon_type="star", content_pady=(2,0), 
            content_padx=(0, 12), heading_padx=12
        )
        rank_card.pack(fill="x", pady=(0, 8))

        # Main title
        self.create_rank_glow(
            parent=rank_content,
            text="BODY REFINEMENT",
            bg=PANEL,
            fg="#FFD477",
            font=("Georgia", 34, "bold")
        )

        self.pulse_rank_label()
        padding_xl = 18

        # Badge text
        self.level_badge = self.make_rounded_badge(
            rank_content,
            "LEVEL --",
            width=108,
            height=29,
            radius=14,
            bg_color="#58358F",
            outline_color="#7650B8",
            text_color="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            padx=(padding_xl, 0),
            pady=(4, 0)
        )
        
        # Realm description
        self.rank_description = tk.Label(
            rank_content,
            text="You are but an ordinary mortal.",
            bg=PANEL,
            fg="#CDC7E4",
            font=("Segoe UI", 8),
            anchor="w"
        )
        self.rank_description.pack(fill="x", padx=(padding_xl, 0), pady=(6, 25))

        # XP + percentage
        xp_header = tk.Frame(rank_content, bg=PANEL)
        xp_header.pack(fill="x", padx=(padding_xl+4, 0))

        # Current XP
        self.xp_canvas = tk.Canvas(
            xp_header,
            width=500,
            height=22,
            bg=PANEL,
            highlightthickness=0,
            bd=0
        )
        self.xp_canvas.pack(side="left")

        self.xp_current_font = tkfont.Font(
            family="Segoe UI", size=14, weight="bold"
        )
        self.xp_separator_font = tkfont.Font(
            family="Segoe UI", size=12, weight="bold"
        )
        self.xp_max_font = tkfont.Font(
            family="Segoe UI", size=12, weight="bold"
        )

        self.xp_current = self.xp_canvas.create_text(
            0, 21, text="5",
            fill=GOLD,
            font=self.xp_current_font,
            anchor="sw"
        )

        self.xp_separator = self.xp_canvas.create_text(
            0, 21, text="/",
            fill="#FFFFFF",
            font=self.xp_separator_font,
            anchor="sw"
        )

        self.xp_max = self.xp_canvas.create_text(
            0, 21, text="50 XP",
            fill=GOLD,
            font=self.xp_max_font,
            anchor="sw"
        )

        # self.update_xp_display("5", "50")

        # Progress bar styling
        xp_progress_row = tk.Frame(rank_content, bg=PANEL)
        xp_progress_row.pack(fill="x", padx=(padding_xl, 0), pady=(0, 0))

        # Progress bar
        self.xp_progress = tk.Canvas(
            xp_progress_row,
            height=22,
            bg=PANEL,
            highlightthickness=0,
            bd=0
        )
        self.xp_progress.pack(side="left", fill="x", expand=True)

        self.xp_progress_value = 0
        self.xp_progress.bind("<Configure>", self.draw_xp_progress)

        # self.draw_xp_progress()

        # Percentage label
        self.xp_percentage_label = tk.Label(
            xp_progress_row,
            text="10%",
            bg=PANEL,
            fg="#E0DCFF",
            font=("Segoe UI", 10, "bold")
        )
        
        self.xp_percentage_label.pack(
            side="left",
            padx=(11, 5),
            pady=(0, 6)
        )

        # Remaining XP
        # XP to next level row
        xp_next_row = tk.Frame(rank_content, bg=PANEL)
        xp_next_row.pack(anchor="w", padx=(padding_xl, 0))

        self.total_xp_icon = AssetHandler.svg_to_photo(
            AssetHandler.chevrons_down_svg(),
            size=(24, 24)
        )

        tk.Label(
            xp_next_row,
            image=self.total_xp_icon,
            bg=PANEL
        ).pack(side="left", padx=(0, 0))

        self.total_xp_label = tk.Label(
            xp_next_row,
            text="45 XP to next level",
            bg=PANEL,
            fg="#A9A2C7",
            font=("Segoe UI", 8)
        )
        self.total_xp_label.pack(side="left")

        # Separator
        # tk.Frame(
        #     rank_content,
        #     bg=PANEL,
        #     height=1
        # ).pack(fill="x", pady=(10, 8))

        # Next breakthrough
        rank_card2, rank_content2 = self.make_card(
            rank_content,
            has_content=False,
            content_pady=(2, 5),
            border_color="#95825A",
            icon_type="diagram",
            
            icon_size=(28, 28)
        )

        self.next_realm_label = tk.Label(
            rank_content2,
            text="NEXT BREAKTHROUGH: THE PATH OF INITIATION",
            bg=PANEL,
            fg=GOLD,
            font=("Segoe UI", 9, "bold")
        )
        self.next_realm_label.pack(side="left", anchor="w")

        # Flexible empty space between label and chevron
        spacer = tk.Frame(rank_content2, bg=PANEL)
        spacer.pack(side="left", fill="x", expand=True)

        # Chevron at the far right
        self.create_icon(
            rank_content2,
            "chevron-right",
            size=(32, 32),
            side="right",
            glow=True
        )
        rank_content2.pack(fill="x", expand=True)
        rank_card2.pack(fill="both", padx=(padding_xl, 0), pady=(10, 0))
        
        # region DAILY STREAK & LIFETIME XP

        stats_frame = tk.Frame(left, bg=BG)
        stats_frame.pack(fill="x", pady=(0, 8))

        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(2, weight=1)

        # DAILY STREAK
        streak_card, streak_content = self.make_card(
            stats_frame, "Daily Streak", "Consistency", content_pady=(5,5), 
            title_color=WHITE_GOLD, subtitle_color=BRIGHT_PURPLE
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
        lifetime_card, lifetime_content = self.make_card(
            stats_frame, "Lifetime XP", "Total earned", content_pady=(5,5),
            title_color=WHITE_GOLD, subtitle_color=BRIGHT_PURPLE
        )
        lifetime_card.grid(row=0, column=1, sticky="nsew", padx=(4, 0))

        self.create_star_icon(
            lifetime_content,
            color=StarIconColors.GOLD,
            filled=True,
            size=(42, 42)
        )

        self.dashboard_xp_card = tk.Label(
            lifetime_content,
            text=f"{self.xp} XP",
            bg=PANEL,
            fg=GOLD,
            font=("Segoe UI", 17, "bold")
        )
        
        self.dashboard_xp_card.pack(anchor="w", side="left")

        # TOTAL BOUNTIES
        total_bounties_card, total_bounties_content = self.make_card(
            stats_frame, "Bounties Completed", "Total victories", content_pady=(5,5), 
            title_color=WHITE_GOLD, subtitle_color=BRIGHT_PURPLE
        )
        total_bounties_card.grid(row=0, column=2, sticky="nsew", padx=(8, 0))

        self.create_icon(
            total_bounties_content,
            "flower",
            size=(48, 48),
            side="left"
        )

        self.dashboard_bounty_card = tk.Label(
            total_bounties_content,
            text=f"{self.total_completed_bounties} "
                f"{'Bounty' if self.total_completed_bounties == 1 else 'Bounties'}",
            bg=PANEL,
            fg=GOLD,
            font=("Segoe UI", 17, "bold")
        )

        self.dashboard_bounty_card.pack(anchor="w", side="left")
        # endregion

        # region ---------- COMPACT MISSION CREATION ----------
        task_card, task_content = self.make_card(
            left, "New Bounty", "Prepare your next cultivation session",
            icon_type="bounty",
            icon_size=(46, 82),
            content_pady=(4, 2),
            icon_with_subtitle=True

        )
        task_card.pack(fill="x", pady=(0, 8))
        # region Bounty name + Sect picker

        bounty_name_row = tk.Frame(task_content, bg=PANEL)
        bounty_name_row.pack(fill="x", pady=(0, 5))

        # Sect field (left)
        sect_field = tk.Frame(bounty_name_row, bg=PANEL)
        sect_field.pack(side="left", padx=(0, 10))

        tk.Label(
            sect_field,
            text="ASSIGN TO SECT",
            bg=PANEL,
            fg=DEEP_MUTED,
            font=("Segoe UI", 8, "bold"),
            anchor="w"
        ).pack(anchor="w", pady=(0, 2))

        self.bounty_project_var = tk.StringVar(value=self.active_project)

        (
            self.bounty_project_picker,
            self.bounty_project_label,
            self.bounty_project_arrow
        ) = self.create_custom_dropdown(
            parent=sect_field,
            variable=self.bounty_project_var,
            values=lambda: list(self.projects.keys()),
            menu_attr="bounty_project_menu",
            width=70
        )

        # Bounty name field (right)
        name_field = tk.Frame(bounty_name_row, bg=PANEL)
        name_field.pack(side="left", fill="x", expand=True)

        tk.Label(
            name_field,
            text="BOUNTY NAME",
            bg=PANEL,
            fg=DEEP_MUTED,
            font=("Segoe UI", 8, "bold"),
            anchor="w"
        ).pack(anchor="w", pady=(0, 2))

        self.task_var = getattr(
            self, "task_var", tk.StringVar()
        )
        
        self.task_entry_container, self.task_entry = self.make_rounded_entry(
            name_field,
            textvariable=self.task_var,
            icon_type="feather",
            icon_size=(24, 24),
            fg_color=DEEP_MUTED,
            icon_padx=(15, 15),
            height=40,
            radius=12
        )
        # endregion

        # Duration and reward side by side
        fields = tk.Frame(task_content, bg=PANEL)
        fields.pack(fill="x")

        fields.columnconfigure(0, weight=1)
        fields.columnconfigure(1, weight=1)

        # Duration
        duration_field = tk.Frame(fields, bg=PANEL)
        duration_field.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        duration_label = tk.Label(
            duration_field,
            text="DURATION (MIN)",
            bg=PANEL, fg=DEEP_MUTED,
            font=("Segoe UI", 7, "bold")
        )
        duration_label.pack(anchor="w")

        self.minutes_var = getattr(
            self, "minutes_var", tk.StringVar(value="25")
        )

        self.entry_duration_container, self.minutes_entry = self.make_rounded_entry(
            duration_field,
            textvariable=self.minutes_var,
            icon_type="clock",
            fg_color=DEEP_MUTED,
            icon_size=(24, 24),
            icon_padx=(15, 15),
            height=40,
            radius=12
        )

        # XP reward
        reward_field = tk.Frame(fields, bg=PANEL)
        reward_field.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        tk.Label(
            reward_field,
            text="XP REWARD",
            bg=PANEL, fg="#EBBE9C",
            font=("Segoe UI", 7, "bold")
        ).pack(anchor="w")

        self.reward_var = getattr(
            self, "reward_var", tk.StringVar(value="50")
        )

        self.entry_reward_container, self.reward_entry = self.make_rounded_entry(
            reward_field,
            textvariable=self.reward_var,
            fg_color="#FCEB6B",
            icon_type="star",
            icon_size=(24, 24),
            icon_padx=(15, 15),
            height=40,
            radius=12
        )

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
            btn = self.make_button(
                presets,
                str(duration),
                lambda d=duration: self.minutes_var.set(str(d)),
                bg=BRIGHT_PURPLE,
                fg=BRIGHT_PURPLE,
                compact=True,
                font_size=9
            )
            btn.pack(side="left", padx=(3, 0))

        # Post bounty
        self.make_button(
            task_content,
            "✦ POST BOUNTY",
            self.add_mission,
            font_size=9,
            bg=GOLD,
            compact=True
        ).pack(fill="x", pady=(9, 0))
        
        # endregion 

        # region Next Cultivation - Featured Bounty
        next_cultivation_card, self.next_cultivation_bounty_content = self.make_card(
            right, "Cultivation", "Choose your path and begin your training",
            content_pady=(0, 10), border_color="#BC74FB", card_bg="#211F38", 
            has_content=False, content_padx=(12, 10)
        ) #"Focus begins with a single decision"
        next_cultivation_card.pack(fill="x", pady=(0, 8))
        
        # accent = tk.Frame(
        #     self.next_cultivation_frame,
        #     bg="#BC74FB",
        #     height=3
        # )
        # accent.pack(fill="x")
        # accent.pack_propagate(False)

        # self.next_cultivation_bounty_content = tk.Frame(
        #     self.next_cultivation_frame,
        #     bg="#211F38",
        #     padx=13,
        #     pady=11
        # )
        # self.next_cultivation_bounty_content.pack(fill="x")

        # endregion

        # region Mission controls
        control_card, control_content = self.make_card(
            right, "Cultivation", "Choose your path and begin your training",
            icon_type="crest",
            icon_size=(46, 82),
            content_pady=(4, 2),
            icon_with_subtitle=True

        ) #"Focus begins with a single decision"
        control_card.pack(fill="x", pady=(0, 8))

        duration_field = tk.Frame(control_content, bg=PANEL)
        duration_field.pack(fill="x", pady=(10, 9))

        tk.Label(
            duration_field,
            text="CULTIVATION DURATION (MIN)",
            bg=PANEL,
            fg=DEEP_MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", pady=(0, 2))

        self.control_minutes_var = getattr(
            self, "control_minutes_var", tk.StringVar(value="25")
        )

        self.control_minutes_container, self.control_minutes_entry = self.make_rounded_entry(
            duration_field,
            textvariable=self.control_minutes_var,
            fg_color=TEXT,
            icon_type=None,
            height=40,
            radius=12
        )

        # Quick duration presets
        duration_presets = tk.Frame(control_content, bg=PANEL)
        duration_presets.pack(fill="x")

        for duration in (5, 10, 25, 30, 45):
            btn = self.make_button(
                duration_presets,
                f"{duration}m",
                lambda d=duration: self.control_minutes_var.set(str(d)),
                bg=BRIGHT_PURPLE,
                compact=True,
                font_size=7
            )

            btn.pack(side="left", expand=True, fill="x", padx=2)
            
        self.start_button = self.make_button(
            control_content, "▶  BEGIN CULTIVATION",
            self.start_session, GREEN
        )
        self.start_button.pack(fill="x", pady=(10, 6))

        self.stop_button = self.make_button(
            control_content, "■  END CULTIVATION",
            self.stop_session, RED
        )
        self.stop_button.pack(fill="x", pady=(0, 6))

        self.hide_button = self.make_button(
            control_content, "➖  MINIMIZE",
            self.minimize_window,
            bg=BRIGHT_PURPLE
        )
        self.hide_button.pack(fill="x")

        # endregion

        # region Status footer
        status_frame = tk.Frame(dashboard_tab, bg=BG)
        status_frame.grid(
            row=1, column=0, columnspan=2,
            sticky="ew"
        )

        self.status_label = tk.Label(
            status_frame,
            text="✦  Your cultivation journey awaits.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 8)
        )
        self.status_label.pack(
            anchor="w",
            padx=12,
            pady=6
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
            ("CURRENT", PURPLE, StarIconColors.PURPLE, True, 10, 0.6),
            ("COMPLETED", GREEN, StarIconColors.GREEN, False, 6, 0.6),
            ("POSTPONED", GOLD, StarIconColors.GOLD, True, 10, 0.6),
        ]

        board.grid_rowconfigure(0, weight=1)

        self.mission_canvases = {}
        for col, (status, accent, star_color, star_filled, star_radius, star_strength) in enumerate(status_columns):
            grid_col = tk.Frame(board, bg=BG)
            grid_col.grid(
                row=0, column=col, sticky="nsew",
                padx=4, pady=4
            )

            grid_col.grid_rowconfigure(0, weight=1)
            grid_col.grid_columnconfigure(0, weight=1)

            col_card, column = self.make_card(
                grid_col, status, None,
                title_color=accent,
                icon_type="star",
                star_color=star_color,
                star_filled=star_filled,
                star_glow=(star_radius, star_strength),
                content_padx=(9, 0),
                content_pady=(9, 0),
                expand_height=True
            )

            col_card.pack(fill="both", expand=True, padx=4, pady=4)

           # Scrollable mission area
            scroll_container = tk.Frame(column, bg=PANEL)
            scroll_container.pack(
                fill="both", expand=True, padx=7, pady=0
            )

            scrollbar_frame = tk.Frame(
                scroll_container,
                bg=PANEL,
                width=12
            )
            scrollbar_frame.pack(side="right", fill="y")
            scrollbar_frame.pack_propagate(False)

            mission_canvas = tk.Canvas(
                scroll_container,
                bg=PANEL,
                highlightthickness=0
            )
            mission_canvas.pack(
                side="left",
                fill="both",
                expand=True,
                padx=(0, 8)
            )

            mission_scrollbar = ttk.Scrollbar(
                scrollbar_frame,
                orient="vertical",
                command=mission_canvas.yview,
                style="Mission.Vertical.TScrollbar"
            )
            mission_scrollbar.pack(
                side="right",
                fill="y",
                expand=True
            )

            # Frame that actually lives inside the Canvas
            mission_inner = tk.Frame(mission_canvas, bg=PANEL)

            mission_canvas.configure(
                yscrollcommand=mission_scrollbar.set
            )
            mission_window = mission_canvas.create_window(
                (0, 0),
                window=mission_inner,
                anchor="nw"
            )

            # Keep embedded Frame as wide as Canvas
            mission_canvas.bind(
                "<Configure>",
                lambda event, canvas=mission_canvas, window=mission_window:
                    canvas.itemconfigure(window, width=event.width)
            )

            self.mission_canvases[status.lower()] = mission_canvas
            self.mission_rows[status.lower()] = (mission_inner, mission_scrollbar)
            
            self.bind_wheel_recursive(
                mission_inner,
                mission_canvas,
                lambda ev: self.update_virtual(status) 
            )

        # Project and mission actions
        actions = tk.Frame(bounty_tab, bg=BG)
        actions.grid(row=2, column=0, sticky="ew", padx=12, pady=(4, 12))

        self.project_var = tk.StringVar(value=self.active_project)

        (
            self.project_picker,
            self.project_label,
            self.project_arrow
        ) = self.create_custom_dropdown(
            parent=actions,
            variable=self.project_var,
            values=lambda: list(self.projects.keys()),
            on_select=self.change_project,
            menu_attr="project_menu",
            bg="#212247",
            height=50,
            width=70
        )
        
        self.make_button(
            actions, "+ SECT", self.render_add_project_popup, colors = {
                "base_bg": "#212247",
                "base_bd": "#3C3B69",
                "base_fg": "#FCE7FF",
                "highlight_bg": "#3C3B69",
                "highlight_bd": "#3C3B69",
                "highlight_fg": "#FCE7FF",
            }, compact=True, font_size=8, radius = (7, 9), size=(100, 50)
        ).pack(side="left", padx=3)

        self.make_button(
            actions, "EDIT BOUNTIES", self.render_edit_mission_markdown_popup, colors = {
                "base_bg": "#212247",
                "base_bd": "#3C3B69",
                "base_fg": "#FCE7FF",
                "highlight_bg": "#3C3B69",
                "highlight_bd": "#3C3B69",
                "highlight_fg": "#FCE7FF",
            }, compact=True, font_size=8, radius = (7, 9), size=(180, 50)
        ).pack(side="left", padx=3)

        # endregion

        # ==========================================================
        # region CHRONICLE TAB
        # ==========================================================
        chronicle_tab.rowconfigure(0, weight=1)
        chronicle_tab.columnconfigure(0, weight=1)
        chronicle_card, chronicle_content = self.make_card(
            chronicle_tab,
            "Cultivation Chronicle",
            "A record of your completed sessions and progress",
            expand_height=True
        )

        chronicle_card.grid(
            row=0, column=0, sticky="nsew",
            padx=12, pady=12
        )

        # Header action button
        reset_border =  tk.Frame(
            chronicle_card,
            bg=PANEL,
            padx=2,
            pady=2
        )

        reset_border.place(relx=0.99, y=12, anchor="ne")

        # Actual button
        
        reset_btn= self.make_button(
            reset_border,
            "✦  RESET CULTIVATION",
            command=self.confirm_reset_cultivation,
            colors={
                "base_bg": "#171923",
                "base_text": "#b99a63",
                "base_bd": "#b99a63",
                "highlight_bg": "#292536",
                "highlight_text": "#e5c58b",
                "highlight_bd": "#e5c58b"
            },
            compact=False,
            font_size=8,
            radius=(7, 5),
            highlight=False
        )
        reset_btn.pack(side="left")

        self.pulse_reset_button(reset_btn)
        
        # chronicle_content.pack_propagate(True)

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
            content_height = self.log_inner.winfo_reqheight()

            self.log_canvas.itemconfigure(
                self.log_window,
                width=event.width,
                height=max(event.height, content_height)
            )

        self.log_canvas.bind("<Configure>", resize_log)

        self.log_inner.bind(
            "<Configure>",
            lambda e: self.log_canvas.configure(
                scrollregion=self.log_canvas.bbox("all")
            )
        )

        # endregion
     

    def _build_mission_card(self, parent, item, status, today_str):
        is_daily = item.get("is_daily", False)
        last_done = item.get("last_done_date")
        streak = item.get("streak_count", 0)
        done_today = is_daily and last_done == today_str

        card = tk.Frame(
            parent, bg="#222A3D",
            highlightbackground="#65D6A0" if done_today else "#303A52",
            highlightthickness=1
        )

        header = tk.Frame(card, bg="#222A3D")
        header.pack(fill="x", padx=8, pady=(7, 3))

        tk.Label(
            header, text=item.get("task"),
            bg="#222A3D", fg="#E8EAF2",
            font=("Segoe UI", 9, "bold"),
            anchor="w", wraplength=500, justify="left"
        ).pack(side="left", fill="x", expand=True)

        if is_daily:
            badge_text, badge_bg, badge_fg = (
                "♻ DAILY", "#244D43", "#65D6A0"
            )
        else:
            badge_text, badge_bg, badge_fg = (
                "◆ STANDARD", "#293B5B", "#91B9FF"
            )

        self.make_button(
            header, badge_text,
            colors={
                "base_bg": badge_bg,
                "base_text": badge_fg,
                "base_bd": badge_bg
            },
            compact=False, font_size=7,
            size=(100, 34), radius=(12, 10), badge=True
        ).pack(side="left", padx=(4, 0), pady=3)

        tk.Frame(card, bg="#354057", height=1).pack(
            fill="x", padx=8, pady=3
        )

        details = tk.Frame(card, bg="#222A3D")
        details.pack(fill="x", padx=8, pady=3)

        tk.Label(
            details, text=f"◷ {item.get('duration', 45)} min",
            bg="#222A3D", fg="#AAB0C0",
            font=("Segoe UI", 8)
        ).pack(side="left")

        tk.Label(
            details, text=f"✦ {item.get('reward_xp', 0)} XP",
            bg="#222A3D", fg="#F5C66A",
            font=("Segoe UI", 8, "bold")
        ).pack(side="right")

        if is_daily:
            streak_frame = tk.Frame(
                card, bg="#302B43",
                highlightbackground="#51446F",
                highlightthickness=1
            )
            streak_frame.pack(fill="x", padx=7, pady=(5, 4))

            streak_header = tk.Frame(streak_frame, bg="#302B43")
            streak_header.pack(fill="x", padx=7, pady=(5, 2))

            tk.Label(
                streak_header, text="🔥 CULTIVATION STREAK",
                bg="#302B43", fg="#F5C66A",
                font=("Segoe UI", 7, "bold")
            ).pack(side="left")

            self.make_button(
                streak_header, f"{streak} DAYS",
                colors={
                    "base_bg": "#51412E",
                    "base_text": "#F5D98A",
                    "base_bd": "#51412E"
                },
                compact=False, font_size=7,
                size=(80, 28), radius=(12, 10), badge=True
            ).pack(side="right", padx=6, pady=2)

            completion_text = (
                "✓ COMPLETED TODAY" if done_today
                else "○ AVAILABLE TODAY"
            )
            completion_color = "#65D6A0" if done_today else "#BDB5D5"
            completion_bg = "#1E493B" if done_today else "#39334D"

            self.make_button(
                streak_frame, completion_text,
                colors={
                    "base_bg": completion_bg,
                    "base_text": completion_color,
                    "base_bd": completion_bg
                },
                compact=False, center_content=False,
                font_size=8, size=(80, 45),
                radius=(7, 5), badge=True
            ).pack(fill="x", padx=6, pady=(2, 5))

            tk.Label(
                streak_frame,
                text=f"Last completed: {last_done or 'Never'}",
                bg="#302B43",
                fg="#65D6A0" if done_today else "#929BB2",
                font=("Segoe UI", 7), anchor="w"
            ).pack(fill="x", padx=7, pady=(0, 6))

        elif status == "completed":
            tk.Label(
                card,
                text=f"✓ Completed: {item.get('completed_date', 'Unknown')}",
                bg="#222A3D", fg="#65D6A0",
                font=("Segoe UI", 7), anchor="w"
            ).pack(fill="x", padx=8, pady=4)

        buttons = tk.Frame(card, bg="#222A3D")
        buttons.pack(fill="x", padx=5, pady=(5, 7))

        if status == "current":
            self.make_button(
                buttons, "COMPLETE",
                command=lambda m=item: self.change_mission_status(m, "completed"),
                colors={
                    "base_bg": "#65D6A0", "base_text": "#10131D",
                    "base_bd": "#65D6A0", "highlight_bg": "#5ABC8D",
                    "highlight_text": "#10131D", "highlight_bd": "#5ABC8D"
                },
                compact=False, font_size=7, size=(100, 34),
                radius=(7, 5)
            ).pack(side="left", padx=2, pady=3)

            self.make_button(
                buttons, "POSTPONE",
                command=lambda m=item: self.change_mission_status(m, "postponed"),
                colors={
                    "base_bg": "#F5C66A", "base_text": "#10131D",
                    "base_bd": "#F5C66A", "highlight_bg": "#C19D55",
                    "highlight_text": "#10131D", "highlight_bd": "#C19D55"
                },
                compact=False, font_size=7, size=(100, 34),
                radius=(7, 5)
            ).pack(side="left", padx=2, pady=3)

        elif done_today:
            tk.Label(
                buttons, text="✦ BOUNTY CLAIMED",
                bg="#222A3D", fg="#65D6A0",
                font=("Segoe UI", 7, "bold")
            ).pack(side="left", padx=3)

            self.make_button(
                buttons, "⟲ UNDO",
                command=lambda m=item: self.undo_daily_completion(m),
                colors={
                    "base_bg": "#D69A65", "base_text": "#10131D",
                    "base_bd": "#D69A65", "highlight_bg": "#D18B4D",
                    "highlight_text": "#10131D", "highlight_bd": "#D18B4D"
                },
                compact=False, font_size=7, size=(80, 34),
                radius=(7, 5)
            ).pack(side="left", padx=2, pady=3)

        else:
            self.make_button(
                buttons, "RESTORE",
                command=lambda m=item: self.change_mission_status(m, "current"),
                colors={
                    "base_bg": "#A78BFA", "base_text": "#10131D",
                    "base_bd": "#A78BFA", "highlight_bg": "#926FFA",
                    "highlight_text": "#10131D", "highlight_bd": "#926FFA"
                },
                compact=False, font_size=7, size=(165, 34),
                radius=(7, 5)
            ).pack(side="left", padx=2, pady=3)

        if is_daily and streak > 0:
            self.make_button(
                buttons, "RESET STREAK",
                command=lambda m=item, d=done_today: self.reset_daily_streak(m, d),
                colors={
                    "base_bg": "#402144", "base_text": "#F57D6A",
                    "base_bd": "#F57D6A", "highlight_bg": "#402144",
                    "highlight_text": "#F1634D", "highlight_bd": "#F1634D"
                },
                compact=False, font_size=7, size=(110, 34),
                radius=(7, 5)
            ).pack(side="left", padx=2, pady=3)

        self.make_button(
            buttons, "✕ DELETE",
            command=lambda m=item: self.confirm_remove_mission(m),
            colors={
                "base_bg": "#402144", "base_text": "#EC6275",
                "base_bd": "#EC6275", "highlight_bg": "#402144",
                "highlight_text": "#E86969", "highlight_bd": "#E86969"
            },
            compact=False, font_size=7, size=(120, 34),
            radius=(7, 5)
        ).pack(side="right", padx=2, pady=3)

        return card
    
    # region MISSION BOARD RENDERER
    def render_mission_board(self, reset_scroll=False):
        self.refresh_project_picker()
        self.schedule_update(
            "dashboard",
            "ui_update_next_cultivation_display"
        )

        grouped, today_str = self.current_grouped_missions()
        def update_scrollbar(canvas, inner, scrollbar):
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))

            content_height = inner.winfo_reqheight()
            visible_height = canvas.winfo_height()

            if content_height > visible_height:
                if not scrollbar.winfo_ismapped():
                    scrollbar.pack(side="right", fill="y")
            else:
                if scrollbar.winfo_ismapped():
                    scrollbar.pack_forget()

        for status in self.mission_rows.keys():
            missions = grouped.get(status, [])

            canvas = self.mission_canvases[status]
            inner, scrollbar = self.mission_rows[status]
            
            if len(missions) <= 10:
                self._render_mission_board_normal(
                    status, missions, today_str, canvas, inner, reset_scroll
                )

                state = self._mission_virtual.setdefault(status, {})
                state["mode"] = "normal"
                update_scrollbar(canvas, inner, scrollbar)
                
            else:
                self._render_mission_board_virtual(
                    status, missions, today_str, canvas, inner, reset_scroll
                )
                if not scrollbar.winfo_ismapped():
                    scrollbar.pack(side="right", fill="y")

            scrollbar.configure(command=canvas.yview)
            canvas.configure(yscrollcommand=scrollbar.set)
                
    def _render_mission_board_virtual(
            self, status, missions, today_str, canvas, inner, reset_scroll=False
    ):
        # Render each column normally.
        old_state = self._mission_virtual.get(status)

        if reset_scroll or old_state is None:
            saved_position = 0
        else:
            saved_position = canvas.yview()[0]

        # Clear the previous render once, not while scrolling.
        for child in inner.winfo_children():
            child.destroy()

        state = {
            "missions": missions,
            "today": today_str,
            "pool": [],
            "heights": {},
            "refresh_id": None,
            "last_view": None,
            "inner": inner,
            "position": saved_position,
            "mode": "virtual"
        }

        self._mission_virtual[status] = state

        def get_height(index, s=state):
            if index in s["heights"]:
                return s["heights"][index]

            item = s["missions"][index]
            if item.get("is_daily"):
                return 297 if status.lower() == "completed" else 297
            else:
                return 177 if status.lower() == "completed" else 144

        def measure_new_cards(slots, st=status):
            s = self._mission_virtual[st]
            changed = False

            for slot in slots:
                index = getattr(slot, "_mission_index", None)
                if index is None:
                    continue

                slot.update_idletasks()
                actual_height = slot.winfo_reqheight() + 20

                if actual_height > 8 and s["heights"][index] != actual_height:
                    s["heights"][index] = actual_height
                    changed = True

            if changed:
                layout(st, preserve_top=True)

        def rebuild_mission_layout_cache(s, get_height):
            missions = s["missions"]
            card_gap = 10

            heights = [get_height(i, s) for i in range(len(missions))]

            positions = []
            total_height = 0

            for height in heights:
                positions.append(total_height)
                total_height += height + card_gap

            s["heights"] = heights
            s["positions"] = positions
            s["total_height"] = total_height
            s["last_visible"] = None   
 
        def layout(st=status, preserve_top=False):
            s = self._mission_virtual[st]
            c = self.mission_canvases[st]
            missions = s["missions"]
            # print(st, "stored mission count:", len(s["missions"]))

            if not missions:
                return

            width = max(c.winfo_width(), 1)
            viewport = max(c.winfo_height(), 1)

            # Rebuild cache only when needed.
            if (
                s.get("heights") is None
                or s.get("cached_width") != width
                or len(s["heights"]) != len(missions)
            ):
                rebuild_mission_layout_cache(s, get_height)
                s["cached_width"] = width

            heights = s["heights"]
            positions = s["positions"]
            total_height = max(s["total_height"], viewport)

            if preserve_top:
                old_top = c.canvasy(0)
            else:
                old_top = None

            s["inner"].configure(
                width=width,
                height=total_height
            )

            c.configure(
                scrollregion=(0, 0, width, total_height)
            )

            if old_top is not None:
                max_scroll = max(total_height - viewport, 1)
                c.yview_moveto(
                    min(old_top / max_scroll, 1)
                )

            top = c.canvasy(0)
            bottom = top + viewport

            # Find the visible range.
            first = 0

            while (
                first < len(missions)
                and positions[first] + get_height(first, s) < top
            ):
                first += 1

            start = max(0, first - 2)
            end = start

            while end < len(missions):
                if positions[end] > bottom + 300:
                    break
                end += 1

            visible_indices = list(range(start, end))
            if visible_indices == s.get("last_visible"):
                return

            s["last_visible"] = visible_indices
            # print(st, start, end)

            # Reuse existing slots whenever possible.
            used_slots = set()
            new_slots = []

            # print(st, "visible:", visible_indices, len(s["missions"]))
            for index in visible_indices:
                slot = next(
                    (
                        candidate
                        for candidate in s["pool"]
                        if candidate not in used_slots
                        and getattr(candidate, "_mission_index", None) == index
                    ),
                    None
                )

                if slot is None:
                    slot = next(
                        (
                            candidate
                            for candidate in s["pool"]
                            if candidate not in used_slots
                        ),
                        None
                    )

                if slot is None:
                    slot = tk.Frame(s["inner"], bg="#222A3D")
                    s["pool"].append(slot)

                used_slots.add(slot)

                assigned_index = getattr(
                    slot, "_mission_index", None
                )

                if assigned_index != index:
                    for child in slot.winfo_children():
                        child.destroy()

                    card = self._build_mission_card(
                        slot,
                        missions[index],
                        st,
                        s["today"]
                    )
                    card.pack(fill="both", expand=True)

                    self.bind_wheel_recursive(
                        card,
                        canvas,
                        lambda ev: self.update_virtual(status) 
                    )

                    slot._mission_index = index
                    slot._mission_measured = False
                    new_slots.append(slot)

                slot.place(
                    x=0,
                    y=positions[index],
                    width=width,
                    height=get_height(index, s),
                    anchor="nw"
                )
                # print(st, index, positions[index], get_height(index, s))

            # Hide unused slots without destroying them.
            for slot in s["pool"]:
                if slot not in used_slots:
                    slot.place_forget()

            if new_slots:
                self.root.after_idle(
                    lambda slots=new_slots, st=status:
                        measure_new_cards(slots, st)
                )

        # Connect Canvas scrolling to the virtualizer.
        scrollbar = next(
            (
                widget
                for widget in canvas.master.winfo_children()
                if isinstance(widget, ttk.Scrollbar)
            ),
            None
        )

        def on_yview(first, last, sb=scrollbar):
            if sb:
                sb.set(first, last)

        canvas.configure(yscrollcommand=on_yview)

        if scrollbar:
            def scroll_canvas(*args, c=canvas, st=status):
                c.yview(*args)
                self.root.after_idle(
                    lambda: self._mission_virtual[st]["layout"]()
                )

            scrollbar.configure(command=scroll_canvas)

        # Store the latest layout callback for this column.
        self._mission_virtual[status]["layout"] = layout

        # Bind events only once per canvas.
        if not getattr(canvas, "_mission_events_bound", False):
            def on_canvas_resize(event, c=canvas):
                state = self._mission_virtual.get(status)
                if state and state.get("layout"):
                    self.root.after_idle(state["layout"])

            canvas.bind("<Configure>", on_canvas_resize, add="+")
            canvas._mission_events_bound = True

        # Restore this column's scroll position.
        canvas.yview_moveto(saved_position)

        layout(status)
   
    def _render_mission_board_normal(
        self, status, missions, today_str, canvas, inner, reset_scroll=False
    ):
        # Save each column's scroll position.
        scroll_position = 0 if reset_scroll else canvas.yview()[0]

        # Remove previous cards.
        for child in inner.winfo_children():
            child.destroy()

        if not missions:
            tk.Label(
                inner,
                text="No bounties here",
                bg="#1A2030",
                fg="#929BB2",
                font=("Segoe UI", 8, "italic")
            ).pack(pady=12)

        for item in missions:
            card = self._build_mission_card(
                inner,
                item,
                status,
                today_str
            )

            card.pack(
                fill="x",
                expand=False,
                pady=4
            )

            self.bind_wheel_recursive(
                card,
                canvas,
                lambda ev: self.update_virtual(status) 
            )

            card.update_idletasks()
            # card_height = card.winfo_height()

        def restore_scroll():
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.yview_moveto(scroll_position)

        self.root.after_idle(restore_scroll)
  
    def update_virtual(self, status):
        state = self._mission_virtual.get(status)
        if state and state.get("mode") == "virtual" and state.get("layout"):
            self.root.after_idle(state["layout"])

    def bind_wheel_recursive(self, widget, scrollable, custom_update=None):
        def on_mousewheel(event):
            first, last = scrollable.yview()

            # No scrolling needed if everything is visible
            if first <= 0 and last >= 1:
                return "break"

            if event.num == 4:
                direction = -1
            elif event.num == 5:
                direction = 1
            else:
                direction = -1 if event.delta > 0 else 1

            # Prevent scrolling beyond the boundaries
            if direction < 0 and first <= 0:
                return "break"

            if direction > 0 and last >= 1:
                return "break"

            scrollable.yview_scroll(direction, "units")

            if custom_update:
                custom_update(event)

            return "break"

            scrollable.yview_scroll(direction, "units")

            if custom_update:
                custom_update(event)

            return "break"

        widget.bind("<MouseWheel>", on_mousewheel, add="+")
        widget.bind("<Button-4>", on_mousewheel, add="+")
        widget.bind("<Button-5>", on_mousewheel, add="+")

        for child in widget.winfo_children():
            self.bind_wheel_recursive(child, scrollable, custom_update)
  
    # endregion

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
                latest_bounties.setdefault(project, []).append(entry)

        today_bounties = sum(
            1
            for entries in latest_bounties.values()
            for entry in entries
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
            bg=PANEL
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
            bg=PANEL
        )
        header_frame.pack(fill="x", padx=8, pady=(4, 8))

        tk.Label(
            header_frame,
            text="HISTORY",
            font=("Segoe UI", 9, "bold"),
            fg="#f0f0f5",
            bg=PANEL
        ).pack(side="left")

        self.make_button(
            header_frame,
            "Clear History",
            command=self.confirm_clear_history,
            colors={
                "base_bg": "#292333",
                "base_text": "#ff8b8b",
                "base_bd": "#ff8b8b",
                "highlight_bg": "#292333",
                "highlight_text": "#a83246",
                "highlight_bd": "#a83246"
            },
            compact=False,
            font_size=7,
            size = (150, 45),
            radius=(10, 8)
        ).pack(side="right", padx=12, pady=(6, 4))
        

        # ==============================
        # SCROLLABLE MISSION LIST
        # ==============================
        list_frame = tk.Frame(history_container, bg=PANEL)
        list_frame.pack(fill="both", expand=True)

        mission_canvas = tk.Canvas(
            list_frame,
            bg=PANEL,
            highlightthickness=0
        )

        mission_scrollbar = ttk.Scrollbar(
            list_frame,
            orient="vertical",
            command=mission_canvas.yview,
            style="Mission.Vertical.TScrollbar"
        )

        mission_scrollbar.pack(side="right", fill="y")
        mission_canvas.pack(side="left", fill="both", expand=True)

        mission_canvas.configure(
            yscrollcommand=mission_scrollbar.set
        )

        # Fonts
        task_font = tkfont.Font(
            family="Segoe UI", size=9, weight="bold"
        )
        normal_font = tkfont.Font(
            family="Segoe UI", size=9
        )
        small_font = tkfont.Font(
            family="Segoe UI", size=7
        )
        badge_font = tkfont.Font(
            family="Segoe UI", size=7, weight="bold"
        )
        xp_font = tkfont.Font(
            family="Segoe UI", size=8, weight="bold"
        )

        # ==============================
        # TEXT WRAPPING
        # ==============================
        def wrap_text(text, font, max_width):
            words = str(text).split()
            lines = []
            current = ""

            for word in words:
                candidate = f"{current} {word}".strip()

                if current and font.measure(candidate) > max_width:
                    lines.append(current)
                    current = word
                else:
                    current = candidate

            if current:
                lines.append(current)

            return lines or [""]


        # ==============================
        # PREPARE CARD POSITIONS
        # ==============================
        card_layouts = []

        CARD_HEIGHT = 34
        PROJECT_BADGE_HEIGHT = 25
        FOOTER_Y_UP_PADDING = 31 # the lower the higher actually lol
        MISSION_TYPE_BADGE_HEIGHT = 25
        MISSION_STATUS_BADGE_HEIGHT = 25
        XP_BADGE_HEIGHT = 25

        def prepare_layout():
            card_layouts.clear()

            width = max(200, mission_canvas.winfo_width())
            card_width = width - 8

            y = 4

            for entry in self.history:
                status = str(entry.get("status", ""))
                mission_type = str(
                    entry.get("type", "GENERAL")
                ).upper()

                accent = {
                    "COMPLETED": "#65cb91",
                    "BONUS": "#ff8ccf",
                    "SKIPPED": "#696969",
                    "PARTIALLY COMPLETED": "#e5b85c"
                }.get(status, "#e5b85c")

                task = entry.get("task")
                project = entry.get("project")

                task_lines = (
                    wrap_text(task, task_font, 330)
                    if task is not None and mission_type != "SESSION"
                    else wrap_text(task, task_font, 380)
                    if task is not None
                    else []
                )

                top_height = max(
                    18,
                    len(task_lines) * 15
                )

                # CARD HEIGHT
                card_height = 22 + top_height + CARD_HEIGHT

                card_layouts.append({
                    "entry": entry,
                    "y": y,
                    "height": card_height,
                    "width": card_width,
                    "status": status,
                    "accent": accent,
                    "mission_type": mission_type,
                    "task_lines": task_lines,
                    "project": project
                })

                y += card_height + 6

            total_height = max(y + 4, mission_canvas.winfo_height())

            mission_canvas.configure(
                scrollregion=(0, 0, width, total_height)
            )


        # ==============================
        # DRAW VISIBLE CARDS ONLY
        # ==============================
        def draw_visible_cards():
            mission_canvas.delete("mission_card")

            top = mission_canvas.canvasy(0)
            bottom = top + mission_canvas.winfo_height()

            for item in card_layouts:
                y = item["y"]
                height = item["height"]

                # Skip cards outside the visible area
                if y + height < top - 100 or y > bottom + 100:
                    continue

                entry = item["entry"]
                status = item["status"]
                mission_type = item["mission_type"]
                accent = item["accent"]

                x = 4
                width = item["width"]

                # Card background
                mission_canvas.create_rectangle(
                    x, y, x + width, y + height,
                    fill="#242638",
                    outline="#393d54",
                    width=1,
                    tags="mission_card"
                )

                # Project badge
                current_x = x + 10
                
                
                if item["project"] is not None:
                    project_text = f" {item['project']} "
                    project_width = badge_font.measure(project_text)
                    
                    mission_canvas.create_rectangle(
                        current_x, y + 10,
                        current_x + project_width + 8, y + PROJECT_BADGE_HEIGHT + 8,
                        fill="#393052",
                        outline="",
                        tags="mission_card"
                    )

                    mission_canvas.create_text(
                        current_x + 4, y + 12,
                        text=project_text,
                        anchor="nw",
                        font=badge_font,
                        fill="#fff39a",
                        tags="mission_card"
                    )

                    current_x += project_width + 15

                # Task title
                task = entry.get("task")

                if task is not None:
                    if mission_type != "SESSION":
                        mission_canvas.create_text(
                            current_x, y + 8,
                            text="Task: ",
                            anchor="nw",
                            font=normal_font,
                            fill="#9298aa",
                            tags="mission_card"
                        )
                        current_x += normal_font.measure("Task: ")

                    for index, line in enumerate(item["task_lines"]):
                        mission_canvas.create_text(
                            current_x,
                            y + 8 + index * 15,
                            text=line,
                            anchor="nw",
                            font=task_font,
                            fill="#f0f0f5",
                            tags="mission_card"
                        )

                # Date and duration
                duration = entry.get("duration", 0)

                duration_text = (
                    f"{duration}m"
                    if isinstance(duration, int) and duration >= 1
                    else duration
                    if isinstance(duration, str)
                    else None
                )

                date_text = str(entry.get("date", "—"))

                if duration_text is not None:
                    date_text += f"  ·  {duration_text}"

                mission_canvas.create_text(
                    x + width - 10,
                    y + 9,
                    text=date_text,
                    anchor="ne",
                    font=small_font,
                    fill="#aab0c0",
                    tags="mission_card"
                )

                # Bottom information row (FOOTER)
                details_y = y + height - FOOTER_Y_UP_PADDING

                # Mission type badge
                type_text = f" {mission_type} "
                type_width = badge_font.measure(type_text)

                mission_canvas.create_rectangle(
                    x + 10, details_y,
                    x + 10 + type_width + 8, details_y + MISSION_TYPE_BADGE_HEIGHT,
                    fill="#393052",
                    outline="",
                    tags="mission_card"
                )

                mission_canvas.create_text(
                    x + 14, details_y + 2,
                    text=type_text,
                    anchor="nw",
                    font=badge_font,
                    fill="#b99aff",
                    tags="mission_card"
                )

                # Status badge
                status_text = f"  ✦ {status.replace('_', ' ')}  "
                status_width = badge_font.measure(status_text)

                status_x = x + 10 + type_width + 14

                mission_canvas.create_rectangle(
                    status_x, details_y,
                    status_x + status_width + 8, details_y + MISSION_STATUS_BADGE_HEIGHT,
                    fill="#303348",
                    outline="",
                    tags="mission_card"
                )

                mission_canvas.create_text(
                    status_x + 4, details_y + 2,
                    text=status_text,
                    anchor="nw",
                    font=badge_font,
                    fill=accent,
                    tags="mission_card"
                )

                # XP badge
                xp = entry.get("xp", 0)

                xp_text = f"✧  {'' if xp < 0 else '+' if xp > 0 else ''}{xp} XP"
                xp_width = xp_font.measure(xp_text)

                xp_x = x + width - 10 - xp_width - 16

                mission_canvas.create_rectangle(
                    xp_x, details_y,
                    xp_x + xp_width + 16, details_y + XP_BADGE_HEIGHT,
                    fill="#303348",
                    outline="",
                    tags="mission_card"
                )

                mission_canvas.create_text(
                    xp_x + 8, details_y + 2,
                    text=xp_text,
                    anchor="nw",
                    font=xp_font,
                    fill="#65cb91" if xp >= 0 else "#e57a5c",
                    tags="mission_card"
                )


        # ==============================
        # EMPTY HISTORY
        # ==============================
        if not self.history:
            mission_canvas.create_text(
                200, 30,
                text=(
                    "Your chronicle is empty.\n"
                    "Complete your first bounty to leave a mark."
                    if self.level == 0
                    else "Your chronicle is empty."
                ),
                font=("Segoe UI", 9, "italic"),
                fill="#969caf",
                justify="left",
                tags="mission_card"
            )
        else:
            def on_canvas_resize(event):
                prepare_layout()
                draw_visible_cards()

            mission_canvas.bind(
                "<Configure>",
                on_canvas_resize
            )

            # Redraw after scrolling
            original_yview = mission_canvas.yview

            def scroll_and_draw(*args):
                original_yview(*args)
                draw_visible_cards()

            mission_scrollbar.configure(
                command=scroll_and_draw
            )

            mission_canvas.configure(
                yscrollcommand=lambda first, last: (
                    mission_scrollbar.set(first, last),
                    draw_visible_cards()
                )
            )

            self.scroll_on_wheel(
                mission_canvas,
                mission_canvas
            )

            prepare_layout()
            draw_visible_cards()

    def update_xp_display(self, current, requirement):
        canvas = self.xp_canvas

        canvas.itemconfig(self.xp_current, text=str(current))
        canvas.itemconfig(self.xp_max, text=f"{requirement} XP")

        gap = 8
        x = 0
        baseline = 27

        canvas.coords(self.xp_current, x, baseline)

        x += self.xp_current_font.measure(str(current)) + gap

        canvas.coords(self.xp_separator, x, baseline)

        x += self.xp_separator_font.measure("/") + gap

        canvas.coords(self.xp_max, x, baseline)

    def ui_render_dashboard_xp_display(self):
        current_xp, realm = self.calculate_progression()
        requirement = realm["xp_required"]

        # Current realm
        # self.rank_label.config(text=realm["name"].upper())
        self.set_rank_text(realm["name"].upper())

        # self.level_label.config(text=f"LEVEL {self.level}")
        self.level_badge.itemconfig(
            self.level_badge.text_id,
            text=f"LEVEL {self.level}"
        )
        self.rank_description.config(text=realm["description"])

        # XP progress
        percentage = (
            min(100, current_xp / requirement * 100)
            if requirement > 0 else 100
        )

        remaining = max(0, requirement - current_xp)

        
        self.schedule_update("dashboard", "update_xp_display", 
                             {"current": current_xp, "requirement": requirement})

        self.xp_percentage_label.config(
            text=f"{percentage:.0f}%"
        )

        progress = (current_xp / max(1, requirement)) * 100
        self.set_xp_progress(progress)

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
                text=f"NEXT BREAKTHROUGH: {next_realm[2].upper()}"
            )
        else:
            self.next_realm_label.config(
                text="HIGHEST CULTIVATION REALM ACHIEVED"
            )

        # Dashboard statistics
        self.dashboard_streak_card.config(
            text=f"🔥  {self.getting_started_streak} "
                f"{'day' if self.getting_started_streak == 1 else 'days'}",
        )

        self.dashboard_xp_card.config(
            text=f"{self.xp} XP"
        )

        self.dashboard_bounty_card.config(
            text=f"{self.total_completed_bounties} "
                f"{'Bounty' if self.total_completed_bounties == 1 else 'Bounties'}"
        )
       
    # region Dashboard - Next Cultivation Variations
    def ui_update_next_cultivation_display(self, next=False):
        grouped = {
            "current": [],
            "completed": [],
            "postponed": []
        }

        today_str = date.today().isoformat()

        for project, items in self.projects.items():
            for item in items:
                status = item.get("status", "current").lower()

                if status not in grouped:
                    status = "current"

                if item.get("is_daily", False) and item.get("last_done_date") == today_str:
                    status = "completed"

                grouped[status].append((project, item))

        bounty_content = self.next_cultivation_bounty_content
        if not next:
            for child in bounty_content.winfo_children():
                child.destroy()

        current_bounties = grouped["current"]

        if current_bounties:
            if not hasattr(self, "next_cultivation_index"):
                self.next_cultivation_index = 0

            self.next_cultivation_index %= len(current_bounties)
            project_name, bounty = current_bounties[self.next_cultivation_index]

            if next:
                self.next_recom_title.config(text=bounty.get("task"))
                self.next_recom_label.config(
            text=f"Sect: {project_name}   ·   Estimated time: {bounty.get("duration")} minutes")
                self.next_recom_reward.update_text(f"{bounty.get('reward_xp')} XP",
                width = 120 if bounty.get('reward_xp') >= 100 else 100)
            else:
                self.update_next_cultivation_has_bounty(
                    project_name, bounty,
                    wrap_size=500,
                    has_another=len(current_bounties) > 1
                )

        elif grouped["completed"]:
            self.next_cultivation_index = 0
            self.next_cultivation_finished_bounties(500)

        else:
            self.next_cultivation_index = 0
            self.next_cultivation_empty(500)

    def show_next_cultivation_recommendation(self):
        self.next_cultivation_index += 1
        self.ui_update_next_cultivation_display(next=True)

    def update_next_cultivation_has_bounty(
        self, project_name, bounty, wrap_size, has_another=False
    ):
        bounty_content = self.next_cultivation_bounty_content

        # Header
        header = tk.Frame(bounty_content, bg="#211F38")
        header.pack(fill="x")

        self.create_star_icon(frame=header, color=StarIconColors.PURPLE, filled=False, size=(22, 22), glow_radius=7)
        
        tk.Label(
            header,
            text="YOUR NEXT CULTIVATION",
            bg="#211F38",
            fg="#BC74FB",
            font=("Segoe UI", 9, "bold")
        ).pack(side="left")

        # Header actions
        header_actions = tk.Frame(header, bg="#211F38")
        header_actions.pack(side="right")

        self.make_button(
            header_actions,
            f"RECOMMENDED",
            colors={
                "base_bg": "#3E2972",
                "base_text": "#B5A2FF",
                "base_bd": "#3E2972"
            },
            compact=False,
            font_size=7,
            size = (140, 40),
            radius=(12, 10),
            badge=True
        ).pack(side="left", padx=(0, 6), pady=3)

        if has_another:
            self.make_button(
                header_actions,
                f"↻ Another",
                command=self.show_next_cultivation_recommendation,
                colors={
                    "base_bg": "#302B49",
                    "base_text": "#C4B5FD",
                    "base_bd": "#302B49",
                    "highlight_bg": "#40375E",
                    "highlight_text": "#E9D5FF",
                    "highlight_bd": "#40375E"
                },
                compact=False,
                font_size=7,
                size = (140, 40),
                radius=(12, 10),
                badge=False
            ).pack(side="left", padx=8, pady=4)

        # Quest title
        self.next_recom_title = tk.Label(
            bounty_content,
            text=bounty.get("task"),
            bg="#211F38",
            fg="#F1F0FF",
            font=("Segoe UI", 11, "bold"),
            anchor="w",
            # wraplength=wrap_size,
            justify="left"
        )
        self.next_recom_title.pack(fill="x", pady=(12, 5))

        # Category and estimated time
        self.next_recom_label = tk.Label(
            bounty_content,
            text=f"Sect: {project_name}   ·   Estimated time: {bounty.get("duration")} minutes",
            bg="#211F38",
            fg="#A5A2BC",
            font=("Segoe UI", 8),
            anchor="w"
        )
        self.next_recom_label.pack(fill="x", pady=(0, 10))

        # Reward and availability
        info_row = tk.Frame(bounty_content, bg="#211F38")
        info_row.pack(fill="x")

        # Left actions group
        actions = tk.Frame(info_row, bg="#211F38")
        actions.pack(side="left")

        star_svg = AssetHandler.make_star_svg(
            color=PURPLE,
            glow_radius=10,
            glow_strength=0.6,
            reflective=True,
            reflection_strength=0
        )

        star_image = AssetHandler.svg_to_photo(star_svg, size=(20, 20))

        self.next_recom_reward = self.make_button(
            actions,
            f"{bounty.get('reward_xp')} XP",
            colors={
                "base_bg": "#2E2659",
                "base_text": "#E4A6FF",
                "base_bd": "#2E2659"
            },
            compact=False,
            font_size=9,
            size = (120 if bounty.get('reward_xp') >= 100 else 100, 42),
            radius=(12, 10),
            badge=True,
            icon_gap=12,
            icon=star_image
        )
        self.next_recom_reward.pack(side="left", padx=(0, 8))

        self.make_button(
            actions,
            "Start  →",
            lambda: self.choose_bounty(bounty),
            bg="FILLED_PURPLE_BUTTON",
            fg="#FFFFFF",
            compact=False,
            font_size=9,
            size = (110, 42),
            radius=(12, 10)
        ).pack(side="left")

        # Availability stays on the far right
        
        self.make_button(
            info_row,
            f"●  AVAILABLE",
            colors={
                "base_bg": "#193B35",
                "base_text": "#6EE7B7",
                "base_bd": "#193B35"
            },
            compact=False,
            font_size=7,
            size = (120, 40),
            radius=(12, 10),
            badge=True
        ).pack(side="right", padx=(8, 5))

        # Footer hint
        tk.Label(
            bounty_content,
            text="Your next challenge awaits.",
            bg="#211F38",
            fg="#77758F",
            font=("Segoe UI", 7),
            anchor="w"
        ).pack(fill="x", pady=(10, 0))

    def next_cultivation_finished_bounties(self, wrap_size):
        bounty_content = self.next_cultivation_bounty_content

        tk.Label(
            bounty_content,
            text="✦  CULTIVATION STATUS",
            bg="#211F38",
            fg="#A78BFA",
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        tk.Label(
            bounty_content,
            text="No active bounties left!",
            bg="#211F38",
            fg="#F1F0FF",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=(12, 5))

        tk.Label(
            bounty_content,
            text="You've completed all your available quests. "
                "Take a moment to appreciate your progress.",
            bg="#211F38",
            fg="#A5A2BC",
            font=("Segoe UI", 8),
            wraplength=wrap_size,
            justify="left"
        ).pack(anchor="w")

        tk.Label(
            bounty_content,
            text="✧  Your next challenge awaits.",
            bg="#211F38",
            fg="#C4B5FD",
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", pady=(12, 0))
   
    def next_cultivation_empty(self, wrap_size):
        bounty_content = self.next_cultivation_bounty_content

        tk.Label(
            bounty_content,
            text="✦  YOUR CULTIVATION JOURNEY",
            bg="#211F38",
            fg="#A78BFA",
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        tk.Label(
            bounty_content,
            text="A journey yet to begin.",
            bg="#211F38",
            fg="#F1F0FF",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w", pady=(12, 5))

        tk.Label(
            bounty_content,
            text="No active or completed tasks just yet. "
                "Every great cultivator starts somewhere. "
                "Your first step is waiting.",
            bg="#211F38",
            fg="#A5A2BC",
            font=("Segoe UI", 8),
            wraplength=wrap_size,
            justify="left"
        ).pack(anchor="w")

        tk.Label(
            bounty_content,
            text="✧  Small steps lead to great things.",
            bg="#211F38",
            fg="#C4B5FD",
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", pady=(12, 0))
    
    # endregion
    
    # endregion 

    # region ---------------- POPUPS ----------------

    def render_edit_mission_markdown_popup(self):
        if self.running and self.chosen_bounty is not None:
            self.error_cannot_edit_bounties()
            return
        
        popup = tk.Toplevel(self.root)
        popup.title(f"Quest Scroll Editor — {self.active_project}")
        
        self.center_geometry(popup, (900, 900))

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

        example_format_text = (
            "- Bounty Name | 30m | 50xp | daily | current | 3 | "
            "2026-11-03 | 2026-11-04"
        )
        
        format_label =tk.Label(
            popup,
            text=(
                "Format (Double-click to copy example):\n"
                f"{example_format_text}\n\n"
                "Fields: name | duration | reward | daily/not_daily | status | streak | previous_completed_date | completed_date\n"
                "Status: current, completed, postponed\n"
                "Use none if the mission has no last completion date or no previous completion date (for streaks).\n"
            ),
            bg="#171923",
            fg="#aab0c0",
            font=("Segoe UI", 9),
            justify="left"
        )
        format_label.pack(anchor="w", padx=16, pady=(0, 10))

        def copy_bounty_format(event=None):
            popup.clipboard_clear()
            popup.clipboard_append(example_format_text)
            popup.update()

            # Small confirmation
            notification = tk.Label(
                popup,
                text="✓  Example copied to clipboard!",
                bg="#193B35",
                fg="#6EE7B7",
                font=("Segoe UI", 8, "bold"),
                padx=10,
                pady=5
            )
            notification.pack(anchor="w", padx=16, pady=(0, 10))
            notification.after(1800, notification.destroy)

        format_label.bind("<Double-Button-1>", copy_bounty_format)
        
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
                is_daily = mission.get("is_daily", False)
                daily = "daily" if is_daily else "not_daily"
                status = mission.get("status", "current")
                streak = mission.get("streak_count", 0)
                previous_done = mission.get("previous_done_date") or "none"
                last_done = mission.get("last_done_date") or "none"
                completed_date = mission.get("completed_date") or "none"

                lines.append(
                    f"- {task} | {duration}m | {reward}xp | "
                    f"{daily} | {status} | {streak} | {previous_done} | {last_done if is_daily else completed_date}"
                )

            lines.append("")

        editor.insert("1.0", "\n".join(lines))

        def projects_changed(old_projects, new_projects):
            return old_projects != new_projects
   
        def apply_markdown():
            parsed_projects = {}
            current_project = "General"

            try:
                for raw in editor.get("1.0", "end-1c").splitlines():
                    line = raw.strip()

                    if not line:
                        continue

                    if line.startswith("#"):
                        current_project = line.lstrip("#").strip()

                        # Allow empty sects
                        parsed_projects.setdefault(current_project, [])
                        continue

                    if line.startswith(("- ", "* ")):
                        line = line[2:].strip()

                    # Allow bounties without a sect
                    parsed_projects.setdefault(current_project, [])

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
                            f"Invalid duration for bounty: {task} - {duration}"
                        )

                    if reward < 0:
                        raise ValueError(
                            f"Invalid XP reward for bounty: {task} - {reward}"
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
                        "previous_done_date": previous_done if is_daily else None,
                        "last_done_date": last_done if is_daily else None,
                        "completed_date": last_done if not is_daily else None
                    }
                    # print(mission)

                    parsed_projects[current_project].append(mission)

                if not parsed_projects:
                    parsed_projects["General"] = []

            except (ValueError, TypeError) as error:
                messagebox.showerror(
                    "Quest Scroll Error",
                    str(error),
                    parent=popup
                )
                return

            changed = projects_changed(self.projects, parsed_projects)

            if changed:
                self.projects = parsed_projects

                if self.active_project not in self.projects:
                    self.active_project = next(iter(self.projects))

                self.schedule_update("board", "render_mission_board")
                self.save_data()

            self.close_custom_popup(popup)
            self.status_label.config(
                text="✦ Quest scrolls successfully updated."
            )

        self.make_button(
            popup,
            "SAVE QUEST SCROLLS",
            command=apply_markdown,
            colors={
                "base_bg": "#7668e8",
                "base_text": "#FFFFFF",
                "base_bd": "#7668e8",
                "highlight_bg": "#5c4dca",
                "highlight_text": "#FFFFFF",
                "highlight_bd": "#5c4dca"
            },
            compact=False,
            font_size=9,
            size = (200, 45),
            radius=(10, 5)
        ).pack(pady=(0, 13), ipadx=15, ipady=7)
        
        self._current_popups.append(popup)
        self.check_tutorial("markdown_editor")
        popup.grab_set()
        popup.wait_window()

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

        title_label = tk.Label(
            content,
            text=title_text,
            font=("Segoe UI", 21 if breakthrough else 25, "bold"),
            fg=gold,
            bg=bg
        )
        title_label.pack(pady=(8, 10))

        self.pulse_label(title_label, content, 80)

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

        button = self.make_button(
            content,
            "CONTINUE CULTIVATING",
            command=lambda: self.close_custom_popup(popup),
            colors={
                "base_bg": "#6c63ff",
                "base_text": "#FFFFFF",
                "base_bd": "#6c63ff",
                "highlight_bg": "#8179ff",
                "highlight_text": "#FFFFFF",
                "highlight_bd": "#8179ff"
            },
            compact=False,
            font_size=10,
            size = (250, 45),
            radius=(10, 5)
        )

        popup_container.after(400, type_message)

        # Dramatic breakthrough screen shake
        if breakthrough:
            self.effect_shake(popup, width, height)

        self.adjust_popup_dimensions(popup, size=(width, height), with_lift=True)
        popup.wait_window()

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

            self.close_custom_popup(popup)
            on_continue()


        button = self.make_button(
            popup_container,
            "BEGIN CULTIVATION  →",
            command=proceed,
            colors={
                "base_bg": "#6c55b5",
                "base_text": "#FFFFFF",
                "base_bd": "#6c55b5",
                "highlight_bg": "#8b72dc",
                "highlight_text": "#FFFFFF",
                "highlight_bd": "#8b72dc"
            },
            compact=False,
            font_size=11,
            size = (280, 45),
            radius=(10, 5)
        )
        button.pack(side="left", pady=22, padx=9)
        button.place(relx=0.5, rely=0.91, anchor="center")

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

        HEIGHT = 610
        WIDTH = 580
        MIDDLE_WIDTH = 580 / 2
       
        canvas = tk.Canvas(
            popup_container,
            width=WIDTH,
            height=550,
            bg="#100f20",
            highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)

        # Heavenly notification
        canvas.create_text(
            MIDDLE_WIDTH, 42,
            text="✦  HEAVENLY WARNING  ✦",
            fill="#bda8ff",
            font=("Segoe UI", 11, "bold")
        )

        # Magical rings
        CENTER_Y = 175
        TEXT_Y_LOC = 320

        ring = canvas.create_oval(  # OUTER RING
            MIDDLE_WIDTH - 80, CENTER_Y - 80,
            MIDDLE_WIDTH + 80, CENTER_Y + 80,
            outline="#a45d79",
            width=3
        )

        canvas.create_oval(  # INNER RING
            MIDDLE_WIDTH - 63, CENTER_Y - 63,
            MIDDLE_WIDTH + 63, CENTER_Y + 63,
            outline="#d9b75f",
            width=2
        )

        canvas.create_text(
            MIDDLE_WIDTH, 150,
            text="⚠",
            fill="#f5d98a",
            font=("Segoe UI Symbol", 55, "bold")
        )

        # Main message
        canvas.create_text(
            MIDDLE_WIDTH, TEXT_Y_LOC,
            text="STREAK BROKEN!",
            fill="#f5d98a",
            font=("Segoe UI", 24, "bold")
        )

        canvas.create_text(
            MIDDLE_WIDTH, TEXT_Y_LOC+45,
            text=f"Your previous streak: {streak} day(s)",
            fill="#ffffff",
            font=("Segoe UI", 13, "bold")
        )

        canvas.create_text(
            MIDDLE_WIDTH, TEXT_Y_LOC+85,
            text="Your Dao Heart has missed a day.",
            fill="#bdb5d5",
            font=("Segoe UI", 11)
        )

        canvas.create_text(
            MIDDLE_WIDTH, TEXT_Y_LOC+117,
            text="Will you preserve your path or begin anew?",
            fill="#bdb5d5",
            font=("Segoe UI", 10)
        )

        # Magical particles
        particles = []

        for _ in range(42):
            px = random.randint(15, WIDTH)
            py = random.randint(45, HEIGHT)
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
            self.close_custom_popup(popup)

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
            rely=0.89,
            anchor="center"
        )

        # Grace button
        
        self.make_button(
            button_frame,
            "✦  USE GRACE DAY",
            command=use_grace,
            colors={
                "base_bg": "#6c55b5",
                "base_text": "#FFFFFF",
                "base_bd": "#6c55b5",
                "highlight_bg": "#8b72dc",
                "highlight_text": "#FFFFFF",
                "highlight_bd": "#8b72dc"
            },
            compact=False,
            font_size=11,
            size = (250, 45),
            radius=(10, 5)
        ).pack(side="left", pady=(6, 6), padx=5)

        # Reset button
        
        self.make_button(
            button_frame,
            "RESET STREAK",
            command=reset_streak,
            colors={
                "base_bg": "#30243e",
                "base_text": "#f5d98a",
                "base_bd": "#30243e",
                "highlight_bg": "#493653",
                "highlight_text": "#FFFFFF",
                "highlight_bd": "#493653"
            },
            compact=False,
            font_size=11,
            size = (240, 45),
            radius=(10, 5)
        ).pack(side="left", pady=(6, 6), padx=5)

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
                MIDDLE_WIDTH - 80 - pulse,
                CENTER_Y - 80 - pulse,
                MIDDLE_WIDTH + 80 + pulse,
                CENTER_Y + 80 + pulse
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

        self.adjust_popup_dimensions(popup, size=(580, 610), with_lift=True)
        popup.wait_window()
        return result["choice"]
    
    def render_inspection_report_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("Cultivation Complete")
        width, height = 700, 575
        mwidth, mheight = 700, 300

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


            self.make_button(
                popup_container,
                "CONTINUE",
                command=lambda: self.close_custom_popup(popup),
                colors={
                    "base_bg": PANEL,
                    "base_text": GOLD,
                    "base_bd": PANEL,
                    "highlight_bg": "#34394b",
                    "highlight_text": GOLD,
                    "highlight_bd": "#34394b"
                },
                compact=False,
                font_size=10,
                size = (300, 45),
                radius=(10, 5)
            ).pack(pady=(25, 15))

            self.overlay.withdraw()

            if self.chosen_bounty is not None:
                if choice == "YES!":
                    self.change_mission_status(
                        self.chosen_bounty, "completed"
                    )
                self.chosen_bounty = None
                self.schedule_update("dashboard", "ui_update_next_cultivation_display")

            popup.grab_set()
            popup.lift()
            popup.focus_force()

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

        popup.wait_window()
        self.bring_window_to_front()

    def render_add_project_popup(self):
        if self.running and self.chosen_bounty is not None:
            self.error_cannot_edit_bounties()
            return
        
        popup = tk.Toplevel(self.root)
        popup.title("Found a New Sect")
        
        # Custom draggable title bar
        popup_container = self.create_custom_titlebar(
            popup, 
            fixed_size=(340, 200), 
            start_hidden=True
        )

        tk.Label(popup_container, text="NAME YOUR SECT", bg="#171923", fg="#e5b85c", font=("Segoe UI", 10, "bold")).pack(pady=(18, 5))

        name_var = tk.StringVar()
        
        entry_container, entry = self.make_rounded_entry(
            popup_container,
            textvariable=name_var,
            fg_color="#FFFFFF",
            bg_color="#252a3a",
            height=40,
            radius=12,
            container_padx=15,
            container_pady=(0, 3),
            inner_padx=15,
            font=("Segoe UI", 10)
        )
    
        def create():
            name = name_var.get().strip()
            if not name:
                return
            
            self.create_project(name)
            self.close_custom_popup(popup)
            self.check_tutorial("sect_creation")

        self.make_button(
            popup_container,
            "JOIN SECT",
            command=create,
            colors={
                "base_bg": "#7668e8",
                "base_text": "#FFFFFF",
                "base_bd": "#7668e8",
                "highlight_bg": "#5c4dca",
                "highlight_text": "#FFFFFF",
                "highlight_bd": "#5c4dca"
            },
            compact=False,
            font_size=9,
            size = (200, 35),
            radius=(10, 5)
        ).pack(pady=12, ipadx=12, ipady=5)

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
        title_label = tk.Label(
            content,
            text="RESTART CULTIVATION",
            bg=bg,
            fg=gold,
            font=("Segoe UI", 19, "bold")
        )
        title_label.pack(pady=(5, 12))

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


        self.make_button(
            button_frame,
            "⚔  RESTART CULTIVATION",
            command=confirm_restart,
            colors={
                "base_bg": "#8e354b",
                "base_text": "#FFFFFF",
                "base_bd": "#8e354b",
                "highlight_bg": "#b44760",
                "highlight_text": "#FFFFFF",
                "highlight_bd": "#b44760"
            },
            compact=False,
            font_size=9,
            size = (300, 45),
            radius=(10, 5)
        ).pack(side="left", pady=10, padx=6)

        self.make_button(
            button_frame,
            "CANCEL",
            command=lambda: self.close_custom_popup(popup),
            colors={
                "base_bg": "#292638",
                "base_text": "#b9a3ff",
                "base_bd": "#292638",
                "highlight_bg": "#403653",
                "highlight_text": "#b9a3ff",
                "highlight_bd": "#403653"
            },
            compact=False,
            font_size=9,
            size = (250, 45),
            radius=(10, 5)
        ).pack(side="left", pady=10, padx=6)

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
        self.pulse_label(title_label, popup_container)
        popup.after(100, create_particles)

        # Display popup
        popup.wait_window()

    def render_message_popup(self, title, description, wrapsize=350, is_welcome=False, close_rollback = True):
        popup = tk.Toplevel(self.root)

        # Custom draggable title bar
        popup_container = self.create_custom_titlebar(
            popup, 
            start_hidden=True,
            close_rollback=close_rollback
        )

     # Icon container (fixed dimensions)
        icon_container = tk.Frame(
            popup_container,
            bg="#171923",
            width=60,
            height=55
        )
        icon_container.pack(pady=(15, 10))
        icon_container.pack_propagate(False)

        # Animated star
        star = tk.Label(
            icon_container,
            text="✦",
            bg="#171923",
            fg="#E5B85C",
            font=("Segoe UI", 25, "bold")
        )
        star.place(relx=0.5, rely=0.5, anchor="center")

        if is_welcome:
            glow_colors = [
                "#C99B45", "#DDB45E", "#E5B85C",
                "#F0CE7A", "#FFE8A8", "#F0CE7A"
            ]
            glow_sizes = [23, 25, 27, 29, 27, 25]

            def animate_star(index=0):
                if not popup.winfo_exists():
                    return

                star.config(
                    fg=glow_colors[index],
                    font=("Segoe UI", glow_sizes[index], "bold")
                )

                next_index = (index + 1) % len(glow_sizes)
                popup.after(180, lambda: animate_star(next_index))

            animate_star()

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
            wraplength=wrapsize
        ).pack(padx=25, pady=5)

        # Understood button
        
        self.make_button(
            popup_container,
            "UNDERSTOOD",
            command=lambda: (
                self.close_custom_popup(popup, close_rollback),
                # self.root.after(100, self.bring_window_to_front)
            ),
            colors={
                "base_bg": "#7668E8",
                "base_text": "#FFFFFF",
                "base_bd": "#7668E8",
                "highlight_bg": "#897CF0",
                "highlight_text": "#FFFFFF",
                "highlight_bd": "#897CF0"
            },
            compact=False,
            font_size=9,
            size = (200, 45),
            radius=(10, 5)
        ).pack(padx=7, pady=(15, 20))

        # Keyboard shortcuts
        popup.bind(
            "<Return>",
            lambda e: (
                self.close_custom_popup(popup, close_rollback),
                # self.root.after(100, self.bring_window_to_front)
            )
        )
        popup.bind(
            "<Escape>",
            lambda e: (
                self.close_custom_popup(popup, close_rollback),
                # self.root.after(100, self.bring_window_to_front)
            )
        )

        # Calculate actual dimensions (DPI-aware)
        popup.update_idletasks()
        width, height = max(420, popup.winfo_reqwidth()), popup.winfo_reqheight()
        self.adjust_popup_dimensions(popup, size=(width, height), with_lift=True)
        return popup

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
            self.close_custom_popup(popup)
            on_confirm()

        self.make_button(
            button_frame,
            "YES",
            command=confirm,
            colors={
                "base_bg": "#7668E8",
                "base_text": "#FFFFFF",
                "base_bd": "#7668E8",
                "highlight_bg": "#897CF0",
                "highlight_text": "#FFFFFF",
                "highlight_bd": "#897CF0"
            },
            compact=False,
            font_size=9,
            size = (200, 45),
            radius=(10, 5)
        ).pack(side="left", padx=7, pady=(20, 3))

        self.make_button(
            button_frame,
            "CANCEL",
            command=lambda: self.close_custom_popup(popup),
            colors={
                "base_bg": "#292D3D",
                "base_text": "#B8BED0",
                "base_bd": "#292D3D",
                "highlight_bg": "#393F52",
                "highlight_text": "#FFFFFF",
                "highlight_bd": "#393F52"
            },
            compact=False,
            font_size=9,
            size = (200, 45),
            radius=(10, 5)
        ).pack(side="left", padx=7, pady=(20, 3))

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
    
    def scroll_on_wheel(self, scrollable, container=None, custom_update=None):
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
            if custom_update is not None: custom_update(event)
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

    def scroll_on_wheel2(self, scrollable, container=None, custom_update=None):

        if not hasattr(self, "_wheel_bindings"):
            self._wheel_bindings = {}

        key = str(scrollable)

        if key in self._wheel_bindings:
            return

        self._wheel_bindings[key] = True

        def on_mousewheel(event):
            target = event.widget

            # Let Text widgets handle their own scrolling
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

            direction = (
                -1 if event.num == 4 else
                1 if event.num == 5 else
                -1 if event.delta > 0 else 1
            )
            print("mousewheel", direction)

            target.yview_scroll(direction, "units")

            if custom_update:
                custom_update(event)

            return "break"

        def bind_wheel(event):
            scrollable.bind_all("<MouseWheel>", on_mousewheel)
            scrollable.bind_all("<Button-4>", on_mousewheel)
            scrollable.bind_all("<Button-5>", on_mousewheel)

        def unbind_wheel(event):
            scrollable.unbind_all("<MouseWheel>")
            scrollable.unbind_all("<Button-4>")
            scrollable.unbind_all("<Button-5>")

        def bind_recursive(widget):
            if getattr(widget, "_wheel_enter_bound", False):
                return

            widget._wheel_enter_bound = True

            widget.bind("<Enter>", bind_wheel, add="+")
            widget.bind("<Leave>", unbind_wheel, add="+")

            for child in widget.winfo_children():
                bind_recursive(child)

        widgets = [scrollable]

        if container is not None:
            widgets.append(container)

        for widget in widgets:
            bind_recursive(widget)

        if container is not None:
            container.bind(
                "<Map>",
                lambda event: bind_recursive(container),
                add="+"
            )
 
    # ---------- HELPERS ----------
    def make_card(
        self,
        parent,
        title = "",
        subtitle=None,
        title_color=GOLD,
        subtitle_color=MUTED,
        border_color = "#705A42",
        card_bg=PANEL,
        heading_padx = None,
        content_padx = 12,
        content_pady = (14, 17), # (10, 0) if has_content
        border_radius = 12,
        border_type : str = "sharp", #"rounded" | "sharp",
        has_content = True,
        star_color = StarIconColors.DEEP_GOLD,
        star_filled = True,
        star_glow=(10, 0.6),
        icon_type = None,
        icon_size = None,
        icon_with_subtitle=False,
        expand_height=False
    ):
        card = tk.Canvas(
            parent,
            bg=parent.cget("bg"),
            highlightthickness=0,
            bd=0,
            height=1
        )

        # Inner content
        inner = tk.Frame(card, bg=card_bg)

        window = card.create_window(
            14, 10,
            anchor="nw",
            window=inner
        )

        def draw_rounded_rect(x1, y1, x2, y2, r=12):
            points = []

            corners = [
                (x2 - r, y1 + r, -90),
                (x2 - r, y2 - r, 0),
                (x1 + r, y2 - r, 90),
                (x1 + r, y1 + r, 180)
            ]

            for cx, cy, start in corners:
                for i in range(9):
                    angle = math.radians(start + i * 90 / 8)
                    points.extend((
                        cx + r * math.cos(angle),
                        cy + r * math.sin(angle)
                    ))

            return points
        
        def draw_sharp_rect(width, height):
            cut = 12  # Size of diagonal corner cuts

            return [
                cut, 1,
                width - cut, 1,
                width - 1, cut,
                width - 1, height - cut,
                width - cut, height - 1,
                cut, height - 1,
                1, height - cut,
                1, cut
            ]
        
        def resize_card(event=None):
            card.update_idletasks()
            inner.update_idletasks()

            width = card.winfo_width()
            if width <= 1:
                return

            inner_height = inner.winfo_reqheight()

            if expand_height:
                height = card.winfo_height()
                if height <= 1:
                    return
                inner_height = height - 20
            else:
                height = inner_height + 20
                card.configure(height=height)

            card.itemconfigure(
                window,
                width=max(1, width - 28),
                height=max(1, inner_height)
            )

            # Calculate background coordinates
            if border_type == "rounded":
                points = draw_rounded_rect(
                    1, 1,
                    width - 1, height - 1,
                    r=border_radius
                )
            else:
                points = draw_sharp_rect(width, height)

            # Create background only once
            if not hasattr(card, "_background_id"):
                card._background_id = card.create_polygon(
                    points,
                    smooth=False,
                    fill=card_bg,
                    outline=border_color,
                    width=1 if border_type == "sharp" else 0.6,
                    tags="card_background"
                )
                card.tag_lower(card._background_id)

            else:
                # Update existing background
                card.coords(card._background_id, *points)

                card.itemconfigure(
                    card._background_id,
                    fill=card_bg,
                    outline=border_color
                )
    
        # Heading
        heading = tk.Frame(inner, bg=card_bg)
        heading.pack(
            fill="x",
            padx=heading_padx or content_padx,
            pady=(10, 0) if has_content else content_pady
        )

        if icon_with_subtitle:
            # Icon + vertically stacked title and subtitle
            header_row = tk.Frame(heading, bg=card_bg)
            header_row.pack(anchor="w", fill="x")

            icon_loc = header_row
        else:
            title_row = tk.Frame(heading, bg=card_bg)
            title_row.pack(anchor="w", fill="x")
            icon_loc = title_row
            title_loc = title_row
            subtitle_loc = heading

        if icon_type is not None:
            if icon_type == "star":
                self.create_star_icon(
                    frame=icon_loc,
                    color=star_color,
                    size=icon_size,
                    filled=star_filled,
                    glow_radius=star_glow[0],
                    glow_strength=star_glow[1]
                )
            else:
                self.create_icon(
                    frame=icon_loc,
                    icon_type=icon_type,
                    size=icon_size
                )

        if icon_with_subtitle:
            text_column = tk.Frame(header_row, bg=card_bg)
            text_column.pack(side="left", anchor="center")

            title_loc=text_column
            subtitle_loc=text_column
            
        if has_content:
            title_label = tk.Label(
                title_loc,
                text=title.upper(),
                bg=card_bg,
                fg=title_color,
                font=("Segoe UI", 9, "bold")
            ).pack(anchor="w")

            if subtitle:
                tk.Label(
                    subtitle_loc,
                    text=subtitle,
                    bg=card_bg,
                    fg=subtitle_color,
                    font=("Segoe UI", 8)
                ).pack(anchor="w")

            # Content
            content = tk.Frame(inner, bg=card_bg)
            content.pack(
                fill="both",
                expand=True,
                padx=content_padx,
                pady=content_pady
            )
            
        card.bind("<Configure>", resize_card)
        inner.bind("<Configure>", resize_card)
        card.after_idle(resize_card)
        
        return card, content if has_content else title_row

    def make_button(self, parent, label, command=None, bg=PANEL,
                    fg=None, colors = None, compact=False, font_size=None,
                    radius=(11, 13), size=None,
                    interactive=True, badge=False,
                    center_content=True, highlight=True, button_state = True,
                    icon=None, icon_size=(18, 18), icon_gap=6):
        
        if colors is not None:
            base_bg, base_bd, base_text, highlight_bg, highlight_bd, highlight_text = (
                colors.get("base_bg", PANEL),
                colors.get("base_bd", "#454D68"),
                colors.get("base_text", TEXT),
                colors.get("highlight_bg", PANEL),
                colors.get("highlight_bd", "#454D68"),
                colors.get("highlight_text", TEXT)
            )
        elif bg == BRIGHT_PURPLE:
            base_bg, base_bd, base_text, highlight_bg, highlight_bd, highlight_text = (
                "#252248", "#4D4676", "#F6F2FA", "#3D3336", GOLD, GOLD
            )

        elif bg == "MUTED_PURPLE_BUTTON":
            base_bg, base_bd, base_text, highlight_bg, highlight_bd, highlight_text = (
                "#252248", "#4D4676", "#F6F2FA", "#3D3336", GOLD, GOLD
            )

        elif bg == "FILLED_PURPLE_BUTTON":
            base_bg, base_bd, base_text, highlight_bg, highlight_bd, highlight_text = (
                "#8B6CF6", "#8B6CF6", TEXT, "#7552F2", "#7552F2", TEXT
            )
        else:
            if bg == GOLD:
                base_bg, base_bd, highlight = (
                    "#F4B653", "#FFE08A", "#FFD36B"
                )
            elif bg == GREEN:
                base_bg, base_bd, highlight = (
                    "#50C99A", "#A5F5C7", "#83E5B5"
                )

                disabled_bg, disabled_bd, disabled_fg = (
                    "#29483F", "#477565", "#83A99A"
                )
            elif bg == RED:
                base_bg, base_bd, highlight = (
                    "#D95757", "#FF9999", "#F07878"
                )

                disabled_bg, disabled_bd, disabled_fg = (
                    "#482F35", "#70434A", "#A8797E"
                )
            elif bg == PURPLE:
                base_bg, base_bd, highlight = (
                    "#252248", "#4D4676", PURPLE
                )

            base_text = "#11131A"
            highlight_bg, highlight_bd, highlight_text = highlight, highlight, base_text
        
        if size:
            width, height = size
        else:
            width = 60 if compact else 200
            height = 32 if compact else 52

        canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            bg=parent.cget("bg"),
            highlightthickness=0,
            bd=0,
            cursor="hand2" if interactive and not badge else "arrow"
        )

        font = ("Segoe UI", font_size or (11 if compact else 10), "bold")
        text_font = tk.font.Font(font=font)

        icon_w = icon_size[0] if icon else 0
        gap = icon_gap if icon else 0
        
        canvas.button_text = label
        canvas.total_w = icon_w + gap + text_font.measure(label)
        canvas.button_state = button_state

        def draw(event=None, hover=False, pressed=False, text_override=None):
            canvas.delete("all")

            w = canvas.winfo_width()

            if w < 10:
                return

            if canvas.button_state == False:
                current_bg = disabled_bg
                current_border = disabled_bd
                current_text = disabled_fg
            else:
                current_bg = highlight_bg if hover and interactive and not badge else base_bg
                current_border = highlight_bd if hover and interactive and not badge else base_bd
                current_text = highlight_text if hover and interactive and not badge else base_text

            self.draw_rounded_rect(
                canvas,
                w,
                height,
                radius[1],
                current_bg,
                current_border,
                border_width=1,
                tag="button"
            )

            w = canvas.winfo_width()
            h = canvas.winfo_height()

            start_x = (w - canvas.total_w) / 2 if center_content else 10
            center_y = h / 2

            if icon:
                canvas.create_image(
                    start_x, center_y,
                    image=icon,
                    anchor="w"
                )

            canvas.create_text(
                start_x + icon_w + gap,
                center_y,
                text=canvas.button_text,
                fill=current_text,
                font=font,
                anchor="w"
            )
   
        canvas.bind("<Configure>", draw) 

        if interactive and not badge:
            if highlight:
                canvas.bind("<Enter>", lambda e: draw(hover=True))
                canvas.bind("<Leave>", lambda e: draw())

            def on_click(event):
                if command:
                    # draw(pressed=True)
                    # canvas.after(80, draw)
                    command()

            canvas.bind("<Button-1>", on_click)

        canvas.after(10, draw)

        canvas.button_text = label

        def update_text(new_text, width=None):
            canvas.button_text = str(new_text)
            text_width = text_font.measure(canvas.button_text)
            canvas.total_w = icon_w + gap + text_width
            if width is not None: 
                if width == "responsive":
                    width = (
                        text_width + icon_w + gap + 20
                        if compact else max(200, text_width + icon_w + gap + 30)
                    )
                canvas.config(width=width)
            draw()

        canvas.update_text = update_text
        def update_text_color(color):
            nonlocal base_text, base_bd
            base_text = color
            base_bd = color
            draw()

        canvas.update_text_color = update_text_color

        def change_button_state(state):
            canvas.button_state = state
            draw()

        canvas.change_button_state = change_button_state
        return canvas

    def add_hover(self, widget, normal, hover):
        widget.bind("<Enter>", lambda e: widget.configure(bg=hover))
        widget.bind("<Leave>", lambda e: widget.configure(bg=normal))
    
    def make_rounded_badge(
        self,
        frame,
        content_text,
        width=108,
        height=29,
        radius=14,
        bg_color="#58358F",
        outline_color="#7650B8",
        text_color="#FFFFFF",
        font=("Segoe UI", 10, "bold"),
        padx=0,
        pady=(4, 0)
    ):
        badge = tk.Canvas(
            frame,
            width=width,
            height=height,
            bg=PANEL,
            highlightthickness=0,
            bd=0
        )
        badge.pack(anchor="w", padx=padx, pady=pady)

        # Keep radius within valid bounds
        radius = min(radius, width / 2, height / 2)

        def draw_rounded_pill(canvas, x1, y1, x2, y2, radius, **kwargs):
            points = [
                x1 + radius, y1,
                x2 - radius, y1,
                x2, y1,
                x2, y1 + radius,
                x2, y2 - radius,
                x2, y2,
                x2 - radius, y2,
                x1 + radius, y2,
                x1, y2,
                x1, y2 - radius,
                x1, y1 + radius,
                x1, y1
            ]

            return canvas.create_polygon(
                points,
                smooth=True,
                splinesteps=36,
                **kwargs
            )

        draw_rounded_pill(
            badge,
            1, 1, width - 1, height - 1,
            radius=radius,
            fill=bg_color,
            outline=outline_color,
            width=1
        )

        badge.text_id = badge.create_text(
            width / 2,
            (height / 2) - 2,
            text=content_text,
            fill=text_color,
            font=font
        )

        return badge
    
    def draw_xp_progress(self, event=None):
        canvas = self.xp_progress

        width = canvas.winfo_width()
        height = canvas.winfo_height()

        if width <= 1:
            return

        scale = 3
        w = width * scale
        h = height * scale

        padding = 5 * scale
        bar_width = w - (padding * 2)

        bar_height = 12 * scale
        y1 = (h - bar_height) // 2
        y2 = y1 + bar_height
        radius = bar_height // 2
        
        percentage = max(0, min(100, self.xp_progress_value))
        fill_width = int(bar_width * percentage / 100)
        fill_end = padding + fill_width

        # Base image
        image = Image.new("RGBA", (w, h), (0, 0, 0, 0))

        # Dark rounded track
        track = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        track_draw = ImageDraw.Draw(track)

        track_draw.rounded_rectangle(
            (padding, y1, w - padding, y2),
            radius=radius,
            fill="#29264B",
            outline="#4B4576",
            width=2
        )

        image.alpha_composite(track)

        if fill_width > 0:
            fill_width = max(fill_width, bar_height)

            # Glow mask
            glow_mask = Image.new("L", (w, h), 0)
            glow_draw = ImageDraw.Draw(glow_mask)

            glow_draw.rounded_rectangle(
                (padding, y1 - 1, fill_end, y2 + 1),
                radius=radius,
                fill=300
            )

            glow_mask = glow_mask.filter(
                ImageFilter.GaussianBlur(4 * scale)
            )

            # Reduce glow intensity
            glow_mask = glow_mask.point(
                lambda p: int(p * 0.65)
            )

            glow = Image.new("RGBA", (w, h), "#A96BFF")
            glow.putalpha(glow_mask)

            image.alpha_composite(glow)

            # Rounded fill mask
            fill_mask = Image.new("L", (w, h), 0)
            mask_draw = ImageDraw.Draw(fill_mask)

            mask_draw.rounded_rectangle(
                (padding, y1, fill_end, y2),
                radius=radius,
                fill=255
            )

            # Purple-to-pink gradient
            gradient = Image.new("RGBA", (w, h), (0, 0, 0, 0))

            colors = [
                (137, 75, 255),
                (174, 91, 255),
                (222, 137, 255)
            ]

            gradient_draw = ImageDraw.Draw(gradient)

            for x in range(padding, fill_end + 1):
                t = (x - padding) / max(fill_width, 1)

                if t < 0.5:
                    local_t = t * 2
                    c1, c2 = colors[0], colors[1]
                else:
                    local_t = (t - 0.5) * 2
                    c1, c2 = colors[1], colors[2]

                color = tuple(
                    int(a + (b - a) * local_t)
                    for a, b in zip(c1, c2)
                )

                gradient_draw.line(
                    (x, y1, x, y2),
                    fill=(*color, 255)
                )

            gradient.putalpha(fill_mask)
            image.alpha_composite(gradient)

            # Subtle top reflection
            highlight = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            highlight_draw = ImageDraw.Draw(highlight)

            highlight_draw.line(
                (
                    padding + radius,
                    y1 + 2 * scale,
                    max(padding + radius, fill_end - radius),
                    y1 + 2 * scale
                ),
                fill=(255, 255, 255, 105),
                width=scale
            )

            highlight.putalpha(
                Image.composite(
                    highlight.getchannel("A"),
                    Image.new("L", (w, h), 0),
                    fill_mask
                )
            )

            image.alpha_composite(highlight)

        # Downscale for smooth edges
        image = image.resize(
            (width, height),
            Image.Resampling.LANCZOS
        )

        self.xp_progress_photo = ImageTk.PhotoImage(image)

        canvas.delete("all")
        canvas.create_image(
            0, 0,
            image=self.xp_progress_photo,
            anchor="nw"
        )
   
    def set_xp_progress(self, value):
        self.xp_progress_value = max(0, min(100, value))
        self.draw_xp_progress()
        
    def draw_rounded_rect(
        self,
        canvas,
        width,
        height,
        radius,
        fill,
        outline,
        border_width=1,
        x_offset=0,
        y_offset=0,
        tag="rounded"
    ):
        canvas.delete(tag)

        inset = border_width / 2 + 1

        x1 = x_offset + inset
        y1 = y_offset + inset
        x2 = x_offset + width - inset
        y2 = y_offset + height - inset

        r = min(radius, (x2 - x1) / 2, (y2 - y1) / 2)

        # Background
        canvas.create_rectangle(
            x1 + r, y1, x2 - r, y2,
            fill=fill, outline="", tags=tag
        )
        canvas.create_rectangle(
            x1, y1 + r, x2, y2 - r,
            fill=fill, outline="", tags=tag
        )

        corners = [
            (x1, y1, x1 + 2*r, y1 + 2*r, 90),
            (x2 - 2*r, y1, x2, y1 + 2*r, 0),
            (x2 - 2*r, y2 - 2*r, x2, y2, 270),
            (x1, y2 - 2*r, x1 + 2*r, y2, 180)
        ]

        for ax1, ay1, ax2, ay2, start in corners:
            canvas.create_arc(
                ax1, ay1, ax2, ay2,
                start=start, extent=90,
                style="pieslice",
                fill=fill, outline="",
                tags=tag
            )

        # Border
        if outline and border_width > 0:
            for ax1, ay1, ax2, ay2, start in corners:
                canvas.create_arc(
                    ax1, ay1, ax2, ay2,
                    start=start, extent=90,
                    style="arc",
                    outline=outline,
                    width=border_width,
                    tags=tag
                )

            canvas.create_line(
                x1 + r, y1, x2 - r, y1,
                fill=outline, width=border_width, tags=tag
            )
            canvas.create_line(
                x1 + r, y2, x2 - r, y2,
                fill=outline, width=border_width, tags=tag
            )
            canvas.create_line(
                x1, y1 + r, x1, y2 - r,
                fill=outline, width=border_width, tags=tag
            )
            canvas.create_line(
                x2, y1 + r, x2, y2 - r,
                fill=outline, width=border_width, tags=tag
            )

    def make_rounded_entry(
        self,
        parent,
        textvariable=None,
        icon_type=None,
        width=None,
        height=38,
        radius=10,
        bg_color=PANEL_ALT,
        outline_color="#454D68",
        border_width=1,
        fg_color=DEEP_MUTED,
        font=("Segoe UI", 9),
        icon_size=(18, 18),
        icon_padx=(15, 15),
        container_padx=10,
        container_pady=0,
        inner_padx=10,
        insert_color=None
    ):
        canvas = tk.Canvas(
            parent,
            height=height,
            width=width or 300,
            bg=parent.cget("bg"),
            highlightthickness=0,
            bd=0
        )
        canvas.pack(fill="x", expand=True, pady=container_pady, padx=container_padx)

        entry = tk.Entry(
            canvas,
            textvariable=textvariable,
            bg=bg_color,
            fg=fg_color,
            insertbackground=insert_color or fg_color,
            relief="flat",
            bd=0,
            font=font
        )

        entry_x = inner_padx

        if icon_type:
            icon_left, icon_right = icon_padx

            icon = self.create_icon(
                canvas,
                icon_type,
                size=icon_size,
                side=("left", icon_padx),
                bg=bg_color
            )

            canvas.create_window(
                icon_left, height // 2,
                window=icon,
                anchor="w"
            )

            entry_x = icon_left + icon_size[0] + icon_right

        entry_window = canvas.create_window(
            entry_x,
            height // 2,
            window=entry,
            anchor="w",
            height=height - 12
        )

        def resize(event):
            self.draw_rounded_rect(
                canvas,
                event.width,
                height,
                radius,
                bg_color,
                outline_color,
                border_width,
                tag="resize"
            )

            canvas.itemconfig(
                entry_window,
                width=max(1, event.width - entry_x - inner_padx)
            )

        canvas.bind("<Configure>", resize)

        return canvas, entry
   
    def create_custom_dropdown(
        self,
        parent,
        variable,
        values,
        on_select=None,
        height=36,
        width=12,
        menu_attr="custom_menu",
        bg="#222A3D",
        fg="#E8EAF2",
        accent="#A78BFA",
        font=("Segoe UI", 9),
        pady=6,
        radius=9,
        border_color="#303A52",
        arrow_size=(16, 16)
    ):
        font_obj = tkfont.Font(font=font)
        text_width = max(
            font_obj.measure(variable.get() or ""),
            font_obj.measure(" " * width)
        )

        canvas_width = text_width + arrow_size[0] + 34

        picker = tk.Canvas(
            parent,
            width=canvas_width + 2,
            height=height + 2,
            bg=parent.cget("bg"),
            highlightthickness=0,
            bd=0,
            cursor="hand2"
        )
        picker.pack(side="left", padx=(0, 6), fill="none", expand=False)

        self.draw_rounded_rect(
            picker,
            canvas_width + 2,
            height + 2,
            radius,
            bg,
            border_color,
            tag="dropdown-input"
        )

        text_id = picker.create_text(
            10,
            height // 2,
            text=variable.get(),
            anchor="w",
            fill=fg,
            font=font
        )

        arrow_image = AssetHandler.svg_to_photo(
            "chevron-down.svg",
            size=arrow_size
        )

        icon_id = picker.create_image(
            canvas_width - 10,
            height // 2,
            image=arrow_image,
            anchor="e"
        )

        picker._arrow_image = arrow_image

        variable.trace_add(
            "write",
            lambda *_: picker.itemconfig(text_id, text=variable.get())
        )

        def render_menu(event=None):
            self.render_custom_dropdown_list(
                picker=picker,
                variable=variable,
                values=values() if callable(values) else values,
                on_select=on_select,
                menu_attr=menu_attr
            )

        def set_hover(hovered):
            picker.itemconfig(
                "background",
                fill="#303A52" if hovered else bg
            )

        picker.bind("<Button-1>", render_menu)
        picker.bind("<Enter>", lambda e: set_hover(True))
        picker.bind("<Leave>", lambda e: set_hover(False))

        return picker, text_id, icon_id
 
    def render_custom_dropdown_list(
        self,
        picker,
        variable,
        values,
        on_select=None,
        width=19,
        item_bg="#1A2030",
        hover_bg="#303A52",
        selected_bg="#222A3D",
        fg="#E8EAF2",
        selected_fg="#A78BFA",
        border="#303A52",
        gap=1,
        menu_attr="custom_menu"
    ):
        # Toggle existing menu
        existing_menu = getattr(self, menu_attr, None)

        if existing_menu and existing_menu.winfo_exists():
            existing_menu.destroy()
            setattr(self, menu_attr, None)
            return

        menu = tk.Toplevel(self.root)
        setattr(self, menu_attr, menu)

        menu.overrideredirect(True)
        menu.configure(bg=border)

        try:
            menu.attributes("-alpha", 0.0)
            supports_fade = True
        except tk.TclError:
            supports_fade = False

        container = tk.Frame(menu, bg=item_bg)

        container.pack(
            fill="both",
            expand=True,
            padx=1,
            pady=1
        )

        # Calculate a width that accommodates long options
        font = tkfont.Font(family="Segoe UI", size=9)

        max_text_width = max(
            (font.measure(str(value)) for value in values),
            default=font.measure(" " * width)
        )

        menu_width = min(max(max_text_width + 58, 180), 340)

        # Wrapped menu items
        for value in values:
            selected = value == variable.get()

            item_frame = tk.Frame(
                container,
                bg=selected_bg if selected else item_bg,
                cursor="hand2"
            )
            item_frame.pack(fill="x", padx=2, pady=1)

            indicator = tk.Label(
                item_frame,
                text="✦" if selected else "",
                bg=selected_bg if selected else item_bg,
                fg=selected_fg,
                font=("Segoe UI", 9, "bold"),
                width=3
            )
            indicator.pack(side="left", padx=(7, 0), pady=7)

            item_label = tk.Label(
                item_frame,
                text=str(value),
                bg=selected_bg if selected else item_bg,
                fg=selected_fg if selected else fg,
                font=("Segoe UI", 9),
                anchor="w",
                justify="left",
                wraplength=menu_width - 55,
                padx=5,
                pady=7
            )
            item_label.pack(side="left", fill="x", expand=True)

            def select_item(v=value):
                if not menu.winfo_exists():
                    return

                close_menu()

                if variable.get() != v:
                    variable.set(v)

                    if on_select:
                        on_select()

            def on_enter(event, frame=item_frame, label=item_label,
                        mark=indicator):
                for widget in (frame, label, mark):
                    widget.configure(bg=hover_bg)

            def on_leave(event, frame=item_frame, label=item_label,
                        mark=indicator, is_selected=selected):
                color = selected_bg if is_selected else item_bg

                for widget in (frame, label, mark):
                    widget.configure(bg=color)

            for widget in (item_frame, item_label, indicator):
                widget.bind("<Button-1>", lambda e, v=value: select_item(v))
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)

        menu.update_idletasks()

        menu_height = container.winfo_reqheight() + 2
        menu_width = max(menu_width, container.winfo_reqwidth() + 2)

        picker_x = picker.winfo_rootx()
        picker_y = picker.winfo_rooty()

        # Open above the picker
        x = picker_x
        y = picker_y - menu_height - gap

        # Keep menu within screen bounds
        screen_width = menu.winfo_screenwidth()
        screen_height = menu.winfo_screenheight()

        x = min(x, screen_width - menu_width)
        x = max(0, x)

        if y < 0:
            y = picker_y + picker.winfo_height() + gap

        y = min(y, screen_height - menu_height)
        y = max(0, y)

        menu.attributes("-topmost", True)
        menu.geometry(
            f"{menu_width}x{menu_height}+{x}+{y}"
        )

        # Fade animation — no window resizing
        def fade_in(step=0):
            if not menu.winfo_exists():
                return

            alpha = min(step / 5, 1.0)

            try:
                menu.attributes("-alpha", alpha)
            except tk.TclError:
                return

            if alpha < 1:
                menu.after(35, lambda: fade_in(step + 1))

        def close_menu():
            if not menu.winfo_exists():
                return

            if getattr(menu, "_closing", False):
                return

            menu._closing = True

            if not supports_fade:
                menu.destroy()
                return

            menu.destroy()

        # Close when clicking outside the menu
        def check_outside_click(event=None):
            if not menu.winfo_exists():
                return

            if getattr(menu, "_closing", False):
                return

            focused = menu.focus_get()

            if focused is not None:
                current = focused

                while current is not None:
                    if current == menu:
                        return
                    current = getattr(current, "master", None)

            pointer_x = self.root.winfo_pointerx()
            pointer_y = self.root.winfo_pointery()

            inside_menu = (
                x <= pointer_x <= x + menu_width
                and y <= pointer_y <= y + menu_height
            )

            if not inside_menu:
                close_menu()

        def on_escape(event=None):
            close_menu()

        menu.bind("<Escape>", on_escape)
        menu.bind("<FocusOut>", lambda e: menu.after(80, check_outside_click))

        menu.focus_force()

        if supports_fade:
            fade_in()
        else:
            try:
                menu.attributes("-alpha", 1.0)
            except tk.TclError:
                pass

        return menu
 
   # endregion

    # region ---------------- FUNCTIONS ----------------

    # region Dashboard

    def calculate_progression(self): # ONLY FOR INIT
        remaining_xp = max(0, int(self.xp))
        level = 0

        for low, high, name, description, subtitle, requirement in REALMS:
            if remaining_xp < requirement:
                realm = {
                    "name": name,
                    "description": description,
                    "subtitle": subtitle,
                    "xp_required": requirement
                }
                break

            remaining_xp -= requirement
            level = high + 1

        self.level = level
        return remaining_xp, realm
    
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

        self.schedule_update("dashboard", "ui_render_dashboard_xp_display")

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
        self.schedule_update("board", "render_mission_board")
        self.save_data()

    def change_project(self):
        self.active_project = self.project_var.get()
        # self.selected_mission = None
        self.schedule_update("board", "render_mission_board", {"reset_scroll": True})

    def refresh_project_picker(self):
        # Ensure there is always a valid active project
        if self.active_project not in self.projects:
            self.active_project = next(iter(self.projects), "General")
            self.projects.setdefault(self.active_project, [])

        # Refresh active project picker
        self.project_var.set(self.active_project)

        # Keep bounty project selection valid
        if self.bounty_project_var.get() not in self.projects:
            self.bounty_project_var.set(self.active_project)
        
    # endregion

    # region Bounties

    def current_missions(self): # get current missions
        return self.projects.setdefault(self.active_project, [])
    
    def current_grouped_missions(self):
        missions = self.current_missions()

        today_str = date.today().isoformat()

        grouped = {
            "current": [],
            "completed": [],
            "postponed": []
        }

        # mission_lookup = {}

        for item in missions:
            # mission_id = item.get("task")
            status = item.get("status", "current").lower()

            if status not in grouped:
                status = "current"

            is_daily = item.get("is_daily", False)
            last_done = item.get("last_done_date")
            # streak = item.get("streak_count", 0)

            done_today = is_daily and last_done == today_str

            if done_today:
                status = "completed"

            grouped[status].append(item)

            # mission_lookup[mission_id] = {
            #     "item": item,
            #     "status": status,
            #     "done_today": done_today
            # }

        return grouped, today_str#, mission_lookup
    
    def change_mission_status(self, mission, new_status):
        # start = time.perf_counter()
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

            self.schedule_update("dashboard", "ui_render_dashboard_xp_display")
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
        self.schedule_update("board", "render_mission_board")
        # print("Render setup:", time.perf_counter() - start)

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

        self.schedule_update("board", "render_mission_board")

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

        self.schedule_update("board", "render_mission_board")
        
    def add_mission(self):
        if self.running and self.chosen_bounty is not None:
            self.error_cannot_edit_bounties()
            return
        
        project =  self.bounty_project_var.get().strip()
        task = self.task_var.get().strip()

        try:
            if project == "":
                raise ValueError
        except ValueError:
            self.status_label.config(
                text="Choose which sect to post the bounty in first."
            )
            return
        
        if not project:
            self.status_label.config(
                text="Give your bounty a name first."
            )
            return
        
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
                text="Bounty duration must be between 1 and 1440 minutes!"
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

        self.projects.setdefault(project, []).append(mission)

        self.save_data()
        self.schedule_update("board", "render_mission_board")

        self.task_var.set("")
        self.minutes_var.set("25")
        self.daily_var.set(False)

        self.status_label.config(
            text="✦ New bounty successfully posted!"
        )

        self.check_tutorial("bounty_creation")

    def confirm_remove_mission(self, mission):
        def remove_mission():
            missions = self.current_missions()

            if mission not in missions:
                return

            missions.remove(mission)

            if hasattr(self, "save_data"):
                self.save_data()

            self.schedule_update("board", "render_mission_board")

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

    def error_cannot_edit_bounties(self):
        self.render_message_popup(
            title="Bounty Board Locked",
            description=(
                "To prevent conflicts during an ongoing cultivation session, "
                "the Bounty Board cannot be modified after choosing a recommended "
                "bounty. You can edit it again once your session has ended."),
            wrapsize=700
        )
        
    def session_in_progress(self):
        self.render_message_popup(
                title="Cultivation in Progress",
                description="You already have an ongoing cultivation session. Complete or end your current session before starting another."
            )
        
    def choose_bounty(self, bounty):
        if self.running:
            self.session_in_progress()
            return

        self.chosen_bounty = bounty
        self.control_minutes_var.set(bounty["duration"])
        self.start_session()

    def start_session(self):
        if self.running:
            # self.session_in_progress()
            return

        try:
            minutes = float(self.control_minutes_var.get())
            if not 0 < minutes <= 1440:
                raise ValueError
            seconds = int(minutes * 60)
        except ValueError:
            self.status_label.config(text="Enter a duration between 0 and 1440 minutes.")
            return

        self.duration = seconds
        bonus = self.award_getting_started_bonus()
        if self.getting_started_streak >= 2 and bonus:
            self.render_streak_continues_popup(bonus, self._begin_session)
        else:
            self._begin_session()

        self.check_tutorial("first_session")

    def _begin_session(self):
        if self.running:
            return
        
        self.start_time = time.monotonic()
        self.end_time = self.start_time + self.duration
        self.running = True
        self.session_finished = False
    
        self.timer_label.config(font=("Segoe UI", 29, "bold"))
        self.progress_value = 0
        self.start_button.change_button_state(False)
        self.stop_button.change_button_state(True)
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

        self.stop_button.change_button_state(False)
        self.start_button.change_button_state(True)
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

        self.stop_button.change_button_state(False)
        self.start_button.change_button_state(True)
        self.status_label.config(text="Session stopped.")

        self.root.deiconify()
        self.root.lift()

        self.render_inspection_report_popup()
        
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
    
    def setup_data_folder(self):
        app_data_folder = os.path.join(
            os.environ["APPDATA"],
            "CultivationRealm"
        )

        os.makedirs(app_data_folder, exist_ok=True)

        self.data_file = os.path.join(
            app_data_folder,
            "cultivation_data.json"
        )

        if getattr(sys, "frozen", False):
            app_folder = os.path.dirname(sys.executable)
        else:
            app_folder = os.path.dirname(os.path.abspath(__file__))

        old_data_file = os.path.join(
            app_folder,
            "cultivation_data.json"
        )

        if (
            os.path.isfile(old_data_file)
            and not os.path.exists(self.data_file)
        ):
            try:
                import shutil
                shutil.copy2(old_data_file, self.data_file)
            except OSError as error:
                print(f"Could not migrate saved progress: {error}")

    def save_data(self):
        data = {
            "xp": self.xp,
            "total_completed_bounties": self.total_completed_bounties,
            "level": self.level,
            "history": self.history,
            "projects": self.projects,
            "active_project": self.active_project,
            "last_getting_started": self.last_getting_started,
            "getting_started_streak": self.getting_started_streak,
            "tutorials": self.tutorials
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
            # self.calculate_progression()

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
          
            saved_tutorials = data.get("tutorials", {})
            self.tutorials = {
                key: saved_tutorials.get(key, False)
                for key in TUTORIALS_DICT
            }

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
        start_hidden = False,
        close_rollback = True
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
                command=lambda: self.close_custom_popup(popup, close_rollback),
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

        self._current_popups.append(popup)
        return popup_container

    def close_custom_popup(self, popup, close_rollback=True):
        try:
            popup.grab_release()
        except tk.TclError:
            pass

        self._current_popups.remove(popup)
        popup.destroy()
        if close_rollback: self.show_window() # not if it was the popup of minimize or first session

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
        self.schedule_update("history", "render_mission_log")

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
            self.schedule_update("history", "render_mission_log")
            self.schedule_update("board", "render_mission_board")
            self.schedule_update("dashboard", "ui_render_dashboard_xp_display")
        
        if self.running:
            self.render_message_popup(
                title="SESSION IS RUNNING",
                description="Stop the currently running session before performing this action!",
            )
        else:
            self.render_restart_cultivation_popup(on_confirm)

    def confirm_clear_history(self):
        # self.render_level_up_popup(breakthrough=True)
        def clear_history():
            if self.history:
                self.history.clear()
                self.schedule_update("history", "render_mission_log")
                self.save_data()
            
        self.render_confirmation_popup(
            "CLEAR CULTIVATION HISTORY?",
            "Are you sure you want to clear all cultivation history?",
            clear_history
        )

    # endregion

    # region ---------------- TUTORIALS --------------
    def check_tutorial(self, k):
        if self.tutorials.get(k, False):
            # print("Tutorial already done", k)
            return

        tutorial = TUTORIAL_MESSAGES.get(k)
        if not tutorial:
            print("Tutorial message not found", k)
            return

        popup = self.render_message_popup(
            title=tutorial["title"],
            description=tutorial["description"],
            wrapsize=tutorial.get("wrapsize", 300),
            is_welcome=True,
            close_rollback=k not in ("first_session", "minimize")
        )

        self.tutorials[k] = True
        self.save_data()

        if popup and popup.winfo_exists():
            popup.wait_window()

        return popup
    
    # endregion

    # region ---------------- ICONS --------------

    def create_star_icon(self, frame, color, size, filled=False, glow_radius=10, glow_strength=0.6):
        color = color or StarIconColors.DEEP_GOLD
        size = size or (22, 22)

        if filled == False:
            star_svg = AssetHandler.make_star_svg_hollow(color=color, glow_radius=glow_radius, glow_strength=glow_strength, reflective=True, reflection_strength=0)
        else:
            star_svg = AssetHandler.make_star_svg(color=color, glow_radius=glow_radius, glow_strength=glow_strength, reflective=True, reflection_strength=0)

        star_image = AssetHandler.svg_to_photo(star_svg, size=size)

        # frame = tk.Frame(heading, bg=PANEL)
        # frame.pack(anchor="w")

        star_label = tk.Label(
            frame,
            image=star_image,
            bg=PANEL
        )
        star_label.pack(side="left", padx=(0, 5))

        # Keep image reference alive
        if not hasattr(self, "_card_star_images"):
            self._card_star_images = []

        self._card_star_images.append(star_image)
        return star_label     

    def create_icon(self, frame, icon_type, size, side="left", glow=False, bg=PANEL, star = (True, StarIconColors.DEEP_GOLD)):
        size = size or (32, 32)

        if icon_type == "star":
            if star[0] == False:
                icon = AssetHandler.make_star_svg_hollow(color=star[1], glow_radius=10, glow_strength=0.6, reflective=True, reflection_strength=0)
            else:
                icon = AssetHandler.make_star_svg(color=star[1], glow_radius=10, glow_strength=0.6, reflective=True, reflection_strength=0)
        else:
            icon = icon_type+".svg"

        star_image = AssetHandler.svg_to_photo(icon, size=size, glow=glow)

        # frame = tk.Frame(heading, bg=PANEL)
        # frame.pack(anchor="w")

        star_label = tk.Label(
            frame,
            image=star_image,
            bg=bg
        )

        if isinstance(side, tuple):
            star_label.pack(side=side[0], padx=side[1])
        else:
            star_label.pack(
                side=side,
                padx=(0, 5) if side == "left" else (5, 0)
            )
            
        # Keep image reference alive
        if not hasattr(self, "_card_star_images"):
            self._card_star_images = []

        self._card_star_images.append(star_image)
        return star_label     

    # endregion

if __name__ == "__main__":
    root = tk.Tk()
    app = CultivationRealmMain(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        app.close_app()
