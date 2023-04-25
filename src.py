#username - simonovsky1
#id1      - 322721705
#name1    - Daniella Simonovsky
#id2      - 322430661
#name2    - Noam Shtrahman



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
		return self.get_left().get_height() - self.get_right().get_height()

"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.

	"""
	def __init__(self, root):
		self.root = root
		self.size = self.root.size
		self.height = self.root.height



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
	def insert(self, key, val):
		cnt = 0
		curr, prev_height = self.helper(key, val)
		prev = curr.get_parent()
		while prev.is_real_node():
			bf = prev.get_bf()
			if 2 > bf > -2 and prev_height == prev.get_height():
				return cnt
			elif 2 > bf > -2:
				curr = curr.get_parent()
				prev = prev.get_parent()
			else:
				#rotaion
				curr = curr.get_parent()
				prev = prev.get_parent()

		return -1


	def helper(self, key, val):
		curr = self.get_root()
		prev = curr
		while curr.is_real_node():
			if curr.get_key < key:
				curr = curr.get_right()
			else:
				curr = curr.get_left()

			prev = curr.get_parent()
			if prev.get_left().get_key() == curr.get_key():
				prev.set_bf(prev.get_bf() + 1)
			else:
				prev.set_bf(prev.get_bf() - 1)
		prev_height = prev.get_height()

		curr.set_key(key)
		curr.set_value(val)
		return curr, prev_height



	"""function rotates the tree in the non-clockwise direction
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
		return left



	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, node):
		return -1


	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		res = []
		return self.get_root().in_order(res)


	def in_order(self, arr):
		if self.get_left().get_key() is not None:
			self.get_left().in_order(arr)
		if self.get_key() is not None:
			arr.append((self.get_key(), self.get_value()))
		if self.get_right().get_key() is not None:
			self.get_right.in_order(arr)
		return arr


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
		return None
