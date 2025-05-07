import sys
import engine.Color as Color

class Buffer : pass

def clear_data(buff_inp):
  columns = []
  for i in range(get_height(buff_inp)):
    rows = []
    for j in range(get_width(buff_inp)):
      rows.append([' ',Color.create_color(255,255,255)])
    columns.append(rows)

  buff_inp.data = columns

def create(width, height):
  buff = Buffer()
  buff.width = width
  buff.height = height

  clear_data(buff)

  return buff

def get_width(buff_inp):
  return buff_inp.width
def get_height(buff_inp):
  return buff_inp.height
def get_pixel(buff__inp,x,y):
  return buff__inp.data[y][x]

def set_width(buff_inp, n_width):
  buff_inp.width = n_width
def set_height(buff_inp, n_height):
  buff_inp.height = n_height

def set_str_buffer(buff_inp,char,color,x,y):
  if len(char) > 1 :
    x_acc = x
    for i in range(len(char)) :
      buff_inp.data[y][x_acc] = [char[i],color]
      x_acc += 1
  else :
    buff_inp.data[y][x] = [char,color]


def rgb_fg(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def move_to(x, y):
    return f"\033[{y};{x}H"

def reset():
    return "\033[0m"

def show_data(buff_inp):
    output = []
    prev_fg = None

    for y, row in enumerate(buff_inp.data, start=1):
        output.append(move_to(1, y))
        for cell in row:
            char = cell[0]
            color_fg = [Color.get_red(cell[1]),Color.get_green(cell[1]),Color.get_blue(cell[1])]

            # Changer couleur si nécessaire
            if color_fg != prev_fg:
                if color_fg :
                    output.append(rgb_fg(color_fg[0],color_fg[1],color_fg[2]))
                else:
                    output.append("\033[39m")  # couleur par défaut
                prev_fg = color_fg

            output.append("\033[49m")  # fond par défaut

            output.append(char)

    output.append(reset())
    sys.stdout.write("".join(output))
    sys.stdout.flush()