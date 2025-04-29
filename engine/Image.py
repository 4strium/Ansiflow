import engine.Buffer as Buffer

class Image : pass

def create(visual, x, y, color):
  global color_index

  img = Image()
  
  img.visual = visual
  img.position = [x,y]
  img.color = color

  return img

def get_visual(img_inp):
  return img_inp.visual
def get_pos(img_inp):
  return img_inp.position
def get_color(img_inp):
  return img_inp.color

def set_pos(img_inp, n_pos):
  img_inp.position = n_pos
def set_color(img_inp, n_color):
  img_inp.color = n_color

def upload_classic_image(path, x, y, color) :
  try :
    with open(path, 'r', encoding='utf-8') as file_txt:
      tmp = file_txt.readlines()
      visual_export = [line.rstrip('\n') for line in tmp]
  except FileNotFoundError :
    return
  
  return create(visual_export, x, y, color)

def draw(window, img_inp):
  height = Buffer.get_height(window)
  width = Buffer.get_width(window)

  for i in range(len(get_visual(img_inp))):
    y_pos = i + img_inp.position[1]
    if 0 <= y_pos < height:  # Ensure y_pos is within window bounds
      x_offset = 0
      # On affiche caractère par caractère car on veut pouvoir "détourer les images"
      for char in img_inp.visual[i]:
        x_pos = img_inp.position[0] + x_offset
        if char != '1' and 0 <= x_pos < width-1:  # Ensure x_pos is within bounds
          Buffer.set_str_buffer(
              window,
              char,
              img_inp.color,
              x_pos, 
              y_pos,                    
          )
        x_offset += 1