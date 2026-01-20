import customtkinter as ctk
import random

# --- Configuration ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- The Master List (85 Bilingual Items) ---
men = [
    "Adam / आदम", "Noah / नूह", "Abraham / अब्राहम", "Isaac / इसहाक", "Jacob / याकूब", 
    "Joseph / यूसुफ", "Moses / मूसा", "Aaron / हारून", "Joshua / यहोशू", "Samuel / शमूएल", 
    "David / दाऊद", "Solomon / सुलेमान", "Elijah / एलिय्याह", "Elisha / एलीशा", 
    "Isaiah / यशायाह", "Jeremiah / यिर्मयाह", "Daniel / दानिय्येल", "Peter / पतरस", 
    "Paul / पौलुस", "John / यूहन्ना", "Matthew / मत्ती"
]

women = [
    "Eve / हव्वा", "Sarah / सारा", "Rebekah / रिबका", "Rachel / राहेल", "Leah / लिआ", 
    "Miriam / मरियम", "Deborah / दबोरा", "Ruth / रूत", "Hannah / हन्ना", "Esther / एस्तेर", 
    "Mary (Mother) / मरियम (माता)", "Martha / मार्था", "Mary Magdalene / मरियम मगदलीनी", 
    "Elizabeth / इलीशिबा", "Priscilla / प्रिस्किला", "Dorcas / दौरकास", "Lydia / लुदिया", 
    "Naomi / नाओमी", "Rahab / राहाब", "Bathsheba / बतशेबा", "Jezebel / ईजेबेल"
]

places = [
    "Jerusalem / यरूशलेम", "Bethlehem / बेतलेहेम", "Nazareth / नासरत", "Jericho / यरीहो", 
    "Capernaum / कफरनहूम", "Bethany / बैतनिया", "Antioch / अन्ताकिया", "Damascus / दमिश्क", 
    "Ephesus / इफिसुस", "Corinth / कुरिन्थ", "Rome / रोम", "Babylon / बाबुल", 
    "Nineveh / नीनवे", "Eden / अदन", "Sodom / सदोम", "Canaan / कनान", "Egypt / मिस्र", 
    "Galilee / गलील", "Judea / यहूदिया", "Samaria / सामरिया", "Gethsemane / गतसमनी"
]

nature = [
    "Mt. Sinai / सीनै पर्वत", "Mt. Zion / सिय्योन पर्वत", "Mt. Carmel / कर्मेल पर्वत", 
    "Mt. Nebo / नबो पर्वत", "Mt. Ararat / अरारात पर्वत", "Mt. Hermon / हेर्मोन पर्वत", 
    "Mt. Olives / जैतून पर्वत", "Mt. Tabor / ताबोर पर्वत", "Mt. Moriah / मोरिय्याह पर्वत", 
    "Jordan River / यरदन नदी", "Nile River / नील नदी", "Euphrates / फरात नदी", 
    "Tigris / हिद्देकेल नदी", "Sea of Galilee / गलील की झील", "Red Sea / लाल समुद्र", 
    "Dead Sea / मृत सागर", "Brook Kidron / किद्रोन नाला", "River Jabbok / यब्बोक नदी", 
    "Mt. Ebal / एबाल पर्वत", "Mt. Gerizim / गरिज्जीम पर्वत", "Mt. Gilboa / गिलबो पर्वत", 
    "River Chebar / कबार नदी"
]

MASTER_LIST = men + women + places + nature

class HousieCallerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Biblical Housie Caller")
        self.geometry("900x700")
        
        # KEYBOARD BINDINGS ADDED HERE
        # <space> calls pick_next, <Tab> calls open_history_window
        self.bind('<space>', self.pick_next)
        self.bind('<Tab>', self.open_history_window)
        
        # Game State Initialization
        self.remaining_names = list(MASTER_LIST)
        self.called_names = []
        random.shuffle(self.remaining_names) 

        # --- Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) 

        # 1. Header Frame
        self.header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a1a1a")
        self.header_frame.grid(row=0, column=0, sticky="ew", ipady=15)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="BIBLICAL HOUSIE NIGHT", 
            font=("Roboto Medium", 24),
            text_color="#3B8ED0"
        )
        self.title_label.pack()

        # 2. Main Display Area
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        # Counter
        self.counter_label = ctk.CTkLabel(
            self.main_frame, 
            text="Calls: 0 / 85", 
            font=("Arial", 16),
            text_color="gray"
        )
        self.counter_label.pack(pady=(10, 5))

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self.main_frame, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(0, 30))

        # The BIG Name Label
        self.current_name_label = ctk.CTkLabel(
            self.main_frame, 
            text="READY?", 
            font=("Arial", 48, "bold"),
            text_color="#ffffff",
            wraplength=800
        )
        self.current_name_label.pack(pady=20)

        # Previous Call Indicator
        self.prev_label = ctk.CTkLabel(
            self.main_frame, 
            text="Last Call: ---", 
            font=("Arial", 18, "italic"),
            text_color="#a0a0a0"
        )
        self.prev_label.pack(pady=(20, 10))

        # 3. Control Buttons Area
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, pady=30)

        # History Button (Mapped to TAB)
        self.btn_history = ctk.CTkButton(
            self.button_frame, 
            text="View History (Tab)", 
            command=self.open_history_window,
            width=150,
            height=50,
            fg_color="#555555",
            hover_color="#333333",
            font=("Arial", 14)
        )
        self.btn_history.grid(row=0, column=0, padx=20)

        # Next Button (Mapped to SPACE)
        self.btn_next = ctk.CTkButton(
            self.button_frame, 
            text="PICK NEXT (Space)", 
            command=self.pick_next,
            width=250,
            height=60,
            font=("Arial", 20, "bold"),
            fg_color="#2CC985",
            hover_color="#228B5E"
        )
        self.btn_next.grid(row=0, column=1, padx=20)

        # Reset Button
        self.btn_reset = ctk.CTkButton(
            self.button_frame, 
            text="RESET GAME", 
            command=self.reset_game,
            width=150,
            height=50,
            fg_color="#E74C3C",  
            hover_color="#C0392B",
            font=("Arial", 14, "bold")
        )
        self.btn_reset.grid(row=0, column=2, padx=20)

        # 4. Footer
        self.footer_label = ctk.CTkLabel(
            self, 
            text="Developed by Yash Soloman& Shaan Jashwant", 
            font=("Courier New", 12),
            text_color="#666666"
        )
        self.footer_label.grid(row=3, column=0, pady=10)
        
        # Give focus to main window so keyboard works immediately
        self.focus_force()

    def pick_next(self, event=None):
        # 'event=None' allows this to be called by button click OR keyboard press
        
        # Check if game is over
        if not self.remaining_names:
            self.current_name_label.configure(text="GAME OVER", text_color="#FF5555")
            self.prev_label.configure(text="All 85 names have been called.")
            return

        # Update History Label
        if self.called_names:
            self.prev_label.configure(text=f"Last Call: {self.called_names[-1]}")

        # Logic
        name = self.remaining_names.pop()
        self.called_names.append(name)

        # Update UI
        self.current_name_label.configure(text=name, text_color="#ffffff")
        
        # Update Stats
        count = len(self.called_names)
        self.counter_label.configure(text=f"Calls: {count} / 85")
        self.progress_bar.set(count / 85)

    def reset_game(self):
        # Reset logic
        self.remaining_names = list(MASTER_LIST)
        self.called_names = []
        random.shuffle(self.remaining_names)

        # Reset UI
        self.current_name_label.configure(text="READY?", text_color="#ffffff")
        self.prev_label.configure(text="Last Call: ---")
        self.counter_label.configure(text="Calls: 0 / 85")
        self.progress_bar.set(0)

    def open_history_window(self, event=None):
        # 'event=None' allows this to be called by button click OR keyboard press
        
        # Create a new top-level window
        history_window = ctk.CTkToplevel(self)
        history_window.title("Called Names History")
        history_window.geometry("500x600")
        history_window.attributes('-topmost', True)
        
        # Header
        ctk.CTkLabel(
            history_window, 
            text="Call Log (Chronological)", 
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # Scrollable Frame
        scroll_frame = ctk.CTkScrollableFrame(history_window, fg_color="transparent")
        scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

        if not self.called_names:
            ctk.CTkLabel(scroll_frame, text="No names called yet.", font=("Arial", 14), text_color="gray").pack(pady=20)
        else:
            for idx, name in enumerate(self.called_names, 1):
                row = ctk.CTkFrame(scroll_frame, fg_color="#2a2a2a", corner_radius=5)
                row.pack(fill="x", pady=5, padx=5)
                
                ctk.CTkLabel(
                    row, 
                    text=f"{idx}.", 
                    width=30,
                    font=("Arial", 12, "bold"),
                    text_color="#2CC985"
                ).pack(side="left", padx=(10, 5), pady=8)
                
                ctk.CTkLabel(
                    row, 
                    text=name, 
                    anchor="w",
                    font=("Arial", 12)
                ).pack(side="left", padx=5, pady=8, fill="x", expand=True)

if __name__ == "__main__":
    app = HousieCallerApp()
    app.mainloop()