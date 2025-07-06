import json

INCREMENT_RAD = 0.017
PI = 3.142

class Game : 
  def __init__(self,differential_time, map_path, npc_list=[]):
    self.__time = 0
    self.__dt = differential_time
    self.__npc_list = npc_list
    self.__fight_session = None
    self.__datafile = "data.json"

    self.__color1 = None
    self.__color2 = None
    self.__death_path = ""
    self.__ending_path = ""

    self.upload_map(map_path)

  def get_time(self):
    return self.__time
  def set_time(self, time):
    self.__time = time
  def get_diff_time(self):
    return self.__dt
  def set_diff_time(self, n_dt):
    self.__dt = n_dt
  def get_map(self):
    return self.__map
  def set_map(self,n_map):
    self.__map = n_map
  def get_npcs(self):
    return self.__npc_list
  def set_npcs(self,n_npcs):
    self.__npc_list = n_npcs
  def get_fight(self):
    return self.__fight_session
  def set_fight(self, n_fight):
    self.__fight_session = n_fight
  def get_datafile(self):
    return self.__datafile
  def set_datafile(self,datafile):
    self.__datafile = datafile
  def get_color1(self):
    return self.__color1
  def set_color1(self,n_color1):
    self.__color1 = n_color1
  def get_color2(self):
    return self.__color2
  def set_color2(self,n_color2):
    self.__color2 = n_color2
  def get_death_path(self):
    return self.__death_path
  def set_death_path(self,n_deathpath):
    self.__death_path = n_deathpath
  def get_ending_path(self):
    return self.__ending_path
  def set_ending_path(self,n_endpath):
    self.__ending_path = n_endpath

  def running_time(self):
    current_time = self.get_time()
    self.set_time(current_time + self.get_diff_time())

  def upload_map(self, path):
    with open(path, 'r') as file :
      data = json.load(file)
    self.set_map(data['map'][::-1])

  def upload_all_end(self, path):
    with open(path, 'r') as file :
      data = json.load(file)
    self.set_death_path(data['end']['death_path'])
    self.set_ending_path(data['end']['ending_path'])