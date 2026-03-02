from typing import Dict, Any, List, Set

def prune_category_tree(
    base_category_tree: Dict[str, Any],
    products_flat: List[dict],
) -> tuple[Dict[str, Any], int]:
    """
    Removes categories whose URL does not appear in any product's categoryPath_ss.
    Preserves hierarchy.

    Returns:
        clean_category_tree (dict)
    """
    used_urls: Set[str] = set()

    for product in products_flat:
        for url in product.get("categoryPath_ss", []):
            used_urls.add(url)

    pruned_counter = 0

    def prune_node(node: Dict[str, Any]) -> Dict[str, Any] | None:
        nonlocal pruned_counter

        children = node.get("children", {})
        pruned_children = {}

        for child_name, child_node in children.items():
            pruned_child = prune_node(child_node)
            if pruned_child is not None:
                pruned_children[child_name] = pruned_child

        node["children"] = pruned_children
        node_url = node.get("url")

        if node_url in used_urls or len(pruned_children) > 0:
            return node

        pruned_counter += 1
        return None

    clean_tree = {}

    for name, node in base_category_tree.items():
        pruned = prune_node(node)
        if pruned is not None:
            clean_tree[name] = pruned

    return clean_tree, pruned_counter