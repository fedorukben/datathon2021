from utils import Debugger
from utils import ImageManager
from model import LinearModel
from visualize import Plotter
from visualize import HistogramSketch
import numpy as np
import config as g

class Analyzer(object):
  def __init__(self):
    self.debug = Debugger()
  def class_name(self):
    return "Analyzer"
  def get_confusion_matrix(self): # Harry
    pass
  def get_specificity(self): # Harry
    pass
  def get_sensitivity(self): # Harry
    pass
  def get_precision(self): # Harry
    pass 
  def get_recall(self): # Harry
    pass
  def get_accuracy(self): # Harry
    pass
  def get_fallout(self): # Harry
    pass
  def get_bias(self): # Harry
    pass
  def get_mean(self): # Harry
    pass
  def get_auc(self): # Harry
    pass
  def get_p_by_f_dist(self): # Harry
    pass
  def get_variance(self, coords, f):
    return self.get_ss_res(coords, f) / len(coords[0])
  def get_r_sq(self, model):
    f_mean = lambda x : np.average(model.training_x)
    x = model.get_training_x()
    y = model.get_training_y()
    f = model.get_f()
    var_mean = self.get_variance(zip(x, y), f_mean)
    var_fit = self.get_variance(zip(x, y), f)
    g.debug.prn(self, 'R squared calculated.')
    return (var_mean - var_fit) / var_mean
  def plot_roc(self):
    plotter = Plotter()
    plotter.set_title('Receiver Operating Characteristic')
    plotter.set_axis_labels('')
    plotter.close()
    pass # Save the image as "roc.png"
  def get_ss_res(self, coords, f):
    ss = 0
    for coord in coords:
      ss += (coord[1] - f(coord[0])) ** 2
    return ss
  def ssr_curve(self, plotter_func, slopes):
    # TODO: Sum of squared residuals plot
    # ssr.png
    pass
  def least_squares_slope_yint_eqn(self, x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(map(lambda x,y : x * y, x, y))
    sum_x_sq = sum(map(lambda x : x ** 2, x))
    x_av = np.mean(x)
    y_av = np.mean(y)

    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x_sq - (sum_x ** 2))
    yint = y_av - slope * x_av
    return slope, yint
  def f_dist(self, model_type, trials):
    plotter = Plotter()
    image_manager = ImageManager()

    plotter.set_title('F Distribution')
    plotter.set_axis_labels('Frequency', 'F Score')
    plotter.set_output_filename('imgs/f.png')

    histogram = HistogramSketch()
    for i in range(trials):
      x_vals = g.randomizer.random_list(g.points_to_gen, g.lower_x_bound, g.upper_x_bound)
      y_vals = g.randomizer.random_list(g.points_to_gen, g.lower_y_bound, g.upper_y_bound)
      
      if model_type == LinearModel:
        slope, yint = self.least_squares_slope_yint_eqn(x_vals, y_vals)
        func = lambda x : slope * x + yint 
      else:
        g.debug.prn(self, 'Incompatible model type.', 1)
        break

      ss_fit = self.get_ss_res(zip(x_vals, y_vals), func)
      ss_mean = self.get_ss_res(zip(x_vals, y_vals), lambda x : np.mean(x_vals))
      p_fit = 2 # TODO: Update for Dataframe
      p_mean = 1 # ""
      n = len(x_vals)
      
      if ss_fit == 0 or (n - p_fit) == 0 or (p_fit - p_mean) == 0:
        self.debug.prn(self, 'F distribution cannot divide by zero.', 1)
        continue
      numerator = (ss_mean - ss_fit) / (p_fit - p_mean)
      denominator = ss_fit / (n - p_fit)

      histogram.add_x(numerator / denominator)
      histogram.set_bins()
    
    plotter.load(histogram)
    plotter.save()
    plotter.close()
    image_manager.scale('imgs/f.png', 'imgs/f.png', 250)
    self.debug.prn(self, 'F distribution created.')
  
class DataSet(object):
  def __init__(self, data):
    self.data = pd.DataFrame(data) 
    g.debug.prn(self, "DataSet initialized.")
  def __str__(self):
    g.debug.prn(self, "Convert DataSet to string.")
    return self.data.to_string()
    # this will be your print code
  def class_name(self):
    return "DataSet"
  def get_cols(self, col_names):
    if type(col_names) != list:
      g.debug.prn(self, "Got single column.")
      return self.data[col_names].tolist()
    if col_names == []:
      g.debug.prn(self, "You need to pass something into get_cols().", 1)
    lst = [] # [[datafromc1], [datafromc2]]
    for col in col_names:
      lst.append(self.data[col].tolist())
    g.debug.prn(self, "Got list of columns.")
    return lst
    # return [1,2,5,3,0,-4]
  def get_rows(self, indices):
    if type(indices) != list:
      return self.data[indices].tolist()
    if indices == []:
      g.debug.prn(self, "You need to pass something into get_cols().", 1)
    lst = [] # [[datafromc1], [datafromc2]]
    for row in indices:
      lst.append(self.data[row].tolist())
    return lst
  def get_input_cols(self): # dependant variables 
    self.get_cols(self.get_label()[:-1])
  def get_output_col(self): # independant variables
    self.get_cols(self.get_label()[-1])
  def get_label(self):
    return list(self.data)
    # ["Temp", "Sea Level Rise"]
  def get_data(self):
    return self.get_cols(self.get_label())
  def get_datum(self, col_names, indices): #TODO:
    if type(indices) != list and type(col_names) != list:
      return self.get_cols(col_names)[indices]
    lst = []
    for col, index in zip(col_names, indices): 
      lst.append(self.get_cols(col)[index])
    return lst
    # dataset.get_datum(["x2", "x1"],[5, 3])
    # --> [-9, 3]
# https://towardsdatascience.com/the-ultimate-guide-to-data-cleaning-3969843991d4
class Cleaner(object):
  def __init__(self):
    pass
  def class_name(self):
    return "Cleaner"
  def delete_rows(self, ds, rows):
    for row in rows:
      pass
      # Delete row code. 
  def replace_values(self, ds):
    pass
  def reformat(self, ds):
    pass
  def delete_duplicates(self, ds):
    pass
  def convert_types(self, ds, type_to):
    pass
  def workflow(self, ds):
    self._inspect(ds)
    self._clean(ds)
    self._verify(ds)
    self._report(ds)
  def _inspect(self, ds):
    pass
  def _clean(self, ds):
    pass
  def _verify(self, ds):
    pass
  def _report(self, ds):
    pass
  

'''

(x1,x2,x3,y)
y=ax1+bx2+c
y = f(x1,x2,x3)

get_vars = [(3, 57, True, True), (0, 18, False, True)]
set_vars([3, 57, True, True])


[(x1,y1),(x2,y2),(x3,y3)...]
y=ax+bz+c
[(x1,z1,y1),(x2,z2,y2)...]
[(x1,x2,x3...), (y1,y2,y3...), (z1,z2,z3...)]

'''

#<!-----Task Board-----!>#

# Russell --> SQL
# Kai     --> Dataset
# Harry   --> Analyzer
# Ben     --> Models

# Tasks:
# Dataset hooked up w visualize. 
# Analyzer
# Models