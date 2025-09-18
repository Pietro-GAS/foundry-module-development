import tkinter as tk
from tkinter import ttk


class ButtonFrame(ttk.Frame):
    def __init__(self, container, target_frame, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.container = container
        self.target_frame = target_frame

        self.__create_widgets()

    def __create_widgets(self):
        options = {"padx": 5, "pady": 5}
        
        setattr(self, "format_button", ttk.Button(self, text="Format"))
        self.format_button["command"] = lambda: self.print_text()
        self.format_button.grid(row=0, column=0, **options)
        
        setattr(self, "format_button", ttk.Button(self, text="Format"))
        self.format_button["command"] = lambda: self.print_text()
        self.format_button.grid(row=0, column=0, **options)
        
        setattr(self, "clean_button", ttk.Button(self, text="Clean"))
        self.clean_button["command"] = lambda: self.clean_text()
        self.clean_button.grid(row=0, column=1, **options)
    
    def copy_text(self):
        """Copy text from the input text field."""
        text = self.target_frame.input_text.get('1.0', tk.END)
        return text
        
    def format(self, text):
        """Fix common formatting errors when copying text from pdf."""
        # replace newline with whitespace
        formatted_text = text.replace("\n", " ")
        # replace double space with single space
        formatted_text = formatted_text.replace("  ", " ")
        # remove spaces at beginning and end
        formatted_text = formatted_text.strip()
        # insert html tags
        formatted_text = f"<p>{formatted_text}</p>"
        return formatted_text
    
    def print_text(self):
        """Copy, format, then print text to output field."""
        text = self.copy_text()
        formatted_text = self.format(text)
        self.target_frame.output_text.delete('1.0', tk.END)
        self.target_frame.output_text.insert('1.0', formatted_text)
    
    def clean_text(self):
        """Apply additional formatting fixes to the output text field."""
        replacements = {
            "  ": " ", 
            " ?": "?", 
            " !": "!", 
            " ,": ",", 
            " ;": ";", 
            " :": ":",
            " .": ".", 
            "\n": " ",
            "<p> ": "<p>", 
            "</p> ": "</p>",
            " <p>": "<p>", 
            " </p>": "</p>"
        }
        text = self.target_frame.output_text.get('1.0', tk.END)

        for i, j in replacements.items():
            text = text.replace(i, j)
        
        self.target_frame.output_text.delete('1.0', tk.END)
        self.target_frame.output_text.insert('1.0', text)



class TextFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.container = container
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        self.__create_widgets()
        self.__create_bindings()

    def paragraph(self):
        """Insert paragraph break at cursor position using html tags."""
        position = self.input_text.index("insert")
        text = "</p><p>"
        self.input_text.insert(position, text)
    
    def __create_widgets(self):
        options = {"padx": 5, "pady": 5}

        setattr(self, "input_text", tk.Text(self, width=40))
        self.input_text.grid(row=0, column=0, **options)

        setattr(self, "output_text", tk.Text(self, width=40))
        self.output_text.grid(row=0, column=1, **options)
    
    def __create_bindings(self):
        """Bind paragrah function to Ctrl+p"""
        self.input_text.bind("<Control_L> p", lambda event: self.paragraph())



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.wm_title("Text formatter")
        #self.geometry("400x540")
        self.resizable(True, True)
        self.minsize(300, 300)
        self.columnconfigure(0, weight=1)

        self.__create_widgets()

    def __create_widgets(self):
        options = {"padx": 10, "pady": 10}

        # create the text frame
        text_frame = TextFrame(self)
        text_frame.grid(column=0, row=1, sticky=tk.NSEW, **options)
        
        # create the button frame
        button_frame = ButtonFrame(self, text_frame)
        button_frame.grid(column=0, row=0, **options)



if __name__ == "__main__":
    app = App()
    app.mainloop()