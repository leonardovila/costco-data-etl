from typing import List, Dict, Any

def build_category_tree(parsed_megamenu: List[dict]) -> Dict[str, Any]:
    """
    Build hierarchical category tree from parsed_megamenu.

    Returns:
        dict representing the category tree.
        Same structure as before, but without any IO side effects.
    """

    root = {}

    for entry in parsed_megamenu:
        path = entry["path"]
        url = entry["url"]
        level = entry["level"]

        current_level = root

        for i, node_name in enumerate(path):

            if node_name not in current_level:
                current_level[node_name] = {
                    "name": node_name,
                    "url": None,
                    "level": None,
                    "children": {}
                }

            if i == len(path) - 1:
                current_level[node_name]["url"] = url
                current_level[node_name]["level"] = level

            current_level = current_level[node_name]["children"]

    return root