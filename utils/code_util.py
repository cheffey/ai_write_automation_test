import re


def extract_code(resp, mark="python"):
    start_mark = f"```{mark}"
    end_mark = f"```"
    start_idx = resp.index(start_mark)
    end_idx = resp.index(end_mark, start_idx + len(start_mark))
    code = resp[start_idx + len(start_mark):end_idx].strip()
    return code


def split_code_by_class(code):
    classes = {}
    lines = code.split("\n")
    current_class_name = None
    current_class = []
    for line in lines:
        if line.startswith("class "):
            if current_class:
                code_block = "\n".join(current_class)
                classes[current_class_name] = code_block
            name0 = line.split()[1]
            name1 = name0.split("(")[0]
            name2 = name1.split(":")[0]
            current_class_name = name2
            current_class = [line]
        else:
            current_class.append(line)
    if current_class:
        code_block = "\n".join(current_class)
        classes[current_class_name] = code_block
    return classes


def camel_to_snake(name):
    s1 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name)
    return s1.lower()


def snake_to_camel(name):
    components = name.split('_')
    return ''.join(x.title() for x in components)
