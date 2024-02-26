import numpy as np 
from core.build.buildTree import buildPackedTree

class MeshBVH:
    def __init__(self, data):
        self.root = buildPackedTree(data)