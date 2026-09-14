import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from investment import emi, future_value

def test_emi_positive():
    assert emi(1000000,8,10)>0

def test_future_value():
    assert abs(future_value(100,10,2)-121) < 1e-9
