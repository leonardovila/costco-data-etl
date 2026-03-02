from typing import Dict, Any, List, Set

def prune_category_tree(
    base_category_tree: Dict[str, Any],
    products_flat: List[dict],
) -> Dict[str, Any]:
    """
    Removes categories whose URL does not appear in any product's categoryPath_ss.
    Preserves hierarchy.

    Returns:
        clean_category_tree (dict)
    """

    # 1️⃣ Collect all category URLs used by products
    used_urls: Set[str] = set()

    for product in products_flat:
        for url in product.get("categoryPath_ss", []):
            used_urls.add(url)

    # 3️⃣ Recursive pruning
    def prune_node(node: Dict[str, Any]) -> Dict[str, Any] | None:

        children = node.get("children", {})

        # Prune children first (post-order traversal)
        pruned_children = {}

        for child_name, child_node in children.items():
            pruned_child = prune_node(child_node)
            if pruned_child is not None:
                pruned_children[child_name] = pruned_child

        node["children"] = pruned_children

        node_url = node.get("url")

        # Node survives if:
        # - Has direct products
        # - OR has children surviving
        if node_url in used_urls or len(pruned_children) > 0:
            return node

        # Otherwise → remove node
        return None

    clean_tree = {}

    for name, node in base_category_tree.items():
        pruned = prune_node(node)
        if pruned is not None:
            clean_tree[name] = pruned

    return clean_tree