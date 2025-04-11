import os
from pathlib import Path

from constants import ROOT, llm_client
from utils.executor_man import ExecutorManager

INTERFACE_FOLDER = ROOT / "output_d_mod_object_interface"
INTERFACE_BLOCK = "\n".join([i.read_text() for i in INTERFACE_FOLDER.iterdir() if i.name.endswith('.py')])
TEMPLATE = (ROOT / "e_write_automation_test/write_automation_test.template").read_text()
CODE_EXAMPLE = (ROOT / "e_write_automation_test/write_automation_test.code_example").read_text()
output_case_folder = ROOT / "output_e_automation_test"

if __name__ == '__main__':
    cases = [
        {"name": "所有公司的人数不超过20", "desc": "所有公司的人数不超过20"},
        {"name": "每个公司中, 用户的头像都不同", "desc": "每个公司中, 用户的头像都不同"},
    ]
    executor_manager = ExecutorManager(20)
    for case in cases:
        name = case["name"]
        case_desc = case["desc"]
        query = TEMPLATE.replace("#CASE#", case_desc).replace("#INTERFACE_BLOCK#", INTERFACE_BLOCK).replace("#CODE_EXAMPLE#", CODE_EXAMPLE)
        to_save0 = output_case_folder / f"{name}.output.txt"
        if os.path.exists(to_save0):
            continue
        executor_manager.submit(llm_client.ask, query, to_save0)
    executor_manager.results(show_progress=True)
