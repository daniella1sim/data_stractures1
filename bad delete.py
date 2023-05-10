def delete_rec(root, node):
    # delete like a regular bst
    if node.get_key() < root.get_key():
        delete_rec(root.get_left(), node)
    elif node.get_key() > root.get_key():
        delete_rec(root.get_right(), node)
    else:
        if root.get_parent().get_left() == root:  # left son
            if root.get_left() is None:
                root.get_parent().set_right(root.get_right())
                return cnt
            elif root.get_right() is None:
                root.get_parent().set_right(root.get_right())
                return cnt
            succ = self.succsessor(root)


count = 0
prev_height = node.get_parent().get_height()
self.delete_like_bst(self, node)
curr = node.get_parent()
max_height = max(curr.get_left().get_height(), curr.get_right().get_height())
curr.set_height(1 + max_height)

balance = self.get_bf(node)

if -2 < balance < 2:
    return count