# username - simonovsky1
# id1      - 322721705
# name1    - Daniella Simonovsky
# id2      - 322430661
# name2    - Noam Shtrahman
import printTree
from printTree import *

"""A class represnting a node in an AVL tree"""


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
        self.height = -1
        self.size = 0
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
        curr = self
        while curr.key != key:
            if curr.left is None and curr.right is None:
                return None
            elif curr.key < key:
                curr = curr.right
            else:
                curr = curr.left
        return curr.value

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
        while curr is not None:
            parent = curr
            prev_height = parent.get_height()
            if node.get_key() < curr.get_key():
                curr = curr.get_left()
            else:
                curr = curr.get_right()

        node.set_parent(parent)
        node.set_size(1)
        node.set_height(0)

        if parent is None:
            self.set_root(node)
            return 0

        elif node.get_key() < parent.get_key():
            parent.set_left(node)
            node.set_parent(parent)
        else:
            parent.set_right(node)
            node.set_parent(parent)


        if parent.get_left() is None and parent.get_right() is None:
            height = 0
        elif parent.get_left() is None:
            height = parent.get_right().get_height() + 1
        elif parent.get_right() is None:
            height = parent.get_left().get_height() + 1
        else:
            height = max(parent.get_left().get_height(), parent.get_right().get_height()) + 1

        parent.set_height(height)
        parent.set_size(parent.get_size() + 1)

        return parent.get_height() - prev_height

    def insert(self, key, val):
        count = 0
        node = AVLNode(key, val)
        delta_height = self.insert_as_usual(node)
        parent = node.get_parent()
        while parent is not None:
            parent.set_bf()
            bf = parent.get_bf()

            if 2 > bf > -2 and delta_height == 0:
                return count

            elif 2 > bf > -2 and delta_height != 0:
                parent = parent.get_parent()
                if parent is None:
                    continue
                prev_height = parent.get_height()
                height = max(parent.get_left().get_height(), parent.get_right().get_height()) + 1
                parent.set_height(height)
                delta_height = parent.get_height() - prev_height
                parent.set_size(parent.get_size() + 1)

            else:  # preform rotations
                if bf == -2:
                    if node.get_right().get_bf() == -1:  # left rotation
                        node = node.left_rotation()
                        count += 1
                    else:  # right_left rotation
                        right_node = node.right_rotation()
                        node = right_node.left_rotaion()
                        count += 2
                else:  # bf = 2
                    if node.get_left().get_bf() == 1:
                        node = node.right_rotation()
                        count += 1
                    else:
                        left_node = node.left_rotation()
                        node = left_node.right_rotation()
                        count += 2

                parent = parent.get_parent()
                parent.set_size(parent.get_size() + 1)

        return count

    """

	function rotates the tree in the non-clockwise direction
	@type node: AVLNode
	@param node: the inserted node before rotation
	@rtype: AVLNode
	@returns: rotated nodes in new order
	"""

    def left_rotation(self, node):
        right = node.get_right()
        right_left = right.get_left()
        right.set_left(node)
        node.set_right(right_left)
        max_height = max(node.get_left().get_height(), right_left.get_height())
        max_right_height = max(node.get_height(), right.get_right().get_height())
        node.set_height(1 + max_height)
        right.set_height(1 + max_right_height)
        return right

    """function rotates the tree in the clockwise direction
		@type node: AVLNode
		@param node: the inserted node before rotation
		@rtype: AVLNode
		@returns: rotated nodes in new order
		"""

    def right_rotation(self, node):
        left = node.get_left()
        left_right = left.get_right()
        left.set_right(node)
        node.set_left(left_right)

        max_height = max(node.get_right().get_height(), left_right.get_height())
        max_right_height = max(left.get_left().get_height(), node.get_height())
        node.set_height(1 + max_height)
        left.set_height(1 + max_right_height)

        node.set_size(node.get_right().get_size() + node.get_left().get_size() + 1)
        left.set_size(node.get_size() + left.get_left().get_size() + 1)

        return left

    """deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""

    def delete(self, node):
        curr = self.root
        cnt = 0

        def delete_rec(root, node):
            # delete like a regular bst
            if node.get_key() < root.get_key():
                delete_rec(root.get_left(), node)
            elif node.get_key() > root.get_key():
                delete_rec(root.get_right(), node)
            else:
                if root.get_parent().get_left() == root:  # left son
                    if not self.is_real_node(root.get_left()):
                        root.get_parent().set_right(root.get_right())
                        return cnt
                    elif not self.is_real_node(root.get_right()):
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

    def delete_like_bst(self, node):
        parent = node.get_parent()
        if not self.is_real_node(node.get_left()) and not self.is_real_node(node.get_right()):
            if node == parent.get_right():
                node.parent.set_right = None
            else:
                node.parent.set_left = None



        elif not self.is_real_node(node.get_left):
            if node == parent.get_right:
                parent.set_right = node.get_right
            else:
                parent.set_left = node.get_right



        elif not self.is_real_node(node.get_right):
            if node == parent.get_right:
                parent.set_right = node.get_left
            else:
                parent.set_left = node.get_left


        else:
            succ = self.succsessor(node)
            parent = succ.get_parent
            parent.set_left(succ.get_right)
            self.reset_height(parent)
            node.set_key(succ.get_key)
            node.set_value(succ.get_value)

        return parent

    def succsessor(self, node):
        res = node
        if self.is_real_node(res.get_right):
            res = node.get_right
            while self.is_real_node(res):
                res = res.get_left
            return res
        else:
            res = node.get_parent
            while not self.is_real_node(res.get_right):
                res = res.get_parent
            return res.get_right

    """returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""

    def avl_to_array(self):
        def inorder_rec(node):
            if not node.is_real_node:
                return []
            return inorder_rec(node.get_left) + [node.get_key] + inorder_rec(node.get_right)

        inorder_rec(self.get_root())

    """returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""

    def size(self):
        return self.rec_size()

        def rec_size(self):
            if not self.is_real_node():
                return 0
            return 1 + rec_size(self.get_left) + rec_size(self.get_right)

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
        left_tree = AVLTree().set_root(node.left)
        right_tree = AVLTree().set_root(node.right)
        while node is not None:
            if node.get_parent.get_left == node:
                right_tree.join(AVLTree(node.get_parent.get_right), node.get_parent.get_key, node.get_parent.get_value)
            else:
                left_tree.join(AVLTree(node.get_parent.get_left), node.get_parent.get_key, node.get_parent.get_value)

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
        self_is_shorter = True
        self_is_smaller = True
        short = 0
        if self.get_root().get_key > key:
            self_is_smaller = False
        if self.get_root.get_height <= tree.get_root.get_height:
            short = self.get_root.get_height
        else:
            short = tree.get_root.get_height
            self_is_shorter = False

        if self_is_shorter and self_is_smaller:
            min_in_tree = tree.get_root
            while min_in_tree.get_height != short:
                min_in_tree = min_in_tree.get_left

            parent = min_in_tree.get_parent
            node.set_left(self.get_root())
            node.set_right(min_in_tree)
            parent.set_left(node)

        if self_is_shorter and not self_is_smaller:
            max_of_tree = tree.get_root
            while max_of_tree.get_height != short:
                max_of_tree = max_of_tree.get_right

            parent = max_of_tree.get_parent
            node.set_right(self.get_root())
            node.set_left(max_of_tree)
            parent.set_right(node)

        if not self_is_shorter and self_is_smaller:
            max_of_self = self.get_root
            while max_of_self.get_height != short:
                max_of_self = max_of_self.get_right

            parent = max_of_self.get_parent
            node.set_right(tree.get_root())
            node.set_left(max_of_self)
            parent.set_right(node)

        if not self_is_shorter and not self_is_smaller:
            min_in_self = self.get_root
            while min_in_self.get_height != short:
                min_in_self = min_in_self.get_left

            parent = min_in_self.get_parent
            node.set_left(tree.get_root())
            node.set_right(min_in_self)
            parent.set_left(node)

        if self_is_shorter:
            return tree.get_root.get_height - self.get_root().get_height
        else:
            return self.get_root.get_height() - tree.get_root().get_height

    """compute the rank of node in the self

	@type node: AVLNode
	@pre: node is in self
	@param node: a node in the dictionary which we want to compute its rank
	@rtype: int
	@returns: the rank of node in self
	"""

    def rank(self, node):
        r = node.get_left.get_size + 1
        curr = node
        while curr is not None:
            if curr == curr.get_parent.get_right:
                r = r + curr.get_parent.get_left.get_size + 1
            curr = curr.get_parent
        return r

    """finds the i'th smallest item (according to keys) in self

	@type i: int
	@pre: 1 <= i <= self.size()
	@param i: the rank to be selected in self
	@rtype: int
	@returns: the item of rank i in self
	"""

    def select(self, i):
        node = self.get_root()

        def select_rec(node, i):
            rank = node.get_left.get_size + 1
            if rank == i:
                return node
            elif rank > i:
                return select_rec(node.get_left(), i)
            else:
                return select_rec(node.get_right(), i - rank)

        select_rec(node, i)

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
    tree.insert(10, 10)
    tree.insert(12, 12)
    tree.insert(8, 8)
    tree.insert(5, 5)
    tree.insert(20, 20)
    tree.insert(9, 9)
    tree.insert(11, 11)
    print(tree)


main()
