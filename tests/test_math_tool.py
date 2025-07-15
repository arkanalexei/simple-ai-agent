from tools import math_tool

def test_basic_math():
  assert math_tool.run("2 + 2") == "4"
  
def test_invalid_math():
  assert "Error" in math_tool.run("X + 2")