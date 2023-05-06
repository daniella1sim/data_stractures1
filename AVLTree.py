# username - complete info
# id1      - complete info
# name1    - complete info
# id2      - complete info
# name2    - complete info

from PrintTreeUtil import *

"""A class represnting a node in an AVL tree"""


class AVLNode(object):

    def __init__(self, key, value, parent):
        self.key = key
        self.value = value
        self.parent = parent
        self.size = 0
        self.height = 0
        if key is not None:
            self.left = AVLNode(None, None, self)
            self.right = AVLNode(None, None, self)
        else:
            self.left = None
            self.right = None

    def __repr__(self):  # no need to understand the implementation of this one
        return f"key={self.key} value={self.value}"

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

    def get_is_right(self):
        if self.parent is not None:
            return self.parent.get_right() is self

    """sets key
    @type key: int or None
    @param key: key
    """

    def set_key(self, key):
        self.key = key

    """sets value
    @type value: any
    @param value: data
    """

    def set_value(self, value):
        self.value = value

    """sets left child
    @type node: AVLNode
    @param node: a node
    """

    def set_left(self, node):
        self.left = node

    """sets right child
    @type node: AVLNode
    @param node: a node
    """

    def set_right(self, node):
        self.right = node

    """sets parent
    @type node: AVLNode
    @param node: a node
    """

    def set_parent(self, node):
        self.parent = node

    """sets the height of the node
    @type h: int
    @param h: the height
    """

    def set_height(self, h):
        self.height = h

    """sets the size of node
    @type s: int
    @param s: the size
    """

    def set_size(self, s):
        self.size = s

    """returns whether self is not a virtual node 
    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    #
    # def get_depth(self):
    #     return self.depth
    #
    # def set_depth(self, d):
    #     self.depth = d

    def is_real_node(self):
        return self.key is not None

    def get_balance(self):
        if not self.is_real_node():
            return None
        return self.get_left().get_height() - self.get_right().get_height()

    def is_leaf(self):
        return not self.is_real_node()

    def set_child(self, old_child, new_child):
        if old_child is self.right:
            self.set_right(new_child)
        elif old_child is self.left:
            self.set_left(new_child)

    # if self.left.is_leaf() and self.right.is_leaf()


# child_to_insert = self.left
# if key > self.key:
#     child_to_insert = self.right
# if child_to_insert.is_leaf():
#     child_to_insert = AVLNode(key=key, value=val, parent=self)
# else:
#     child_to_insert.insert(key, val)


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.
    """

    def __init__(self):
        self.root = None
        self.size = 0

    # add your fields here

    """searches for a value in the dictionary corresponding to the key
    @type key: int
    @param key: a key to be searched
    @rtype: any
    @returns: the value corresponding to key.
    """

    def search(self, key):
        if self.root is None:
            return None
        node = self.root
        while node.get_key() is not None:
            if key == node.key:
                return node
            elif key > node.key:
                node = node.right
            elif key < node.key:
                node = node.left
        return None

    """inserts val at position i in the dictionary
    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: any
    @param val: the value of the item
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, key, val):
        # BST insertion
        if self.root is None:
            self.root = AVLNode(key=key, value=val, parent=None)
        else:
            inserted = self.bst_insert_rec(node=self.root, key=key, val=val)
            heights_updated_count = self.update_parents_height(inserted.get_parent(), inserted)
            print()
            return self.manage_rotation_after_insert(inserted, heights_updated_count)

    def manage_rotation_after_insert(self, inserted, height_updated_count):
        loop_counter = height_updated_count
        parent = inserted.get_parent()
        # algorithm exactly as pseudo code in presentation - can be refactoed with for loop probably
        while parent is not None:
            loop_counter -= 1
            balance = parent.get_balance()
            if abs(balance) < 2 and loop_counter == 0:
                return 0
            elif abs(balance) < 2 and loop_counter > 0:
                parent = parent.get_parent()
            else:  # balance ==2
                criminal_parent_before_rotation = parent.get_parent()
                self.rotate_after_insert(criminal=parent)
                height_to_update = criminal_parent_before_rotation
                # fix all heights starting from original criminal's parent
                for i in range(height_updated_count - 2):
                    if height_to_update is None:
                        break
                    height_to_update.set_height(height_to_update.get_height() - 1)
                    height_to_update = height_to_update.get_parent()
                return 1
        return 0

    def rotate_after_insert(self, criminal):
        if criminal.get_balance() == -2:
            right_child_balance = criminal.get_right().get_balance()
            if right_child_balance == -1:
                self.left_rotation(criminal)
            elif right_child_balance == 1:
                self.right_left_rotation(criminal)
        elif criminal.get_balance() == 2:
            left_child_balance = criminal.get_left().get_balance()
            if left_child_balance == -1:
                self.left_right_rotation(criminal)
            elif left_child_balance == 1:
                self.right_rotation(criminal)

    def left_rotation(self, criminal):
        print("left rotation")
        parent = criminal.get_parent()
        criminal_replacer = criminal.get_right()
        # update the criminal's parent child pointer
        if parent is not None:
            parent.set_child(criminal, criminal_replacer)
        else:
            self.root = criminal_replacer
        # update the criminal's parent
        criminal.set_parent(criminal_replacer)
        #
        criminal.set_right(criminal_replacer.get_left())
        criminal_replacer.get_left().set_parent(criminal.get_right())
        # update the replacer of the criminal
        criminal_replacer.set_left(criminal)
        criminal_replacer.set_parent(parent)
        # fix heights
        criminal.set_height(criminal.get_height() - 2)
        # fix sizes
        criminal_original_size = criminal.get_size()
        criminal.set_size(criminal.get_size() - 2 - criminal_replacer.get_right().get_size())
        criminal_replacer.set_size(criminal_original_size)

    def right_rotation(self, criminal):
        print("right rotation")
        parent = criminal.get_parent()
        criminal_replacer = criminal.get_left()
        # update the criminal's parent child pointer
        if parent is not None:
            parent.set_child(criminal, criminal_replacer)
        else:
            self.root = criminal_replacer
        # update the criminal's parent
        criminal.set_parent(criminal_replacer)
        #
        criminal.set_left(criminal_replacer.get_right())
        criminal_replacer.get_right().set_parent(criminal.get_left())
        # update the replacer of the criminal
        criminal_replacer.set_right(criminal)
        criminal_replacer.set_parent(parent)
        # fix heights
        criminal.set_height(criminal.get_height() - 2)
        # fix sizes
        criminal_original_size = criminal.get_size()
        criminal.set_size(criminal.get_size() - 2 - criminal_replacer.get_left().get_size())
        criminal_replacer.set_size(criminal_original_size)

    def left_right_rotation(self, criminal):
        print("left right rotation")
        parent = criminal.get_parent()
        criminal_replacer = criminal.get_left().get_right()
        # update the criminal's parent child pointer
        if parent is not None:
            parent.set_child(criminal, criminal_replacer)
        else:
            self.root = criminal_replacer
        criminal_replacer.set_parent(parent)

        new_left = criminal.get_left()
        new_right = criminal

        # store new sizes for later
        criminal_new_size = criminal.get_right().get_size() + criminal_replacer.get_right().get_size()
        new_left_new_size = (new_left.get_size() - 1 - criminal_replacer.get_right().get_size())
        criminal_replacer_new_size = criminal.get_size()

        criminal_replacer.get_left().set_parent(criminal.get_left())
        criminal.get_left().set_right(criminal_replacer.get_left())

        criminal_replacer.get_right().set_parent(criminal)
        criminal.set_left(criminal_replacer.get_right())

        criminal_replacer.set_left(new_left)
        new_left.set_parent(criminal_replacer)

        criminal_replacer.set_right(new_right)
        new_right.set_parent(criminal_replacer)
        # Fix heights
        criminal_replacer.set_height(criminal.get_height() - 1)
        criminal.set_height(criminal.get_right().get_height() + 1)
        new_left.set_height(new_left.get_height() - 1)

        # Fix sizes
        criminal.set_size(criminal_new_size)
        if new_left is not None:
            new_left.set_size(new_left_new_size)
        criminal_replacer.set_size(criminal_replacer_new_size)

    def right_left_rotation(self, criminal):
        print("right left rotation")
        parent = criminal.get_parent()
        criminal_replacer = criminal.get_right().get_left()
        # update the criminal's parent child pointer
        if parent is not None:
            parent.set_child(criminal, criminal_replacer)
        else:
            self.root = criminal_replacer
        criminal_replacer.set_parent(parent)

        new_right = criminal.get_right()
        new_left = criminal

        # store new sizes for later
        criminal_new_size = criminal.get_left().get_size() + criminal_replacer.get_left().get_size()
        new_right_new_size = (new_right.get_size() - 1 - criminal_replacer.get_left().get_size())
        criminal_replacer_new_size = criminal.get_size()


        criminal_replacer.get_right().set_parent(criminal.get_right())
        criminal.get_right().set_left(criminal_replacer.get_right())

        criminal_replacer.get_left().set_parent(criminal)
        criminal.set_right(criminal_replacer.get_left())

        criminal_replacer.set_right(new_right)
        new_right.set_parent(criminal_replacer)

        criminal_replacer.set_left(new_left)
        new_left.set_parent(criminal_replacer)
        # Fix heights
        criminal_replacer.set_height(criminal.get_height() - 1)
        criminal.set_height(criminal.get_left().get_height() + 1)
        new_right.set_height(new_right.get_height() - 1)

        # Fix sizes
        criminal.set_size(criminal_new_size)
        if new_right is not None:
            new_right.set_size(new_right_new_size)
        criminal_replacer.set_size(criminal_replacer_new_size)

    def bst_insert_rec(self, node, key, val):
        res = None
        if key == node.get_key():
            node.value = val
            return node
        else:
            if key > node.get_key():
                if node.get_right().is_leaf():
                    res = AVLNode(key=key, value=val, parent=node)
                    node.set_right(res)
                else:
                    res = self.bst_insert_rec(node.get_right(), key, val)
            else:
                if node.get_left().is_leaf():
                    res = AVLNode(key=key, value=val, parent=node)
                    node.set_left(res)
                else:
                    res = self.bst_insert_rec(node.get_left(), key, val)
        node.size += 1
        return res

    """
    updates all the parents heights and returns
    """

    def update_parents_height(self, parent, updated_child_node, parents_updated=0):
        other_child = parent.get_right()
        if updated_child_node.get_is_right():
            other_child = parent.get_left()

        if not other_child.is_real_node() or updated_child_node.get_height() > other_child.get_height():
            parent.set_height(parent.get_height() + 1)
            parents_updated += 1
            if self.root != parent:
                return self.update_parents_height(parent.get_parent(), parent, parents_updated)
            else:
                return parents_updated
        else:
            return parents_updated

    """deletes node from the dictionary
    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, node):
        return 0

    """returns an array representing dictionary 
    @rtype: list
    @returns: a sorted list according to key of touples (key, value) representing the data structure
    """

    def avl_to_array(self):
        if self.root is None:
            return []
        res = []

        def in_order(node):
            in_order(node.get_left())
            if node.key is not None:
                res.append((node.get_key(), node.get_value()))
            in_order(node.get_right())

        in_order(self.root)
        return res

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
        return None

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
        return None

    """compute the rank of node in the self
    @type node: AVLNode
    @pre: node is in self
    @param node: a node in the dictionary which we want to compute its rank
    @rtype: int
    @returns: the rank of node in self
    """

    def rank(self, node):
        return None

    """finds the i'th smallest item (according to keys) in self
    @type i: int
    @pre: 1 <= i <= self.size()
    @param i: the rank to be selected in self
    @rtype: int
    @returns: the item of rank i in self
    """

    def select(self, i):
        return None

    """returns the root of the tree representing the dictionary
    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        return self.root

    def __repr__(self):  # no need to understand the implementation of this one
        # return "tree"
        out = ""
        for row in printree(self.root):  # need printree.py file
            out = out + row + "\n"
        return out
