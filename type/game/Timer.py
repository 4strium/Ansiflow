import json
import engine.Tools as Tools
import engine.Image as Image

class Timer : 
  def __init__(self,data_path,color):

    with open(data_path, 'r') as file :
      data = json.load(file)
    timer_elements = data['Timer']

    self.__start_amount = 1200
    self.__remaining_time = 1200
    self.__two_points = Image.upload_classic_image(timer_elements[0],0,0,color)
    self.__numbers_visuals = []

    for ind_img in range(1,len(timer_elements)) :
      self.__numbers_visuals.append(Image.upload_classic_image(timer_elements[ind_img],0,0,color))

  def get_start_amount(self):
    return self.__start_amount
  def set_start_amount(self,start_amount):
    self.__start_amount = start_amount
  def get_remaining_time(self):
    return self.__remaining_time
  def set_remaining_time(self, remaining_time):
    self.__remaining_time = remaining_time
  def get_two_points(self):
    return self.__two_points
  def set_two_points(self,two_points):
    self.__two_points = two_points
  def get_numbers_visuals(self):
    return self.__numbers_visuals
  def set_numbers_visuals(self,numbers_visuals):
    self.__numbers_visuals = numbers_visuals

  def remove_time(self,sec_mesure) :
    self.set_remaining_time(self.get_start_amount() + sec_mesure)


  def show_timer(self, buffer_win):
    timestamp = Tools.convert_sec_to_min(self.get_remaining_time())
    minutes = str(timestamp[0])
    seconds = str(timestamp[1])

    if len(minutes) == 2 :
      minutes_visuals = [self.get_numbers_visuals()[int(minutes[0])],self.get_numbers_visuals()[int(minutes[1])]]
    else :
      minutes_visuals = [self.get_numbers_visuals()[0],self.get_numbers_visuals()[int(minutes[0])]]


    if len(seconds) == 2 :
      seconds_visuals = [self.get_numbers_visuals()[int(seconds[0])],self.get_numbers_visuals()[int(seconds[1])]]
    else :
      seconds_visuals = [self.get_numbers_visuals()[0],self.get_numbers_visuals()[int(seconds[0])]]

    x_start = 0
    y_fix = 0

    for image_min in minutes_visuals :
      Image.set_pos(image_min,[x_start, y_fix])
      Image.draw(buffer_win,image_min,0)
      x_start += 10
    Image.set_pos(self.get_two_points(),[x_start, y_fix])
    Image.draw(buffer_win,self.get_two_points(),0)
    x_start += 4
    for image_sec in seconds_visuals :
      Image.set_pos(image_sec,[x_start, y_fix])
      Image.draw(buffer_win,image_sec,0)
      x_start += 10

