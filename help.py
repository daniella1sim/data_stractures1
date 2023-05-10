
        def rotator(node, prev_height, cnt):
            bf = node.get_bf()

            if 2 > bf > -2 and node.get_height() == prev_height:
                return node

            elif 2 > bf > -2:  # check bf with node's parent
                node = node.get_parent()
                rotator(node, node.get_height(), cnt)

            else:  # preform rotations
                if bf == -2:
                    if node.get_right().get_bf() == -1:  # left rotation
                        node = node.left_rotation()
                        cnt += 1
                    else:  # right_left rotation
                        right_node = node.right_rotation()
                        node = right_node.left_rotaion()
                        cnt += 2
                else:  # bf = 2
                    if node.get_left().get_bf() == 1:
                        node = node.right_rotation()
                        cnt += 1
                    else:
                        left_node = node.left_rotation()
                        node = left_node.right_rotation()
                        cnt += 2
                # as written in slide 36 - check bf with node's parent
                node = node.get_parent()
                rotator(node, node.get_height(), cnt)
            return cnt

        def insert_as_bst(node, key, value, cnt):
            if not node.is_real_node():
                node.set_key(key)
                node.set_value(value)
                node.set_height(0)
                node.set_size(1)
                return 0, node

            prev_height = node.get_height()
            if key < node.get_key():
                print(key)
                print(type(node.get_left()))
                if node.get_left() is None:
                    node.set_left(AVLNode(key, value))
                    node.get_left().set_height(0)
                    node.get_left().set_size(1)
                cnt, left = insert_as_bst(node.get_left(), key, val, cnt)
                node.set_left(left)
            else:
                if node.get_right() is None:
                    node.set_right(AVLNode(key, value))
                    node.get_right().set_height(0)
                    node.get_right().set_size(1)
                cnt, right = insert_as_bst(node.get_right(), key, val, cnt)
                node.set_right(right)

            max_height = max(node.get_left().get_height(), node.get_right().get_height())
            node.set_height(1 + max_height)
            node.set_size(1 + node.get_left().get_size() + node.get_right().get_size())

            cnt += rotator(node, prev_height, cnt)
            return cnt, node

        cnt, node = insert_as_bst(self.get_root(), key, val, -1)
        print("it is", type(self.get_root()))
        print(self.get_root().get_key())
        self.set_root(node)
        return cnt