import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from deal_scorer import deal_score
def test_undervalued():
    x=deal_score(80,100,8,80)
    assert x["label"]=="Undervalued"
