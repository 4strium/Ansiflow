import json
import random
import time
import type.game.memory.Card as Card
import type.game.Game as Game
import engine.Image as  Image
import engine.Buffer as Buffer
import engine.Button as Button
import engine.Tools as Tools

class MemoryGame : pass

def create(path_data):
  memory_export = MemoryGame()

  memory_export.cards_list = []
  memory_export.acc_points = 0
  memory_export.elapsed_time = 0.0
  memory_export.first_card_selected = -1
  memory_export.second_card_selected = -1
  memory_export.cursor_position = 0
  memory_export.already_discovered = []

  memory_export.backcard = Image.upload_with_colors("images/Cards/backcard.txt")

  with open(path_data, 'r') as file :
    data = json.load(file)

  cards_data = data['MemoryGame']['Cards']

  for card in cards_data :
    memory_export.cards_list.append(Card.create(card['id'][0],Image.upload_with_colors(card['path_visual']),card['couple_id']))
    memory_export.cards_list.append(Card.create(card['id'][1],Image.upload_with_colors(card['path_visual']),card['couple_id']))

  random.shuffle(memory_export.cards_list)

  return memory_export

def get_first_card_selected(mem_inp):
  return mem_inp.first_card_selected
def get_second_card_selected(mem_inp):
  return mem_inp.second_card_selected
def get_cursor_selection(mem_inp):
  return mem_inp.cursor_position
def get_backcard(mem_inp):
  return mem_inp.backcard
def get_elapsed_time(mem_inp):
  return mem_inp.elapsed_time

def set_cursor_selection(mem_inp, n_select):
  mem_inp.cursor_position = n_select
def set_first_card_selected(mem_inp, n_select_first):
  mem_inp.first_card_selected = n_select_first
def set_second_card_selected(mem_inp, n_select_second):
  mem_inp.second_card_selected = n_select_second

def display_game(window_inp, memory_inp, color_no_hover, color_hover):

  x_counter = 0

  x_acc = int((Buffer.get_width(window_inp) // 12)*1.4)
  x_increment = x_acc

  
  y_acc = 2
  y_increment = Buffer.get_width(window_inp) // 18

  Buffer.clear_data(window_inp)
  cards = memory_inp.cards_list
  for i in range(len(cards)) :
    if i == get_cursor_selection(memory_inp) :
      if i in memory_inp.already_discovered or i in (get_first_card_selected(memory_inp),get_second_card_selected(memory_inp)): 
        Button.draw_image_button(window_inp,Button.create(Card.get_visual(cards[i]),[x_acc,y_acc],color_no_hover,color_hover),1)
      else :
        Button.draw_image_button(window_inp,Button.create(get_backcard(memory_inp),[x_acc,y_acc],color_no_hover,color_hover),1)
    else :
      if i in memory_inp.already_discovered or i == get_first_card_selected(memory_inp):
        Button.draw_image_button(window_inp,Button.create(Card.get_visual(cards[i]),[x_acc,y_acc],color_no_hover,color_hover),0)
      else :
        Button.draw_image_button(window_inp,Button.create(get_backcard(memory_inp),[x_acc,y_acc],color_no_hover,color_hover),0)
    x_counter += 1 
    x_acc += x_increment
    if x_counter == 7 :
      x_counter = 0
      y_acc += y_increment
      x_acc = x_increment
  Buffer.show_data(window_inp)  

def check_correspondance(mem_inp):
  card1, card2 = get_first_card_selected(mem_inp), get_second_card_selected(mem_inp)

  if mem_inp.cards_list[card1].couple_id == mem_inp.cards_list[card2].couple_id :
    mem_inp.acc_points += 1
    mem_inp.already_discovered.append(card1)
    mem_inp.already_discovered.append(card2)
  set_first_card_selected(mem_inp,-1)
  set_second_card_selected(mem_inp,-1)

def run_game(window_inp, game_inp, color_no_hover, color_hover):
  mem_game = create('data.json')
  start_time = time.time()

  while True :
    key = Tools.get_key(1)
    cursor = get_cursor_selection(mem_game)
    if key == ord('z') and cursor > 6 :
      mem_game.cursor_position -= 7
    elif key == ord('s') and cursor < 21 :
      mem_game.cursor_position += 7
    elif key == ord('q') and (cursor%7 != 0) :
      mem_game.cursor_position -= 1
    elif key == ord('d') and (cursor not in [6,13,20,27]) :
      mem_game.cursor_position += 1
    elif key == 32 :
      if cursor not in mem_game.already_discovered :
        if get_first_card_selected(mem_game) == -1 :
          set_first_card_selected(mem_game,cursor)
        elif cursor != get_first_card_selected(mem_game) and get_second_card_selected(mem_game) == -1 :
          set_second_card_selected(mem_game,cursor)
          display_game(window_inp,mem_game,color_no_hover,color_hover)
          time.sleep(2)
          check_correspondance(mem_game)
    if mem_game.acc_points == 14 :
      break
    display_game(window_inp,mem_game,color_no_hover,color_hover)
    diff_time = Game.get_diff_time(game_inp)
    time.sleep(diff_time)
  
  mem_game.elapsed_time = time.time() - start_time

  Buffer.clear_data(window_inp)

  return get_elapsed_time(mem_game)

if __name__ == "__main__":
  create("data.json")