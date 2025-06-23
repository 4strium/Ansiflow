import json
import random
import time
import sys
import termios
from type.game.memory.Card import Card
from type.game.Game import Game
from engine.Image import Image
from engine.Buffer import Buffer
from engine.Button import Button
import engine.Tools as Tools

class MemoryGame : 
  def __init__(self, path_data):
    self.__cards_list = []
    self.__acc_points = 0
    self.__elapsed_time = 0.0
    self.__first_card_selected = -1
    self.__second_card_selected = -1
    self.__cursor_position = 0
    self.__already_discovered = []
    self.__backcard = Image.upload_with_colors("images/Cards/backcard.txt")

    with open(path_data, 'r') as file :
      data = json.load(file)

    cards_data = data['MemoryGame']['Cards']

    for card in cards_data :
      self.__cards_list.append(Card(card['id'][0],Image.upload_with_colors(card['path_visual']),card['couple_id']))
      self.__cards_list.append(Card(card['id'][1],Image.upload_with_colors(card['path_visual']),card['couple_id']))

    random.shuffle(self.__cards_list)

  def get_cards_list(self):
    return self.__cards_list
  def set_cards_list(self, cards_list):
    self.__cards_list = cards_list
  def get_acc_points(self):
    return self.__acc_points
  def set_acc_points(self,acc_points):
    self.__acc_points = acc_points
  def get_elapsed_time(self):
    return self.__elapsed_time
  def set_elapsed_time(self,elapsed_time):
    self.__elapsed_time = elapsed_time
  def get_first_card_selected(self):
    return self.__first_card_selected
  def set_first_card_selected(self, n_select_first):
    self.__first_card_selected = n_select_first
  def get_second_card_selected(self):
    return self.__second_card_selected
  def set_second_card_selected(self, n_select_second):
    self.__second_card_selected = n_select_second
  def get_cursor_selection(self):
    return self.__cursor_position
  def set_cursor_selection(self, cursor_position):
    self.__cursor_position = cursor_position
  def get_already_discovered(self):
    return self.__already_discovered
  def set_already_discovered(self, already_discovered):
    self.__already_discovered = already_discovered
  def get_backcard(self):
    return self.__backcard
  def set_backcard(self,backcard):
    self.__backcard = backcard

  def display_game(self, window_inp, color_no_hover, color_hover):
    x_counter = 0

    x_acc = int((Buffer.get_width(window_inp) // 12)*1.4)
    x_increment = x_acc

    y_acc = 2
    y_increment = Buffer.get_width(window_inp) // 18

    Buffer.clear_data(window_inp)
    cards = self.get_cards_list()
    for i in range(len(cards)) :
      if i == self.get_cursor_selection() :
        if i in self.get_already_discovered() or i in (self.get_first_card_selected(),self.get_second_card_selected()): 
          Button.draw_image_button(Button(Card.get_visual(cards[i]),[x_acc,y_acc],color_no_hover,color_hover),window_inp,1)
        else :
          Button.draw_image_button(Button(self.get_backcard(),[x_acc,y_acc],color_no_hover,color_hover),window_inp,1)
      else :
        if i in self.get_already_discovered() or i == self.get_first_card_selected():
          Button.draw_image_button(Button(Card.get_visual(cards[i]),[x_acc,y_acc],color_no_hover,color_hover),window_inp,0)
        else :
          Button.draw_image_button(Button(self.get_backcard(),[x_acc,y_acc],color_no_hover,color_hover),window_inp,0)
      x_counter += 1 
      x_acc += x_increment
      if x_counter == 7 :
        x_counter = 0
        y_acc += y_increment
        x_acc = x_increment
    Buffer.show_data(window_inp)  

  def check_correspondance(self):
    card1, card2 = self.get_first_card_selected(), self.get_second_card_selected()

    if self.get_cards_list()[card1].get_couple_id() == self.get_cards_list()[card2].get_couple_id() :
      self.set_acc_points(self.get_acc_points() + 1)
      self.get_already_discovered().append(card1)
      self.get_already_discovered().append(card2)
    self.set_first_card_selected(-1)
    self.set_second_card_selected(-1)

  def run_game(window_inp, game_inp, color_no_hover, color_hover):
    mem_game = MemoryGame('data.json')
    start_time = time.time()

    while True :
      key = Tools.get_key(1)
      cursor = mem_game.get_cursor_selection()
      if key == 27:  # Quitter avec 'échap'
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, Game.get_backup_terminal(game_inp))
        sys.exit()
        exit()
      if key == ord('z') and cursor > 6 :
        mem_game.set_cursor_selection(mem_game.get_cursor_selection()-7)
      elif key == ord('s') and cursor < 21 :
        mem_game.set_cursor_selection(mem_game.get_cursor_selection()+7)
      elif key == ord('q') and (cursor%7 != 0) :
        mem_game.set_cursor_selection(mem_game.get_cursor_selection()-1)
      elif key == ord('d') and (cursor not in [6,13,20,27]) :
        mem_game.set_cursor_selection(mem_game.get_cursor_selection()+1)
      elif key == 32 :
        if cursor not in mem_game.get_already_discovered() :
          if mem_game.get_first_card_selected() == -1 :
            mem_game.set_first_card_selected(cursor)
          elif cursor != mem_game.get_first_card_selected() and mem_game.get_second_card_selected() == -1 :
            mem_game.set_second_card_selected(cursor)
            mem_game.display_game(window_inp,color_no_hover,color_hover)
            time.sleep(2)
            mem_game.check_correspondance()
      if mem_game.get_acc_points() == 14 :
        break
      mem_game.display_game(window_inp,color_no_hover,color_hover)
      diff_time = Game.get_diff_time(game_inp)
      time.sleep(diff_time)
    
    mem_game.set_elapsed_time(time.time() - start_time)

    Buffer.clear_data(window_inp)

    return mem_game.get_elapsed_time()

if __name__ == "__main__":
  MemoryGame("data.json")