"""
 Pratenoria — Monster World
========================
HOW TO USE CUSTOM IMAGES:
  1. Create a folder called  "images"  in the same directory as this file.
  2. Place your PNG files inside it, named exactly:
       flamora.png     pyroclaw.png    Embercage.png
       aquafin.png     tidalore.png    frostclaw.png
       thornix.png     mosshog.png     quakemole.png
     (all 9  Pratemons — bosses reuse these same 9, no extra art needed)
  3. Optional character portraits:
       professor_pratty.png   — shown on the intro screen
       linox.png               — shown when Linox beats you
     If these are missing, the game falls back to its hand-drawn art.
  4. Run the game — your images will appear automatically!
     If a  Pratemon image is missing, a coloured placeholder is shown instead.

Image sizes that work best:
  • Monster cards       : ~120 x 120 px
  • Confirmation        : ~200 x 200 px  (the game auto-resizes for you)
  • Professor Pratty    : ~220 x 350 px (portrait, taller than wide)
  • Linox                : ~100 x 100 px (square portrait)

Requirements:
  pip install Pillow
"""

import tkinter as tk
import random
import os

# ─── Image directory (same folder as this script) ────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# ─── Color Palette ───────────────────────────────────────────────
BG_DARK    = "#0d0f1a"
BG_CARD    = "#161929"
ACCENT_GOLD= "#f5c842"
ACCENT_CYAN= "#3ef0d8"
ACCENT_RED = "#ff4f6b"
TEXT_WHITE = "#f0f4ff"
TEXT_MUTED = "#8890aa"
BORDER_DIM = "#2a2f4a"

# ─── Monster Data ────────────────────────────────────────────────
# "image" is the PNG filename (without path) inside the images/ folder.
MONSTERS = [
    # ── Fire ─────────────────────────────────────
    {
        "name" : "Flamora",
        "type" : "Fire 🔥",
        "emoji": "🦊",
        "image": "flamora.png",
        "color": "#ff6b35",
        "glow" : "#ff4500",
        "hp"   : 95,
        "atk"  : 85,
        "spd"  : 75,
        "desc" : "A fierce fox wreathed in eternal flames.\nFears no heat, craves battle.",
    },
    {
        "name" : "Pyroclaw",
        "type" : "Fire 🔥",
        "emoji": "🦁",
        "image": "pyroclaw.png",
        "color": "#e84c00",
        "glow" : "#b23000",
        "hp"   : 90,
        "atk"  : 95,
        "spd"  : 70,
        "desc" : "A lion whose claws burn white-hot.\nStrikers fear its searing swipe.",
    },
    {
        "name" : "Embercage",
        "type" : "Fire 🔥",
        "emoji": "🦅",
        "image": "Embercage.png",
        "color": "#ff8c00",
        "glow" : "#cc5500",
        "hp"   : 85,
        "atk"  : 80,
        "spd"  : 95,
        "desc" : "A blazing eagle that dives like a meteor.\nIts speed leaves trails of fire.",
    },
    # ── Water ─────────────────────────────────────
    {
        "name" : "Aquafin",
        "type" : "Water 💧",
        "emoji": "🐬",
        "image": "aquafin.png",
        "color": "#3ab5e6",
        "glow" : "#007acc",
        "hp"   : 100,
        "atk"  : 70,
        "spd"  : 90,
        "desc" : "Swift as a current, calm as the deep.\nCommands tidal forces effortlessly.",
    },
    {
        "name" : "Tidalore",
        "type" : "Water 💧",
        "emoji": "🐢",
        "image": "tidalore.png",
        "color": "#00bcd4",
        "glow" : "#008fa3",
        "hp"   : 115,
        "atk"  : 65,
        "spd"  : 55,
        "desc" : "An ancient sea turtle with iron-hard shell.\nSlow to move, impossible to break.",
    },
    {
        "name" : "frostclaw",
        "type" : "Water 💧",
        "emoji": "🦈",
        "image": "frostclaw.png",
        "color": "#0077b6",
        "glow" : "#004f80",
        "hp"   : 105,
        "atk"  : 75,
        "spd"  : 80,
        "desc" : "A shark cloaked in icy currents.\nIts bite chills enemies to the bone.",
    },
    # ── Earth ─────────────────────────────────────
    {
        "name" : "Thornix",
        "type" : "Earth 🌿",
        "emoji": "🦎",
        "image": "thornix.png",
        "color": "#5ec45e",
        "glow" : "#2d8a2d",
        "hp"   : 110,
        "atk"  : 75,
        "spd"  : 60,
        "desc" : "Ancient lizard armored in living bark.\nIts strength grows from the soil.",
    },
    {
        "name" : "Mosshog",
        "type" : "Earth 🌿",
        "emoji": "🐗",
        "image": "mosshog.png",
        "color": "#7ab648",
        "glow" : "#4a8a1a",
        "hp"   : 105,
        "atk"  : 80,
        "spd"  : 65,
        "desc" : "A boar covered in thick moss armor.\nCharges with the force of a landslide.",
    },
    {
        "name" : "Quakemole",
        "type" : "Earth 🌿",
        "emoji": "🦔",
        "image": "quakemole.png",
        "color": "#8db600",
        "glow" : "#5a7a00",
        "hp"   : 120,
        "atk"  : 70,
        "spd"  : 50,
        "desc" : "A burrowing beast that shakes the earth.\nIts tunnels have toppled mountains.",
    },
]

# ─── Lookup helper — used to build boss/trainer teams from the SAME
#      Pratemons already defined above, instead of inventing new ones ────
def _get_monster(name):
    return next(m for m in MONSTERS if m["name"] == name)

# ─── Image Loader Utility ────────────────────────────────────────
def load_image(filename, size):
    """
    Load a PNG from the images/ folder and resize it.
    Returns a PhotoImage, or None if the file is missing / unreadable.
    size = (width, height)
    """
    try:
        from PIL import Image, ImageTk
        path = os.path.join(IMAGES_DIR, filename)
        if not os.path.isfile(path):
            return None
        img = Image.open(path).convert("RGBA")
        img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"[Image Error] {filename}: {e}")
        return None


