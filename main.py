import tkinter as tk
from tkinter import ttk

# Create main window
root = tk.Tk()
root.title("Tkinter Containers Example")
root.geometry("1000x600")

style = ttk.Style()
style.configure("My.TFrame", borderwidth=2, relief="solid")
style.configure("Border.TLabel", padding=5, borderwidth=2, relief="solid")

#--------------FRAME 1--------------
frame1 = ttk.Frame(root, padding="10", style="My.TFrame")
frame1.pack(fill="both", pady=10,side="left", expand=True)

label1 =  ttk.Label(frame1, text="This is a frame with padding",style="Border.TLabel")
label1.pack(pady=10)
label2 = ttk.Label(frame1, text="It contains labels and buttons",style="Border.TLabel")
label2.pack(pady=10)

#--------------FRAME 2--------------
frame2 = ttk.Frame(root, padding="10", style="My.TFrame")
frame2.pack(fill="both", pady=10, side="right",expand=True)  

label1 =  ttk.Label(frame2, text="This is a frame with padding",style="Border.TLabel")
label1.pack(pady=10)
label2 = ttk.Label(frame2, text="It contains labels and buttons",style="Border.TLabel")
label2.pack(pady=10)

# Start the main event loop
root.mainloop()
