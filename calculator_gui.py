import tkinter as tk
import math

class CalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("계산기")
        master.configure(bg='#333')

        # Grid-based layout for responsiveness
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=4)
        master.grid_columnconfigure(0, weight=1)

        # Display
        self.display = tk.Entry(master, justify='right', font=('Arial', 40), bd=0, bg='#333', fg='white')
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=20)
        self.display.insert(0, "0")

        # Button Frame
        button_frame = tk.Frame(master, bg='#333')
        button_frame.grid(row=1, column=0, columnspan=4, sticky="nsew")

        buttons = [
            '%', 'CE', 'C', '<',
            '1/x', 'x²', '√x', '/',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '+/-', '0', '.', '='
        ]

        # Configure button frame grid
        for i in range(6):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)

        row_val = 0
        col_val = 0
        for button in buttons:
            self.create_button(button_frame, button, row_val, col_val)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

    def create_button(self, frame, text, row, col):
        bg_color = 'orange' if text == '=' else '#555'
        fg_color = 'white'
        
        b = tk.Button(frame, text=text, font=('Arial', 18), bd=0, bg=bg_color, fg=fg_color,
                      command=lambda t=text: self.button_click(t))
        b.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        return b

    def button_click(self, button):
        current = self.display.get()
        
        if button == 'C' or button == 'CE':
            self.display.delete(0, tk.END)
            self.display.insert(0, "0")
        elif button == '<':
            if len(current) > 1:
                self.display.delete(len(current)-1, tk.END)
            else:
                self.display.delete(0, tk.END)
                self.display.insert(0, "0")
        elif button == '=':
            try:
                current = current.replace('√', 'math.sqrt').replace('x²', '**2').replace('%', '/100')
                result = eval(current)
                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))
            except Exception:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
        elif button == '1/x':
            try:
                result = 1 / float(current)
                self.display.delete(0, tk.END)
                self.display.insert(0, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
        elif button == 'x²':
            try:
                result = float(current) ** 2
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
            except:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
        elif button == '√x':
            try:
                result = math.sqrt(float(current))
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
            except:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
        elif button == '+/-':
            if current.startswith('-'):
                self.display.delete(0)
            elif current != '0':
                self.display.insert(0, '-')
        else:
            if current == "0" and button != '.':
                self.display.delete(0, tk.END)
            self.display.insert(tk.END, button)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("380x600") # Set initial window size
    app = CalculatorApp(root)
    root.mainloop()