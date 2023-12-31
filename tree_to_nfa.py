import re

p = re.compile("[A-Za-z0-9]")


def isTerm(c):
    return p.match(c)


class State:
    def __init__(self):
        self.next_state = {}


class NFA:
    def __init__(self):
        self.delta_funcs: list(DeltaFunc) = []
        self.state_set = []
        self.symbols = set()
        self.start_state = "q000"
        self.final_state = None

    def add_func(self, func):
        self.delta_funcs.append(func)
        self.symbols.add(func.symbol)

    def print_NFA(self):
        print("StateSet = {", ", ".join(sorted(self.state_set)), "}")
        print("DeltaFunctions = {")
        for d in self.delta_funcs:
            print("   ", end="")
            d.print_delta()
        print("}")
        print("StartState = q000")
        print("FinalStateSet = {", self.final_state, "}")


class DeltaFunc:
    def __init__(self, state, symbol, next_state):
        self.state = state
        self.symbol = symbol
        self.next = next_state

    def print_delta(self):
        print(f"({self.state}, {self.symbol}) = {{{', '.join(self.next)}}}")


def convert(node):
    if node.type == 1:
        return convertSymbol(node)
    elif node.type == 2:
        return convertConcat(node)
    elif node.type == 3:
        return convertUnion(node)
    elif node.type == 4:
        return convertSTAR(node)


def convertSymbol(node):
    i_state = State()
    f_state = State()

    # 터미널 심볼(또는 입실론)으로 아크 연결
    i_state.next_state[node.value] = [f_state]

    return i_state, f_state


def convertConcat(node):
    # • 연산자 왼쪽의 종결 -> • 연산자 오른쪽의 시작과 연결
    left_node = convert(node.node_0)
    right_node = convert(node.node_1)

    left_node[1].next_state["ε"] = [right_node[0]]
    return left_node[0], right_node[1]


def convertUnion(node):
    # i, f 추가
    i_state = State()
    f_state = State()

    upper_node = convert(node.node_0)
    lower_node = convert(node.node_1)

    # epsilon-arc 연결
    i_state.next_state["ε"] = [upper_node[0], lower_node[0]]
    upper_node[1].next_state["ε"] = [f_state]
    lower_node[1].next_state["ε"] = [f_state]

    return i_state, f_state


def convertSTAR(node):
    # i, f 추가
    i_state = State()
    f_state = State()

    recursive_node = convert(node.node_0)

    # epsilon-arc 연결
    i_state.next_state["ε"] = [recursive_node[0], f_state]
    recursive_node[1].next_state["ε"] = [recursive_node[0], f_state]

    return i_state, f_state


def access_states(state, visited, symbol_table, NFA):
    # dfs 알고리즘
    if state in visited:
        return

    visited.append(state)
    NFA.state_set.append("q" + str(symbol_table[state]).zfill(3))

    for symbol in list(state.next_state):
        nfa_state = "q" + str(symbol_table[state]).zfill(3)
        next_states = []
        for ns in state.next_state[symbol]:
            if ns not in symbol_table:
                symbol_table[ns] = 1 + sorted(symbol_table.values())[-1]
            next_states.append("q" + str(symbol_table[ns]).zfill(3))
        NFA.add_func(DeltaFunc(nfa_state, symbol, next_states))
        for ns in state.next_state[symbol]:
            access_states(ns, visited, symbol_table, NFA)
