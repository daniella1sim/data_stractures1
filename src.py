# username - simonovsky1
# id1      - 322721705
# name1    - Daniella Simonovsky
# id2      - 322430661
# name2    - Noam Shtrahman


from PrintTreeUtil import *
import random


class AVLNode(object):
    """A class representing a node in an AVL tree

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
        if node is None:  # creating virtual children for every node
            self.left = AVLNode(None, None)

        self.left = node
        return None

    """sets right child

	@type node: AVLNode
	@param node: a node
	"""

    def set_right(self, node):
        if node is None:  # creating virtual children for every node
            self.right = AVLNode(None, None)

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
        return self.get_key() is not None  # virtual nodes are the only nodes that have None as the key, value

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

    def set_bf(self):
        self.bf = self.get_left().get_height() - self.get_right().get_height()
        return None


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
	a Class representing an AVL tree
	"""

    def __init__(self):
        self.root = None
        self.max = None

    """searches for a value in the dictionary corresponding to the key, using a binary search starting from the root
    of the tree. if the node is not found None is returned

    time complexity: O(logn)

	@type key: int
	@param key: a key to be searched
	@rtype: any
	@returns: the value corresponding to key.
	"""

    def search(self, key):
        node = self.get_root()  # bst search starting at the root
        while node.get_key() != key:
            if not node.get_left().is_real_node() and not node.get_right().is_real_node():
                # we reached a leaf that is different than the required node
                return None
            elif node.get_key() < key:  # regular bst search pattern
                node = node.get_right()
            else:
                node = node.get_left()
        return node.get_value()

    """searches for a value in the dictionary corresponding to the key, using a finger tree search starting from the maximum
        of the tree. if the node is not found None is returned

        time complexity: O(logk), with k being the rank of the given node

    	@type key: int
    	@param key: a key to be searched
    	@rtype: any
    	@returns: the value corresponding to key.
    	"""

    def finger_search(self, key):
        max_node = self.max

        parent = max_node.get_parent()
        while key < parent.get_key():
            parent = parent.get_parent()

        tree = AVLTree()
        tree.set_root(parent)
        return tree.search(key)

    """" inserts a node to the tree as a leaf using regular BST insertion

    time complexity: O(logn)

    @type node: AVLNode
    @pre: node currently does not appear in the dictionary
    @rtype: int
    @returns: the height difference of the parent of the node before and after insertion 
    """

    def insert_as_usual(self, node, finger_flag):
        curr = self.get_root()   # starting at the root
        parent = None
        prev_height = 0
        cnt = 0

        if curr is None:  # the tree was empty and so node needs to be the new root
            self.set_root(node)
            self.max = node
            node.set_left(AVLNode(None, None))  # virtual kids
            node.set_right(AVLNode(None, None))
            node.get_left().set_parent(node)
            node.get_right().set_parent(node)
            self.reset_size(node)
            self.reset_height(node)
            return 0, 0  # the root has no parent to change height

        if finger_flag:
            curr = self.max

            while node.get_key() < curr.get_key() and curr.get_parent() is not None:
                curr = curr.get_parent()
                cnt += 1

        while curr.is_real_node():  # going down the tree to the correct position
            parent = curr
            cnt += 1
            if node.get_key() < curr.get_key():
                curr = curr.get_left()
            else:
                curr = curr.get_right()

        if parent is not None:  # saving the height before the insert to compare
            prev_height = parent.get_height()

        node.set_parent(parent)

        if node.get_key() < parent.get_key():  # inserting the node as a left or right leaf
            parent.set_left(node)
            node.set_parent(parent)
            node.set_left(AVLNode(None, None))
            node.set_right(AVLNode(None, None))
            node.get_left().set_parent(node)
            node.get_right().set_parent(node)
        else:
            parent.set_right(node)
            node.set_parent(parent)
            node.set_left(AVLNode(None, None))
            node.set_right(AVLNode(None, None))
            node.get_left().set_parent(node)
            node.get_right().set_parent(node)

        self.reset_size(node)
        self.reset_height(node)
        self.reset_height(parent)
        self.reset_size(parent)

        if finger_flag and node.get_key() > self.max.get_key():  ###
            self.max = node

        return parent.get_height() - prev_height, cnt
        # the new height minus the old one and the search counter for the theoretical part

    """inserts a new node with val, key to the dictionary using insertAsUsual,
    then rotates as needed to keep the correct balance factor for all nodes in the dictionary

    time complexity: O(logn)

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
    @type val: any
	@param val: the value of the item
	@rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, key, val, is_finger=False):
        cnt = 0
        node = AVLNode(key, val)  # creating a new node with the given parameters
        delta_height, search_cost = self.insert_as_usual(node, is_finger)  #inserting a leaf
        parent = node.get_parent()

        while parent is not None:
            parent.set_bf()
            bf = parent.get_bf()
            self.reset_size(parent)

            if 2 > bf > -2 and delta_height == 0:
                self.recursive_reset(parent)
                if is_finger:
                    return cnt + search_cost
                return cnt

            elif 2 > bf > -2 and delta_height != 0:
                cnt += 1

            else:  # preform rotations
                if bf == -2:
                    if parent.get_right().get_bf() == -1:  # left rotation
                        parent = self.left_rotation(parent)
                        cnt += 1
                    else:  # right_left rotation
                        parent.set_right(self.right_rotation(parent.get_right()))
                        parent = self.left_rotation(parent)
                        cnt += 2
                elif bf == 2:  # bf = 2
                    if parent.get_left().get_bf() == 1:
                        parent = self.right_rotation(parent)
                        cnt += 1
                    else:
                        parent.set_left(self.left_rotation(parent.get_left()))
                        parent = self.right_rotation(parent)
                        cnt += 2

            parent = parent.get_parent()
            if parent is None:
                break
            prev_height = parent.get_height()  # getting the height before the corrections
            self.reset_height(parent)
            delta_height = parent.get_height() - prev_height

        if is_finger:
            return cnt + search_cost
        return cnt

    """
	function rotates the tree in the non-clockwise direction

	time complexity: O(1)

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
        right_left.set_parent(node)

        if parent is not None:
            if parent.get_right().get_key() == node.get_key():
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

        time complexity: O(1)

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
        print("l ", node.get_left(), "ll ", node.get_left().get_left(), "r ", node.get_right(), "rr ",
              node.get_right().get_right(), "lr ", node.get_left().get_right(), "rl ", node.get_right().get_left())

        left_right.set_parent(node)

        if parent is not None:
            if parent.get_right().get_key() == node.get_key():
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

    """function resets the size of the given node using the size of its children

        time complexity: O(1)

    	@type node: AVLNode
    	@param node: the node before size correction
    	@rtype: None
		@returns: None
    """

    def reset_size(self, node):
        size = node.get_left().get_size() + node.get_right().get_size() + 1
        # getting size using the children parameters
        node.set_size(size)
        return None

    """function resets the height of the given node using the height of its children

    time complexity: O(1)

		@type node: AVLNode
		@param node: the node before height correction
		@rtype: None
		@returns: None
    """

    def reset_height(self, node):
        height = max(node.get_left().get_height(), node.get_right().get_height()) + 1
        node.set_height(height)
        return None

    """function resets the size, height and bf of the given node and all its ancestors up to the root
        using the parameters of its children

        time complexity: O(logn)

    		@type node: AVLNode
    		@param node: the node after rotations
        	@rtype: None
    		@returns: None
    """

    def recursive_reset(self, node):
        while node is not None:  # resetting size, height, bf for all the nodes in the path to the root
            self.reset_height(node)
            self.reset_size(node)
            node.set_bf()
            node = node.get_parent()

    """uses delete_like_bst to delete the node from the dictionary and then
    rebalances the tree to have correct bf values

    time complexity = O(logn)

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, node):
        cnt = 0

        if self.get_root().get_size() == 1:  # deleting a tree with only root
            self.set_root(None)
            self.max = None
            return 1

        delta_height, parent = self.delete_like_bst(node)  # deleting the node as usual

        while parent is not None:
            parent.set_bf()
            self.reset_size(node)

            if -2 < parent.get_bf() < 2 and delta_height == 0:  # if parent is unchanged check and correct up to root
                self.recursive_reset(parent)
                break

            elif -2 < parent.get_bf() < 2 and delta_height != 0:
                cnt += 1

            else:
                if parent.get_bf() == 2:
                    if parent.get_left().get_bf() == -1:  # left right rotation
                        parent.set_left(self.left_rotation(parent.get_left()))
                        parent = self.right_rotation(parent)
                        cnt += 2  # two rotations
                    else:
                        parent = self.right_rotation(parent)  # right rotation
                        cnt += 1

                elif parent.get_bf() == -2:
                    if parent.get_right().get_bf() == 1:  # right left rotation
                        parent.set_right(self.right_rotation(parent.get_right()))
                        parent = self.left_rotation(parent)
                        cnt += 2  # two rotations
                    else:  # left rotation
                        parent = self.left_rotation(parent)
                        cnt += 1

            parent = parent.get_parent()
            if parent is None:
                break
            prev_height = parent.get_height()
            self.reset_height(parent)
            delta_height = parent.get_height() - prev_height
        return cnt

    """deletes node from the dictionary as a BST delete

        time complexity = O(logn)

        @type node: AVLNode
        @pre: node is a real pointer to a node in self
        @rtype: int, AVLNode
        @returns: the height difference of the parent of the deleted node and the parent itself
        """

    def delete_like_bst(self, node):
        parent = node.get_parent()

        if node.get_key() == self.max.get_key():  ###
            self.max = self.predecessor(node)

        if not node.get_left().is_real_node() and not node.get_right().is_real_node():
            # node is leaf
            if node.get_key() == parent.get_right().get_key():
                parent.set_right(AVLNode(None, None))
                parent.get_right().set_parent(parent)
            else:
                # node is left child
                parent.set_left(AVLNode(None, None))
                parent.get_left().set_parent(parent)

        elif not node.get_left().is_real_node() and parent is not None:
            # node has only left child
            if node.get_key() == parent.get_right().get_key():
                parent.set_right(node.get_right())
                node.get_right().set_parent(parent)
            else:
                parent.set_left(node.get_right())
                node.get_right().set_parent(parent)

        elif not node.get_right().is_real_node() and parent is not None:
            # node has only right child
            if node == parent.get_right():
                parent.set_right(node.get_left())
                node.get_left().set_parent(parent)
            else:
                parent.set_left(node.get_left())
                node.get_left().set_parent(parent)

        else:  # node has both children
            near = self.succsessor(node)  # get the successor
            parent = near.get_parent()

            if parent.get_right().get_key() == near.get_key():  # successor is right child
                parent.set_right(near.get_right())
            else:
                parent.set_left(near.get_right())

            near.get_right().set_parent(parent)
            node.set_key(near.get_key())
            node.set_value(near.get_value())

        prev_height = parent.get_height()
        self.recursive_reset(parent)  # correct for unbalances up to root
        delta = parent.get_height() - prev_height
        return delta, parent

    """finds the successor of the given node according to the key in the dictionary

        time complexity = O(logn)

        @type node: AVLNode
        @pre: node is a real pointer to a node in self
        @rtype: AVLNode
        @returns: the successor of the given node
    """

    def succsessor(self, node):
        if node.get_right().is_real_node():  # node has a right child
            res = node.get_right()
            while res.get_left().is_real_node():
                res = res.get_left()
            return res
        else:  # node has no right child
            res = node.get_parent()
            while res is not None:
                if node != res.get_right():  # check if parent is smaller or larger
                    break
                node = res
                res = res.get_parent()
            return res

    """finds the predecessor of the given node according to the key in the dictionary

            time complexity = O(logn)

            @type node: AVLNode
            @pre: node is a real pointer to a node in self
            @rtype: AVLNode
            @returns: the predecessor of the given node
        """

    def predecessor(self, node):
        if node.get_left().is_real_node():
            res = node.get_left()
            while res.get_right().is_real_node():
                res = res.get_right()
            return res
        else:
            res = node.get_parent()
            while res is not None:
                if node != res.get_left():
                    break
                node = res
                res = res.get_parent()
            return res

    """returns an array representing dictionary 

    time complexity: O(n)

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

    time complexity: O(1)

	@rtype: int
	@returns: the number of items in dictionary 
	"""

    def size(self):
        return self.get_root().get_size()

    """splits the dictionary at a given node

    time complexity: O(logn)

	@type node: AVLNode
	@pre: node is in self
	@param node: The intended node in the dictionary according to whom we split
	@rtype: list
	@returns: a list [left, right], where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""

    def split(self, node):
        cnt = 0
        ops = 0
        leftTree = AVLTree()
        rightTree = AVLTree()

        parent = node.get_parent()

        leftTree.set_root(node.get_left())
        rightTree.set_root(node.get_right())

        while parent is not None:

            if node.get_key() == parent.get_right().get_key():  # parent is smaller than node
                ops += 1
                left = AVLTree()
                left.set_root(parent.get_left())
                node = parent
                parent = parent.get_parent()
                left.get_root().set_parent(None)
                cnt += leftTree.join(left, node.get_key(), node.get_value())  # join left with parent left subtree

            else:
                ops += 1
                right = AVLTree()
                right.set_root(parent.get_right())
                node = parent
                parent = parent.get_parent()
                right.get_root().set_parent(None)
                cnt += rightTree.join(right, node.get_key(), node.get_value())

        return cnt/ops, [leftTree, rightTree]

    """joins self with key and another AVLTree

    time complexity: O(logn)

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

        if not root.is_real_node() and not tree.get_root().is_real_node():
            # both trees are empty
            self.set_root(node)
            node.set_left(AVLNode(None, None))
            node.set_right(AVLNode(None, None))
            return 1

        if not root.is_real_node():  # only self is empty
            prev_height = tree.get_root().get_height()
            tree.insert(key, val)
            self.set_root(tree.get_root())
            return tree.get_root().get_height() - prev_height

        if not tree.get_root().is_real_node():  # only second tree is empty
            prev_height = root.get_height()
            self.insert(key, val)
            return root.get_height() - prev_height

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

        if self_is_shorter and self_is_smaller:  # case 1: find minimum of tree
            min_tree = tree.get_root()
            while min_tree.is_real_node() and min_tree.get_height() != min_height:
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

        if self_is_shorter and not self_is_smaller:  # case 2: find maximum of tree
            max_tree = tree.get_root()
            while max_tree.is_real_node() and max_tree.get_height() != min_height:
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

        if not self_is_shorter and self_is_smaller:  # case 3: find maximum of self
            max_self = root
            while max_self.is_real_node() and max_self.get_height() != min_height:
                max_self = max_self.get_right()

            parent = max_self.get_parent()
            node.set_right(tree.get_root())
            tree.get_root().set_parent(node)
            node.set_left(max_self)
            max_self.set_parent(node)
            parent.set_right(node)
            node.set_parent(parent)
            self.recursive_reset(node)

        if not self_is_shorter and not self_is_smaller:  # case 4: find minimum of self
            min_self = root

            while min_self.is_real_node() and min_self.get_height() >= min_height:
                min_self = min_self.get_left()

            parent = min_self.get_parent()
            node.set_left(tree.get_root())
            tree.get_root().set_parent(node)
            node.set_right(min_self)
            min_self.set_parent(node)
            parent.set_left(node)
            node.set_parent(parent)

        # balancing the tree
        while node is not None:
            self.reset_size(node)
            self.reset_height(node)
            node.set_bf()

            if node.get_bf() == -2:
                if node.get_right().get_bf() == -1:  # left rotation
                    node = self.left_rotation(node)
                else:  # right_left rotation
                    node.set_right(self.right_rotation(node.get_right()))



                    if not node.get_left().is_real_node():
                        fix_none(node.get_left())

                    if not node.get_right().is_real_node():
                        fix_none(node.get_right())



                    #print("l ", node.get_left(), "ll ", node.get_left().get_left(), "r ", node.get_right(), "rr ", node.get_right().get_right(), "lr ", node.get_left().get_right(),  "rl ", node.get_right().get_left())
                    node = self.left_rotation(node)
            elif node.get_bf == 2:
                if node.get_left().get_bf() == 1:  # right rotation
                    node = self.right_rotation(node)
                else:  # left_right rotation
                    node.set_left(self.left_rotation(node.get_left()))



                    if not node.get_left().is_real_node():
                        fix_none(node.get_left())

                    if not node.get_right().is_real_node():
                        fix_none(node.get_right())



                    node = self.right_rotation(node)
            node = node.get_parent()

        if self_is_shorter:  # absolute value
            return 1 + tree.get_root().get_height() - root.get_height()
        else:
            return 1 + root.get_height() - tree.get_root().get_height()


    def fix_none(self, node):
        if node.get_right() is None:
            node.set_right(AVLNode(None, None))
        if node.get_left() is None:
            node.set_left(AVLNode(None, None))

    """compute the rank of node in the self

    time complexity: O(logn)

	@type node: AVLNode
	@pre: node is in self
	@param node: a node in the dictionary which we want to compute its rank
	@rtype: int
	@returns: the rank of node in self
	"""

    def rank(self, node):
        if not node.get_left().is_real_node():  # smallest node in the tree
            r = 1
        else:
            r = node.get_left().get_size() + 1  # accumulate size of left subtrees
        while node.get_parent() is not None:
            if node == node.get_parent().get_right():
                if not node.get_parent().get_left().is_real_node():
                    r += 1
                else:
                    r += node.get_parent().get_left().get_size() + 1
            node = node.get_parent()
        return r

    """uses select_rec to find the i'th smallest node with the root of self

    time complexity: O(logn)

	@type i: int
	@pre: 1 <= i <= self.size()
	@param i: the rank to be selected in self
	@rtype: AVLNode
	@returns: the item of rank i in self
	"""

    def select(self, i):
        root = self.get_root()
        return self.select_rec(root, i)

    """finds the i'th smallest item (according to keys) in self

        time complexity: O(logn)

    	@type i: int
    	@pre: 1 <= i <= self.size()
    	@param i: the rank to be selected in self
    	@rtype: AVLNode
    	@returns: the item of rank i in self
    	"""

    def select_rec(self, node, i):
        if not node.is_real_node():
            return None

        if not node.get_left().is_real_node():  # smallest node
            curr_rank = 1
        else:
            curr_rank = node.get_left().get_size() + 1

        if i == curr_rank:  # check if finished
            return node
        elif i < curr_rank:
            return self.select_rec(node.get_left(), i)
        else:
            return self.select_rec(node.get_right(), i - curr_rank)

    """returns the root of the tree representing the dictionary

    time complexity: O(1)

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""

    def get_root(self):
        return self.root

    """sets node to be the root of the tree representing the dictionary

    time complexity: O(1)

    @rtype: None
    @returns: None
    """

    def set_root(self, node):
        self.root = node
        return None

    def __repr__(self):  # no need to understand the implementation of this one
        # return "tree"
        out = ""
        for row in printree(self.root):  # need printree.py file
            out = out + row + "\n"
        return out


