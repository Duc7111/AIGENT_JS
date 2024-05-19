
from Main import *
from pathlib import Path

parent_path = Path(__file__).resolve().parents[1]

add_module('questionHolder', 'IO', 'TextHolder')
set_module_hyperparameters('questionHolder', {'text': 'What is the deadline?'})

add_module('contextHolder', 'IO', 'TextHolder')
set_module_hyperparameters('contextHolder', {'text': """Dear students,
Due to several requests (I actually do not know exactly if this is true), the deadline for final project submission is rescheduled to 11:59 p.m. Sunday, May 20, 2024 (GMT+7).
Please use the following link to submit your final projects:
https://www.dropbox.com/request/sScwrT5Rg1dkGUyoG3wc
When submitting, please note:
- Name the compressed file as StudentID1-StudentID2.zip/rar... Please remember to include IDs of all team members in the file name (compressed) for submission.
- Within the compressed file, there should be the following folders:
Source: containing full source code
Report: containing the documentation (analysis and design report) of the project. The report includes a problem statement, use-case diagram, software architecture, class diagram, and interface design. You need to list all implemented functions and emphasize the advanced software architecture techniques you applied. Remember to summarize the functions you implemented and include screenshots illustrating all key features).
Demo: containing demo videos
Release: containing the executable program or URL to the deployed location."""})

load_pipeline_as_module('pipeline', parent_path / '__cache__' / 'Project Name.json')

connect_modules('questionHolder', 'pipeline', 'output', 'question')
connect_modules('contextHolder', 'pipeline', 'output', 'context')

output_register('output', 'pipeline', 'output')

res = run()
if res['status']:
    print(res['outputs'])
else:
    print(res['msg'])

save_pipeline(parent_path / '__cache__' / 'TestPipeline.json')