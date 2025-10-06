#=======================================================================
# import
#=======================================================================
import random

def randomRgbColor():
  r = str(random.randint(1,255))
  g = str(random.randint(1,255))
  b = str(random.randint(1,255))
  return "(" + r + "," + g + "," + b + ")"

def randomFloat():
  i = random.randint(1,9)
  i = i/10
  return i

print(randomFloat())
