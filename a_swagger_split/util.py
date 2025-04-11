import json
from copy import deepcopy


def tojson(obj):
    return json.dumps(obj, ensure_ascii=False)

def resolve_ref(ref_path, openapi_data):
    parts = ref_path.strip('#/').split('/')
    current = openapi_data
    for part in parts:
        current = current.get(part, {})
    return deepcopy(current)


def merge_schema(schema, openapi_data, refs=()):
    """递归合并 schema 中的引用（支持嵌套）"""
    if isinstance(schema, dict):
        _type = schema.get("type")
        if _type == 'string':
            return schema.get("title") or "str"
        if _type == 'integer':
            return "int"
        if _type == 'object':
            properties = schema.get('properties', {})
            if properties:
                return {k: merge_schema(v, openapi_data, refs) for k, v in properties.items()}
            return {}
        if _type == 'array':
            items = schema.get('items', {})
            if items:
                return [merge_schema(items, openapi_data, refs)]
            return []
        if '$ref' in schema:
            ref_path = schema['$ref']
            if ref_path in refs:
                # 避免循环引用
                return {"$ref": ref_path}
            ref_schema = resolve_ref(ref_path, openapi_data)
            # 合并属性和保留覆盖逻辑
            merged = merge_schema(ref_schema, openapi_data, refs + (ref_path,))
            merged.update({k: v for k, v in schema.items() if k != '$ref'})
            return merged
        else:
            return {k: merge_schema(v, openapi_data, refs) for k, v in schema.items()}
    elif isinstance(schema, list):
        return [merge_schema(item, openapi_data, refs + (0,)) for item in schema]
    return schema
