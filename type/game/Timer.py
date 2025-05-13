import json
import engine.Tools as Tools
import engine.Image as Image

class Timer : pass

def create(data_path, color):

  with open(data_path, 'r') as file :
    data = json.load(file)
  timer_elements = data['Timer']

  timer_export = Timer()

  timer_export.start_amount = 1200
  timer_export.remaining_time = 1200 # en secondes

  timer_export.two_points = Image.upload_classic_image(timer_elements[0],0,0,color)
  timer_export.numbers_visuals = []

  for ind_img in range(1,len(timer_elements)) :
   timer_export.numbers_visuals.append(Image.upload_classic_image(timer_elements[ind_img],0,0,color))

  return timer_export

def remove_time(timer_inp,sec_mesure) :
  timer_inp.remaining_time = timer_inp.start_amount +  sec_mesure

def get_remaining_time(timer_inp):
  return timer_inp.remaining_time
def get_number_visuals(timer_inp):
  return timer_inp.numbers_visuals
def get_two_points(timer_inp):
  return timer_inp.two_points

def show_timer(buffer_win,timer_inp):
  timestamp = Tools.convert_sec_to_min(get_remaining_time(timer_inp))
  minutes = str(timestamp[0])
  seconds = str(timestamp[1])

  if len(minutes) == 2 :
    minutes_visuals = [get_number_visuals(timer_inp)[int(minutes[0])],get_number_visuals(timer_inp)[int(minutes[1])]]
  else :
    minutes_visuals = [get_number_visuals(timer_inp)[0],get_number_visuals(timer_inp)[int(minutes[0])]]


  if len(seconds) == 2 :
    seconds_visuals = [get_number_visuals(timer_inp)[int(seconds[0])],get_number_visuals(timer_inp)[int(seconds[1])]]
  else :
    seconds_visuals = [get_number_visuals(timer_inp)[0],get_number_visuals(timer_inp)[int(seconds[0])]]

  x_start = 0
  y_fix = 0

  for image_min in minutes_visuals :
    Image.set_pos(image_min,[x_start, y_fix])
    Image.draw(buffer_win,image_min,0)
    x_start += 10
  Image.set_pos(get_two_points(timer_inp),[x_start, y_fix])
  Image.draw(buffer_win,get_two_points(timer_inp),0)
  x_start += 4
  for image_sec in seconds_visuals :
    Image.set_pos(image_sec,[x_start, y_fix])
    Image.draw(buffer_win,image_sec,0)
    x_start += 10

