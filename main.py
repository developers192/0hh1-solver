import tkinter as tk
from collections import Counter as C
import os
import sys
import ctypes

myappid = 'developers192.0hh1solver.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def mouse_click(event):
	global colors
	x = (event.y // square_size)
	y = (event.x // square_size)
	change_color(x, y)
	
def change_color(x, y, colour = None):
	if 0 <= x < num_squares and 0 <= y < num_squares:
		colors[x][y] = (colour if colour else(colors[x][y] + 1)) % 3 
		color = ["gray", "yellow", "blue"][colors[x][y]]
		canvas.itemconfig(rectangles[x][y], fill=color)

def opposite_color(color):
	if color == 1:
		return 2
	elif color == 2:
		return 1

def findFullRow():
	rows = []
	for j in range(num_squares):
		count = C(colors[j])
		if count[0] == 0 and count[1] == num_squares // 2 and count[2] == num_squares // 2:
			rows.append(j)
	return rows

def findFullColumn():
	columns = []
	for i in range(num_squares):
		count = C([colors[j][i] for j in range(num_squares)])
		if count[0] == 0 and count[1] == num_squares // 2 and count[2] == num_squares // 2:
			columns.append(i)
	return columns

def difference(missing, full):
	differences = []
	for i in range(num_squares):
		if missing[i] != full[i]:
			differences.append(i)
	return differences

def clear_grid():
	global colors
	colors = [[0 for _ in range(num_squares)] for _ in range(num_squares)]
	for row in rectangles:
		for rectangle in row:
			canvas.itemconfig(rectangle, fill="gray")

def resize_grid(size):
	global num_squares, rectangles, canvas

	canvas.pack_forget()
	
	num_squares = size
	canvas = tk.Canvas(window, width=num_squares * square_size, height=num_squares * square_size)
	canvas.pack()
	canvas.bind("<Button-1>", mouse_click)
	clear_grid()
	rectangles = [[canvas.create_rectangle(j * square_size, i * square_size, (j + 1) * square_size, (i + 1) * square_size, fill="gray") for j in range(num_squares)] for i in range(num_squares)]

def solve_grid():
	prevColors = [row[:] for row in colors]
		
	for j in range(num_squares):
		for i in range(num_squares):
			if colors[j][i] == 0:
				continue

			# Check if 2 same color squares are adjacent
			if i < num_squares - 1 and colors[j][i] == colors[j][i + 1]:
				try:
					change_color(j, i + 2, opposite_color(colors[j][i]))
				except IndexError: pass
				try:
					change_color(j, i - 1, opposite_color(colors[j][i]))
				except IndexError: pass
			
			if j < num_squares - 1 and colors[j][i] == colors[j + 1][i]:
				try:
					change_color(j + 2, i, opposite_color(colors[j][i]))
				except IndexError: pass
				try:
					change_color(j - 1, i, opposite_color(colors[j][i]))
				except IndexError: pass

			# Check if a gray square is surrounded by 2 same color squares
			if i < num_squares - 2 and colors[j][i] == colors[j][i + 2]:
				try:
					change_color(j, i + 1, opposite_color(colors[j][i]))
				except IndexError: pass
			if j < num_squares - 2 and colors[j][i] == colors[j + 2][i]:
				try:
					change_color(j + 1, i, opposite_color(colors[j][i]))
				except IndexError: pass

	for j in range(num_squares):
		# Check if row has enough color of one type
		count = C(colors[j])
		if count[1] == num_squares // 2:
			for i in range(num_squares):
				if colors[j][i] == 0:
					change_color(j, i, 2)
		elif count[2] == num_squares // 2:
			for i in range(num_squares):
				if colors[j][i] == 0:
					change_color(j, i, 1)

		# Check if row has 2 gray squares
		if count[0] == 2:
			fullRows = findFullRow()
			for fullrow in fullRows:
				differences = difference(colors[j], colors[fullrow])
				if len(differences) == 2:
					change_color(j, differences[0], opposite_color(colors[fullrow][differences[0]]))
					change_color(j, differences[1], opposite_color(colors[fullrow][differences[1]]))

	for i in range(num_squares):
		# Check if column has enough color of one type
		count = C([colors[j][i] for j in range(num_squares)])
		if count[1] == num_squares // 2:
			for j in range(num_squares):
				if colors[j][i] == 0:
					change_color(j, i, 2)
		elif count[2] == num_squares // 2:
			for j in range(num_squares):
				if colors[j][i] == 0:
					change_color(j, i, 1)

		# Check if column has 2 gray squares
		if count[0] == 2:
			fullColumns = findFullColumn()
			for fullcolumn in fullColumns:
				differences = difference([colors[j][i] for j in range(num_squares)], [colors[j][fullcolumn] for j in range(num_squares)])
				if len(differences) == 2:
					change_color(differences[0], i, opposite_color(colors[differences[0]][fullcolumn]))
					change_color(differences[1], i, opposite_color(colors[differences[1]][fullcolumn]))
	
	if prevColors != colors:
		return -1

def solve():
	while solve_grid() == -1:
		pass

def resource_path(relative_path):
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)

window = tk.Tk()
window.title("0hh1 solver")
window.iconbitmap(resource_path("icon.ico"))

num_squares = 14  # Number of squares horizontally and vertically
square_size = 50  # Size of each square in pixels

canvas = tk.Canvas(window, width=num_squares * square_size, height=num_squares * square_size)
canvas.pack()

colors = [[0 for _ in range(num_squares)] for _ in range(num_squares)]
rectangles = [[canvas.create_rectangle(j * square_size, i * square_size, (j + 1) * square_size, (i + 1) * square_size, fill="gray") for j in range(num_squares)] for i in range(num_squares)]

canvas.bind("<Button-1>", mouse_click)

solve_button = tk.Button(window, text="Solve", command=solve)
solve_button.pack(side=tk.BOTTOM)

clear_button = tk.Button(window, text="Clear Grid", command=clear_grid)
clear_button.pack(side=tk.BOTTOM)

resize4_button = tk.Button(window, text="4x4", command = lambda : resize_grid(4))
resize4_button.pack(side=tk.LEFT)

resize6_button = tk.Button(window, text="6x6", command = lambda : resize_grid(6))
resize6_button.pack(side=tk.LEFT)

resize8_button = tk.Button(window, text="8x8", command = lambda : resize_grid(8))
resize8_button.pack(side=tk.LEFT)

resize10_button = tk.Button(window, text="10x10", command = lambda : resize_grid(10))
resize10_button.pack(side=tk.RIGHT)

resize12_button = tk.Button(window, text="12x12", command = lambda : resize_grid(12))
resize12_button.pack(side=tk.RIGHT)

resize14_button = tk.Button(window, text="14x14", command = lambda : resize_grid(14))
resize14_button.pack(side=tk.RIGHT)

window.mainloop()
