class Color : pass

def create_color(R, G, B):
  
  color_export = Color()

  color_export.red = R
  color_export.green = G
  color_export.blue = B

  return color_export

def get_red(color_inp):
  return color_inp.red
def get_green(color_inp):
  return color_inp.green
def get_blue(color_inp):
  return color_inp.blue

def set_red(color_inp, n_red):
  color_inp.red = n_red
def set_green(color_inp, n_green):
  color_inp.green = n_green
def set_blue(color_inp, n_blue):
  color_inp.blue = n_blue