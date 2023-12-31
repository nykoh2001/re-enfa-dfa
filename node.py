class Node:
    node_0 = None
    node_1 = None
    operator = None

    def __init__(self, exp):
        self.exp = exp

    def build_tree(self):

        length = len(self.exp)

        if length == 1:

            return

        i = 0
        paren_cnt = 0
        if self.exp[i] == "(":
            paren_cnt += 1

            while True:
                i += 1

                if self.exp[i] == "(":
                    paren_cnt += 1

                if self.exp[i] == ")":
                    paren_cnt -= 1

                    if paren_cnt <= 0:
                        break

        temp = i
        while True:

            if self.exp[i] == "+":
                self.node_0 = Node(self.exp[:i])
                self.node_1 = Node(self.exp[i + 1 :])
                self.operator = "+"
                self.node_0.build_tree()
                self.node_1.build_tree()
                return
            i += 1
            if i >= length:
                break
        i = temp
        while True:

            if self.exp[i] == "•":
                self.node_0 = Node(self.exp[:i])
                self.node_1 = Node(self.exp[i + 1 :])
                self.operator = "•"
                self.node_0.build_tree()
                self.node_1.build_tree()
                return
            i += 1
            if i >= length:
                break
        i = temp
        while True:

            if self.exp[i] == "*":
                self.node_0 = Node(self.exp[:i])
                self.operator = "*"
                self.node_0.build_tree()
                return
            i += 1
            if i >= length:
                break
        i = temp
        while True:

            if self.exp[i] == ")":
                self.node_0 = Node(self.exp[1 : length - 1])
                self.node_0.build_tree()
                return
            i += 1
            if i >= length:
                break
