# -*- coding: utf-8 -*-
# Author: zzl
# Date: 2024.07.15

from py2neo import Graph, Node, Relationship

"""
Neo4j基础操作类
"""
class Neo4jHelper(object):
def __init__(self, uri, user, password):
		self.graph = Graph(uri, auth=(user, password))
 
	def create_node(self, label, properties):
		node = Node(label, **properties)
		self.graph.create(node)
		return node
 
	def create_relationship(self, start_node, end_node, relationship_type, properties=None):
		rel = Relationship(start_node, relationship_type, end_node)
		if properties:
			for key, value in properties.items():
				setattr(rel, key, value)
		self.graph.create(rel)
		return rel

if __name__ == '__main__':
	pass