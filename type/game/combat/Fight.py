import engine.Image as Image
import engine.Buffer as Buffer

class Fight : pass

def create(window_inp):
  fight_element = Fight()
  fight_element.target_image = Image.upload_with_colors("images/target.txt")[0] # Possible car couleur unique
  Image.set_pos(fight_element.target_image,[(Buffer.get_width(window_inp)//2)-7,(Buffer.get_height(window_inp)//2)-7])

  fight_element.enemy_list = []

  return fight_element

def update_fight(window_inp, fight_inp):
  Image.draw(window_inp, fight_inp.target_image)