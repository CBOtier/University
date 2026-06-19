class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def find_max(root):
    if root is None:
        return float('-inf')
    
    left_max = find_max(root.left)
    right_max = find_max(root.right)
    
    return max(root.val, left_max, right_max)


# Пример из задачи:
#         1
#        / \
#       3   5
#      / \ / \
#     8  10 2  6
#    / \   |  / \
#   14 15  3  0  1

root = TreeNode(1)
root.left = TreeNode(3)
root.right = TreeNode(5)
root.left.left = TreeNode(8)
root.left.right = TreeNode(10)
root.right.left = TreeNode(2)
root.right.right = TreeNode(6)
root.left.left.left = TreeNode(14)
root.left.left.right = TreeNode(15)
root.left.right.left = TreeNode(3)
root.right.right.left = TreeNode(0)
root.right.right.right = TreeNode(1)

print("Максимальная яркость:", find_max(root))  # Ожидаем: 15
