# A class based on tkinter Frame to plot a 'real-time' graph

from tkinter import *
import threading

# Import tkinter compatible plotting
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Window(Frame):
	# Pass in a Tk() object as master
	def __init__(self, master):
		# Construct parent Frame - white background
		super(Window, self).__init__(master, bg='white')
		self.master = master

		# Figure for plotting
		self.fig = Figure()
		self.continuePlotting = False
		self.ax = None
		self.graph = None

		# Set up GUI
		self.init_window()

	# Define GUI widgets and their properties
	def init_window(self):
		# give desktop application a name
		self.master.title("SpineLine Tracker")
		# Window will take up full space of desktop Frame
		self.pack(fill=BOTH, expand=1)

		# Page title
		title = Button(self, text="SpineLine: Posture History",bg='white',height=4)
		title.config(font=('helvetica', 18, 'underline bold'))
		title.place(x=0, y=0)

		# Safe quit button
		quitButton = Button(self, text="Safely Quit",bg='red',height=3,command=self.safe_exit)
		quitButton.config(font=('helvetica', 11))
		quitButton.place(x=1200, y=0)

		# Clear graph button
		clearButton = Button(self, text="Clear graph",activebackground='red',height=3,command=self.clear_graph)
		clearButton.config(font=('helvetica', 11))
		clearButton.place(x=1115, y=0)

		# Add a graph to the window
		self.init_graph()

	# Define graph widget
	def init_graph(self):
		# ax: Time vs Curve plot
		self.ax = self.fig.add_subplot(111)
		self.set_axis()

		# Add graph as a widget to the window
		self.graph = FigureCanvasTkAgg(self.fig, master=self.master)
		self.graph.get_tk_widget().pack(side="top",fill='both',expand=True)

	# Set up grid and axis for the graph
	def set_axis(self):
		self.ax.set_xlabel("Time")
		self.fig.autofmt_xdate(bottom=0.2, rotation=30, ha='right')
		self.ax.set_ylabel("Curve (degrees)")
		self.ax.grid()

	# Plot a line on the graph
	def plot_line(self, xvals, yvals, label, _color):
		self.ax.plot(xvals, yvals, marker='o', color=_color, label=label)

	# Plot a dotted horizontal line on the graph
	def plot_hline_d(self, xvals, yval, label, _color):
		self.ax.hlines(yval, xvals[0], xvals[-1], linestyle='--', color=_color, label=label)

	# Plot 4 lines, 2 filled, 2 dashed
	# Dashed lines refer to x-values from first 2 lines
	# Inteneded use: plot 2 real-value lines along with 2 reference lines
	def plotter(self, line1_data, line2_data, line1ref_val, line2ref_val):
		# Clear graph
		self.ax.cla()
		self.set_axis()

		# Add top sensor history line
		self.plot_line(line1_data[0], line1_data[1], 'Top', 'blue')
		# Add top sensor reference line
		self.plot_hline_d(line1_data[0], line1ref_val, 'Top ref', 'blue')
		# Add bottom sensor history line
		self.plot_line(line2_data[0], line2_data[1], 'Bottom', 'green')
		# Add bottom sensor reference line
		self.plot_hline_d(line2_data[0], line2ref_val, 'Bottom ref', 'green')

		# Draw graph
		self.ax.legend()
		self.graph.draw()


	# Clear and reset graph
	# Override this function to also clear data stored
	def clear_graph(self):
		self.ax.cla()
		self.set_axis()
		self.graph.draw()

	# Override to also handle network disconnection
	def safe_exit(self):
		exit()
