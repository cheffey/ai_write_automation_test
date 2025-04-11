from concurrent.futures.thread import ThreadPoolExecutor

from constants import ROOT, llm_client
from utils.executor_man import ExecutorManager

if __name__ == '__main__':
    template = (ROOT / "b_api2mod_object/api2mod_object.template").read_text()
    example = (ROOT / "b_api2mod_object/api2mod_object.code_example").read_text()
    input_single_api_docs = ROOT / 'output_a_split_APIs'
    output_single_api_model_object_responses = ROOT / 'output_b_single_api_model_object'
    executor_manager = ExecutorManager(max_workers=10)
    for file in input_single_api_docs.iterdir():
        if file.is_file() and file.suffix == '.yaml':
            save_to = output_single_api_model_object_responses / f"{file.stem}.resp"
            if save_to.exists():
                continue
            print(f"ask {file}")
            api_doc = file.read_text()
            query = template.format(EXAMPLE=example, API_DOC=api_doc)
            executor_manager.submit(llm_client.ask, query, save_to=save_to, print_response=True)
    executor_manager.results(show_progress=True)
