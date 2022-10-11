import tkinter as tk
import numpy as np
import PyPDF2
from tkinter.filedialog import askopenfile
import io
from time import time

win = tk.Tk()


#premenne
wid, hey = 500,500
zoom, vys = 10, 10
bezi = False
idecka = []
razy = 0
bunka = 0

bunky = np.zeros((wid//zoom, hey//zoom), dtype = int)

#funkcie
def create_stage():
	global idecka, bunky, zoom, bunka
	for x in range(wid//vys):
		for y in range(hey//vys):
			if bunky[y,x] == 0:
				bunka = canvas.create_rectangle(x*zoom,y*zoom, x*zoom + zoom, y*zoom + zoom, fill = "black",
												outline = "gray")
			else:
				bunka = canvas.create_rectangle(x*zoom,y*zoom, x*zoom + zoom, y*zoom + zoom, fill = "white",
												outline = "white")
			idecka.append(bunka)


def spusti():
	global go, bezi
	if bezi:
		bezi = False
		go.config(text = "stop")
	else:
		bezi = True
		go.config(text = "ide sa")

def pocitame_suradnice(id):
	global vys, wid, razy
	row = wid // vys
	y = id
	while y > row: y -= row
	y -= 1
	x = (id -(razy*2500)) // (row)
	if x == 50: x = 49
	return y, x

def susedia(id):
	neigh = 0
	if id > 49+(2500*razy) and id < 2499+(2500*razy):
		neigh += bunky[pocitame_suradnice(id - 51)]
		neigh += bunky[pocitame_suradnice(id - 50)]
		neigh += bunky[pocitame_suradnice(id - 49)]
		neigh += bunky[pocitame_suradnice(id - 1)]
		neigh += bunky[pocitame_suradnice(id + 1)]
		neigh += bunky[pocitame_suradnice(id + 49)]
		neigh += bunky[pocitame_suradnice(id + 50)]
		neigh += bunky[pocitame_suradnice(id + 51)]
	elif id > 51+(2500*razy):
		neigh += bunky[pocitame_suradnice(id - 51)]
		neigh += bunky[pocitame_suradnice(id - 50)]
		neigh += bunky[pocitame_suradnice(id - 49)]
		neigh += bunky[pocitame_suradnice(id - 1)]
	elif id < 2499+(2500*razy):
		neigh += bunky[pocitame_suradnice(id + 1)]
		neigh += bunky[pocitame_suradnice(id + 49)]
		neigh += bunky[pocitame_suradnice(id + 50)]
		neigh += bunky[pocitame_suradnice(id + 51)]
	return neigh

def open_file():
	global zoom, razy
	how_many = 0
	file = askopenfile(parent = win, mode = "rb", filetype = [("Pdf file", "*.pdf")])
	if file:
		read_pdf = PyPDF2.PdfFileReader(file)
		page = read_pdf.getPage(0)
		content = page.extractText()
		for line in io.StringIO(content):
			hell = 0
			for znak in line:
				if znak.isalnum():
					bunky[how_many,hell] = int(znak)
					hell += 1
			how_many += 1
		canvas.delete("all")
		idecka.clear()
		create_stage()
		razy += 1

def zoom_ale_fakt(e):
	global zoom, razy
	canvas.delete("all")
	idecka.clear()
	zoom = slider.get()
	create_stage()
	razy += 1

def sarapata(e):
	global bunky, idecka, razy
	new_bunky = np.zeros((wid//zoom, hey//zoom), dtype = int)
	if bezi == True:
		print("loopujeme")
		for idecko in idecka:
			print(canvas.itemcget(idecko, "fill"))
			if bunky[pocitame_suradnice(idecko)] == 1 and 1<susedia(idecko)<4:
				new_bunky[pocitame_suradnice(idecko)] = 1
			elif bunky[pocitame_suradnice(idecko)] == 0 and susedia(idecko) == 3:
				new_bunky[pocitame_suradnice(idecko)] = 1
			else:
				new_bunky[pocitame_suradnice(idecko)] = 0
		canvas.delete("all")
		idecka.clear()
		bunky = new_bunky
		create_stage()
		razy += 1

def zomri_zi(e):
	global idecka, bunky, vys, hey, wid, razy
	row = wid//vys
	idecko = canvas.find_withtag("current")[0]

	y,x = pocitame_suradnice(idecko)

	if canvas.itemcget(idecko, "fill")=="white":
		canvas.itemconfig(idecko +(2500*razy), fill = "black", outline = "grey")
		bunky[y,x] = 0
	else:
		canvas.itemconfig(idecko +(2500*razy), fill = "white", outline = "white")
		bunky[y,x] = 1


#komponenty
canvas = tk.Canvas(width = wid, height = hey, bg = "black")
go = tk.Button(win, text = "stop", command = spusti, height = 2, width = 10)
slider = tk.Scale(win,from_ = 10, to = 50, orient = "horizontal", command = zoom_ale_fakt, length = 500)
gombik = tk.Button(win, text = "vyber PDFko", command = lambda:open_file())

#balenie
canvas.pack()
go.pack()
slider.pack()
gombik. pack()

#ukony
canvas.bind("<Button-1>", zomri_zi)
canvas.bind("<Motion>", sarapata)


print( pocitame_suradnice(2550))
#spustame
create_stage()
win.mainloop()
