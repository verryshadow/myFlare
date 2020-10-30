endpoints = {"Patient": [str(i) for i in range(1000, 1030)],
             "Observation": [f'M-{i}' for i in range(1000, 1172)] + [f'O-{i}' for i in range(1000, 1622)],
             "Encounter": [str(i) for i in range(1000, 1036)]}


def get_temp_file_path(obj_id: str, obj_type) -> str:
    return f'temp/{obj_type}/{obj_id}.xml'
