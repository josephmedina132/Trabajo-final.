import tkinter as tk
from tkinter import ttk, messagebox
import calendar, datetime as dt

# -------- lógica simple --------
def estado_dia(d, ini, fin, trab, desc):
    if d < ini or d > fin: return "X"           # fuera de rango
    ciclo = trab + desc
    return "T" if ((d - ini) % ciclo) < trab else "D"

# -------- GUI --------
root = tk.Tk(); root.title("Planificador de turnos")

frm = ttk.Frame(root, padding=6); frm.grid()

# Entradas básicas
ttk.Label(frm, text="Mes").grid(row=0, column=0);  ent_mes = ttk.Entry(frm, width=4);  ent_mes.grid(row=0, column=1)
ttk.Label(frm, text="Año").grid(row=0, column=2);  ent_a  = ttk.Entry(frm, width=6);  ent_a.grid(row=0, column=3)
hoy = dt.date.today(); ent_mes.insert(0, hoy.month); ent_a.insert(0, hoy.year)

ttk.Label(frm, text="Modalidad").grid(row=1, column=0)
modo = tk.StringVar(value="4x4")
ttk.OptionMenu(frm, modo, "4x4", "4x4", "7x7", "14x14", "Personalizado").grid(row=1, column=1, columnspan=3, sticky="we")

ttk.Label(frm, text="Trabajo").grid(row=2, column=0); ent_t = ttk.Entry(frm, width=4); ent_t.insert(0,"4"); ent_t.grid(row=2, column=1)
ttk.Label(frm, text="Descanso").grid(row=2, column=2); ent_d = ttk.Entry(frm, width=4); ent_d.insert(0,"4"); ent_d.grid(row=2, column=3)

ttk.Label(frm, text="Inicio").grid(row=3, column=0);  ent_i = ttk.Entry(frm, width=4); ent_i.insert(0,"1"); ent_i.grid(row=3, column=1)
ttk.Label(frm, text="Término (0=fin)").grid(row=3, column=2); ent_f = ttk.Entry(frm, width=4); ent_f.insert(0,"0"); ent_f.grid(row=3, column=3)

# Calendario (6x7 etiquetas)
dias = ["Lun","Mar","Mié","Jue","Vie","Sáb","Dom"]
for c,n in enumerate(dias): ttk.Label(frm, text=n, width=6).grid(row=5, column=c)
celdas = [[tk.Label(frm, width=6, height=2, relief="ridge") for c in range(7)] for r in range(6)]
for r in range(6):
    for c in range(7): celdas[r][c].grid(row=6+r, column=c, padx=1, pady=1)

def aplicar_modo():
    if modo.get() != "Personalizado":
        t, d = map(int, modo.get().split("x")); ent_t.delete(0, tk.END); ent_t.insert(0, t)
        ent_d.delete(0, tk.END); ent_d.insert(0, d)

def generar():
    try:
        m, a = int(ent_mes.get()), int(ent_a.get())
        t, d = int(ent_t.get()), int(ent_d.get()); 
        _, ultimo = calendar.monthrange(a, m)
        i = int(ent_i.get()); f = int(ent_f.get()) or ultimo
        if not(1<=m<=12 and 1900<=a<=2100 and 1<=i<=ultimo and i<=f<=ultimo and t>0 and d>=0):
            raise ValueError
    except:
        return messagebox.showerror("Error", "Verifica tus datos.")
    aplicar_modo()
    mat = calendar.monthcalendar(a, m)  # semanas x 7
    for r in range(6):
        for c in range(7):
            dia = mat[r][c]
            lbl = celdas[r][c]
            if dia==0:
                lbl.config(text="", bg="white"); continue
            est = estado_dia(dia, i, f, int(ent_t.get()), int(ent_d.get()))
            bg = "lightgreen" if est=="T" else ("salmon" if est=="D" else "lightgray")
            lbl.config(text=str(dia), bg=bg)

def limpiar():
    for r in celdas:
        for lbl in r: lbl.config(text="", bg="white")

# Botones
ttk.Button(frm, text="Generar", command=generar).grid(row=4, column=0, columnspan=2, sticky="we", pady=4)
ttk.Button(frm, text="Limpiar",  command=limpiar ).grid(row=4, column=2, columnspan=2, sticky="we", pady=4)

root.mainloop()
