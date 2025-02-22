import argparse
import os
import re
import yaml

def parse_table(text):

    text = text.strip()
    if text.startswith("#|"):
        text = text[2:]
    if text.endswith("|#"):
        text = text[:-2]
    
    parts = [part.strip() for part in text.split("||") if part.strip()]
    
    data = []
    for row in parts[1:]:
        cells = [cell.strip() for cell in row.split("|") if cell.strip()]
        if len(cells) >= 2:
            data.append({
                "method": cells[0],
                "description": cells[1]
            })
    return data

def generate_paths(data):
    import re

    def clean_method_name(method_name):
        if method_name.startswith("["):
            end_bracket = method_name.find("]")
            if end_bracket != -1:
                return method_name[1:end_bracket]
        return method_name

    paths = {}
    for entry in data:
        raw_method = entry["method"]
        method_name = clean_method_name(raw_method)
        if re.search(r'[а-яА-Я]', method_name):
            continue

        description = entry["description"]
        path = "/" + method_name
        tag = method_name.split('.')[0] if '.' in method_name else method_name
        paths[path] = {
            "post": {
                "tags": [tag],
                "summary": description,
                "responses": {
                    "200": {
                        "description": "Successful operation"
                    }
                }
            }
        }
    return paths

def load_main_openapi(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    else:
        return {
            "openapi": "3.0.3",
            "info": {
                "title": "Bitrix24 API",
                "version": "1.0"
            },
            "servers": [
                {"url": "https://github.com/estvita"}
            ],
            "paths": {}
        }

def find_tables_in_file(file_path):
    tables = []
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        matches = re.findall(r'(#\|.*?\|#)', content, re.DOTALL)
        for match in matches:
            if "|| **Метод** | **Описание** ||" in match:
                tables.append(match)
    return tables

def find_tables_in_directory(root_dir):
    all_tables = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower() == "index.md":
                file_path = os.path.join(dirpath, filename)
                tables = find_tables_in_file(file_path)
                if tables:
                    all_tables.extend(tables)
    return all_tables

if __name__ == "__main__":
    parser = argparse.ArgumentParser( )
    parser.add_argument("input_dir", nargs="?", default="b24-rest-docs/api-reference")
    parser.add_argument("-o", "--output_file", default="swagger.yaml")
    args = parser.parse_args()
    
    table_texts = find_tables_in_directory(args.input_dir)
    
    all_data = []
    for table in table_texts:
        data = parse_table(table)
        all_data.extend(data)
    
    new_paths = generate_paths(all_data)
    
    main_openapi = load_main_openapi(args.output_file)
    
    main_openapi["paths"].update(new_paths)
    
    with open(args.output_file, "w", encoding="utf-8") as f:
        yaml.dump(main_openapi, f, sort_keys=False, allow_unicode=True)