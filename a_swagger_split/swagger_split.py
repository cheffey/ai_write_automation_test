import os
import yaml

from a_swagger_split.util import merge_schema, tojson
from constants import ROOT

template = """path: {path}
method: {method}
request_schema: {request_schema}
response_schema: {response_schema}
"""


def split_openapi(data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for path, methods in data['paths'].items():
        for method, details in methods.items():
            # 处理请求参数
            request_schema = {}
            if 'requestBody' in details:
                content = details['requestBody'].get('content', {})
                if 'application/json' in content:
                    request_schema = merge_schema(
                        content['application/json'].get('schema', {}),
                        data
                    )

            # 处理响应参数
            response_schema = {}
            if 'responses' in details:
                content = details['responses'].get('200', {}).get('content', {})
                if 'application/json' in content:
                    response_schema = merge_schema(
                        content['application/json'].get('schema', {}),
                        data
                    )

            # 生成文件名（处理路径中的特殊字符）
            safe_path = path.replace('/', '_').replace('{', '').replace('}', '')
            filename = f"{safe_path}_{method}.yaml"

            # 写入文件
            content = template.format(
                path=path,
                method=method.upper(),
                request_schema=tojson(request_schema),
                response_schema=tojson(response_schema),
            )
            with open(f"{output_dir}/{filename}", 'w', encoding='utf-8') as f:
                f.write(content)


if __name__ == '__main__':
    with open(ROOT / 'a_swagger_split/swagger_example.yaml', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    output_dir = ROOT / 'output_a_split_APIs'
    split_openapi(data, output_dir)
