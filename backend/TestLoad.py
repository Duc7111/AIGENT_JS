from Main import *
from pathlib import Path

parent_path = Path(__file__).resolve().parents[1]

load_pipeline(parent_path / '__cache__' / 'TestHuggingFace.json')
res = run()
if res['status']:
    print(res['outputs'])
else:
    print(res['msg'])
