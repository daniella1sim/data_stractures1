left_tree = AVLTree()
        right_tree = AVLTree()
        left_tree.set_root(node.get_left())
        right_tree.set_root(node.get_right())

        while node is not None:
            parent = node.get_parent()

            if parent is None:
                break

            elif parent.get_left() is not None:
                if parent.get_left().get_key() == node.get_key():
                    righty = AVLTree()
                    righty.set_root(parent.get_right())
                    righty.get_root().set_parent(None)
                    right_tree.join(righty, parent.get_key(), parent.get_value())
                else:
                    lefty = AVLTree()
                    lefty.set_root(parent.get_left())
                    lefty.get_root().set_parent(None)
                    left_tree.join(lefty, parent.get_key(), parent.get_value())

        return [left_tree, right_tree]