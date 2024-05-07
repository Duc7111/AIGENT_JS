from Main import *
from pathlib import Path
from TestMain import parent_path

#parent_path = Path(__file__).resolve().parents[1]

load_pipeline(parent_path / '__cache__' / 'TestMain.json')
res = run()
if res['status']:
    print(res['outputs']['output'])
else:
    print(res['outputs']['msg'])
