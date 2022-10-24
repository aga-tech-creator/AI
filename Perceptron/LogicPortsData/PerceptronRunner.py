import enum

class And:
    baseE = [
        [[0, 0], [0]], 
        [[0, 1], [0]], 
        [[1, 0], [0]], 
        [[1, 1], [1]]
    ]

class Or:
    baseE = [
        [[0, 0], [0]],
        [[0, 1], [1]],
        [[1, 0], [1]],
        [[1, 1], [1]]
    ]

class Xor:
    baseE = [
        [[0, 0], [0]],
        [[0, 1], [1]],
        [[1, 0], [1]],
        [[1, 1], [0]]
    ]

class Robot:
    baseE = [
        [[0, 0, 0], [1, 1]],
        [[0, 0, 1], [0, 1]],
        [[0, 1, 0], [1, 0]],
        [[0, 1, 1], [0, 1]],
        [[1, 0, 0], [1, 0]],
        [[1, 0, 1], [1, 0]],
        [[1, 1, 0], [1, 0]],
        [[1, 1, 1], [1, 0]]
    ]
