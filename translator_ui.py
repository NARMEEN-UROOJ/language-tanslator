import tkinter as tk
from tkinter import ttk, scrolledtext
from translator import LanguageTranslator
import pyperclip  # pip install pyperclip

class TranslatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CodeAlpha Language Translator")
        self.root.geometry("800x600")
        self.root.configure(bg="#F5F7FA")
        self.translator = LanguageTranslator()
        
        # Define styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors
        self.bg_color = "#F5F7FA"
        self.primary_color = "#4A90E2"
        self.secondary_color = "#FFFFFF"
        self.text_color = "#333333"
        self.accent_color = "#50C878"
        
        # Main container
        main_frame = tk.Frame(root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Title
        title = tk.Label(main_frame, text="Language Translator", font=("Segoe UI", 24, "bold"), 
                         fg=self.primary_color, bg=self.bg_color)
        title.pack(pady=(0, 20))
        
        # Language selection frame
        lang_frame = tk.LabelFrame(main_frame, text="Language Settings", font=("Segoe UI", 10, "bold"),
                                  bg=self.bg_color, fg=self.text_color, padx=10, pady=10)
        lang_frame.pack(fill=tk.X, pady=10)
        
        # Source language
        tk.Label(lang_frame, text="From:", bg=self.bg_color, font=("Segoe UI", 10)).grid(row=0, column=0, padx=5, sticky="w")
        self.source_lang = ttk.Combobox(lang_frame, values=["Auto Detect"] + list(self.translator.get_language_codes().keys()), width=25)
        self.source_lang.set("Auto Detect")
        self.source_lang.grid(row=0, column=1, padx=15, pady=5)
        
        # Swap Icon (Functional)
        self.swap_label = tk.Label(lang_frame, text=" ⇄ ", bg=self.bg_color, font=("Segoe UI", 16, "bold"), 
                                   fg=self.primary_color, cursor="hand2")
        self.swap_label.grid(row=0, column=2, padx=10)
        self.swap_label.bind("<Button-1>", lambda e: self.swap_languages())
        self.swap_label.bind("<Enter>", lambda e: self.swap_label.config(fg=self.accent_color))
        self.swap_label.bind("<Leave>", lambda e: self.swap_label.config(fg=self.primary_color))
        
        # Target language
        tk.Label(lang_frame, text="To:", bg=self.bg_color, font=("Segoe UI", 10, "bold")).grid(row=0, column=3, padx=5, sticky="w")
        self.target_lang = ttk.Combobox(lang_frame, values=list(self.translator.get_language_codes().keys()), width=25)
        self.target_lang.set("Spanish")
        self.target_lang.grid(row=0, column=4, padx=15, pady=10)
        
        # Input Section
        input_container = tk.Frame(main_frame, bg=self.bg_color)
        input_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(input_container, text="Source Text", bg=self.bg_color, font=("Segoe UI", 11, "bold"), fg="#555555").pack(anchor="w")
        self.input_text = scrolledtext.ScrolledText(input_container, height=5, width=70, font=("Segoe UI", 11), 
                                                   relief=tk.FLAT, borderwidth=0, highlightthickness=2, 
                                                   highlightbackground="#E2E8F0", highlightcolor=self.primary_color)
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=(5, 15))
        
        # Action Buttons Container
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(pady=5)
        
        # Translate button
        self.translate_btn = tk.Button(btn_frame, text="TRANSLATE", command=self.translate, 
                                      bg=self.primary_color, fg="white", font=("Segoe UI", 12, "bold"),
                                      padx=40, pady=12, relief=tk.FLAT, cursor="hand2", 
                                      activebackground="#357ABD", activeforeground="white")
        self.translate_btn.pack(side=tk.LEFT, padx=10)
        # Add hover effect
        self.translate_btn.bind("<Enter>", lambda e: self.translate_btn.config(bg="#357ABD"))
        self.translate_btn.bind("<Leave>", lambda e: self.translate_btn.config(bg=self.primary_color))
        
        # Output Section
        output_container = tk.Frame(main_frame, bg=self.bg_color)
        output_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(output_container, text="Translation Result", bg=self.bg_color, font=("Segoe UI", 11, "bold"), fg="#555555").pack(anchor="w")
        self.output_text = scrolledtext.ScrolledText(output_container, height=5, width=70, font=("Segoe UI", 11), 
                                                    state='disabled', relief=tk.FLAT, borderwidth=0, 
                                                    highlightthickness=2, highlightbackground="#E2E8F0", bg="#F1F5F9")
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Footer Action Buttons
        footer_btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        footer_btn_frame.pack(pady=15)
        
        # Copy button
        self.copy_btn = tk.Button(footer_btn_frame, text="Copy Result", command=self.copy_translation, 
                                 bg=self.accent_color, fg="white", font=("Segoe UI", 10, "bold"),
                                 padx=20, pady=8, relief=tk.FLAT, cursor="hand2")
        self.copy_btn.pack(side=tk.LEFT, padx=10)
        self.copy_btn.bind("<Enter>", lambda e: self.copy_btn.config(bg="#3DAE60"))
        self.copy_btn.bind("<Leave>", lambda e: self.copy_btn.config(bg=self.accent_color))
        
        # Clear button
        self.clear_btn = tk.Button(footer_btn_frame, text="Clear", command=self.clear_fields, 
                                  bg="#94A3B8", fg="white", font=("Segoe UI", 10, "bold"),
                                  padx=20, pady=8, relief=tk.FLAT, cursor="hand2")
        self.clear_btn.pack(side=tk.LEFT, padx=10)
        self.clear_btn.bind("<Enter>", lambda e: self.clear_btn.config(bg="#64748B"))
        self.clear_btn.bind("<Leave>", lambda e: self.clear_btn.config(bg="#94A3B8"))

    def swap_languages(self):
        s = self.source_lang.get()
        t = self.target_lang.get()
        if s != "Auto Detect":
            self.source_lang.set(t)
            self.target_lang.set(s)
        else:
            # If auto-detect is on, maybe just set target to English or something 
            # or do nothing. Let's just swap if they are both specific.
            pass

    def clear_fields(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state='normal')
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state='disabled')
    
    def translate(self):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            return
        
        lang_codes = self.translator.get_language_codes()
        source = 'auto' if self.source_lang.get() == "Auto Detect" else lang_codes.get(self.source_lang.get(), 'auto')
        target = lang_codes.get(self.target_lang.get(), 'en')
        
        result = self.translator.translate_text(text, source, target)
        
        self.output_text.config(state='normal')
        self.output_text.delete("1.0", tk.END)
        
        if 'error' in result:
            self.output_text.insert(tk.END, f"Error: {result['error']}")
        else:
            self.output_text.insert(tk.END, result['translated_text'])
        
        self.output_text.config(state='disabled')
    
    def copy_translation(self):
        translation = self.output_text.get("1.0", tk.END).strip()
        pyperclip.copy(translation)

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorUI(root)
    root.mainloop()