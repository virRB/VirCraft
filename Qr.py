import VirGPT
import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
import os
import Wierdness

root = tk.Tk()
root.title('Vir Craft')
root.withdraw()

wierdest = 0
wierdest_word = ""

if os.path.exists("name.txt"):
    with open("name.txt", "r") as f:
        content = f.read()
        if content:
            name = content
        else:

            name = simpledialog.askstring(
                "Username",
                "Enter your username:"
            )
            with open("name.txt", "w") as f:
                f.write(name)


root.deiconify()

def view_board():
    with open("Wierdness.txt", "r") as f:
        content = f.read()
        if content:
            messagebox.showinfo('Wierdest', content)
        else:
            messagebox.showinfo('Wierdest', 'Nothing to display')



if not os.path.exists("save.txt"):
    with open("save.txt", "w") as f:
        f.write("")
 
with open("save.txt", "r") as f:
    save = f.read()

if save:
    items = save.split(', ')
else:
    items = ['water', 'fire', 'plant', 'earth']

system_instruction = " only return one word, and do not explain why you chose the word. return ONLY the word - make it memey and funny - but it should still make sense. ONLY ONE WORD. IF you wish to make a small phrase use dashes example: Hello-world. They should also be real words, not random lexicon slang"

entry = tk.Entry(root)
entry.pack()

menu = tk.Menu(root, tearoff=0)
item1 = ""
item2 = ""
isFuse = False

menu.add_command(label='View your best', command=view_board)

def say(text):
    status.config(text=text)


def reset():
    button.config(state='normal')

def ai_ify(a, b):
    global system_instruction
    result = VirGPT.askAI(f'{a} + {b}, {system_instruction}')
    result = result.replace(",", "")
    if not (result in items):
        give(result)
        say(f'NEW ITEM: {result}')
    else:
        print('You already have this item')
    reset()


def ai_worker(a, b):
    button.config(state='disabled')
    ai_ify(a, b)

def send(item):
    global item1, item2, isFuse
    if not (item in items):
        print('You do not have this')
        entry.delete(0, tk.END)
        return
    if not item1:
        item1 = item
        fusion.config(text=item1)
        print(item1)
    elif not item2:
        item2 = item
        fusion.config(text=f"{item1} + {item2}")
        print(item2)
        button.config(text='Fuse!')
        isFuse = True
    entry.delete(0, tk.END)


def clear():
    global item1, item2
    fusion.config(text="Nothing selected")
    item1 = ""
    item2 = ""

def handle():
    global isFuse, item1, item2
    if not isFuse:
        send(entry.get())
    elif isFuse:
        button.config(text='Send')
        isFuse = False
        threading.Thread(target=ai_worker, args=(item1, item2)).start()
        clear()

def give(item):
    if item == 'Lol error':
        item = 'Secret'
    wierdness = Wierdness.test(item)
    global items, name, wierdest, wierdest_word
    items.append(item)
    with open("save.txt", "w") as f:
        f.write(", ".join(items))
    if wierdness > wierdest:
        wierdest = wierdness
        wierdest_word = item
        if os.path.exists("Wierdest.txt"):
            with open("Wierdness.txt", "w") as f:
                f.write(f'{item}, Wierdness: {wierdness}')
    menu.add_command(label=item)

for item in items:
    menu.add_command(label=item)

def popup(event):
    menu.post(event.x_root, event.y_root)


button = tk.Button(root, text='Send', command=handle)
button.pack()


status = tk.Label(root, text='Start Creating...')
status.pack()

fusion = tk.Label(root, text="Nothing selected")
fusion.pack()

root.bind("<Button-3>", popup)


root.bind("<Return>", lambda event: handle())


root.mainloop()