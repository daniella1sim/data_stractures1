# username - simonovsky1
# id1      - 322721705
# name1    - Daniella Simonovsky
# id2      - 322430661
# name2    - Noam Shtrahman

"""A class represnting a node in an AVL tree"""
from PrintTreeUtil import *
import random


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

	@param key: int or None
	@param key: key of your node
	@type value: any
	@param value: data of your node
	"""

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0
        self.size = 1
        self.bf = 0

    """returns the key

	@rtype: int or None
	@returns: the key of self, None if the node is virtual
	"""

    def get_key(self):
        return self.key

    """returns the value

	@rtype: any
	@returns: the value of self, None if the node is virtual
	"""

    def get_value(self):
        return self.value

    """returns the left child

	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child (if self is virtual)
	"""

    def get_left(self):
        return self.left

    """returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child (if self is virtual)
	"""

    def get_right(self):
        return self.right

    """returns the parent 

	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
	"""

    def get_parent(self):
        return self.parent

    """returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	"""

    def get_height(self):
        if not self.is_real_node():
            return -1
        return self.height

    """returns the size of the subtree

	@rtype: int
	@returns: the size of the subtree of self, 0 if the node is virtual
	"""

    def get_size(self):
        return self.size

    """sets key

	@type key: int or None
	@param key: key
	"""

    def set_key(self, key):
        self.key = key
        return None

    """sets value

	@type value: any
	@param value: data
	"""

    def set_value(self, value):
        self.value = value
        return None

    """sets left child

	@type node: AVLNode
	@param node: a node
	"""

    def set_left(self, node):
        self.left = node
        return None

    """sets right child

	@type node: AVLNode
	@param node: a node
	"""

    def set_right(self, node):
        self.right = node
        return None

    """sets parent

	@type node: AVLNode
	@param node: a node
	"""

    def set_parent(self, node):
        self.parent = node
        return None

    """sets the height of the node

	@type h: int
	@param h: the height
	"""

    def set_height(self, h):
        self.height = h
        return None

    """sets the size of node

	@type s: int
	@param s: the size
	"""

    def set_size(self, s):
        self.size = s
        return None

    """returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""

    def is_real_node(self):
        return self.key is not None

    """returns the balance factor of a node

		@rtype: int
		@returns: the balance factor of a node #think about what to do if a node is virtual
		"""

    def get_bf(self):
        return self.bf

    """sets balance factor for node

		@type s: int
		@param s: the balance factor
		"""

    def set_bf(self, *args):
        if self.get_left() is None and self.get_right() is None:
            self.bf = 0
        elif self.get_left() is None:
            self.bf = 0 - self.get_right().get_height() - 1
        elif self.get_right() is None:
            self.bf = 1 + self.get_left().get_height()
        else:
            self.bf = self.get_left().get_height() - self.get_right().get_height()

        return None


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
	Constructor, you are allowed to add more fields.

	"""

    def __init__(self):
        self.root = None

    """searches for a value in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: any
	@returns: the value corresponding to key.
	"""

    def search(self, key):
        node = self.get_root()
        while node.get_key() != key:
            if node.get_left() is None and node.get_right() is None:
                return None
            elif node.get_key() < key:
                node = node.get_right()
            else:
                node = node.get_left()
        return node.get_value()

    """inserts val at position i in the dictionary

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: any
	@param val: the value of the item
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""

    def insert_as_usual(self, node):
        curr = self.get_root()
        parent = None
        prev_height = 0

        while curr is not None:
            parent = curr
            if node.get_key() < curr.get_key():
                curr = curr.get_left()
            else:
                curr = curr.get_right()

        if parent is not None:
            prev_height = parent.get_height()

        node.set_parent(parent)

        if parent is None:
            self.set_root(node)
            return 0

        elif node.get_key() < parent.get_key():
            parent.set_left(node)
            node.set_parent(parent)
        else:
            parent.set_right(node)
            node.set_parent(parent)

        self.reset_height(parent)
        self.reset_size(parent)

        return parent.get_height() - prev_height

    def insert(self, key, val):
        count = 0
        node = AVLNode(key, val)
        delta_height = self.insert_as_usual(node)
        parent = node.get_parent()

        while parent is not None:
            parent.set_bf()
            bf = parent.get_bf()
            self.reset_size(parent)

            if 2 > bf > -2 and delta_height == 0:
                self.recursive_reset(parent)
                return count

            else:  # preform rotations
                if bf == -2:
                    if parent.get_right().get_bf() == -1:  # left rotation
                        parent = self.left_rotation(parent)
                        count += 1
                    else:  # right_left rotation
                        parent = self.right_left_rotation(parent)
                        count += 2
                elif bf == 2:  # bf = 2
                    if parent.get_left().get_bf() == 1:
                        parent = self.right_rotation(parent)
                        count += 1
                    else:
                        parent = self.left_right_rotation(parent)
                        count += 2

            parent = parent.get_parent()
            if parent is None:
                break
            prev_height = parent.get_height()
            self.reset_height(parent)
            delta_height = parent.get_height() - prev_height


        return count

    """
	function rotates the tree in the non-clockwise direction
	@type node: AVLNode
	@param node: the inserted node before rotation
	@rtype: AVLNode
	@returns: rotated nodes in new order
	"""

    def left_rotation(self, node):
        parent = node.get_parent()

        right = node.get_right()
        right_left = right.get_left()
        right.set_left(node)
        node.set_right(right_left)

        node.set_parent(right)
        right.set_parent(parent)

        if right_left is not None:
            right_left.set_parent(node)
        if parent is not None:
            if parent.get_right() is not None and parent.get_right().get_key() == node.get_key():
                parent.set_right(right)
            else:
                parent.set_left(right)
        else:
            self.set_root(right)

        self.reset_height(node)
        self.reset_height(right)
        self.reset_size(node)
        self.reset_size(right)
        node.set_bf()
        right.set_bf()

        return right

    """function rotates the tree in the clockwise direction
		@type node: AVLNode
		@param node: the inserted node before rotation
		@rtype: AVLNode
		@returns: rotated nodes in new order
		"""

    def right_rotation(self, node):
        parent = node.get_parent()
        left = node.get_left()
        left_right = left.get_right()

        left.set_right(node)
        node.set_left(left_right)
        node.set_parent(left)
        left.set_parent(parent)

        if left_right is not None:
            left_right.set_parent(node)
        if parent is not None:
            if parent.get_right() is not None and parent.get_right().get_key() == node.get_key():
                parent.set_right(left)
            else:
                parent.set_left(left)
        else:
            self.set_root(left)

        self.reset_height(node)
        self.reset_height(left)
        self.reset_size(node)
        self.reset_size(left)
        node.set_bf()
        left.set_bf()

        return left

    def left_right_rotation(self, node):
        parent = node.get_parent()
        left = node.get_left()  # a
        left_right = left.get_right()  # b
        left_right_right = left_right.get_right()  # br
        left_right_left = left_right.get_left()  # bl

        left_right.set_parent(parent)
        left_right.set_right(node)
        node.set_parent(left_right)
        node.set_left(left_right_left)
        if left_right_left is not None:
            left_right_left.set_parent(node)

        left_right.set_left(left)
        left.set_parent(left_right)
        left.set_right(left_right_right)
        if left_right_left is not None:
            left_right_left.set_parent(left)

        if parent is not None:
            if parent.get_right() is not None and parent.get_right().get_key() == node.get_key():
                parent.set_right(left_right)
            else:
                parent.set_left(left_right)
        else:
            self.set_root(left_right)

        self.reset_height(node)
        self.reset_height(left)
        self.reset_height(left_right)
        self.reset_size(node)
        self.reset_size(left)
        self.reset_size(left_right)
        node.set_bf()
        left.set_bf()
        left_right.set_bf()

        return left_right

    def right_left_rotation(self, node):
        parent = node.get_parent()
        right = node.get_right()
        right_left = right.get_left()
        right_left_right = right_left.get_right()
        right_left_left = right_left.get_left()

        right_left.set_parent(parent)
        right_left.set_left(node)
        node.set_parent(right_left)
        node.set_right(right_left_right)
        if right_left_right is not None:
            right_left_right.set_parent(node)

        right_left.set_right(right)
        right.set_parent(right_left)
        right.set_left(right_left_left)
        if right_left_left is not None:
            right_left_left.set_parent(right)

        if parent is not None:
            if parent.get_right() is not None and parent.get_right().get_key() == node.get_key():
                parent.set_right(right_left)
            else:
                parent.set_left(right_left)
        else:
            self.set_root(right_left)

        self.reset_height(node)
        self.reset_height(right)
        self.reset_height(right_left)
        self.reset_size(node)
        self.reset_size(right)
        self.reset_size(right_left)
        node.set_bf()
        right.set_bf()
        right_left.set_bf()

        return right_left

    def reset_size(self, node):
        if node.get_left() is None and node.get_right() is None:
            node.set_size(1)
        elif node.get_right() is None:
            node.set_size(node.get_left().get_size() + 1)
        elif node.get_left() is None:
            node.set_size(node.get_right().get_size() + 1)
        else:
            size = node.get_left().get_size() + node.get_right().get_size() + 1
            node.set_size(size)

        return None

    def reset_height(self, node):
        if node.get_left() is None and node.get_right() is None:
            node.set_height(0)
        elif node.get_right() is None:
            node.set_height(node.get_left().get_height() + 1)
        elif node.get_left() is None:
            node.set_height(node.get_right().get_height() + 1)
        else:
            height = max(node.get_left().get_height(), node.get_right().get_height()) + 1
            node.set_height(height)

        return None

    def recursive_reset(self,node):
        while node is not None:
            self.reset_height(node)
            self.reset_size(node)
            node.set_bf()
            node = node.get_parent()

    """deletes node from the dictionary
    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, node):
        cnt = 0
        delta_height ,parent = self.delete_like_bst(node)

        while parent is not None:
            parent.set_bf()
            self.reset_size(node)

            if -2 < parent.get_bf() < 2 and delta_height == 0:
                self.recursive_reset(parent)
                break

            else:
                if parent.get_bf() == 2:
                    if parent.get_left().get_bf() == -1:
                        parent = self.left_right_rotation(parent)
                        cnt += 2
                    else:
                        parent = self.right_rotation(parent)
                        cnt += 1

                elif parent.get_bf() == -2:
                    if parent.get_right().get_bf() == 1:
                        parent = self.right_left_rotation(parent)
                        cnt += 2
                    else:
                        parent = self.left_rotation(parent)
                        cnt += 1

            parent = parent.get_parent()
            if parent is None:
                break
            prev_height = parent.get_height()
            self.reset_height(parent)
            delta_height = parent.get_height() - prev_height
        return cnt



    def delete_like_bst(self, node):
        parent = node.get_parent()
        if node.get_left() is None and node.get_right() is None:
            if node == parent.get_right():
                parent.set_right(None)
            else:
                parent.set_left(None)

        elif node.get_left() is None:
            if node == parent.get_right():
                parent.set_right(node.get_right())
                node.get_right().set_parent(parent)
            else:
                parent.set_left(node.get_right())
                node.get_right().set_parent(parent)

        elif node.get_right() is None:
            if node == parent.get_right():
                parent.set_right(node.get_left())
                node.get_left().set_parent(parent)
            else:
                parent.set_left(node.get_left())
                node.get_left().set_parent(parent)

        else:
            near = self.succsessor(node)
            parent = near.get_parent()

            if parent.get_right().get_key() == near.get_key():
                parent.set_right(near.get_right())
            else:
                parent.set_left(near.get_right())

            if near.get_right() is not None:
                near.get_right().set_parent(parent)
            node.set_key(near.get_key())
            node.set_value(near.get_value())

        prev_height = parent.get_height()
        self.recursive_reset(parent)
        delta = parent.get_height() - prev_height
        return delta, parent

    def succsessor(self, node):
        if node.get_right() is not None:
            res = node.get_right()
            while res.get_left() is not None:
                res = res.get_left()
            return res
        else:
            res = node.get_parent()
            while res is not None:
                if node != res.get_right():
                    break
                node = res
                res = res.get_parent()
            return res

    """returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""

    def avl_to_array(self):
        def inorder_rec(node):
            if node is None:
                return []
            return inorder_rec(node.get_left()) + [node.get_key()] + inorder_rec(node.get_right())

        return inorder_rec(self.get_root())

    """returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""

    def size(self):
        return self.get_root().get_size()

    """splits the dictionary at a given node

	@type node: AVLNode
	@pre: node is in self
	@param node: The intended node in the dictionary according to whom we split
	@rtype: list
	@returns: a list [left, right], where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""

    def split(self, node):
        left_tree = AVLTree()
        right_tree = AVLTree()
        left_tree.set_root(node.get_left())
        right_tree.set_root(node.get_right())

        while node is not None:
            parent = node.get_parent()
            if parent is None:
                break

            elif parent.get_left() is not None:
                if parent.get_left().get_key() <= node.get_key():
                    if right_tree.get_root() is None:
                        parent = self.right_rotation(parent)
                        right_tree.set_root(parent)
                        parent.set_parent(None)
                    else:
                        left = AVLTree()
                        left.set_root(parent.get_left())
                        left.get_root().set_parent(None)
                        left_tree.join(left, parent.get_key(), parent.get_value())

                else:
                    if left_tree.get_root() is None:
                        parent = self.left_rotation(parent)
                        left_tree.set_root(parent)
                        parent.set_parent(None)
                    else:
                        right = AVLTree()
                        right.set_root(parent.get_right())
                        right.get_root().set_parent(None)
                        right_tree.join(right, parent.get_key(), parent.get_value())

        return [left_tree, right_tree]


    """joins self with key and another AVLTree

	@type tree: AVLTree 
	@param tree: a dictionary to be joined with self
	@type key: int 
	@param key: The key separting self with tree
	@type val: any 
	@param val: The value attached to key
	@pre: all keys in self are smaller than key and all keys in tree are larger than key,
	or the other way around.
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""

    def join(self, tree, key, val):
        node = AVLNode(key, val)
        root = self.get_root()
        self_is_shorter = True
        self_is_smaller = True
        if root.get_key() > key:
            self_is_smaller = False

        if root.get_height() == tree.get_root().get_height():
            self.set_root(node)
            if self_is_smaller:
                node.set_left(root)
                root.set_parent(node)
                node.set_right(tree.get_root())
                tree.get_root().set_parent(node)

            else:
                node.set_right(root)
                root.set_parent(node)
                node.set_left(tree.get_root())
                tree.get_root().set_parent(node)

            self.reset_height(node)
            self.reset_size(node)
            node.set_bf()

            return 0

        min_height = min(root.get_height(), tree.get_root().get_height())
        if root.get_height() > min_height:
            self_is_shorter = False

        if self_is_shorter and self_is_smaller:
            min_tree = tree.get_root()
            while min_tree.get_height() != min_height:
                min_tree = min_tree.get_left()

            parent = min_tree.get_parent()

            node.set_left(root)
            root.set_parent(node)
            node.set_right(min_tree)
            min_tree.set_parent(node)
            parent.set_left(node)
            node.set_parent(parent)
            self.set_root(tree.get_root())
            self.recursive_reset(node)

        if self_is_shorter and not self_is_smaller:
            max_tree = tree.get_root()
            while max_tree.get_height() != min_height:
                max_tree = max_tree.get_right()

            parent = max_tree.get_parent()
            node.set_right(root)
            root.set_parent(node)
            node.set_left(max_tree)
            max_tree.set_parent(node)
            parent.set_right(node)
            node.set_parent(parent)
            self.set_root(tree.get_root())
            self.recursive_reset(node)

        if not self_is_shorter and self_is_smaller:
            max_self = root
            while max_self.get_height() != min_height:
                max_self = max_self.get_right()

            parent = max_self.get_parent()
            node.set_right(tree.get_root())
            tree.get_root().set_parent(node)
            node.set_left(max_self)
            max_self.set_parent(node)
            parent.set_right(node)
            node.set_parent(parent)
            self.recursive_reset(node)

        if not self_is_shorter and not self_is_smaller:
            min_self = root
            while min_self.get_height() != min_height:
                min_self = min_self.get_left()

            parent = min_self.get_parent()
            node.set_left(tree.get_root())
            tree.get_root().set_parent(node)
            node.set_right(min_self)
            min_self.set_parent(node)
            parent.set_left(node)
            node.set_parent(parent)

        ###balancing the tree
        while node is not None:
            self.reset_size(node)
            self.reset_height(node)
            node.set_bf()

            if node.get_bf() == -2:
                if node.get_right().get_bf() == -1:  # left rotation
                    node = self.left_rotation(node)
                else:  # right_left rotation
                    node = self.right_left_rotation(node)
            elif node.get_bf == 2:  # bf = 2
                if node.get_left().get_bf() == 1:
                    node = self.right_rotation(node)
                else:
                    node = self.left_right_rotation(node)
            node = node.get_parent()




        if self_is_shorter:
            return tree.get_root().get_height() - root.get_height()
        else:
            return root.get_height() - tree.get_root().get_height()


    """compute the rank of node in the self

	@type node: AVLNode
	@pre: node is in self
	@param node: a node in the dictionary which we want to compute its rank
	@rtype: int
	@returns: the rank of node in self
	"""

    def rank(self, node):
        if node.get_left() is None:
            r = 1
        else:
            r = node.get_left().get_size() + 1
        while node.get_parent() is not None:
            if node == node.get_parent().get_right():
                if node.get_parent().get_left() is None:
                    r += 1
                else:
                    r += node.get_parent().get_left().get_size() + 1
            node = node.get_parent()
        return r

    """finds the i'th smallest item (according to keys) in self

	@type i: int
	@pre: 1 <= i <= self.size()
	@param i: the rank to be selected in self
	@rtype: int
	@returns: the item of rank i in self
	"""

    def select(self, i):
        root = self.get_root()

        def select_rec(node, i):
            if node is None:
                return None

            if node.get_left() is None:
                curr_rank = 1
            else:
                curr_rank = node.get_left().get_size() + 1

            if i == curr_rank:
                return node
            elif i < curr_rank:
                return select_rec(node.get_left(), i)
            else:
                return select_rec(node.get_right(), i - curr_rank)

        return select_rec(root, i)

    """returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""

    def get_root(self):
        return self.root

    def set_root(self, node):
        self.root = node
        return None

    def __repr__(self):  # no need to understand the implementation of this one
        # return "tree"
       out = ""
       for row in printree(self.root):  # need printree.py file
           out = out + row + "\n"
       return out


def main():
    tree = AVLTree()
    for i in range(10):
        tree.insert(2**i+1, 2**i+1)

    node = tree.select(5)
    tree1 = tree.split(node)

    print(tree1)


main()
