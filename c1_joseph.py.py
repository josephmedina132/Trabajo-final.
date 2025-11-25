import tkinter as tk

OPS = set("+-*/")

def agregar(ch):
    s = var.get()
    if s == "0" and ch.isdigit():
        var.set(ch); return
    if ch in OPS:
        while len(s) > 0 and s[-1] in OPS:
            s = s[:-1]
        if len(s) == 0 and ch != "-":
            return
        var.set(s + ch); return
    if ch == ".":
        i = len(s) - 1
        found = False
        while i >= 0 and s[i] not in OPS:
            if s[i] == ".": found = True; break
            i -= 1
        if found: return
    if ch.isdigit():
        i = len(s) - 1
        while i >= 0 and s[i] not in OPS:
            i -= 1
        num = s[i+1:]
        if num == "0":
            s = s[:i+1]
            var.set(s + ch)
            return
    var.set(s + ch)

def limpiar():
    var.set("0")

def borrar():
    s = var.get()
    if len(s) <= 1:
        var.set("0")
    else:
        var.set(s[:-1])

def igual():
    expr = var.get()
    if len(expr) == 0 or expr[-1] in OPS:
        return
    for ch in expr:
        if not (ch.isdigit() or ch in OPS or ch == "."):
            var.set("0"); return
    try:
        r = eval(expr)
        var.set(f"{r:.10g}")
    except:
        var.set("0")

root = tk.Tk()
root.title("Calculadora")
root.resizable(False, False)
var = tk.StringVar(value="0")
entry = tk.Entry(root, textvariable=var, justify="right", font=("Segoe UI",18))
entry.grid(row=0, column=0, columnspan=4, padx=6, pady=6, sticky="nsew")

buttons = [
    ("7", lambda: agregar("7")), ("8", lambda: agregar("8")), ("9", lambda: agregar("9")), ("/", lambda: agregar("/")),
    ("4", lambda: agregar("4")), ("5", lambda: agregar("5")), ("6", lambda: agregar("6")), ("*", lambda: agregar("*")),
    ("1", lambda: agregar("1")), ("2", lambda: agregar("2")), ("3", lambda: agregar("3")), ("-", lambda: agregar("-")),
    ("0", lambda: agregar("0")), (".", lambda: agregar(".")), ("AC", limpiar), ("+", lambda: agregar("+")),
    ("⌫", borrar), ("=", igual)
]

r, c = 1, 0
for t, cmd in buttons:
    b = tk.Button(root, text=t, command=cmd, font=("Segoe UI",14), width=5, height=2)
    b.grid(row=r, column=c, padx=3, pady=3, sticky="nsew")
    c += 1
    if c == 4:
        r += 1
        c = 0

for i in range(r+1):
    root.grid_rowconfigure(i, weight=1)
for j in range(4):
    root.grid_columnconfigure(j, weight=1)

def on_key(e):
    k = e.keysym
    ch = e.char
    if ch in "0123456789+-*/.":
        agregar(ch)
    elif k in ("Return", "KP_Enter"):
        igual()
    elif k == "BackSpace":
        borrar()
    elif k == "Escape":
        limpiar()

root.bind("<Key>", on_key)
entry.focus()
root.mainloop()
