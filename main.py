from utils import ImageManager
from utils import Randomizer
from utils import Debugger
from utils import OutputFileFormatter

from guis import GUI
from guis import Console

from model import Modeller
from model import LinearModel

from analyze import Analyzer

from visualize import Plotter
from visualize import ScatterSketch

from maps import Mapper

import config as g

import sys

def init_globals():
  g.randomizer = Randomizer()
  g.debug = Debugger()
  g.console = Console()
  g.analyzer = Analyzer()
  g.modeller = Modeller(g.analyzer)
  g.gui = GUI(plotter, g.analyzer, g.modeller)
  g.output_file_formatter = OutputFileFormatter()
  g.mapper = Mapper()

def gen_plot():
  plotter.set_title(g.graph_titles['main'])

  g.x = g.randomizer.random_list(25, 0, 100)
  g.y = g.randomizer.random_list(25, 0, 100)

  # plotter.add_x_val(x) # [-2, -1, 0, 1, 2]
  # plotter.add_y_val(y) # [4,1,0,1,4]

  scatter = ScatterSketch()
  scatter.add_x(g.x)
  scatter.add_y(g.y)
  plotter.load(scatter)

  plotter.save()
  plotter.close()

  # g.modeller.gen_least_squares(x,y)
  # g.analyzer.f_dist(LinearModel, 100)

  image_manager.scale(g.files['plot'], g.files['plot'], g.image_height)

if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <debug_mode>')
    print('debug_level -->')
    print('\t0 - Supress all messages.')
    print('\t1 - Show errors and warnings.')
    print('\t2 - Show log of relevant actions.')
    print('\t3 - Show all messages.')
    quit()

g.debug_level = int(sys.argv[1])

plotter = Plotter()
init_globals()
g.output_file_formatter.format_folder('imgs')
image_manager = ImageManager()

gen_plot()

#sg.theme('Dark Red 5')

g.gui.standard()
g.gui.compile()
g.gui.loop()
g.gui.close()
