class BasicBlock:

    def __init__(self, block_id):
        self.block_id = block_id
        self.instructions = []
        self.next_blocks = []
        self.prev_blocks = []
        self.isTerminal = False

    def add_instruction(self, op):
        self.instructions.append(op)

    def add_next(self, block):

        if self.isTerminal:
            return

        if block not in self.next_blocks:
            self.next_blocks.append(block)
            block.prev_blocks.append(self)


def cfg(ops, calls):

    blocks = []
    exit_blocks = []

    current_block = BasicBlock(0)
    blocks.append(current_block)

    if_stack = []
    loop_stack = []

    for op in ops:

        _, opr, called_fun = op

        # ---------------- IF ----------------
        if opr == "IF_COND":

            current_block.add_instruction(op)

            true_block = BasicBlock(len(blocks))
            blocks.append(true_block)

            current_block.add_next(true_block)

            if_stack.append({
                "if_block": current_block,
                "true_block": true_block,
                "false_block": None
            })

            current_block = true_block

        elif opr == "ELSE":

            ctx = if_stack[-1]

            false_block = BasicBlock(len(blocks))
            blocks.append(false_block)

            ctx["if_block"].add_next(false_block)
            ctx["false_block"] = false_block

            current_block = false_block

        elif opr == "ENDIF":

            ctx = if_stack.pop()

            merge_block = BasicBlock(len(blocks))
            blocks.append(merge_block)

            ctx["true_block"].add_next(merge_block)

            if ctx["false_block"]:
                ctx["false_block"].add_next(merge_block)
            else:
                ctx["if_block"].add_next(merge_block)

            current_block = merge_block

        # ---------------- FOR ----------------
        elif opr == "FOR_COND":

            current_block.add_instruction(op)

            cond_block = current_block

            body_block = BasicBlock(len(blocks))
            blocks.append(body_block)

            after_block = BasicBlock(len(blocks))
            blocks.append(after_block)

            cond_block.add_next(body_block)
            cond_block.add_next(after_block)

            loop_stack.append({
                "cond": cond_block,
                "after": after_block
            })

            current_block = body_block

        elif opr == "ENDFOR":

            ctx = loop_stack.pop()

            current_block.add_next(ctx["cond"])

            current_block = ctx["after"]

        # ---------------- WHILE ----------------
        elif opr == "WHILE_COND":

            current_block.add_instruction(op)

            cond_block = current_block

            body_block = BasicBlock(len(blocks))
            blocks.append(body_block)

            after_block = BasicBlock(len(blocks))
            blocks.append(after_block)

            cond_block.add_next(body_block)
            cond_block.add_next(after_block)

            loop_stack.append({
                "cond": cond_block,
                "after": after_block
            })

            current_block = body_block

        elif opr == "ENDWHILE":

            ctx = loop_stack.pop()

            current_block.add_next(ctx["cond"])

            current_block = ctx["after"]

        # ---------------- BREAK ----------------
        elif opr == "BREAK":

            ctx = loop_stack[-1]

            current_block.add_instruction(op)
            current_block.add_next(ctx["after"])

            new_block = BasicBlock(len(blocks))
            blocks.append(new_block)

            current_block = new_block

        # ---------------- CONTINUE ----------------
        elif opr == "CONTINUE":

            ctx = loop_stack[-1]

            current_block.add_instruction(op)
            current_block.add_next(ctx["cond"])

            new_block = BasicBlock(len(blocks))
            blocks.append(new_block)

            current_block = new_block

        # ---------------- RETURN ----------------
        elif opr == "RETURN":

            current_block.add_instruction(op)

            current_block.isTerminal = True

            current_block = None

        # ---------------- FUNCTION CALL ----------------
        elif opr == "function_call":

            call_block = current_block
            call_block.add_instruction(op)

            return_block = BasicBlock(len(blocks))
            blocks.append(return_block)

            call_block.add_next(return_block)

            calls.append({
                "block": call_block,
                "called_func": called_fun,
                "return_block": return_block
            })

            current_block = return_block

        # ---------------- REQUIRE ----------------

        elif opr == "require_condition":

            current_block.add_instruction(op)

            success_block = BasicBlock(len(blocks))
            blocks.append(success_block)

            revert_block = BasicBlock(len(blocks))
            blocks.append(revert_block)

            revert_block.isTerminal = True

            current_block.add_next(success_block)
            current_block.add_next(revert_block)

            current_block = success_block

        # ---------------- REVERT ----------------
        elif (opr == "function_call" and called_fun == "revert"):

            current_block.add_instruction(op)

            current_block.isTerminal = True

            new_block = BasicBlock(len(blocks))
            blocks.append(new_block)

            current_block = new_block

        # ---------------- NORMAL ----------------
        else:

            current_block.add_instruction(op)

    for ex_block in blocks:
        if(len(ex_block.next_blocks) == 0):
            exit_blocks.append(ex_block)

    return blocks, exit_blocks