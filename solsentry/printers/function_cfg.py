from solsentry.ir.ast_walker import analyze_function
from solsentry.cfg.basic_blocks import cfg, BasicBlock

from graphviz import Digraph

def flow_graph(functions, state_set):

    unresolved_calls = []
    function_map = {}
    function_blocks = {}
    function_exits = {}

    for func in functions:

        name = func.get("name") or "constructor"

        ops = analyze_function(func, state_set)

        blocks, exits = cfg(ops, unresolved_calls)

        function_blocks[name] = blocks
        function_map[name] = blocks[0]   # entry block
        function_exits[name] = exits

    # resolve calls
    for call in unresolved_calls:

        block = call["block"]
        called = call["called_func"]
        ret = call["return_block"]

        if called in function_map:
            entry = function_map[called]
            exit = function_exits[called]

            block.add_next(entry)

            for ex in exit:
                ex.add_next(ret)

    visualize_program_cfg(function_blocks)

def visualize_program_cfg(function_blocks, filename="program_cfg"):

    dot = Digraph(engine="dot")
    dot.attr(overlap="false")
    dot.attr(splines="line")      # avoid spline routing bug
    dot.attr(rankdir="LR")

    # nodes
    for func, blocks in function_blocks.items():
        for b in blocks:
            node = f"{func}_{b.block_id}"

            label = f"{func}:{b.block_id}\\l"
            for instr in b.instructions:
                label += f"{instr}\\l"

            dot.node(node, label=label, shape="box")

    # edges
    for func, blocks in function_blocks.items():
        for b in blocks:
            src = f"{func}_{b.block_id}"
            for nxt in b.next_blocks:
                for f2, blks in function_blocks.items():
                    if nxt in blks:
                        dst = f"{f2}_{nxt.block_id}"
                        dot.edge(src, dst)
                        break

    dot.render(filename, format="png", cleanup=True)