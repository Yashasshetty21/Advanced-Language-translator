from tkinter import *
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES
import pyperclip

class LanguageTranslator:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1200x700')
        self.root.resizable(0,0)
        self.root.title("Advanced Language Translator")
        self.root.config(bg='#2C3E50')
        
        # Create a style
        style = ttk.Style()
        style.configure('TButton', padding=8, relief="flat", background="#3498DB", font=('Helvetica', 10, 'bold'))
        style.configure('TCombobox', padding=8, background="#ECF0F1")

        # Main Frame
        main_frame = Frame(root, bg='#2C3E50')
        main_frame.pack(expand=True, fill='both', padx=30, pady=30)

        # Heading
        Label(main_frame, text="ADVANCED LANGUAGE TRANSLATOR", 
              font="Helvetica 28 bold", bg='#2C3E50', fg='#ECF0F1').pack(pady=20)

        # Input/Output Frame
        io_frame = Frame(main_frame, bg='#2C3E50')
        io_frame.pack(fill='both', expand=True)

        # Input Section
        input_frame = Frame(io_frame, bg='#2C3E50')
        input_frame.pack(side=LEFT, expand=True, fill='both', padx=15)
        
        Label(input_frame, text="Source Language:", font='Helvetica 14 bold', bg='#2C3E50', fg='#ECF0F1').pack()
        self.src_lang = ttk.Combobox(input_frame, values=list(LANGUAGES.values()), width=35, font=('Helvetica', 12))
        self.src_lang.pack(pady=10)
        self.src_lang.set('choose input language')

        Label(input_frame, text="Enter Text:", font='Helvetica 14 bold', bg='#2C3E50', fg='#ECF0F1').pack()
        self.Input_text = Text(input_frame, font='Helvetica 12', height=14, wrap=WORD, 
                             padx=10, pady=10, width=50, bg='#ECF0F1')
        self.Input_text.pack(pady=10)

        # Character count for input
        self.input_char_count = Label(input_frame, text="Characters: 0", font='Helvetica 10', 
                                    bg='#2C3E50', fg='#ECF0F1')
        self.input_char_count.pack()
        self.Input_text.bind('<KeyRelease>', self.update_input_char_count)

        # Output Section
        output_frame = Frame(io_frame, bg='#2C3E50')
        output_frame.pack(side=RIGHT, expand=True, fill='both', padx=15)
        
        Label(output_frame, text="Target Language:", font='Helvetica 14 bold', bg='#2C3E50', fg='#ECF0F1').pack()
        self.dest_lang = ttk.Combobox(output_frame, values=list(LANGUAGES.values()), width=35, font=('Helvetica', 12))
        self.dest_lang.pack(pady=10)
        self.dest_lang.set('choose output language')

        Label(output_frame, text="Translation:", font='Helvetica 14 bold', bg='#2C3E50', fg='#ECF0F1').pack()
        self.Output_text = Text(output_frame, font='Helvetica 12', height=14, wrap=WORD, 
                              padx=10, pady=10, width=50, bg='#ECF0F1')
        self.Output_text.pack(pady=10)

        # Character count for output
        self.output_char_count = Label(output_frame, text="Characters: 0", font='Helvetica 10', 
                                     bg='#2C3E50', fg='#ECF0F1')
        self.output_char_count.pack()

        # Buttons Frame
        button_frame = Frame(main_frame, bg='#2C3E50')
        button_frame.pack(pady=20)

        # Buttons with improved styling
        ttk.Button(button_frame, text='Translate', command=self.Translate, 
                  style='Custom.TButton').pack(side=LEFT, padx=10)
        ttk.Button(button_frame, text='Clear', command=self.clear_text, 
                  style='Custom.TButton').pack(side=LEFT, padx=10)
        ttk.Button(button_frame, text='Copy', command=self.copy_text, 
                  style='Custom.TButton').pack(side=LEFT, padx=10)
        ttk.Button(button_frame, text='Swap Languages', command=self.swap_languages, 
                  style='Custom.TButton').pack(side=LEFT, padx=10)

        # Status Bar with improved styling
        self.status_var = StringVar()
        self.status_var.set('Ready')
        Label(main_frame, textvariable=self.status_var, 
              font='Helvetica 11 italic', bg='#2C3E50', fg='#ECF0F1').pack(side=BOTTOM, pady=10)

    def update_input_char_count(self, event=None):
        count = len(self.Input_text.get(1.0, END).strip())
        self.input_char_count.config(text=f"Characters: {count}")

    def update_output_char_count(self):
        count = len(self.Output_text.get(1.0, END).strip())
        self.output_char_count.config(text=f"Characters: {count}")

    def swap_languages(self):
        src = self.src_lang.get()
        dest = self.dest_lang.get()
        self.src_lang.set(dest)
        self.dest_lang.set(src)
        # Swap text content
        src_text = self.Input_text.get(1.0, END).strip()
        dest_text = self.Output_text.get(1.0, END).strip()
        self.Input_text.delete(1.0, END)
        self.Output_text.delete(1.0, END)
        self.Input_text.insert(END, dest_text)
        self.Output_text.insert(END, src_text)
        self.update_input_char_count()
        self.update_output_char_count()

    def Translate(self):
        try:
            self.status_var.set('Translating...')
            self.root.update()
            
            translator = Translator()
            translated = translator.translate(
                text=self.Input_text.get(1.0, END),
                src=self.src_lang.get(),
                dest=self.dest_lang.get()
            )
            
            self.Output_text.delete(1.0, END)
            self.Output_text.insert(END, translated.text)
            self.update_output_char_count()
            
            self.status_var.set('Translation completed!')
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set('Translation failed!')

    def clear_text(self):
        self.Input_text.delete(1.0, END)
        self.Output_text.delete(1.0, END)
        self.update_input_char_count()
        self.update_output_char_count()
        self.status_var.set('Cleared all text')

    def copy_text(self):
        translated_text = self.Output_text.get(1.0, END).strip()
        pyperclip.copy(translated_text)
        self.status_var.set('Text copied to clipboard!')

if __name__ == '__main__':
    root = Tk()
    app = LanguageTranslator(root)
    root.mainloop()
