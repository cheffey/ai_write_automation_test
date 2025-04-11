import re

from constants import ROOT


def extract_interface(class_code):
    # 移除所有方法实现（包括docstring）
    # 保留方法签名和装饰器
    lines = class_code.split('\n')
    interface_lines = []
    in_method = False
    skip_until_indent = False
    last_pass_added = True

    for line in lines:
        stripped = line.strip()

        # 跳过空行
        if not stripped:
            continue

        # 处理类定义行
        if line.startswith('class '):
            interface_lines.append(line)
            continue

        # 处理装饰器
        if stripped.startswith('@'):
            if not last_pass_added:
                last_pass_added = True
                interface_lines.append('    pass\n')
            interface_lines.append(line)
            continue

        # 处理方法定义
        if (stripped.startswith('def ') or
                stripped.startswith('async def ') or
                stripped.startswith('@property')):
            if not last_pass_added:
                last_pass_added = True
                interface_lines.append('    pass\n')
            interface_lines.append(line)
            last_pass_added = False
            in_method = True
            skip_until_indent = False
            continue

        # 处理返回类型注解
        if stripped.startswith('->') and in_method:
            interface_lines[-1] += ' ' + stripped
            skip_until_indent = True
            continue

        # 跳过方法体
        if in_method and (line.startswith(' ') or line.startswith('\t')):
            if skip_until_indent:
                skip_until_indent = False
            continue
        else:
            in_method = False
            skip_until_indent = False

        # 添加pass语句
        if in_method and not skip_until_indent:
            interface_lines.append('    pass')
            in_method = False

    # 确保最后一个方法有pass
    if in_method:
        interface_lines.append('    pass')

    # 重新组合代码
    interface_code = '\n'.join(interface_lines)

    # 移除多余的空行
    interface_code = re.sub(r'\n{3,}', '\n\n', interface_code)

    return interface_code


if __name__ == '__main__':
    input_mod_objects = ROOT / 'output_c_mod_object' / "mod_objects"
    output_mod_objects = ROOT / 'output_d_mod_object_interface'
    output_mod_objects.mkdir(parents=True, exist_ok=True)
    for py_file in input_mod_objects.iterdir():
        if not py_file.is_file() or py_file.suffix != '.py':
            continue
        class_code = py_file.read_text()
        interface_code = extract_interface(class_code)
        output_file = output_mod_objects / py_file.name
        output_file.write_text(interface_code)
