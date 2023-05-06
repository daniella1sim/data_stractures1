def split(self, node):
    left_tree = AVLTree()
    right_tree = AVLTree()
    if node.get_left() is not None:
        self.split_rec(node.get_left(), node, True, left_tree, right_tree)
    if node.get_right() is not None:
        self.split_rec(node.get_right(), node, False, left_tree, right_tree)
    return [left_tree, right_tree]


def split_rec(self, root, node, is_left, left, right):
    key = node.get_key()
    value = node.get_value()
    if root is None:
        return None
    if root.get_key() <= key:
        if is_left:
            left.insert(key, value)
        else:
            right.insert(key, value)
        return self.split_rec(root.get_right(), node, False, left, right)

    elif root.get_key() > key:
        if is_left:
            right.insert(key, value)
        else:
            left.insert(key, value)
        return self.split_rec(root.get_left(), node, False, left, right)