def reverser(n):
    lst = []
    for i in range(n // 300):
        for j in range(300):
            lst.append(300 * (i + 1) - j)
    return lst


def count_switch(lst):
    cnt = 0
    for i in range(len(lst)):
        for j in range(len(lst)):
            if j > i and lst[j] < lst[i]:
                cnt += 1
    return cnt


def nisuy1():
    for j in range(1, 11):
        n = 1500 * (2 ** j)
        count_random_AVL = 0
        count_reverse_AVL = 0
        count_almost_reverse_AVL = 0

        random_lst = [i for i in range(n)]
        random.shuffle(random_lst)
        reverse_lst = [n - i for i in range(n)]
        almost_reverse_lst = reverser(n)

        random_tree = AVLTree()
        reverse_tree = AVLTree()
        almost_reverse_tree = AVLTree()
        count_random_switch = count_switch(random_lst)
        count_reverse_switch = count_switch(reverse_lst)
        count_almost_reverse_switch = count_switch(almost_reverse_lst)
        for i in range(n):
            count_random_AVL += random_tree.insert(random_lst[i], random_lst[i], True)
            count_reverse_AVL += reverse_tree.insert(reverse_lst[i], reverse_lst[i], True)
            count_almost_reverse_AVL += almost_reverse_tree.insert(almost_reverse_lst[i], almost_reverse_lst[i], True)

        print(j)
        print(f'random AVL count is: {count_random_AVL} and random switch count: {count_random_switch}')
        print(f'reverse AVL count is: {count_reverse_AVL} and reverse switch count: {count_reverse_switch}')
        print(f'almost reverse AVL count is: {count_almost_reverse_AVL} and almost reverse switch count: {count_almost_reverse_switch}')


def main():
    for j in range(50):
        n = 1500 * (2)

        random_lst = [i for i in range(n)]
        random_tree = AVLTree()
        random.shuffle(random_lst)
        for i in range(n):
            random_tree.insert(random_lst[i], random_lst[i])

        rand_node = random_tree.select(random.randrange(n))

        random_cnt, tree_arr = random_tree.split(rand_node)

        print(f'n is: {n} and mean cost for joins is {random_cnt}')

main()
