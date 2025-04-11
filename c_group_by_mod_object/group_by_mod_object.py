import shutil
from pathlib import Path

from constants import ROOT, llm_client
from utils.code_util import extract_code, split_code_by_class, camel_to_snake
from utils.executor_man import ExecutorManager


def move_to_groups(input_single_api_model_object_responses, output0_mod_object_groups):
    for file in input_single_api_model_object_responses.iterdir():
        if file.is_file() and file.suffix == '.resp':
            ds_response = file.read_text()
            code = extract_code(ds_response, mark="python")
            clazz_codes = split_code_by_class(code)
            for mod_object, code0 in clazz_codes.items():
                folder = output0_mod_object_groups / mod_object
                folder.mkdir(exist_ok=True, parents=True)
                folder.joinpath(f"{file.stem}.py").write_text(code0)


def group2mod_object(output0_mod_object_groups, output1_mod_objects):
    template = (ROOT / "c_group_by_mod_object/group_by_mod_object.template").read_text()
    output1_mod_objects.mkdir(parents=True, exist_ok=True)
    executor_manager = ExecutorManager(max_workers=10)
    for group in output0_mod_object_groups.iterdir():
        if not group.is_dir():
            continue
        py_files = [p for p in group.iterdir() if p.suffix == ".py"]
        py_file_contents = [content.read_text() for content in py_files]
        py_file_content_block = "\n####\n".join(py_file_contents)
        mod_name = camel_to_snake(group.stem)
        query = template.format(CODES=py_file_content_block)
        resp_target = output1_mod_objects / f"{mod_name}.resp"
        if resp_target.exists():
            print(f"skip {mod_name}")
            continue
        executor_manager.submit(llm_client.ask, query, resp_target)
    executor_manager.results(show_progress=True)
    for f in output1_mod_objects.iterdir():
        if f.suffix != ".resp":
            continue
        py_target = output1_mod_objects / f"{f.stem}.py"
        raw_code = f.read_text()
        code = extract_code(raw_code).strip()
        full_code = f"""from mod_object import ModObject\n\n{code}"""
        py_target.write_text(full_code)


if __name__ == '__main__':
    input_single_api_model_object_responses = ROOT / 'output_b_single_api_model_object'
    output0_mod_object_groups = ROOT / 'output_c_mod_object' / "groups"
    output1_mod_objects = ROOT / 'output_c_mod_object' / "mod_objects"

    move_to_groups(input_single_api_model_object_responses, output0_mod_object_groups)
    group2mod_object(output0_mod_object_groups, output1_mod_objects)
