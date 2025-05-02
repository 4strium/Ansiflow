import engine.Buffer as Buffer
import engine.Image as Image

class Button : pass

def create(content, position, color1, color2):
  button_export = Button()

  button_export.content = content
  button_export.position = position
  button_export.color1 = color1
  button_export.color2 = color2

  return button_export

def get_content(button_inp) :
  return button_inp.content
def get_position(button_inp):
  return button_inp.position
def get_color1(button_inp):
  return button_inp.color1
def get_color2(button_inp):
  return button_inp.color2

def set_content(button_inp, n_content):
  button_inp.content = n_content
def set_position(button_inp, n_position):
  button_inp.position = n_position
def set_color1(button_inp, n_color1):
  button_inp.color1 = n_color1
def set_color2(button_inp, n_color2):
  button_inp.color2 = n_color2

def draw_text_button(window_inp, button_inp, hover):
  if hover :
    color_drawing = get_color2(button_inp)
  else :
    color_drawing = get_color1(button_inp)
  space_needed = len(get_content(button_inp))
  x_fix = get_position(button_inp)[0]
  y_fix = get_position(button_inp)[1]
  x_index = x_fix+1
  Buffer.set_str_buffer(window_inp,get_content(button_inp), color_drawing, x_fix+1,y_fix+2)
  Buffer.set_str_buffer(window_inp,'┌', color_drawing, x_fix,y_fix)
  Buffer.set_str_buffer(window_inp,'│', color_drawing, x_fix,y_fix+1)
  Buffer.set_str_buffer(window_inp,'│', color_drawing, x_fix,y_fix+2)
  Buffer.set_str_buffer(window_inp,'│', color_drawing, x_fix,y_fix+3)
  Buffer.set_str_buffer(window_inp,'└', color_drawing, x_fix,y_fix+4)
  for i in range(space_needed):
    Buffer.set_str_buffer(window_inp,'─', color_drawing, x_index,y_fix)
    Buffer.set_str_buffer(window_inp,'─', color_drawing, x_index,y_fix+4)
    x_index += 1
  Buffer.set_str_buffer(window_inp,'┐', color_drawing, x_index,y_fix)
  Buffer.set_str_buffer(window_inp,'│', color_drawing, x_index,y_fix+1)
  Buffer.set_str_buffer(window_inp,'│', color_drawing, x_index,y_fix+2)
  Buffer.set_str_buffer(window_inp,'│', color_drawing, x_index,y_fix+3)
  Buffer.set_str_buffer(window_inp,'┘', color_drawing, x_index,y_fix+4)

def draw_image_button(window_inp, button_inp, hover):
  if hover :
    color_drawing = get_color2(button_inp)
  else :
    color_drawing = get_color1(button_inp)
  x_space_needed = len(Image.get_visual(get_content(button_inp)[0])[0])+1
  y_space_needed = len(Image.get_visual(get_content(button_inp)[0]))+1
  x_fix = get_position(button_inp)[0]
  y_fix = get_position(button_inp)[1]
  for color in get_content(button_inp) :
    Image.set_pos(color,[x_fix+1,y_fix+1])
    Image.draw(window_inp, color)
  for y_index in range(y_fix+1,y_fix+y_space_needed):
    Buffer.set_str_buffer(window_inp,'|', color_drawing,x_fix,y_index)
    Buffer.set_str_buffer(window_inp,'|', color_drawing,x_fix+x_space_needed,y_index)
  for x_index in range(x_fix+1,x_fix+x_space_needed):
    Buffer.set_str_buffer(window_inp,'─', color_drawing,x_index,y_fix)
    Buffer.set_str_buffer(window_inp,'─', color_drawing,x_index,y_fix+y_space_needed)
  Buffer.set_str_buffer(window_inp,'┌', color_drawing,x_fix,y_fix)
  Buffer.set_str_buffer(window_inp,'└', color_drawing, x_fix,y_fix+y_space_needed)
  Buffer.set_str_buffer(window_inp,'┐', color_drawing, x_fix+x_space_needed,y_fix)
  Buffer.set_str_buffer(window_inp,'┘', color_drawing, x_fix+x_space_needed,y_fix+y_space_needed)