def make_placeholder(size, hex_color):
    """
    Create a solid-colour square PhotoImage used when the PNG is missing.
    """
    try:
        from PIL import Image, ImageTk, ImageDraw
        img  = Image.new("RGBA", size, hex_color + "bb")
        draw = ImageDraw.Draw(img)
        # Dashed border
        draw.rectangle([2, 2, size[0]-3, size[1]-3],
                        outline="#ffffff55", width=2)
        # Centre "?" mark
        draw.text((size[0]//2 - 6, size[1]//2 - 10), "?",
                   fill="#ffffffaa")
        return ImageTk.PhotoImage(img)
    except Exception:
        # Absolute fallback: blank PhotoImage via tkinter
        return tk.PhotoImage(width=size[0], height=size[1])


# ═════════════════════════════════════════════════════════════════
class  PratemonsGame:
    def __init__(self, root):
        self.root = root
        self.root.title(" PratemonS — Monster World")
        self.root.geometry("1024x720")
        self.root.minsize(800, 600)
        self.root.resizable(True, True)
        self.root.configure(bg=BG_DARK)

        self._fullscreen = False
        self.root.bind("<F11>", self._toggle_fullscreen)
        self.root.bind("<Escape>", self._exit_fullscreen)

        self.selected_monster = None
        self.anim_id          = None
        self._img_refs = []
        self._resize_after_id = None

        self.show_title_screen()

    def _toggle_fullscreen(self, event=None):
        self._fullscreen = not self._fullscreen
        self.root.attributes("-fullscreen", self._fullscreen)

    def _exit_fullscreen(self, event=None):
        self._fullscreen = False
        self.root.attributes("-fullscreen", False)

    # ── helpers ──────────────────────────────────────────────────
    # ── Size helpers (always returns live window dimensions) ────────
    def W(self): return self.root.winfo_width()  or 1024
    def H(self): return self.root.winfo_height() or 720

    # ── Responsive canvas: bind resize → redraw ─────────────────────
    def _bind_resize(self, canvas, redraw_fn):
        """Call redraw_fn whenever the window is resized.

        Only ONE screen's redraw handler is ever active at a time. Using
        add="+" here would stack a new <Configure> handler on top of the
        root window every time a screen is shown, without removing the
        previous screen's handler when clear() destroys its canvas — so
        every resize would keep firing old handlers pointing at destroyed
        widgets (raising errors that could block other handlers in the
        same event), which is why only *some* screens appeared to resize
        correctly. Rebinding (no add="+") replaces the previous handler
        outright, and we also cancel any pending redraw in clear().
        """
        if self._resize_after_id:
            self.root.after_cancel(self._resize_after_id)
            self._resize_after_id = None

        def _on_resize(e):
            if e.widget is self.root:
                if self._resize_after_id:
                    self.root.after_cancel(self._resize_after_id)
                self._resize_after_id = self.root.after(60, redraw_fn)
        self.root.bind("<Configure>", _on_resize)

    def clear(self):
        if self.anim_id:
            self.root.after_cancel(self.anim_id)
            self.anim_id = None
        if hasattr(self, '_dlg_anim_id') and self._dlg_anim_id:
            self.root.after_cancel(self._dlg_anim_id)
            self._dlg_anim_id = None
        # Cancel any pending debounced redraw and drop the old screen's
        # <Configure> handler so it can't fire against widgets we're
        # about to destroy (this was the cause of resizing only working
        # for some screens — see _bind_resize).
        if self._resize_after_id:
            self.root.after_cancel(self._resize_after_id)
            self._resize_after_id = None
        self.root.unbind("<Configure>")
        for w in self.root.winfo_children():
            w.destroy()
        self._img_refs.clear()

    def _keep(self, img):
        """Prevent a PhotoImage from being garbage-collected."""
        self._img_refs.append(img)
        return img

    def _get_img(self, monster, size):
        """Return a live PhotoImage for a monster card (real PNG or placeholder)."""
        img = load_image(monster["image"], size) if monster.get("image") else None
        if img is None:
            img = make_placeholder(size, monster.get("color", "#9933cc"))
        return self._keep(img)

    def _draw_shadowfang(self, canvas, x, y, r, tags=()):
        """
        Draw Shadowfang centred at (x, y) with radius r. Uses
        images/shadowfang.png when present, otherwise a drawn
        dark wolf-like face so it is always clearly visible.
        """
        img = self._get_char_img("shadowfang.png", (r*2, r*2))
        if img:
            canvas.create_image(x, y, image=img, anchor="center", tags=tags)
            return
        k = r / 100.0
        # ears
        canvas.create_polygon(x-int(70*k), y-int(20*k), x-int(55*k), y-int(100*k), x-int(15*k), y-int(55*k),
                              fill="#2a0040", outline="#9933cc", width=2, tags=tags)
        canvas.create_polygon(x+int(70*k), y-int(20*k), x+int(55*k), y-int(100*k), x+int(15*k), y-int(55*k),
                              fill="#2a0040", outline="#9933cc", width=2, tags=tags)
        # head
        canvas.create_oval(x-int(80*k), y-int(70*k), x+int(80*k), y+int(80*k),
                           fill="#1a0028", outline="#9933cc", width=3, tags=tags)
        # snout
        canvas.create_oval(x-int(38*k), y+int(5*k), x+int(38*k), y+int(70*k),
                           fill="#2a0040", outline="#7700bb", width=2, tags=tags)
        canvas.create_oval(x-int(10*k), y+int(15*k), x+int(10*k), y+int(28*k),
                           fill="#cc44ff", outline="", tags=tags)
        # glowing eyes
        for sx in (-1, 1):
            canvas.create_polygon(x+sx*int(14*k), y-int(18*k), x+sx*int(58*k), y-int(34*k),
                                  x+sx*int(50*k), y-int(2*k),
                                  fill="#ff2266", outline="#ffaacc", width=1, tags=tags)
        # fangs
        for sx in (-1, 1):
            canvas.create_polygon(x+sx*int(26*k), y+int(52*k), x+sx*int(14*k), y+int(52*k),
                                  x+sx*int(20*k), y+int(82*k),
                                  fill="white", outline="#ddd", tags=tags)

    def _get_char_img(self, filename, size):
        """
        Return a live PhotoImage for a named character portrait
        (e.g. 'professor_pratty.png', 'linox.png') from images/, or
        None if the file isn't there — callers fall back to the
        existing hand-drawn artwork in that case.
        """
        img = load_image(filename, size)
        if img is None:
            return None
        return self._keep(img)

    # ══════════════════════════════════════════════
    #  TITLE SCREEN
    # ══════════════════════════════════════════════
    def show_title_screen(self):
        self.clear()
        self.canvas = tk.Canvas(self.root, bg=BG_DARK, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.stars = []
        self._draw_title()
        self._bind_resize(self.canvas, self._draw_title)
        self._animate_stars()

    def _draw_title(self):
        c = self.canvas
        c.delete("static")
        self._img_refs = [r for r in self._img_refs if True]   # keep star ovals
        W, H = self.W(), self.H()
        cx, cy = W//2, H//2
        fs_title = max(28, min(54, W//18))
        fs_sub   = max(9,  min(14, W//70))
        fs_btn   = max(10, min(13, W//80))

        # Background fill
        c.create_rectangle(0,0,W,H, fill=BG_DARK, outline="", tags="static")

        # Rebuild stars if first time or resize
        if not self.stars:
            for _ in range(140):
                x, y = random.randint(0,W), random.randint(0,H)
                r = random.uniform(0.8, 2.2)
                s = c.create_oval(x-r,y-r,x+r,y+r, fill="white", outline="")
                self.stars.append(s)

        # Decorative rings around center
        for i,(col,r) in enumerate([(ACCENT_CYAN, H//3),(ACCENT_GOLD, H//4),(ACCENT_RED, H//5)]):
            c.create_oval(cx-r,cy-r-H//12,cx+r,cy+r-H//12,
                          outline=col, width=1, dash=(4+i*2,8+i*2), tags="static")

        # Title
        ty = int(H*0.27)
        for dx,dy in [(-2,-2),(-2,2),(2,-2),(2,2)]:
            c.create_text(cx+dx,ty+dy, text=" PratemonS",
                          font=("Courier",fs_title,"bold"), fill="#1a0a3a", tags="static")
        c.create_text(cx, ty, text=" PratemonS",
                      font=("Courier",fs_title,"bold"), fill=ACCENT_GOLD, tags="static")
        c.create_text(cx, ty+int(H*0.08), text="✦  M O N S T E R   W O R L D  ✦",
                      font=("Courier",fs_sub), fill=ACCENT_CYAN, tags="static")

        # Monster parade
        seen_t = set()
        parade = [m for m in MONSTERS if m["type"] not in seen_t and not seen_t.add(m["type"])]
        icon_size = max(150, min(200, W//14))
        parade_y = int(H*0.54)
        spread = min(120, W//8)
        for i,m in enumerate(parade):
            px = cx + (i - len(parade)//2) * spread
            img = self._get_img(m, (icon_size, icon_size))
            c.create_image(px, parade_y, image=img, anchor="center", tags="static")
            c.create_text(px, parade_y+icon_size//2+8, text=m["name"],
                          font=("Courier",max(7,fs_sub-2)), fill=TEXT_MUTED, tags="static")

        # Buttons
        bw = max(130, min(180, W//6))
        bh = max(38, min(52, H//15))
        bx = cx - bw//2
        self._make_button(c, bx, int(H*0.68), bw, bh,
                          "▶  START", ACCENT_CYAN, BG_DARK, self.show_monster_select)
        self._make_button(c, bx, int(H*0.68)+bh+14, bw, bh,
                          "✕  QUIT",  ACCENT_RED,  BG_DARK, self.root.destroy)

        # F11 hint
        c.create_text(cx, H-24,
                      text="F11 = Fullscreen  |  © 2026  Pratemons World · Python Edition",
                      font=("Courier",max(7,fs_sub-2)), fill=TEXT_MUTED, tags="static")

    def _animate_stars(self):
        for sid in self.stars:
            try:
                cur = self.canvas.itemcget(sid, "fill")
                new = BG_DARK if (cur == "white" and random.random() < 0.015) \
                      else ("white" if cur == BG_DARK else cur)
                self.canvas.itemconfig(sid, fill=new)
            except tk.TclError:
                pass
        self.anim_id = self.root.after(120, self._animate_stars)

    def _make_button(self, canvas, x, y, w, h, text, color, bg, command):
        canvas.create_rectangle(x+3, y+3, x+w+3, y+h+3,
                                 fill="#000000", outline="")
        rect  = canvas.create_rectangle(x, y, x+w, y+h,
                                         fill=BG_CARD, outline=color, width=2)
        label = canvas.create_text(x+w//2, y+h//2, text=text,
                                    fill=color, font=("Courier",13,"bold"))

        def on_enter(e):
            canvas.itemconfig(rect,  fill=color)
            canvas.itemconfig(label, fill=BG_DARK)
        def on_leave(e):
            canvas.itemconfig(rect,  fill=BG_CARD)
            canvas.itemconfig(label, fill=color)
        def on_click(e):
            command()

        for item in (rect, label):
            canvas.tag_bind(item, "<Enter>",    on_enter)
            canvas.tag_bind(item, "<Leave>",    on_leave)
            canvas.tag_bind(item, "<Button-1>", on_click)

    # ══════════════════════════════════════════════
    #  MONSTER SELECTION SCREEN
    # ══════════════════════════════════════════════
    def show_monster_select(self):
        self.clear()
        canvas = tk.Canvas(self.root, bg=BG_DARK, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        seen_types = set()
        starters = [m for m in MONSTERS if m["type"] not in seen_types and not seen_types.add(m["type"])]

        def draw():
            canvas.delete("all")
            self._img_refs.clear()
            W, H = self.W(), self.H()
            cx = W // 2
            fs_title = max(14, min(22, W // 48))
            fs_sub   = max(8,  min(11, W // 95))
            fs_card  = max(9,  min(12, W // 88))
            fs_stat  = max(7,  min(9,  W // 120))

            # Header
            canvas.create_rectangle(0, 0, W, int(H*0.14), fill=BG_CARD, outline=BORDER_DIM)
            canvas.create_text(cx, int(H*0.055), text="SELECT YOUR  Pratemon",
                               font=("Courier", fs_title, "bold"), fill=ACCENT_GOLD)
            canvas.create_text(cx, int(H*0.105),
                               text="Choose your companion wisely — they fight for you!",
                               font=("Courier", fs_sub), fill=TEXT_MUTED)
            canvas.create_line(40, int(H*0.14), W-40, int(H*0.14), fill=ACCENT_GOLD, width=1)

            # Cards
            n = len(starters)
            card_w = max(140, min(200, (W - 80) // n - 24))
            card_h = max(240, min(320, int(H * 0.60)))
            total_w = n * card_w + (n-1) * 20
            start_x = (W - total_w) // 2
            card_tops = []

            for i, m in enumerate(starters):
                cx2 = start_x + i * (card_w + 20)
                cy2 = int(H * 0.18)
                card_tops.append((cx2, cy2))
                selected = self.selected_monster == m
                border_col = m["color"] if selected else BORDER_DIM

                # Card shadow
                canvas.create_rectangle(cx2+4, cy2+4, cx2+card_w+4, cy2+card_h+4,
                                        fill="#000000", outline="", tags=f"card_{i}")
                # Card body
                canvas.create_rectangle(cx2, cy2, cx2+card_w, cy2+card_h,
                                        fill=BG_CARD, outline=border_col, width=3,
                                        tags=f"card_{i}")
                # Type badge
                canvas.create_rectangle(cx2, cy2, cx2+card_w, cy2+int(card_h*0.09),
                                        fill=m["color"], outline="", tags=f"card_{i}")
                canvas.create_text(cx2+card_w//2, cy2+int(card_h*0.045),
                                   text=m["type"], font=("Courier", fs_stat, "bold"),
                                   fill=BG_DARK, tags=f"card_{i}")
                # Monster image
                img_sz = max(80, min(130, card_w - 20))
                img = self._get_img(m, (img_sz, img_sz))
                img_y = cy2 + int(card_h*0.09) + img_sz//2 + 6
                canvas.create_image(cx2+card_w//2, img_y, image=img, anchor="center",
                                    tags=f"card_{i}")
                # Name
                canvas.create_text(cx2+card_w//2, img_y+img_sz//2+14,
                                   text=m["name"], font=("Courier", fs_card, "bold"),
                                   fill=m["color"], tags=f"card_{i}")
                # Stats
                stat_y = img_y + img_sz//2 + 32
                for j, (lbl, val, col) in enumerate([("HP", m["hp"], ACCENT_CYAN),
                                                      ("ATK",m["atk"],ACCENT_RED),
                                                      ("SPD",m["spd"],ACCENT_GOLD)]):
                    sy = stat_y + j * int(card_h*0.085)
                    canvas.create_text(cx2+18, sy, text=lbl,
                                       font=("Courier", fs_stat), fill=TEXT_MUTED,
                                       anchor="w", tags=f"card_{i}")
                    bar_x = cx2 + 40
                    bar_w2 = card_w - 60
                    canvas.create_rectangle(bar_x, sy-5, bar_x+bar_w2, sy+5,
                                            fill=BORDER_DIM, outline="", tags=f"card_{i}")
                    canvas.create_rectangle(bar_x, sy-5,
                                            bar_x+int(bar_w2*val/120), sy+5,
                                            fill=col, outline="", tags=f"card_{i}")
                    canvas.create_text(cx2+card_w-8, sy,
                                       text=str(val), font=("Courier", fs_stat),
                                       fill=TEXT_WHITE, anchor="e", tags=f"card_{i}")

                # Hover/click bindings
                def make_click(monster=m, idx=i):
                    def on_click(e):
                        self.selected_monster = monster
                        draw()
                    return on_click

                def make_hover(monster=m, idx=i, enter=True):
                    def on_hover(e):
                        if self.selected_monster != monster:
                            draw()
                    return on_hover

                canvas.tag_bind(f"card_{i}", "<Button-1>", make_click(m, i))

            # Confirm button
            btn_y = int(H * 0.84)
            bw = max(160, min(240, W // 5))
            bh = max(36, min(50, int(H * 0.07)))
            if self.selected_monster:
                m = self.selected_monster
                canvas.create_text(cx, btn_y - 16,
                                   text=f"You selected: {m['name']} ({m['type']})",
                                   font=("Courier", fs_sub, "bold"), fill=m["color"])
                self._make_button(canvas, cx - bw//2, btn_y, bw, bh,
                                  f"CHOOSE {m['name'].upper()}  ▶",
                                  m["color"], BG_DARK, self.confirm_selection)
            else:
                canvas.create_text(cx, btn_y + bh//2,
                                   text="← Click a  Pratemon card to select →",
                                   font=("Courier", fs_sub, "italic"), fill=TEXT_MUTED)

            # Back
            self._make_button(canvas, 20, int(H*0.93), max(100,W//10), max(28,int(H*0.05)),
                              "← BACK", BORDER_DIM, BG_DARK, self.show_title_screen)

        draw()
        self._bind_resize(canvas, draw)

    # ══════════════════════════════════════════════
    #  CONFIRMATION SCREEN
    # ══════════════════════════════════════════════
    def confirm_selection(self):
        if not self.selected_monster:
            return
        self.clear()
        m = self.selected_monster
        canvas = tk.Canvas(self.root, bg=BG_DARK, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        def draw():
            canvas.delete("all")
            self._img_refs.clear()
            W, H = self.W(), self.H()
            cx, cy = W//2, H//2
            fs_big  = max(20, min(32, W//30))
            fs_med  = max(10, min(14, W//70))
            fs_sm   = max(8,  min(10, W//100))

            canvas.create_rectangle(0,0,W,H, fill=BG_DARK, outline="")
             
            canvas.create_text(cx, int(H*0.10), text="✦  YOU CHOSE  ✦",
                               font=("Courier",fs_med), fill=TEXT_MUTED)
            img_sz = max(120, min(220, int(H*0.32)))
            big_img = self._get_img(m,(img_sz,img_sz))
            canvas.create_image(cx, int(H*0.37), image=big_img, anchor="center")
            canvas.create_text(cx, int(H*0.56), text=m["name"].upper(),
                               font=("Courier",fs_big,"bold"), fill=m["color"])
            canvas.create_text(cx, int(H*0.63), text=m["type"],
                               font=("Courier",fs_med), fill=TEXT_WHITE)
            

            stat_y = int(H*0.79)
            stat_gap = max(100, W//8)
            for i,(lbl,val,col) in enumerate([("HP",m["hp"],ACCENT_CYAN),
                                              ("ATK",m["atk"],ACCENT_RED),
                                              ("SPD",m["spd"],ACCENT_GOLD)]):
                sx = cx - stat_gap + i*stat_gap
                canvas.create_text(sx, stat_y, text=lbl,
                                   font=("Courier",fs_sm), fill=TEXT_MUTED)
                canvas.create_text(sx, stat_y+int(H*0.045), text=str(val),
                                   font=("Courier",max(14,fs_big-8),"bold"), fill=col)

            canvas.create_text(cx, int(H*0.88),
                               text="Your adventure is about to begin...",
                               font=("Courier",fs_sm,"italic"), fill=TEXT_MUTED)

            bw = max(140,min(200,W//6)); bh = max(30,min(40,int(H*0.06)))
            self._make_button(canvas, cx-bw-10, int(H*0.91), bw, bh,
                              "← CHANGE", BORDER_DIM, BG_DARK, self.show_monster_select)
            self._make_button(canvas, cx+10, int(H*0.91), bw, bh,
                              "▶  CONTINUE", m["color"], BG_DARK,
                              lambda: self.show_professor_screen(m))

        draw()
        self._bind_resize(canvas, draw)

    # ══════════════════════════════════════════════
    #  PROFESSOR SCREEN
    # ══════════════════════════════════════════════
    def show_professor_screen(self, m):
        self.clear()

        canvas = tk.Canvas(self.root,
                           bg=BG_DARK, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # ── Background decoration ─────────────────────
        canvas.create_rectangle(0, 0, 760, 580, fill=BG_DARK, outline="")
        canvas.create_rectangle(0, 440, 760, 580, fill="#0a1520", outline="")
        canvas.create_line(0, 440, 760, 440, fill=BORDER_DIM, width=1)

        # ── Floor tiles ──────────────────────────────
        for x in range(0, 760, 60):
            canvas.create_line(x, 440, x, 580, fill=BORDER_DIM, width=1)

        # ── Professor Pratty ──────────────────────────
        px = 200   # center x of professor
        prof_img = self._get_char_img("professor_pratty.png", (220, 350))

        if prof_img:
            # Real portrait — drop in images/professor_pratty.png to use it.
            canvas.create_oval(px-50, 438, px+50, 450, fill="#050a0f", outline="")
            canvas.create_image(px, 270, image=prof_img, anchor="center")
            canvas.create_rectangle(px-38, 434, px+38, 452, fill=ACCENT_CYAN, outline=BG_DARK, width=1)
            canvas.create_text(px, 443, text="PROF. PRATTY",
                               font=("Courier", 7, "bold"), fill=BG_DARK)
        else:
            # Fallback illustration (drawn with tkinter shapes) — used
            # automatically whenever images/professor_pratty.png is missing.

            # Shadow under feet
            canvas.create_oval(px-50, 438, px+50, 450, fill="#050a0f", outline="")

            # Legs
            canvas.create_rectangle(px-28, 360, px-6,  435, fill="#2a3a5a", outline="#1a2a4a", width=1)
            canvas.create_rectangle(px+6,  360, px+28, 435, fill="#2a3a5a", outline="#1a2a4a", width=1)

            # Shoes
            canvas.create_oval(px-34, 425, px+0,  445, fill="#111122", outline="")
            canvas.create_oval(px+0,  425, px+34, 445, fill="#111122", outline="")

            # Lab coat body
            canvas.create_rectangle(px-55, 200, px+55, 368, fill="#e8f0f8", outline="#99aabb", width=2)

            # Coat lapels
            canvas.create_polygon(px, 200, px-30, 260, px-5, 255,
                                   fill="#ccdde8", outline="#99aabb", width=1)
            canvas.create_polygon(px, 200, px+30, 260, px+5, 255,
                                   fill="#ccdde8", outline="#99aabb", width=1)

            # Shirt / tie area
            canvas.create_rectangle(px-18, 200, px+18, 285, fill="#b8cfe0", outline="")
            canvas.create_polygon(px-6, 210, px+6, 210, px+4, 270, px-4, 270,
                                   fill=ACCENT_CYAN, outline="")  # tie

            # Arms
            canvas.create_rectangle(px-80, 205, px-52, 320, fill="#e8f0f8", outline="#99aabb", width=1)
            canvas.create_rectangle(px+52, 205, px+80, 320, fill="#e8f0f8", outline="#99aabb", width=1)

            # Hands
            canvas.create_oval(px-82, 315, px-48, 340, fill="#f5c8a0", outline="#d4a870", width=1)
            canvas.create_oval(px+48, 315, px+82, 340, fill="#f5c8a0", outline="#d4a870", width=1)

            # Pointing finger on right hand (toward speech bubble)
            canvas.create_rectangle(px+75, 308, px+95, 320, fill="#f5c8a0", outline="#d4a870", width=1)

            # Name badge
            canvas.create_rectangle(px-38, 295, px+38, 320, fill=ACCENT_CYAN, outline=BG_DARK, width=1)
            canvas.create_text(px, 307, text="PROF. PRATTY",
                               font=("Courier", 7, "bold"), fill=BG_DARK)

            # Neck
            canvas.create_rectangle(px-14, 155, px+14, 205, fill="#f5c8a0", outline="#d4a870", width=1)

            # Head
            canvas.create_oval(px-45, 95, px+45, 200, fill="#f5c8a0", outline="#d4a870", width=2)

            # Hair
            canvas.create_arc(px-45, 90, px+45, 165, start=0, extent=180,
                              fill="#5a3a1a", outline="#3a2010", width=1)
            # Side hair tufts
            canvas.create_oval(px-50, 110, px-30, 145, fill="#5a3a1a", outline="")
            canvas.create_oval(px+30, 110, px+50, 145, fill="#5a3a1a", outline="")

            # Eyes
            canvas.create_oval(px-24, 138, px-10, 152, fill="white", outline="#555", width=1)
            canvas.create_oval(px+10, 138, px+24, 152, fill="white", outline="#555", width=1)
            canvas.create_oval(px-21, 141, px-13, 149, fill="#1a1a2a", outline="")  # pupils
            canvas.create_oval(px+13, 141, px+21, 149, fill="#1a1a2a", outline="")

            # Eyebrows
            canvas.create_line(px-25, 133, px-8,  130, fill="#3a2010", width=2)
            canvas.create_line(px+8,  130, px+25, 133, fill="#3a2010", width=2)

            # Glasses frames
            canvas.create_rectangle(px-26, 135, px-8,  153, outline=ACCENT_GOLD, width=2)
            canvas.create_rectangle(px+8,  135, px+26, 153, outline=ACCENT_GOLD, width=2)
            canvas.create_line(px-8, 143, px+8, 143, fill=ACCENT_GOLD, width=2)

            # Nose
            canvas.create_oval(px-5, 153, px+5, 162, fill="#e8b090", outline="")

            # Smile
            canvas.create_arc(px-18, 158, px+18, 182,
                              start=205, extent=130, style="arc",
                              outline="#884422", width=2)

        # ── Speech bubble (right side) ───────────────
        bx, by, bw, bh = 370, 55, 360, 340

        # Bubble shadow
        canvas.create_rectangle(bx+4, by+4, bx+bw+4, by+bh+4,
                                 fill="#000000", outline="")
        # Bubble body
        canvas.create_rectangle(bx, by, bx+bw, by+bh,
                                 fill=BG_CARD, outline=ACCENT_CYAN, width=2)
        # Tail toward professor
        canvas.create_polygon(bx+2, by+80, bx-20, by+105, bx+2, by+125,
                               fill=BG_CARD, outline=BG_CARD, width=1)
        canvas.create_line(bx+1, by+81, bx+1, by+124,
                           fill=BG_CARD, width=4)
        canvas.create_line(bx-1, by+80, bx-20, by+105,
                           fill=ACCENT_CYAN, width=2)
        canvas.create_line(bx-20, by+105, bx-1, by+125,
                           fill=ACCENT_CYAN, width=2)

        # Professor name in bubble
        canvas.create_text(bx+bw//2, by+20,
                           text="— Professor Pratty —",
                           font=("Courier", 11, "bold"), fill=ACCENT_CYAN)
        canvas.create_line(bx+15, by+36, bx+bw-15, by+36,
                           fill=BORDER_DIM, width=1)

        # ── Dialogue lines ────────────────────────────
        dialogue = [
            f"Welcome, {m['name']} trainer!",
            "",
            "I am Professor Pratty.",
            "I need your help urgently.",
            "",
            "A villain named",
            "** L I N O X **",
            "is hunting the world's",
            "STRONGEST  Pratemon.",
            "",
            "If he captures it,",
            "the world is in danger.",
            "",
            "YOU must stop him!",
            "Start your journey now!",
        ]

        self._dialogue_lines  = dialogue
        self._dialogue_index  = 0
        self._dialogue_canvas = canvas
        self._dialogue_x      = bx + bw // 2
        self._dialogue_y0     = by + 50
        self._dialogue_ids    = []
        self._dlg_anim_id     = None
        self._type_next_line()

        # Monster reminder bottom left
        mini_img = self._get_img(m, (60, 60))
        canvas.create_image(50, 490, image=mini_img, anchor="center")
        canvas.create_text(50, 528, text=m["name"],
                           font=("Courier", 8, "bold"), fill=m["color"])

        # Journey button shown after dialogue ends
        self._journey_canvas    = canvas
        self._journey_monster   = m
        self._journey_btn_drawn = False

    def _type_next_line(self):
        lines = self._dialogue_lines
        canvas = self._dialogue_canvas
        idx    = self._dialogue_index

        if idx >= len(lines):
            self._show_journey_btn()
            return

        line = lines[idx]
        y    = self._dialogue_y0 + idx * 17

        # Special highlight for LINOX
        if "L I N O X" in line:
            tid = canvas.create_text(self._dialogue_x, y, text=line,
                                      font=("Courier",11,"bold"), fill=ACCENT_RED,
                                      anchor="center")
        elif line.startswith("YOU") or line.startswith("STRONGEST"):
            tid = canvas.create_text(self._dialogue_x, y, text=line,
                                      font=("Courier",10,"bold"), fill=ACCENT_GOLD,
                                      anchor="center")
        else:
            tid = canvas.create_text(self._dialogue_x, y, text=line,
                                      font=("Courier",10), fill=TEXT_WHITE,
                                      anchor="center")

        self._dialogue_ids.append(tid)
        self._dialogue_index += 1
        delay = 60 if line.strip() else 20
        self._dlg_anim_id = self.root.after(delay, self._type_next_line)

    def _show_journey_btn(self):
        if self._journey_btn_drawn:
            return
        self._journey_btn_drawn = True
        canvas = self._journey_canvas
        m      = self._journey_monster

        # Pulsing "Start Journey" button
        canvas.create_text(380, 475,
                           text="The world is waiting for you, trainer...",
                           font=("Courier",10,"italic"), fill=TEXT_MUTED)
        self._make_button(canvas, 255, 500, 250, 46,
                          "🌍  START JOURNEY", ACCENT_GOLD, BG_DARK,
                          lambda: self._play_screen(m))

    # ══════════════════════════════════════════════
    #  PLAY / JOURNEY SCREEN (placeholder)
    # ══════════════════════════════════════════════
    # ══════════════════════════════════════════════
    #  HUB SCREEN  (Team / Battle / Help)
    # ══════════════════════════════════════════════
    def _play_screen(self, starter):
        if not hasattr(self, 'player_team'):
            self.player_team = [starter]
        if not hasattr(self, 'player_collection'):
            self.player_collection = [starter]   # only owned monsters
        self.current_checkpoint = getattr(self, 'current_checkpoint', 0)
        self.show_hub()

    def show_hub(self):
        self.clear()
        canvas = tk.Canvas(self.root, bg=BG_DARK, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        def draw():
            canvas.delete("all")
            self._img_refs.clear()
            W, H = self.W(), self.H()
            cx = W//2
            fs  = max(10, min(20, W//52))
            fss = max(8,  min(10, W//100))

            # Header
            canvas.create_rectangle(0,0,W,int(H*0.12), fill=BG_CARD, outline=BORDER_DIM)
            canvas.create_text(cx, int(H*0.045), text=" PratemonS  WORLD",
                               font=("Courier",fs,"bold"), fill=ACCENT_GOLD)
            canvas.create_text(cx, int(H*0.09),
                               text="Find LINOX and protect the strongest  Pratemon!",
                               font=("Courier",fss), fill=TEXT_MUTED)

            # Landscape
            canvas.create_rectangle(0,int(H*0.65),W,H, fill="#0a1a0a", outline="")
            canvas.create_rectangle(0,int(H*0.58),W,int(H*0.66), fill="#112211", outline="")
            for mx,mh in [(int(W*0.13),int(H*0.31)),(int(W*0.30),int(H*0.24)),
                          (int(W*0.63),int(H*0.34)),(int(W*0.82),int(H*0.27)),(int(W*0.95),int(H*0.22))]:
                canvas.create_polygon(mx-int(W*0.11),int(H*0.58),mx,int(H*0.58)-mh,
                                      mx+int(W*0.11),int(H*0.58),
                                      fill="#1a2a1a", outline="#223322")
            for _ in range(40):
                sx,sy = random.randint(0,W), random.randint(int(H*0.13),int(H*0.40))
                canvas.create_oval(sx,sy,sx+2,sy+2, fill="#aabbcc", outline="")
            canvas.create_oval(int(W*0.37),int(H*0.60),int(W*0.63),int(H*0.69),
                               fill="#1e3a1e", outline="")
            canvas.create_text(cx, int(H*0.64),
                               text="Your Journey Awaits...",
                               font=("Courier",fss,"italic"), fill="#4a8a4a")

            # Team preview
            canvas.create_text(int(W*0.07), int(H*0.69),
                               text="TEAM", font=("Courier",fss,"bold"), fill=TEXT_MUTED)
            icon_sz = max(50, min(75, W//16))
            for i,mon in enumerate(self.player_team[:3]):
                tx = int(W*0.04) + i*int(icon_sz*1.3)
                ty = int(H*0.77)
                ti = self._get_img(mon,(icon_sz,icon_sz))
                canvas.create_image(tx,ty,image=ti,anchor="center")
                canvas.create_text(tx,ty+icon_sz//2+8,
                                   text=mon["name"][:6],
                                   font=("Courier",max(6,fss-2)), fill=mon["color"])

            # 4 buttons evenly spaced
            btn_labels  = ["TEAM","BATTLE","DEX","HELP"]
            btn_colors  = [ACCENT_CYAN, ACCENT_RED, "#aa66ff", ACCENT_GOLD]
            btn_subs    = ["Manage monsters","Fight enemies","All  Pratemons","View type chart"]
            btn_actions = [self.show_team_screen, self.show_battle_screen,
                           self.show_dex_screen,  self.show_help_screen]
            bw  = max(120, min(180, (W-80)//4 - 20))
            bh  = max(40,  min(56,  int(H*0.08)))
            by  = int(H*0.84)
            gap = (W - 4*bw) // 5
            for i,(lbl,col,sub,act) in enumerate(zip(btn_labels,btn_colors,btn_subs,btn_actions)):
                bx = gap + i*(bw+gap)
                self._make_button(canvas, bx, by, bw, bh, lbl, col, BG_DARK, act)
                canvas.create_text(bx+bw//2, by+bh+12, text=sub,
                                   font=("Courier",max(7,fss-1)), fill=TEXT_MUTED)

            canvas.create_text(cx, H-14, text="[ MAIN MENU ]",
                               font=("Courier",fss), fill=BORDER_DIM, tags="back_lbl")
            canvas.tag_bind("back_lbl","<Button-1>", lambda e: self.show_title_screen())
            canvas.tag_bind("back_lbl","<Enter>",    lambda e: canvas.itemconfig("back_lbl",fill=TEXT_MUTED))
            canvas.tag_bind("back_lbl","<Leave>",    lambda e: canvas.itemconfig("back_lbl",fill=BORDER_DIM))

        draw()
        self._bind_resize(canvas, draw)

    # ══════════════════════════════════════════════
    #  DEX SCREEN  — all 9  Pratemons by type
    # ══════════════════════════════════════════════
    def show_dex_screen(self):
        self.clear()

        frame = tk.Frame(self.root, bg=BG_DARK)
        frame.pack(fill="both", expand=True)

        # Header
        hdr = tk.Frame(frame, bg=BG_CARD)
        hdr.pack(fill="x")
        tk.Label(hdr, text=" Pratemon  DEX",
                 font=("Courier", 20, "bold"),
                 fg="#aa66ff", bg=BG_CARD, pady=8).pack()
        tk.Label(hdr, text="All  Pratemons in the world — own them all!",
                 font=("Courier", 9), fg=TEXT_MUTED, bg=BG_CARD, pady=2).pack()

        # Scrollable body
        body = tk.Frame(frame, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=12, pady=8)

        canvas_dex = tk.Canvas(body, bg=BG_DARK, highlightthickness=0)
        scrollbar  = tk.Scrollbar(body, orient="vertical", command=canvas_dex.yview)
        canvas_dex.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas_dex.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas_dex, bg=BG_DARK)
        inner_win = canvas_dex.create_window((0, 0), window=inner, anchor="nw")

        def on_resize(e):
            canvas_dex.itemconfig(inner_win, width=e.width)
        canvas_dex.bind("<Configure>", on_resize)

        def on_frame_configure(e):
            canvas_dex.configure(scrollregion=canvas_dex.bbox("all"))
        inner.bind("<Configure>", on_frame_configure)

        # Group monsters by type
        type_order = ["Fire 🔥", "Water 💧", "Earth 🌿"]
        type_colors = {"Fire 🔥": "#ff6b35", "Water 💧": "#3ab5e6", "Earth 🌿": "#5ec45e"}

        for typ in type_order:
            mons = [m for m in MONSTERS if m["type"] == typ]

            # Type section header
            sec_hdr = tk.Frame(inner, bg=type_colors[typ], pady=4)
            sec_hdr.pack(fill="x", pady=(10, 2))
            tk.Label(sec_hdr, text=f"  {typ}  TYPE  ({len(mons)}  Pratemons)",
                     font=("Courier", 12, "bold"),
                     fg=BG_DARK, bg=type_colors[typ]).pack(side="left")

            # Card row
            row = tk.Frame(inner, bg=BG_DARK)
            row.pack(fill="x", padx=4, pady=4)

            for m in mons:
                owned = m in self.player_collection
                card  = tk.Frame(row, bg=BG_CARD,
                                 highlightbackground=m["color"] if owned else BORDER_DIM,
                                 highlightthickness=2)
                card.pack(side="left", padx=6, pady=4, ipadx=6, ipady=6)

                # Type badge strip
                badge = tk.Frame(card, bg=m["color"], height=6)
                badge.pack(fill="x")

                # Monster image
                img = self._get_img(m, (180, 180))
                img_lbl = tk.Label(card, image=img, bg=BG_CARD)
                img_lbl.pack(pady=(6, 2))

                # Name
                tk.Label(card, text=m["name"],
                         font=("Courier", 10, "bold"),
                         fg=m["color"], bg=BG_CARD).pack()

                # Owned badge or locked
                if owned:
                    tk.Label(card, text="✔ OWNED",
                             font=("Courier", 8, "bold"),
                             fg=ACCENT_GOLD, bg=BG_CARD).pack()
                else:
                    tk.Label(card, text="? LOCKED",
                             font=("Courier", 8),
                             fg=TEXT_MUTED, bg=BG_CARD).pack()

                # Stats (always visible)
                stats_frame = tk.Frame(card, bg=BG_CARD)
                stats_frame.pack(pady=(4, 2))
                for label, val, col in [("HP",  m["hp"],  ACCENT_CYAN),
                                        ("ATK", m["atk"], ACCENT_RED),
                                        ("SPD", m["spd"], ACCENT_GOLD)]:
                    tk.Label(stats_frame, text=f"{label} {val}",
                             font=("Courier", 8),
                             fg=col, bg=BG_CARD).pack(side="left", padx=3)

               

        # Back button
        tk.Button(frame, text="<- BACK TO HUB",
                  font=("Courier", 10, "bold"),
                  fg=BG_DARK, bg="#aa66ff",
                  activeforeground=BG_DARK, activebackground="#aa66ff",
                  relief="flat", bd=0, cursor="hand2",
                  pady=8,
                  command=self.show_hub).pack(pady=8)

    # ══════════════════════════════════════════════
    #  TEAM SCREEN
    # ══════════════════════════════════════════════
    def show_team_screen(self):
        self.clear()

        frame = tk.Frame(self.root, bg=BG_DARK)
        frame.pack(fill="both", expand=True)

        # Header
        hdr = tk.Frame(frame, bg=BG_CARD)
        hdr.pack(fill="x")
        tk.Label(hdr, text="YOUR  TEAM",
                 font=("Courier", 20, "bold"),
                 fg=ACCENT_CYAN, bg=BG_CARD, pady=10).pack()
        tk.Label(hdr,
                 text="Select 1–3 monsters for your team. Click to add / remove.",
                 font=("Courier", 9), fg=TEXT_MUTED, bg=BG_CARD).pack(pady=(0,8))
        tk.Frame(hdr, bg=ACCENT_CYAN, height=2).pack(fill="x")

        # Body split: available pool (left) | current team (right)
        body = tk.Frame(frame, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=16, pady=10)

        # ── Left: owned monsters pool ──────────────────
        pool_frame = tk.Frame(body, bg=BG_DARK)
        pool_frame.pack(side="left", fill="both", expand=True)
        tk.Label(pool_frame, text="YOUR  PratemonS",
                 font=("Courier", 11, "bold"),
                 fg=ACCENT_GOLD, bg=BG_DARK).pack(pady=(0,6))

        self._team_status_var = tk.StringVar(value="")

        for mon in self.player_collection:
            self._make_team_row(pool_frame, mon)

        # ── Right: current team slots ────────────────
        team_frame = tk.Frame(body, bg=BG_CARD, width=240)
        team_frame.pack(side="right", fill="y", padx=(12,0))
        team_frame.pack_propagate(False)

        tk.Label(team_frame, text="ACTIVE TEAM  (max 3)",
                 font=("Courier", 10, "bold"),
                 fg=ACCENT_CYAN, bg=BG_CARD, pady=8).pack()
        tk.Frame(team_frame, bg=BORDER_DIM, height=1).pack(fill="x", padx=10)

        self._team_slots_frame = tk.Frame(team_frame, bg=BG_CARD)
        self._team_slots_frame.pack(fill="both", expand=True, padx=8, pady=6)
        self._refresh_team_slots()

        tk.Label(team_frame, textvariable=self._team_status_var,
                 font=("Courier", 8), fg=ACCENT_RED, bg=BG_CARD).pack(pady=2)

        # Back button
        tk.Frame(frame, bg=BORDER_DIM, height=1).pack(fill="x")
        tk.Button(frame, text="<- BACK TO HUB",
                  font=("Courier", 11, "bold"),
                  fg=TEXT_MUTED, bg=BG_CARD,
                  activeforeground=TEXT_WHITE, activebackground=BORDER_DIM,
                  relief="flat", bd=0, padx=20, pady=8, cursor="hand2",
                  command=self.show_hub).pack(pady=6)

    def _make_team_row(self, parent, mon):
        in_team = mon in self.player_team

        row_bg = BG_CARD if not in_team else mon["color"]
        row = tk.Frame(parent, bg=row_bg, cursor="hand2")
        row.pack(fill="x", pady=3, padx=4, ipady=4)

        img = self._get_img(mon, (40, 40))
        tk.Label(row, image=img, bg=row_bg, bd=0).pack(side="left", padx=6)

        info = tk.Frame(row, bg=row_bg)
        info.pack(side="left", fill="x", expand=True)
        tk.Label(info, text=mon["name"],
                 font=("Courier", 11, "bold"),
                 fg=BG_DARK if in_team else mon["color"],
                 bg=row_bg).pack(anchor="w")
        tk.Label(info, text=mon["type"],
                 font=("Courier", 8),
                 fg=BG_DARK if in_team else TEXT_MUTED,
                 bg=row_bg).pack(anchor="w")

        badge_text = "IN TEAM" if in_team else "+ ADD"
        badge_col  = BG_DARK   if in_team else ACCENT_CYAN
        tk.Label(row, text=badge_text,
                 font=("Courier", 9, "bold"),
                 fg=badge_col, bg=row_bg,
                 padx=8).pack(side="right", padx=6)

        def toggle(e, m=mon):
            if m in self.player_team:
                if len(self.player_team) == 1:
                    self._team_status_var.set("Team needs at least 1 monster!")
                    return
                self.player_team.remove(m)
            else:
                if len(self.player_team) >= 3:
                    self._team_status_var.set("Team is full! (max 3)")
                    return
                self.player_team.append(m)
            self._team_status_var.set("")
            self.show_team_screen()

        row.bind("<Button-1>", toggle)
        for child in row.winfo_children():
            child.bind("<Button-1>", toggle)

    def _refresh_team_slots(self):
        for w in self._team_slots_frame.winfo_children():
            w.destroy()
        for i in range(3):
            slot_bg = BG_DARK
            slot = tk.Frame(self._team_slots_frame, bg=slot_bg,
                            height=70, relief="flat")
            slot.pack(fill="x", pady=4)
            slot.pack_propagate(False)
            if i < len(self.player_team):
                mon = self.player_team[i]
                tk.Frame(slot, bg=mon["color"], width=4).pack(side="left", fill="y")
                img = self._get_img(mon, (50, 50))
                tk.Label(slot, image=img, bg=slot_bg, bd=0).pack(side="left", padx=6)
                info = tk.Frame(slot, bg=slot_bg)
                info.pack(side="left")
                tk.Label(info, text=mon["name"],
                         font=("Courier", 10, "bold"),
                         fg=mon["color"], bg=slot_bg).pack(anchor="w")
                tk.Label(info, text=mon["type"],
                         font=("Courier", 8),
                         fg=TEXT_MUTED, bg=slot_bg).pack(anchor="w")
                hp_bar = tk.Frame(slot, bg=BORDER_DIM, height=5, width=80)
                hp_bar.pack(side="right", padx=8)
                hp_bar.pack_propagate(False)
                tk.Frame(hp_bar, bg=ACCENT_CYAN, height=5,
                         width=int(80 * mon["hp"] / 110)).place(x=0, y=0)
            else:
                tk.Label(slot, text=f"  Slot {i+1}  —  empty",
                         font=("Courier", 9, "italic"),
                         fg=BORDER_DIM, bg=slot_bg).pack(expand=True)

    # ══════════════════════════════════════════════
    #  HELP SCREEN  (Type chart)
    # ══════════════════════════════════════════════
    def show_help_screen(self):
        self.clear()
        canvas = tk.Canvas(self.root,
                           bg=BG_DARK, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        import math

        def draw():
            canvas.delete("all")
            W, H = self.W(), self.H()
            cx_hdr = W // 2
            fs   = max(14, min(20, W//52))
            fss  = max(8,  min(10, W//100))

            # Header
            hdr_h = int(H*0.10)
            canvas.create_rectangle(0, 0, W, hdr_h, fill=BG_CARD, outline=BORDER_DIM)
            canvas.create_text(cx_hdr, int(hdr_h*0.36), text="TYPE  ADVANTAGE  CHART",
                               font=("Courier", fs, "bold"), fill=ACCENT_GOLD)
            canvas.create_text(cx_hdr, int(hdr_h*0.76), text="Know your strengths — choose wisely in battle!",
                               font=("Courier", fss), fill=TEXT_MUTED)

            # ── Triangle layout ───────────────────────────
            cx, cy = W//2, hdr_h + int((H - hdr_h - int(H*0.22)) * 0.5)
            r = max(90, min(170, int(min(W, H) * 0.22)))

            positions = {
                "Fire":  (cx + int(r * math.sin(math.radians(0))),
                          cy - int(r * math.cos(math.radians(0)))),
                "Earth": (cx + int(r * math.sin(math.radians(120))),
                          cy - int(r * math.cos(math.radians(120)))),
                "Water": (cx + int(r * math.sin(math.radians(240))),
                          cy - int(r * math.cos(math.radians(240)))),
            }
            colors = {"Fire": "#ff6b35", "Earth": "#5ec45e", "Water": "#3ab5e6"}
            symbols = {"Fire": "FIRE", "Earth": "EARTH", "Water": "WATER"}
            icons   = {"Fire": "~F~", "Earth": "~E~", "Water": "~W~"}

            advantages = [
                ("Fire",  "Earth"),
                ("Earth", "Water"),
                ("Water", "Fire"),
            ]
            arrow_colors = ["#ff6b35", "#5ec45e", "#3ab5e6"]
            node_r = max(30, min(52, r//3))

            for (src, dst), acol in zip(advantages, arrow_colors):
                sx, sy = positions[src]
                dx, dy = positions[dst]
                angle = math.atan2(dy - sy, dx - sx)
                ox = int(node_r * math.cos(angle))
                oy = int(node_r * math.sin(angle))
                ax1, ay1 = sx + ox, sy + oy
                ax2, ay2 = dx - ox, dy - oy
                canvas.create_line(ax1, ay1, ax2, ay2,
                                    fill=acol, width=3, arrow=tk.LAST,
                                    arrowshape=(16, 20, 6))
                mx2 = (ax1 + ax2) // 2
                my2 = (ay1 + ay2) // 2
                canvas.create_text(mx2, my2 - 12,
                                   text="STRONG",
                                   font=("Courier", 8, "bold"), fill=acol)
                canvas.create_text(mx2, my2 + 2,
                                   text="AGAINST",
                                   font=("Courier", 8), fill=TEXT_MUTED)

            for elem, (nx, ny) in positions.items():
                col = colors[elem]
                canvas.create_oval(nx-node_r-6, ny-node_r-6,
                                    nx+node_r+6, ny+node_r+6,
                                    fill=col, outline="")
                canvas.create_oval(nx-node_r, ny-node_r,
                                    nx+node_r, ny+node_r,
                                    fill=BG_CARD, outline=col, width=3)
                canvas.create_text(nx, ny - 14,
                                   text=symbols[elem],
                                   font=("Courier", 14, "bold"), fill=col)
                canvas.create_text(nx, ny + 10,
                                   text=icons[elem],
                                   font=("Courier", 11), fill=col)

            # ── Legend text ───────────────────────────────
            legend_y = H - int(H*0.19)
            canvas.create_line(int(W*0.13), legend_y - 10, int(W*0.87), legend_y - 10,
                               fill=BORDER_DIM, width=1)
            canvas.create_text(cx_hdr, legend_y + 5,
                               text="STRONG AGAINST  =  1.5x damage      WEAK AGAINST  =  0.5x damage",
                               font=("Courier", 9, "bold"), fill=ACCENT_GOLD)
            rules = [
                ("Fire",  "Fire beats Earth  (1.5x)  |  Fire vs Water  (0.5x)",  "#ff6b35"),
                ("Earth", "Earth beats Water (1.5x)  |  Earth vs Fire  (0.5x)",  "#5ec45e"),
                ("Water", "Water beats Fire  (1.5x)  |  Water vs Earth (0.5x)",  "#3ab5e6"),
            ]
            for i, (_, txt, col) in enumerate(rules):
                canvas.create_text(cx_hdr, legend_y + 26 + i * 22,
                                   text=txt,
                                   font=("Courier", 9, "bold"), fill=col)

            # Back button
            bw = max(120, min(160, W//7))
            bh = max(24, min(30, H//24))
            self._make_button(canvas, cx_hdr-bw//2, H-int(H*0.058), bw, bh,
                              "<- BACK", TEXT_MUTED, BG_DARK,
                              self.show_hub)

        draw()
        self._bind_resize(canvas, draw)

    # ══════════════════════════════════════════════
    #  BATTLE MAP  — 5 checkpoints
    # ══════════════════════════════════════════════
    # Every boss/trainer below fields one of the 9  Pratemons already
    # defined in MONSTERS above (via _get_monster) — no invented
    # one-off enemies. hp/atk are overridden here to tune difficulty;
    # name/type/image/color all come straight from the real  Pratemon.
    # LINOX's Shadowfang is the one deliberate exception — it's written
    # into the story as an unknown, undocumented creature outside the
    # normal  Pratemon roster.
    CHECKPOINTS = [
        {"name": "Beginnings",  "color": "#ffffff",
         "trainer": "Guard Rex",
         "enemies": [
             dict(_get_monster("Flamora"),   hp=55, atk=40),
         ]},
        {"name": "Tidal Pass",   "color": "#3ab5e6",
         "trainer": "Water Guard",
         "enemies": [
             dict(_get_monster("Aquafin"),   hp=65, atk=48),
             dict(_get_monster("Tidalore"),  hp=72, atk=54),
         ]},
        {"name": "Mossy Hollow", "color": "#5ec45e",
         "trainer": "Grass Guard",
         "enemies": [
             dict(_get_monster("Thornix"),   hp=78, atk=55),
             dict(_get_monster("Mosshog"),   hp=85, atk=60),
         ]},
        {"name": "Ember Ridge",  "color": "#ff6b35",
         "trainer": "Fire Guard",
         "enemies": [
             dict(_get_monster("Pyroclaw"),  hp=88, atk=65),
             dict(_get_monster("Embercage"), hp=95, atk=72),
         ]},
        {"name": "Linox's Lair", "color": "#ff4f6b",
         "trainer": "LINOX",
         "enemies": [
             {"name": "Shadowfang", "type": "Dark", "hp": 140, "atk": 110, "color": "#9933cc",
              "image": "shadowfang.png",
              "dark_reveal": True},
         ]},
    ]

    TYPE_SKILLS = {
        "Fire":  [
            {"name": "Fireball",     "damage": 22, "heal": 0,  "desc": "Hurls a ball of fire!"},
            {"name": "Flamethrow",   "damage": 34, "heal": 0,  "desc": "Breathes a stream of flames!"},
        ],
        "Earth": [
            {"name": "Heal",         "damage": 0,  "heal": 25, "desc": "Restores own HP!"},
            {"name": "Poison Gas",   "damage": 20, "heal": 0,  "desc": "Releases toxic spores!"},
        ],
        "Water": [
            {"name": "Water Blast",  "damage": 26, "heal": 0,  "desc": "Fires a high-pressure jet!"},
            {"name": "Bubble Beam",  "damage": 18, "heal": 0,  "desc": "Launches a rapid bubble volley!"},
        ],
        "Dark":  [
            {"name": "Shadow Strike", "damage": 38, "heal": 0,  "desc": "Strikes from the darkness!"},
            {"name": "Soul Drain",    "damage": 28, "heal": 15, "desc": "Drains the enemy's life force!"},
        ],
    }

    def show_battle_screen(self):
        self.clear()
        canvas = tk.Canvas(self.root, bg=BG_DARK, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        def draw():
            canvas.delete("all")
            self._img_refs.clear()
            W, H = self.W(), self.H()
            cx_w = W//2
            fs  = max(10, min(20, W//52))
            fss = max(7,  min(10, W//100))

            # Header
            canvas.create_rectangle(0,0,W,int(H*0.12), fill=BG_CARD, outline=BORDER_DIM)
            canvas.create_text(cx_w, int(H*0.045), text="JOURNEY  MAP",
                               font=("Courier",fs,"bold"), fill=ACCENT_GOLD)
            canvas.create_text(cx_w, int(H*0.09),
                               text="Choose a checkpoint to battle — reach Linox's Lair!",
                               font=("Courier",fss), fill=TEXT_MUTED)

            # Checkpoint positions scale to window
            pad_x, pad_y = int(W*0.12), int(H*0.17)
            area_w, area_h = W - pad_x*2, int(H*0.70)
            cp_pos = [
                (pad_x + int(area_w*0.06), pad_y + int(area_h*0.80)),
                (pad_x + int(area_w*0.28), pad_y + int(area_h*0.52)),
                (pad_x + int(area_w*0.50), pad_y + int(area_h*0.72)),
                (pad_x + int(area_w*0.72), pad_y + int(area_h*0.36)),
                (pad_x + int(area_w*0.92), pad_y + int(area_h*0.08)),
            ]

            # Path lines
            for i in range(len(cp_pos)-1):
                x1,y1 = cp_pos[i]; x2,y2 = cp_pos[i+1]
                canvas.create_line(x1,y1,x2,y2, fill=BORDER_DIM, width=4, dash=(8,6))
                if i < self.current_checkpoint:
                    canvas.create_line(x1,y1,x2,y2, fill=ACCENT_GOLD, width=3, dash=(8,6))

            r = max(22, min(36, W//28))
            fs_cp  = max(7, min(14, W//80))
            fs_sub = max(6, min(9,  W//110))

            for i,(cp,(cpx,cpy)) in enumerate(zip(self.CHECKPOINTS, cp_pos)):
                col = cp["color"]
                completed = i < self.current_checkpoint
                active    = i == self.current_checkpoint
                locked    = i > self.current_checkpoint

                if active:
                    canvas.create_oval(cpx-r-8,cpy-r-8,cpx+r+8,cpy+r+8,
                                       outline=col, width=2)
                fill_col = col if (completed or active) else BG_CARD
                canvas.create_oval(cpx-r,cpy-r,cpx+r,cpy+r,
                                   fill=fill_col,
                                   outline=col if not locked else BORDER_DIM,
                                   width=3)
                if completed:
                    canvas.create_text(cpx,cpy, text="✓",
                                       font=("Courier",fs_cp,"bold"), fill=BG_DARK)
                else:
                    canvas.create_text(cpx,cpy, text=f"{i+1}",
                                       font=("Courier",fs_cp,"bold"),
                                       fill=BG_DARK if active else (BORDER_DIM if locked else col))

                label_y = cpy + r + 12
                canvas.create_text(cpx, label_y, text=cp["name"],
                                   font=("Courier",fs_sub,"bold"),
                                   fill=col if not locked else BORDER_DIM)
                enemy_label = ", ".join(e["name"] for e in cp["enemies"])
                canvas.create_text(cpx, label_y+13, text=enemy_label,
                                   font=("Courier",max(5,fs_sub-1)),
                                   fill=TEXT_MUTED if not locked else BORDER_DIM)

                if active:
                    tag = f"cp_{i}"
                    canvas.create_oval(cpx-r,cpy-r,cpx+r,cpy+r,
                                       fill="", outline="", tags=tag)
                    canvas.tag_bind(tag,"<Button-1>",
                                    lambda e,idx=i: self.start_checkpoint_battle(idx))
                    canvas.tag_bind(tag,"<Enter>",
                                    lambda e,x=cpx,y=cpy,rr=r,cl=col:
                                        canvas.create_oval(x-rr-4,y-rr-4,x+rr+4,y+rr+4,
                                                           outline=cl,width=2,tags="hover"))
                    canvas.tag_bind(tag,"<Leave>", lambda e: canvas.delete("hover"))
                    canvas.create_text(cpx, label_y+26, text="[ FIGHT! ]",
                                       font=("Courier",max(6,fs_sub),"bold"),
                                       fill=ACCENT_RED, tags=tag)

            # Progress bar
            pb_x, pb_y = int(W*0.1), int(H*0.91)
            pb_w = int(W*0.8)
            canvas.create_rectangle(pb_x,pb_y,pb_x+pb_w,pb_y+16,
                                    fill=BG_CARD, outline=BORDER_DIM)
            prog_w = int(pb_w * self.current_checkpoint / len(self.CHECKPOINTS))
            if prog_w > 0:
                canvas.create_rectangle(pb_x,pb_y,pb_x+prog_w,pb_y+16,
                                        fill=ACCENT_GOLD, outline="")
            canvas.create_text(cx_w, pb_y+8,
                               text=f"Progress: {self.current_checkpoint}/{len(self.CHECKPOINTS)}",
                               font=("Courier",fss,"bold"),
                               fill=BG_DARK if prog_w > pb_w//2 else TEXT_MUTED)

            bw = max(120, min(160, W//7))
            bh = max(20, min(28, H//28))
            self._make_button(canvas, cx_w-bw//2, int(H*0.955), bw, bh,
                              "<- BACK", TEXT_MUTED, BG_DARK, self.show_hub)

        draw()
        self._bind_resize(canvas, draw)

    # ══════════════════════════════════════════════
    #  CHECKPOINT BATTLE
    # ══════════════════════════════════════════════
    def start_checkpoint_battle(self, cp_idx):
        cp = self.CHECKPOINTS[cp_idx]
        if cp_idx == len(self.CHECKPOINTS) - 1:
            # Linox — show dark reveal screen first, then battle
            self._show_linox_intro(cp_idx)
        else:
            enemies = [dict(e, max_hp=e["hp"], hp=e["hp"]) for e in cp["enemies"]]
            self._run_battle(cp_idx, enemies)

    def _show_linox_intro(self, cp_idx):
        """Full-screen dramatic popup shown the moment player clicks FIGHT on Linox."""
        self.clear()
        canvas = tk.Canvas(self.root,
                           bg="#050008", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # Dark aura rings
        for r2, rc in [(220,"#1a0030"),(170,"#2d0050"),(120,"#440070")]:
            canvas.create_oval(380-r2, 290-r2, 380+r2, 290+r2,
                               fill="", outline=rc, width=3)

        # Shadowfang
        self._draw_shadowfang(canvas, 380, 285, 85)

        canvas.create_text(380, 100,
                           text="! ! !  A NEW  Pratemon APPEARS  ! ! !",
                           font=("Courier", 14, "bold"), fill="#cc44ff")
        canvas.create_text(380, 138,
                           text="LINOX unleashes a creature never seen before!",
                           font=("Courier", 10), fill=TEXT_MUTED)
        canvas.create_text(380, 168,
                           text="Its type is... unrecognised.",
                           font=("Courier", 12, "bold"), fill="#aa33ff")
        canvas.create_text(380, 193,
                           text="No data exists for this  Pratemon.",
                           font=("Courier", 10, "italic"), fill=TEXT_MUTED)
        canvas.create_text(380, 218,
                           text="Your attacks may have no effect...",
                           font=("Courier", 10, "italic"), fill=BORDER_DIM)

        canvas.create_text(380, 400,
                           text="S H A D O W F A N G",
                           font=("Courier", 18, "bold"), fill="#cc44ff")
        canvas.create_text(380, 428,
                           text="Type:  Dark",
                           font=("Courier", 11), fill="#9933cc")

        canvas.create_text(380, 530,
                           text="[ TAP ANYWHERE TO BATTLE ]",
                           font=("Courier", 11, "bold"), fill=ACCENT_GOLD,
                           tags="tap")

        # This cinematic is laid out on a fixed 760x580 design canvas —
        # scale it to fit however big the window actually is right now.
        W, H = self.W(), self.H()
        canvas.scale("all", 0, 0, W/760, H/580)

        def _start():
            enemies = [dict(e, max_hp=e["hp"], hp=e["hp"])
                       for e in self.CHECKPOINTS[cp_idx]["enemies"]]
            self._run_linox_battle(cp_idx, enemies)

        canvas.bind("<Button-1>", lambda e: _start())

    def _run_battle(self, cp_idx, enemies):
        self.clear()
        cp = self.CHECKPOINTS[cp_idx]

        # ── State ─────────────────────────────────────
        # Active player monster index (mutable list so closures can write)
        cur_player_idx  = [0]
        cur_enemy_idx   = [0]
        # Per-monster HP tracking for player team
        team_hp = {i: m["hp"] for i, m in enumerate(self.player_team)}

        def active_player():
            return self.player_team[cur_player_idx[0]]

        def active_enemy():
            return enemies[cur_enemy_idx[0]]

        buttons_active = [True]

        canvas = tk.Canvas(self.root,
                           bg=BG_DARK, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        log_var = tk.StringVar(value=f"{cp['trainer']} wants to battle!")
        log_lbl = tk.Label(self.root, textvariable=log_var,
                           font=("Courier", 10, "italic"),
                           fg=ACCENT_GOLD, bg=BG_CARD,
                           wraplength=355, justify="center")
        log_lbl.place(relx=0.49, rely=0.78, relwidth=0.47, relheight=0.047)

        btn_frame   = tk.Frame(self.root, bg=BG_CARD)
        btn_frame.place(relx=0.49, rely=0.825, relwidth=0.47, relheight=0.12)

        sub_frame   = tk.Frame(self.root, bg=BG_CARD)
        sub_frame.place(relx=0.49, rely=0.825, relwidth=0.47, relheight=0.12)
        sub_frame.lower()

        # ── Draw ──────────────────────────────────────
        def draw_arena():
            canvas.delete("arena")
            self._img_refs = [r for r in self._img_refs]
            pm = active_player()
            em = active_enemy()
            p_hp_val = team_hp[cur_player_idx[0]]
            p_max    = pm["hp"]
            e_hp_val = em["hp"]
            e_max    = em["max_hp"]
            W, H = self.W(), self.H()
            cx_w = W//2
            fs_hdr = max(9,  min(12, W//82))
            fs_nm  = max(9,  min(11, W//90))
            fs_sm  = max(6,  min(8,  W//120))
            fs_vs  = max(10, min(13, W//80))

            # Backgrounds
            canvas.create_rectangle(0,0,W,H, fill=BG_DARK, outline="", tags="arena")
            canvas.create_rectangle(0,int(H*0.51),W,int(H*0.77),
                                    fill="#0e1820", outline="", tags="arena")
            canvas.create_line(0,int(H*0.51),W,int(H*0.51),
                               fill=BORDER_DIM, width=1, tags="arena")

            # Header
            hh = int(H*0.09)
            canvas.create_rectangle(0,0,W,hh, fill=BG_CARD, outline=BORDER_DIM, tags="arena")
            en_count = f"({cur_enemy_idx[0]+1}/{len(enemies)})" if len(enemies)>1 else ""
            canvas.create_text(cx_w, int(hh*0.32),
                               text=f"{cp['trainer'].upper()}  wants to battle!  {en_count}",
                               font=("Courier",fs_hdr,"bold"), fill=cp["color"], tags="arena")
            canvas.create_text(cx_w, int(hh*0.72), text=cp["name"],
                               font=("Courier",fs_sm), fill=TEXT_MUTED, tags="arena")

            # Enemy info box (top-right)
            eib_x1,eib_y1 = int(W*0.53), int(H*0.10)
            eib_x2,eib_y2 = int(W*0.97), int(H*0.235)
            canvas.create_rectangle(eib_x1,eib_y1,eib_x2,eib_y2,
                                    fill=BG_CARD, outline=BORDER_DIM, tags="arena")
            ecx = (eib_x1+eib_x2)//2
            canvas.create_text(ecx, eib_y1+14, text=em["name"].upper(),
                               font=("Courier",fs_nm,"bold"), fill=em["color"], tags="arena")
            canvas.create_text(ecx, eib_y1+28, text=f"Type: {em['type']}",
                               font=("Courier",fs_sm), fill=TEXT_MUTED, tags="arena")
            bar_x1,bar_y1 = eib_x1+14, eib_y1+40
            bar_x2,bar_y2 = eib_x2-14, eib_y1+54
            bar_w = bar_x2-bar_x1
            canvas.create_rectangle(bar_x1,bar_y1,bar_x2,bar_y2,
                                    fill=BORDER_DIM, outline="", tags="arena")
            e_fill = max(0, int(bar_w * e_hp_val/e_max))
            canvas.create_rectangle(bar_x1,bar_y1,bar_x1+e_fill,bar_y2,
                                    fill=ACCENT_RED if e_hp_val>e_max*0.3 else "#dd2222",
                                    outline="", tags="arena")
            canvas.create_text(ecx, (bar_y1+bar_y2)//2,
                               text=f"HP  {max(0,e_hp_val)} / {e_max}",
                               font=("Courier",fs_sm,"bold"), fill=TEXT_WHITE, tags="arena")

            # Enemy sprite (top-right area) — real  Pratemon art when the
            # enemy is one of the known MONSTERS (has an "image" key);
            # falls back to the mystery circle for Shadowfang.
            ex = int(W*0.76); ey = int(H*0.4)
            er = max(150, min(120, W//10))
            if em.get("image"):
                ##canvas.create_oval(ex-er-4,ey-er-4,ex+er+4,ey+er+4,
                                  ## fill="", outline=em["color"], width=3, tags="arena")
                eimg = self._get_img(em, (er*2, er*2))
                canvas.create_image(ex, ey, image=eimg, anchor="center", tags="arena")
            else:
                canvas.create_oval(ex-er,ey-er,ex+er,ey+er,
                                   fill=em["color"], outline=BG_DARK, width=3, tags="arena")
                canvas.create_text(ex,ey, text=em["name"][0].upper(),
                                   font=("Courier",max(16,er//2),"bold"),
                                   fill=BG_DARK, tags="arena")

            # Player info box (bottom-left)
            pib_x1,pib_y1 = int(W*0.03), int(H*0.59)
            pib_x2,pib_y2 = int(W*0.50), int(H*0.775)
            canvas.create_rectangle(pib_x1,pib_y1,pib_x2,pib_y2,
                                    fill=BG_CARD, outline=BORDER_DIM, tags="arena")
            pcx = (pib_x1+pib_x2)//2
            canvas.create_text(pcx, pib_y1+14, text=pm["name"].upper(),
                               font=("Courier",fs_nm,"bold"), fill=pm["color"], tags="arena")
            canvas.create_text(pcx, pib_y1+28, text=f"Type: {pm['type']}",
                               font=("Courier",fs_sm), fill=TEXT_MUTED, tags="arena")
            pb_x1,pb_y1 = pib_x1+14, pib_y1+40
            pb_x2,pb_y2 = pib_x2-14, pib_y1+54
            pb_w = pb_x2-pb_x1
            canvas.create_rectangle(pb_x1,pb_y1,pb_x2,pb_y2,
                                    fill=BORDER_DIM, outline="", tags="arena")
            p_fill = max(0, int(pb_w * p_hp_val/p_max))
            canvas.create_rectangle(pb_x1,pb_y1,pb_x1+p_fill,pb_y2,
                                    fill=ACCENT_CYAN if p_hp_val>p_max*0.3 else "#ffaa00",
                                    outline="", tags="arena")
            canvas.create_text(pcx, (pb_y1+pb_y2)//2,
                               text=f"HP  {max(0,p_hp_val)} / {p_max}",
                               font=("Courier",fs_sm,"bold"), fill=TEXT_WHITE, tags="arena")

            # Team mini-icons
            icon_sz = max(28, min(40, W//32))
            for ti,tm in enumerate(self.player_team):
                tx = pib_x1+18 + ti*int(icon_sz*1.4)
                ty = pib_y2-icon_sz//2-6
                icon = self._get_img(tm,(icon_sz,icon_sz))
                canvas.create_image(tx,ty,image=icon,anchor="center",tags="arena")
                if team_hp[ti]<=0:
                    canvas.create_line(tx-icon_sz//2,ty-icon_sz//2,
                                       tx+icon_sz//2,ty+icon_sz//2,
                                       fill=ACCENT_RED,width=2,tags="arena")
                if ti==cur_player_idx[0]:
                    canvas.create_rectangle(tx-icon_sz//2-2,ty-icon_sz//2-2,
                                            tx+icon_sz//2+2,ty+icon_sz//2+2,
                                            outline=pm["color"],width=2,tags="arena")

            # Player sprite (bottom-left)
            px2 = int(W*0.24); py2 = int(H*0.41)
            ps = max(250, min(200, W//10))
            p_img = self._get_img(pm,(ps,ps))
            canvas.create_image(px2,py2,image=p_img,anchor="center",tags="arena")

            # VS badge
            canvas.create_oval(cx_w-28,int(H*0.38),cx_w+28,int(H*0.50),
                               fill=BG_CARD,outline=ACCENT_GOLD,width=2,tags="arena")
            canvas.create_text(cx_w,int(H*0.44),text="VS",
                               font=("Courier",fs_vs,"bold"),fill=ACCENT_GOLD,tags="arena")

            # Action box background
            canvas.create_rectangle(int(W*0.49),int(H*0.78),W-4,H-4,
                                    fill=BG_CARD,outline=BORDER_DIM,tags="arena")

        draw_arena()
        self._bind_resize(canvas, draw_arena)

        # ── Helpers ───────────────────────────────────
        def get_type_key(mon):
            return mon["type"].replace(" 🔥","").replace(" 💧","").replace(" 🌿","").strip()

        def cleanup():
            for w in [log_lbl, btn_frame, sub_frame]:
                try:
                    if w.winfo_exists(): w.destroy()
                except: pass

        # ── Button screens ────────────────────────────
        def show_main_buttons():
            for w in btn_frame.winfo_children(): w.destroy()
            btn_frame.lift()
            moves = [
                ("SCRATCH",      "#cc8844",   do_scratch),
                ("SKILL ATTACK", ACCENT_GOLD, show_skills),
                ("SWITCH",       ACCENT_CYAN, show_switch),
                ("EXIT",         TEXT_MUTED,  do_exit),
            ]
            for i, (label, col, cmd) in enumerate(moves):
                r, c = divmod(i, 2)
                tk.Button(btn_frame, text=label,
                          font=("Courier", 10, "bold"),
                          fg=BG_DARK, bg=col,
                          activeforeground=BG_DARK, activebackground=col,
                          relief="flat", bd=0, cursor="hand2",
                          command=cmd).grid(row=r, column=c, padx=4, pady=4,
                                            sticky="nsew", ipadx=4, ipady=6)
            btn_frame.grid_columnconfigure(0, weight=1)
            btn_frame.grid_columnconfigure(1, weight=1)
            btn_frame.grid_rowconfigure(0, weight=1)
            btn_frame.grid_rowconfigure(1, weight=1)

        def show_skills():
            for w in sub_frame.winfo_children(): w.destroy()
            sub_frame.lift()
            pm = active_player()
            skills = self.TYPE_SKILLS.get(get_type_key(pm), [])
            tk.Label(sub_frame, text=f"{pm['name']} Skills:",
                     font=("Courier", 9, "italic"), fg=TEXT_MUTED, bg=BG_CARD
                     ).grid(row=0, column=0, columnspan=2, pady=(3,1))
            if not skills:
                tk.Label(sub_frame, text="No skills!", font=("Courier",9),
                         fg=ACCENT_RED, bg=BG_CARD).grid(row=1, column=0, columnspan=2)
            else:
                for i, sk in enumerate(skills):
                    lbl = f"{sk['name']}  ({'DMG '+str(sk['damage']) if sk['damage']>0 else 'HEAL '+str(sk['heal'])})"
                    tk.Button(sub_frame, text=lbl,
                              font=("Courier", 9, "bold"),
                              fg=BG_DARK, bg=pm["color"],
                              activeforeground=BG_DARK, activebackground=pm["color"],
                              relief="flat", bd=0, cursor="hand2",
                              command=lambda s=sk: use_skill(s)
                              ).grid(row=i+1, column=0, columnspan=2,
                                     padx=6, pady=3, sticky="ew", ipady=5)
            tk.Button(sub_frame, text="<- BACK", font=("Courier",8),
                      fg=TEXT_MUTED, bg=BG_CARD, relief="flat", bd=0, cursor="hand2",
                      command=show_main_buttons).grid(row=10, column=0, columnspan=2, pady=(1,0))
            sub_frame.grid_columnconfigure(0, weight=1)
            sub_frame.grid_columnconfigure(1, weight=1)

        def show_switch():
            for w in sub_frame.winfo_children(): w.destroy()
            sub_frame.lift()
            available = [(i, m) for i, m in enumerate(self.player_team)
                         if i != cur_player_idx[0] and team_hp[i] > 0]
            tk.Label(sub_frame, text="Switch to:",
                     font=("Courier", 9, "italic"), fg=TEXT_MUTED, bg=BG_CARD
                     ).grid(row=0, column=0, columnspan=2, pady=(3,1))
            if not available:
                tk.Label(sub_frame, text="No other healthy monster!",
                         font=("Courier", 9), fg=ACCENT_RED, bg=BG_CARD
                         ).grid(row=1, column=0, columnspan=2)
            else:
                for row_i, (idx, mon) in enumerate(available):
                    lbl = f"{mon['name']}  ({mon['type'].split()[0]})  HP:{team_hp[idx]}"
                    tk.Button(sub_frame, text=lbl,
                              font=("Courier", 9, "bold"),
                              fg=BG_DARK, bg=mon["color"],
                              activeforeground=BG_DARK, activebackground=mon["color"],
                              relief="flat", bd=0, cursor="hand2",
                              command=lambda i=idx: do_switch_to(i)
                              ).grid(row=row_i+1, column=0, columnspan=2,
                                     padx=6, pady=3, sticky="ew", ipady=5)
            tk.Button(sub_frame, text="<- BACK", font=("Courier",8),
                      fg=TEXT_MUTED, bg=BG_CARD, relief="flat", bd=0, cursor="hand2",
                      command=show_main_buttons).grid(row=10, column=0, columnspan=2, pady=(1,0))
            sub_frame.grid_columnconfigure(0, weight=1)
            sub_frame.grid_columnconfigure(1, weight=1)

        # ── Type chart ────────────────────────────────
        # STRONG_AGAINST[attacker] = defender it beats  → 1.5x damage
        # WEAK_AGAINST[attacker]   = defender it loses  → 0.5x damage
        STRONG_AGAINST = {"Fire": "Earth", "Earth": "Water", "Water": "Fire"}
        WEAK_AGAINST   = {"Fire": "Water", "Earth": "Fire",  "Water": "Earth"}

        def type_modifier(attacker_type, defender_type):
            if STRONG_AGAINST.get(attacker_type) == defender_type:
                return 1.5   # super effective
            if WEAK_AGAINST.get(attacker_type) == defender_type:
                return 0.5   # not very effective
            return 1.0

        def effectiveness_msg(mod):
            if mod > 1: return "  Super effective!"
            if mod < 1: return "  Not very effective..."
            return ""

        # ── Actions ───────────────────────────────────
        def do_scratch():
            if not buttons_active[0]: return
            pm  = active_player()
            em  = active_enemy()
            mod = type_modifier(get_type_key(pm), get_type_key(em))
            base = max(4, pm["atk"] // 5 + random.randint(1, 5))
            dmg  = max(1, int(base * mod))
            em["hp"] -= dmg
            log_var.set(f"{pm['name']} scratches {em['name']}!  -{dmg} HP!{effectiveness_msg(mod)}")
            draw_arena()
            if em["hp"] <= 0:
                on_enemy_fainted(); return
            buttons_active[0] = False
            show_main_buttons()
            canvas.after(900, enemy_turn)

        def use_skill(sk):
            if not buttons_active[0]: return
            pm  = active_player()
            em  = active_enemy()
            if sk["damage"] > 0:
                mod  = type_modifier(get_type_key(pm), get_type_key(em))
                base = sk["damage"] + random.randint(-3, 4)
                dmg  = max(1, int(base * mod))
                em["hp"] -= dmg
                log_var.set(f"{pm['name']} uses {sk['name']}!  -{dmg} HP to {em['name']}!{effectiveness_msg(mod)}")
            else:
                heal = sk["heal"]
                team_hp[cur_player_idx[0]] = min(pm["hp"], team_hp[cur_player_idx[0]] + heal)
                log_var.set(f"{sk['name']}! {pm['name']} recovers {heal} HP!")
            draw_arena()
            show_main_buttons()
            if em["hp"] <= 0:
                on_enemy_fainted(); return
            buttons_active[0] = False
            canvas.after(900, enemy_turn)

        def do_switch_to(idx):
            cur_player_idx[0] = idx
            pm = self.player_team[idx]
            log_var.set(f"Go, {pm['name']}!")
            draw_arena()
            show_main_buttons()
            buttons_active[0] = False
            canvas.after(900, enemy_turn)

        def do_exit():
            cleanup()
            self.show_battle_screen()

        def on_enemy_fainted():
            em = active_enemy()
            log_var.set(f"{em['name']} fainted!")
            next_idx = cur_enemy_idx[0] + 1
            if next_idx < len(enemies):
                cur_enemy_idx[0] = next_idx
                nem = active_enemy()
                draw_arena()
                if nem.get("dark_reveal"):
                    canvas.after(800, lambda: _dark_reveal(nem))
                else:
                    canvas.after(1000, lambda: _next_enemy_intro(nem))
            else:
                canvas.after(600, lambda: battle_over(won=True))

        def _dark_reveal(nem):
            """Full-screen dramatic popup when Linox sends Shadowfang."""
            cleanup()
            canvas.delete("arena")
            canvas.create_rectangle(0, 0, 760, 580, fill="#0a000f", outline="")

            # Pulsing dark aura rings
            for r2, alpha_col in [(200,"#2a004a"),(160,"#3d0066"),(120,"#550088")]:
                canvas.create_oval(380-r2, 290-r2, 380+r2, 290+r2,
                                   fill="", outline=alpha_col, width=3)

            # Shadowfang
            self._draw_shadowfang(canvas, 380, 290, 80)

            canvas.create_text(380, 110,
                               text="! ! !  A NEW  Pratemon APPEARS  ! ! !",
                               font=("Courier", 13, "bold"), fill="#cc44ff")
            canvas.create_text(380, 148,
                               text="LINOX sends out a completely unknown creature!",
                               font=("Courier", 10), fill=TEXT_MUTED)
            canvas.create_text(380, 400,
                               text="Its type is... unrecognised.",
                               font=("Courier", 12, "bold"), fill="#aa33ff")
            canvas.create_text(380, 428,
                               text="No data exists for this  Pratemon.",
                               font=("Courier", 10, "italic"), fill=TEXT_MUTED)
            canvas.create_text(380, 465,
                               text="Your moves may have no effect...",
                               font=("Courier", 10, "italic"), fill=BORDER_DIM)

            def _continue_to_battle():
                self.clear()
                # Rebuild canvas and widgets for battle continuation
                self._run_battle_resume(cp_idx, enemies, cur_enemy_idx[0],
                                        team_hp, cur_player_idx[0])

            canvas.create_text(380, 540, text="[ TAP TO CONTINUE ]",
                               font=("Courier", 10, "bold"), fill=ACCENT_GOLD,
                               tags="tap_cont")
            canvas.tag_bind("tap_cont", "<Button-1>", lambda e: _continue_to_battle())
            canvas.bind("<Button-1>", lambda e: _continue_to_battle())

            # Fixed 760x580 design canvas — scale to the current window size.
            W, H = self.W(), self.H()
            canvas.scale("all", 0, 0, W/760, H/580)

        def _next_enemy_intro(nem):
            log_var.set(f"{cp['trainer']} sends {nem['name']}!")
            draw_arena()
            buttons_active[0] = True
            show_main_buttons()

        def enemy_turn():
            em   = active_enemy()
            pm   = active_player()
            mod  = type_modifier(get_type_key(em), get_type_key(pm))
            skills = self.TYPE_SKILLS.get(get_type_key(em), [])
            if skills and random.random() < 0.70:   # 70% chance to use a skill
                sk = random.choice(skills)
                if sk["damage"] > 0:
                    base = max(2, sk["damage"] // 2 + random.randint(1, 5))
                    dmg  = max(1, int(base * mod))
                    team_hp[cur_player_idx[0]] -= dmg
                    log_var.set(f"{em['name']} uses {sk['name']}!  -{dmg} HP to {pm['name']}!{effectiveness_msg(mod)}")
                else:
                    heal = sk["heal"] // 2
                    em["hp"] = min(em["max_hp"], em["hp"] + heal)
                    log_var.set(f"{em['name']} uses {sk['name']}! +{heal} HP!")
            else:
                base = max(3, em["atk"] // 5 + random.randint(2, 6))
                dmg  = max(1, int(base * mod))
                team_hp[cur_player_idx[0]] -= dmg
                log_var.set(f"{em['name']} scratches {pm['name']}!  -{dmg} HP!{effectiveness_msg(mod)}")
            draw_arena()
            if team_hp[cur_player_idx[0]] <= 0:
                on_player_fainted(); return
            buttons_active[0] = True
            show_main_buttons()

        def on_player_fainted():
            pm = active_player()
            log_var.set(f"{pm['name']} fainted!")
            # Check if any other team member alive
            alive = [i for i, m in enumerate(self.player_team) if team_hp[i] > 0]
            if alive:
                cur_player_idx[0] = alive[0]
                draw_arena()
                canvas.after(900, lambda: _auto_switch_intro())
            else:
                canvas.after(600, lambda: battle_over(won=False))

        def _auto_switch_intro():
            pm = active_player()
            log_var.set(f"{pm['name']} is sent out!")
            draw_arena()
            buttons_active[0] = True
            show_main_buttons()

        def battle_over(won):
            cleanup()
            canvas.delete("arena")
            canvas.create_rectangle(0, 0, 760, 580, fill=BG_DARK, outline="")
            if won:
                canvas.create_text(380, 140, text="VICTORY!",
                                   font=("Courier", 44, "bold"), fill=ACCENT_GOLD)
                canvas.create_text(380, 200,
                                   text=f"You defeated {cp['trainer']}!",
                                   font=("Courier", 14), fill=TEXT_WHITE)

                def give_rewards(reward_list, continue_y=380):
                    """Show reward cards and add monsters to collection/team."""
                    added = []
                    for m in reward_list:
                        if m not in self.player_collection:
                            self.player_collection.append(m)
                            added.append(m)
                        if len(self.player_team) < 3 and m not in self.player_team:
                            self.player_team.append(m)
                    if added:
                        canvas.create_text(380, 245,
                                           text="You received new  Pratemons!",
                                           font=("Courier", 12, "bold"), fill=ACCENT_CYAN)
                        total = len(added)
                        for i, m in enumerate(added):
                            cx2 = (380 - (total-1)*105) + i*210
                            cy2 = 310
                            canvas.create_rectangle(cx2-90, cy2-55, cx2+90, cy2+85,
                                                    fill=BG_CARD, outline=m["color"], width=2)
                            canvas.create_rectangle(cx2-90, cy2-55, cx2+90, cy2-32,
                                                    fill=m["color"], outline="")
                            canvas.create_text(cx2, cy2-43, text=m["type"],
                                               font=("Courier", 8, "bold"), fill=BG_DARK)
                            ri = self._get_img(m, (80, 80))
                            canvas.create_image(cx2, cy2+10, image=ri, anchor="center")
                            canvas.create_text(cx2, cy2+58, text=m["name"],
                                               font=("Courier", 11, "bold"), fill=m["color"])
                            canvas.create_text(cx2, cy2+76,
                                               text=f"HP {m['hp']}  ATK {m['atk']}",
                                               font=("Courier", 8), fill=TEXT_MUTED)
                        for sx, sy in [(130,270),(630,270),(380,260)]:
                            canvas.create_text(sx, sy, text="*",
                                               font=("Courier",14,"bold"), fill=ACCENT_GOLD)
                    self.current_checkpoint = cp_idx + 1
                    self._make_button(canvas, 275, continue_y, 210, 44,
                                      "CONTINUE ->", ACCENT_GOLD, BG_DARK,
                                      self.show_battle_screen)

                if cp_idx == 0:
                    # Reward: 1 starter from each of the other 2 types
                    starter_type = get_type_key(self.player_team[0])
                    rewards = []
                    seen_types = set()
                    for m in MONSTERS:
                        t = get_type_key(m)
                        if m not in self.player_collection and t != starter_type and t not in seen_types:
                            rewards.append(m)
                            seen_types.add(t)
                        if len(rewards) == 2:
                            break
                    give_rewards(rewards, continue_y=468)

                elif cp_idx == 1:
                    # Reward: up to 2 Water monsters not yet owned (2nd + 3rd)
                    water_reward = [m for m in MONSTERS
                                    if get_type_key(m) == "Water"
                                    and m not in self.player_collection]
                    give_rewards(water_reward[:2], continue_y=420)

                elif cp_idx == 2:
                    # Reward: up to 2 Earth monsters not yet owned (2nd + 3rd)
                    earth_reward = [m for m in MONSTERS
                                    if get_type_key(m) == "Earth"
                                    and m not in self.player_collection]
                    give_rewards(earth_reward[:2], continue_y=420)

                elif cp_idx == 3:
                    # Reward: up to 2 Fire monsters not yet owned (2nd + 3rd)
                    fire_reward = [m for m in MONSTERS
                                   if get_type_key(m) == "Fire"
                                   and m not in self.player_collection]
                    give_rewards(fire_reward[:2], continue_y=420)

                elif cp_idx == len(self.CHECKPOINTS) - 1:
                    # Linox battle — player ALWAYS loses (scripted)
                    # Force defeat regardless
                    canvas.delete("all")
                    _linox_defeat_screen()
                    return

                else:
                    self.current_checkpoint = cp_idx + 1
                    nxt = self.CHECKPOINTS[cp_idx + 1]
                    canvas.create_text(380, 260,
                                       text=f"Checkpoint {cp_idx+1} cleared!",
                                       font=("Courier", 12), fill=ACCENT_GOLD)
                    canvas.create_text(380, 285, text=f"Next: {nxt['name']}",
                                       font=("Courier", 11), fill=TEXT_MUTED)
                    self._make_button(canvas, 275, 340, 210, 46,
                                      "CONTINUE ->", ACCENT_GOLD, BG_DARK,
                                      self.show_battle_screen)
            else:
                # Regular defeat (non-Linox)
                if cp_idx == len(self.CHECKPOINTS) - 1:
                    _linox_defeat_screen()
                    return
                canvas.create_text(380, 185, text="DEFEATED...",
                                   font=("Courier", 38, "bold"), fill=ACCENT_RED)
                canvas.create_text(380, 255, text="All your  Pratemons fainted!",
                                   font=("Courier", 14), fill=TEXT_WHITE)
                canvas.create_text(380, 295, text="Train harder and try again!",
                                   font=("Courier", 11), fill=TEXT_MUTED)
                self._make_button(canvas, 275, 370, 210, 46,
                                  "RETRY", ACCENT_RED, BG_DARK,
                                  lambda: self.start_checkpoint_battle(cp_idx))
                self._make_button(canvas, 275, 428, 210, 36,
                                  "<- MAP", TEXT_MUTED, BG_DARK,
                                  self.show_battle_screen)

            # Fixed 760x580 design canvas — scale to the current window size.
            # (Skipped automatically for the Linox branches above, which
            # `return` before reaching here and hand off to their own
            # screen.)
            W, H = self.W(), self.H()
            canvas.scale("all", 0, 0, W/760, H/580)
            # This screen reuses the arena canvas without calling
            # self.clear(), so drop the still-active resize handler that
            # used to redraw the battle arena — re-running it here would
            # redraw the arena on top of this screen, and re-running
            # battle_over() itself isn't safe since it hands out rewards
            # and advances the checkpoint as a side effect.
            if self._resize_after_id:
                self.root.after_cancel(self._resize_after_id)
                self._resize_after_id = None
            self.root.unbind("<Configure>")

        def _linox_defeat_screen():
            """Cinematic screen shown after Linox beats the player."""
            self.clear()
            canvas2 = tk.Canvas(self.root,
                                bg="#050008", highlightthickness=0)
            canvas2.pack(fill="both", expand=True)

            # Dark atmosphere
            for rx, ry, rr, rc in [(120,180,80,"#1a0030"),(640,400,60,"#1a0030"),
                                     (380,520,100,"#0d001a")]:
                canvas2.create_oval(rx-rr, ry-rr, rx+rr, ry+rr,
                                    fill=rc, outline="")

            # LINOX portrait — drop in images/linox.png to use a real image;
            # falls back to the stylised "L" emblem when it's missing.
            linox_img = self._get_char_img("linox.png", (100, 100))
            if linox_img:
                canvas2.create_image(380, 90, image=linox_img, anchor="center")
            else:
                canvas2.create_oval(330, 40, 430, 140,
                                    fill="#220033", outline="#9933cc", width=3)
                canvas2.create_text(380, 90, text="L",
                                    font=("Courier", 42, "bold"), fill="#cc44ff")
            self._draw_shadowfang(canvas2, 620, 100, 52)

            canvas2.create_text(380, 165,
                                text="L I N O X",
                                font=("Courier", 28, "bold"), fill="#cc44ff")
            canvas2.create_text(380, 200,
                                text="— The Shadow Tamer —",
                                font=("Courier", 11, "italic"), fill="#7733aa")

            # Divider
            canvas2.create_line(120, 225, 640, 225, fill="#440066", width=1)

            # Linox speech bubble
            canvas2.create_rectangle(80, 240, 680, 390,
                                     fill="#0d001a", outline="#6600aa", width=2)

            lines = [
                "Ha... you fought well, little trainer.",
                "",
                "But Shadowfang is just the beginning.",
                "",
                '"You failed this time."',
                "",
                "Stop me if you can —",
                "I have MORE  Pratemons yet to unleash.",
                "The world will bow to the Dark type.",
            ]
            for i, line in enumerate(lines):
                col = "#cc44ff" if line.startswith('"') else (
                      ACCENT_GOLD if "Stop me" in line or "MORE" in line else TEXT_WHITE)
                canvas2.create_text(380, 258 + i * 16,
                                    text=line,
                                    font=("Courier", 10, "bold" if col != TEXT_WHITE else "normal"),
                                    fill=col)

            canvas2.create_line(120, 398, 640, 398, fill="#440066", width=1)

            canvas2.create_text(380, 420,
                                text="Your journey isn't over...",
                                font=("Courier", 11, "italic"), fill=TEXT_MUTED)
            canvas2.create_text(380, 448,
                                text="Train. Grow stronger. Find the Dark type's weakness.",
                                font=("Courier", 10), fill=BORDER_DIM)

            self._make_button(canvas2, 250, 490, 260, 46,
                              "BACK TO HUB", "#6600aa", "#050008",
                              self.show_hub)

            # Fixed 760x580 design canvas — scale to the current window size.
            W, H = self.W(), self.H()
            canvas2.scale("all", 0, 0, W/760, H/580)

        show_main_buttons()

    def _run_linox_battle(self, cp_idx, enemies):
        """Dedicated Linox battle — Shadowfang uses Dark skills, player always loses."""
        self.clear()
        cp = self.CHECKPOINTS[cp_idx]

        cur_player_idx = [0]
        team_hp = {i: m["hp"] for i, m in enumerate(self.player_team)}
        buttons_active = [True]
        em = enemies[0]   # Only one enemy: Shadowfang

        DARK_ATTACKS = [
            {"name": "Shadow Strike", "damage": 42},
            {"name": "Soul Drain",    "damage": 32},
            {"name": "Dark Pulse",    "damage": 38},
            {"name": "Nightmare",     "damage": 36},
        ]

        canvas = tk.Canvas(self.root,
                           bg="#050008", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        log_var = tk.StringVar(value="LINOX: Shadowfang, show them darkness!")
        log_lbl = tk.Label(self.root, textvariable=log_var,
                           font=("Courier", 10, "italic"),
                           fg="#cc44ff", bg=BG_CARD,
                           wraplength=355, justify="center")
        log_lbl.place(relx=0.49, rely=0.78, relwidth=0.47, relheight=0.047)

        btn_frame = tk.Frame(self.root, bg=BG_CARD)
        btn_frame.place(relx=0.49, rely=0.825, relwidth=0.47, relheight=0.12)
        sub_frame = tk.Frame(self.root, bg=BG_CARD)
        sub_frame.place(relx=0.49, rely=0.825, relwidth=0.47, relheight=0.12)
        sub_frame.lower()

        def active_player(): return self.player_team[cur_player_idx[0]]
        def get_type_key(mon):
            return mon["type"].replace(" 🔥","").replace(" 💧","").replace(" 🌿","").strip()

        def cleanup():
            for w in [log_lbl, btn_frame, sub_frame]:
                try:
                    if w.winfo_exists(): w.destroy()
                except: pass

        def draw_arena():
            canvas.delete("arena")
            pm = active_player()
            p_hp_val = team_hp[cur_player_idx[0]]
            p_max    = pm["hp"]
            e_hp_val = em["hp"]
            e_max    = em["max_hp"]
            W, H     = self.W(), self.H()
            cx_w     = W // 2
            fs_hdr   = max(9,  min(12, W // 82))
            fs_nm    = max(9,  min(11, W // 90))
            fs_sm    = max(6,  min(8,  W // 120))
            fs_vs    = max(10, min(13, W // 80))

            # Backgrounds
            canvas.create_rectangle(0, 0, W, H,
                                    fill="#050008", outline="", tags="arena")
            canvas.create_rectangle(0, int(H*0.51), W, int(H*0.77),
                                    fill="#0e0018", outline="", tags="arena")
            canvas.create_line(0, int(H*0.51), W, int(H*0.51),
                               fill="#330044", width=1, tags="arena")

            # Header
            hh = int(H * 0.09)
            canvas.create_rectangle(0, 0, W, hh,
                                    fill=BG_CARD, outline=BORDER_DIM, tags="arena")
            canvas.create_text(cx_w, int(hh*0.32),
                               text="LINOX'S LAIR  —  FINAL BATTLE",
                               font=("Courier", fs_hdr, "bold"),
                               fill="#cc44ff", tags="arena")
            canvas.create_text(cx_w, int(hh*0.72),
                               text="The darkness is overwhelming...",
                               font=("Courier", fs_sm, "italic"),
                               fill=TEXT_MUTED, tags="arena")

            # Enemy info box (top-right)
            eib_x1, eib_y1 = int(W*0.53), int(H*0.10)
            eib_x2, eib_y2 = int(W*0.97), int(H*0.235)
            canvas.create_rectangle(eib_x1, eib_y1, eib_x2, eib_y2,
                                    fill=BG_CARD, outline="#550088", tags="arena")
            ecx = (eib_x1 + eib_x2) // 2
            canvas.create_text(ecx, eib_y1+14, text="SHADOWFANG",
                               font=("Courier", fs_nm, "bold"),
                               fill="#cc44ff", tags="arena")
            canvas.create_text(ecx, eib_y1+28,
                               text="Type:  Dark",
                               font=("Courier", fs_sm),
                               fill="#aa55cc", tags="arena")
            bar_x1, bar_y1 = eib_x1+14, eib_y1+40
            bar_x2, bar_y2 = eib_x2-14, eib_y1+54
            bar_w = bar_x2 - bar_x1
            canvas.create_rectangle(bar_x1, bar_y1, bar_x2, bar_y2,
                                    fill=BORDER_DIM, outline="", tags="arena")
            e_fill = max(0, int(bar_w * e_hp_val / e_max))
            canvas.create_rectangle(bar_x1, bar_y1, bar_x1+e_fill, bar_y2,
                                    fill="#9933cc", outline="", tags="arena")
            canvas.create_text(ecx, (bar_y1+bar_y2)//2,
                               text=f"HP  {max(0,e_hp_val)} / {e_max}",
                               font=("Courier", fs_sm, "bold"),
                               fill=TEXT_WHITE, tags="arena")

            # Shadowfang image (top-right)
            ex = int(W*0.76); ey = int(H*0.36)
            er = max(60, min(90, W//12))
            self._draw_shadowfang(canvas, ex, ey, er, tags="arena")

            # Player info box (bottom-left)
            pib_x1, pib_y1 = int(W*0.03), int(H*0.59)
            pib_x2, pib_y2 = int(W*0.50), int(H*0.775)
            canvas.create_rectangle(pib_x1, pib_y1, pib_x2, pib_y2,
                                    fill=BG_CARD, outline=BORDER_DIM, tags="arena")
            pcx = (pib_x1 + pib_x2) // 2
            canvas.create_text(pcx, pib_y1+14, text=pm["name"].upper(),
                               font=("Courier", fs_nm, "bold"),
                               fill=pm["color"], tags="arena")
            canvas.create_text(pcx, pib_y1+28, text=f"Type: {pm['type']}",
                               font=("Courier", fs_sm),
                               fill=TEXT_MUTED, tags="arena")
            pb_x1, pb_y1 = pib_x1+14, pib_y1+40
            pb_x2, pb_y2 = pib_x2-14, pib_y1+54
            pb_w = pb_x2 - pb_x1
            canvas.create_rectangle(pb_x1, pb_y1, pb_x2, pb_y2,
                                    fill=BORDER_DIM, outline="", tags="arena")
            p_fill = max(0, int(pb_w * p_hp_val / p_max))
            canvas.create_rectangle(pb_x1, pb_y1, pb_x1+p_fill, pb_y2,
                                    fill=ACCENT_CYAN if p_hp_val > p_max*0.3 else "#ffaa00",
                                    outline="", tags="arena")
            canvas.create_text(pcx, (pb_y1+pb_y2)//2,
                               text=f"HP  {max(0,p_hp_val)} / {p_max}",
                               font=("Courier", fs_sm, "bold"),
                               fill=TEXT_WHITE, tags="arena")

            # Team mini-icons
            icon_sz = max(28, min(40, W//32))
            for ti, tm in enumerate(self.player_team):
                tx = pib_x1+18 + ti*int(icon_sz*1.4)
                ty = pib_y2 - icon_sz//2 - 6
                icon = self._get_img(tm, (icon_sz, icon_sz))
                canvas.create_image(tx, ty, image=icon, anchor="center", tags="arena")
                if team_hp[ti] <= 0:
                    canvas.create_line(tx-icon_sz//2, ty-icon_sz//2,
                                       tx+icon_sz//2, ty+icon_sz//2,
                                       fill=ACCENT_RED, width=2, tags="arena")
                if ti == cur_player_idx[0]:
                    canvas.create_rectangle(tx-icon_sz//2-2, ty-icon_sz//2-2,
                                            tx+icon_sz//2+2, ty+icon_sz//2+2,
                                            outline=pm["color"], width=2, tags="arena")

            # Player sprite
            ps = max(80, min(130, W//10))
            p_img = self._get_img(pm, (ps, ps))
            canvas.create_image(int(W*0.24), int(H*0.41),
                                image=p_img, anchor="center", tags="arena")

            # VS badge
            canvas.create_oval(cx_w-28, int(H*0.38), cx_w+28, int(H*0.50),
                               fill=BG_CARD, outline="#9933cc", width=2, tags="arena")
            canvas.create_text(cx_w, int(H*0.44), text="VS",
                               font=("Courier", fs_vs, "bold"),
                               fill="#cc44ff", tags="arena")

            # Action box background
            canvas.create_rectangle(int(W*0.49), int(H*0.78), W-4, H-4,
                                    fill=BG_CARD, outline=BORDER_DIM, tags="arena")

        draw_arena()
        self._bind_resize(canvas, draw_arena)

        def show_main_buttons():
            for w in btn_frame.winfo_children(): w.destroy()
            btn_frame.lift()
            moves = [("SCRATCH","#cc8844",do_scratch),
                     ("SKILL ATTACK",ACCENT_GOLD,show_skills),
                     ("SWITCH",ACCENT_CYAN,show_switch),
                     ("EXIT",TEXT_MUTED,do_exit)]
            for i,(label,col,cmd) in enumerate(moves):
                r,c = divmod(i,2)
                tk.Button(btn_frame,text=label,font=("Courier",10,"bold"),
                          fg=BG_DARK,bg=col,activeforeground=BG_DARK,activebackground=col,
                          relief="flat",bd=0,cursor="hand2",command=cmd
                          ).grid(row=r,column=c,padx=4,pady=4,sticky="nsew",ipadx=4,ipady=6)
            btn_frame.grid_columnconfigure(0,weight=1); btn_frame.grid_columnconfigure(1,weight=1)
            btn_frame.grid_rowconfigure(0,weight=1);   btn_frame.grid_rowconfigure(1,weight=1)

        def show_skills():
            for w in sub_frame.winfo_children(): w.destroy()
            sub_frame.lift()
            pm = active_player()
            skills = self.TYPE_SKILLS.get(get_type_key(pm),[])
            tk.Label(sub_frame,text=f"{pm['name']} Skills:",font=("Courier",9,"italic"),
                     fg=TEXT_MUTED,bg=BG_CARD).grid(row=0,column=0,columnspan=2,pady=(3,1))
            for i,sk in enumerate(skills):
                lbl = f"{sk['name']}  ({'DMG '+str(sk['damage']) if sk['damage']>0 else 'HEAL '+str(sk['heal'])})"
                tk.Button(sub_frame,text=lbl,font=("Courier",9,"bold"),
                          fg=BG_DARK,bg=pm["color"],activeforeground=BG_DARK,
                          activebackground=pm["color"],relief="flat",bd=0,cursor="hand2",
                          command=lambda s=sk: use_skill(s)
                          ).grid(row=i+1,column=0,columnspan=2,padx=6,pady=3,sticky="ew",ipady=5)
            tk.Button(sub_frame,text="<- BACK",font=("Courier",8),fg=TEXT_MUTED,bg=BG_CARD,
                      relief="flat",bd=0,cursor="hand2",command=show_main_buttons
                      ).grid(row=10,column=0,columnspan=2,pady=(1,0))
            sub_frame.grid_columnconfigure(0,weight=1); sub_frame.grid_columnconfigure(1,weight=1)

        def show_switch():
            for w in sub_frame.winfo_children(): w.destroy()
            sub_frame.lift()
            available = [(i,m) for i,m in enumerate(self.player_team)
                         if i != cur_player_idx[0] and team_hp[i] > 0]
            tk.Label(sub_frame,text="Switch to:",font=("Courier",9,"italic"),
                     fg=TEXT_MUTED,bg=BG_CARD).grid(row=0,column=0,columnspan=2,pady=(3,1))
            if not available:
                tk.Label(sub_frame,text="No other healthy monster!",font=("Courier",9),
                         fg=ACCENT_RED,bg=BG_CARD).grid(row=1,column=0,columnspan=2)
            else:
                for ri,(idx,mon) in enumerate(available):
                    tk.Button(sub_frame,
                              text=f"{mon['name']}  ({mon['type'].split()[0]})  HP:{team_hp[idx]}",
                              font=("Courier",9,"bold"),fg=BG_DARK,bg=mon["color"],
                              activeforeground=BG_DARK,activebackground=mon["color"],
                              relief="flat",bd=0,cursor="hand2",
                              command=lambda i=idx: do_switch_to(i)
                              ).grid(row=ri+1,column=0,columnspan=2,padx=6,pady=3,sticky="ew",ipady=5)
            tk.Button(sub_frame,text="<- BACK",font=("Courier",8),fg=TEXT_MUTED,bg=BG_CARD,
                      relief="flat",bd=0,cursor="hand2",command=show_main_buttons
                      ).grid(row=10,column=0,columnspan=2,pady=(1,0))
            sub_frame.grid_columnconfigure(0,weight=1); sub_frame.grid_columnconfigure(1,weight=1)

        def do_scratch():
            if not buttons_active[0]: return
            # Player attacks — Shadowfang barely takes damage (it's scripted to win)
            pm = active_player()
            dmg = random.randint(1, 4)   # nearly no effect
            em["hp"] = max(em["max_hp"] // 2, em["hp"] - dmg)  # hp never drops below half
            log_var.set(f"{pm['name']} scratches... it has almost no effect! -{dmg} HP")
            draw_arena()
            buttons_active[0] = False
            show_main_buttons()
            canvas.after(900, shadowfang_attacks)

        def use_skill(sk):
            if not buttons_active[0]: return
            pm = active_player()
            if sk["damage"] > 0:
                dmg = random.randint(2, 6)   # Dark resists everything
                em["hp"] = max(em["max_hp"] // 2, em["hp"] - dmg)
                log_var.set(f"{pm['name']} uses {sk['name']}... Shadowfang barely flinches! -{dmg} HP")
            else:
                heal = sk["heal"]
                team_hp[cur_player_idx[0]] = min(pm["hp"], team_hp[cur_player_idx[0]] + heal)
                log_var.set(f"{sk['name']}! {pm['name']} recovers {heal} HP!")
            draw_arena()
            show_main_buttons()
            buttons_active[0] = False
            canvas.after(900, shadowfang_attacks)

        def do_switch_to(idx):
            cur_player_idx[0] = idx
            pm = self.player_team[idx]
            log_var.set(f"Go, {pm['name']}! (Shadowfang watches coldly...)")
            draw_arena(); show_main_buttons()
            buttons_active[0] = False
            canvas.after(900, shadowfang_attacks)

        def do_exit():
            cleanup(); self.show_battle_screen()

        def shadowfang_attacks():
            """Shadowfang always uses a Dark skill — massive damage."""
            pm = active_player()
            atk = random.choice(DARK_ATTACKS)
            dmg = atk["damage"] + random.randint(5, 15)   # heavy Dark damage
            team_hp[cur_player_idx[0]] -= dmg
            log_var.set(f"Shadowfang uses {atk['name']}!  -{dmg} HP!  The darkness is overwhelming!")
            draw_arena()

            if team_hp[cur_player_idx[0]] <= 0:
                alive = [i for i,m in enumerate(self.player_team) if team_hp[i] > 0]
                if alive:
                    cur_player_idx[0] = alive[0]
                    draw_arena()
                    canvas.after(900, lambda: _auto_faint_next())
                else:
                    canvas.after(800, lambda: _show_linox_taunt())
                return
            buttons_active[0] = True
            show_main_buttons()

        def _auto_faint_next():
            pm = active_player()
            log_var.set(f"{pm['name']} is sent out! But Shadowfang stands unmoved...")
            draw_arena()
            buttons_active[0] = True
            show_main_buttons()

        def _show_linox_taunt():
            cleanup()
            canvas.delete("arena")
            canvas.delete("all")
            canvas.create_rectangle(0,0,760,580, fill="#050008", outline="")
            for rx,ry,rr,rc in [(120,180,80,"#1a0030"),(640,400,60,"#1a0030"),(380,520,100,"#0d001a")]:
                canvas.create_oval(rx-rr,ry-rr,rx+rr,ry+rr, fill=rc, outline="")
            linox_img = self._get_char_img("linox.png", (100, 100))
            if linox_img:
                canvas.create_image(380,90, image=linox_img, anchor="center")
            else:
                canvas.create_oval(330,40,430,140, fill="#220033", outline="#9933cc", width=3)
                canvas.create_text(380,90, text="L", font=("Courier",42,"bold"), fill="#cc44ff")
            self._draw_shadowfang(canvas, 620, 100, 52)
            canvas.create_text(380,165, text="L I N O X",
                               font=("Courier",28,"bold"), fill="#cc44ff")
            canvas.create_text(380,200, text="— The Shadow Tamer —",
                               font=("Courier",11,"italic"), fill="#7733aa")
            canvas.create_line(120,225,640,225, fill="#440066", width=1)
            canvas.create_rectangle(80,240,680,400, fill="#0d001a", outline="#6600aa", width=2)
            lines = [
                "Ha...  pathetic.",
                "",
                "Shadowfang didn't even break a sweat.",
                "",
                '"You failed this time."',
                "",
                "Stop me if you can —",
                "I have MORE  Pratemons yet to unleash.",
                "The world will bow to me.",
            ]
            for i,line in enumerate(lines):
                col = "#cc44ff" if line.startswith('"') else (
                      ACCENT_GOLD if ("Stop me" in line or "MORE" in line) else TEXT_WHITE)
                canvas.create_text(380,258+i*16, text=line,
                                   font=("Courier",10,"bold" if col!=TEXT_WHITE else "normal"),
                                   fill=col)
            canvas.create_line(120,405,640,405, fill="#440066", width=1)
            canvas.create_text(380,425, text="Your journey isn't over...",
                               font=("Courier",11,"italic"), fill=TEXT_MUTED)
            canvas.create_text(380,450,
                               text="Train. Grow stronger. Discover the Dark type's weakness.",
                               font=("Courier",10), fill=BORDER_DIM)
            self._make_button(canvas,250,490,260,46,
                              "BACK TO HUB","#6600aa","#050008", self.show_hub)

            # Fixed 760x580 design canvas — scale to the current window size.
            W, H = self.W(), self.H()
            canvas.scale("all", 0, 0, W/760, H/580)
            # This is a terminal (game-over) screen reusing the battle canvas
            # without calling self.clear(), so re-point the live resize
            # handler at this redraw instead of the old arena redraw —
            # otherwise resizing here would redraw the battle arena on top
            # of this screen.
            self._bind_resize(canvas, _show_linox_taunt)

        show_main_buttons()


# ─── Launch ──────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        from PIL import Image, ImageTk
    except ImportError:
        import tkinter.messagebox as mb
        _r = tk.Tk(); _r.withdraw()
        mb.showerror("Missing library",
                     "Pillow is required for custom images.\n\n"
                     "Install it by running:\n\n"
                     "    pip install Pillow\n\n"
                     "Then restart the game.")
        raise SystemExit

    root = tk.Tk()
    app  =  PratemonsGame(root)
    root.mainloop()
