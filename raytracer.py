import matplotlib
import math


pos = (0.0, 0.0)

def create_rotation_matric(alpha):
  return [[math.cos(alpha), -math.sin(alpha)],[math.sin(alpha), math.cos(alpha)]]
