class FunctionSummary:

    def __init__(self, name, ops, modifiers,visibility,mutability):

        self.name = name
        self.reentrancy = False
        self.unchecked_call = False
        self.delegatecall = False
        self.access_control = False
        self.value_check = False
        self.eth_transfer = False
        self.visibility = visibility   
        self.mutability = mutability

        self.analyze(ops)
        self.apply_modifiers(modifiers)


    def analyze(self, ops):

        from detectors.reentrancy import detect_reentrancy, detect_state_after_call
        from detectors.unchecked_call import detect_unchecked_call
        from detectors.delegatecall import detect_delegatecall
        from detectors.access_control import access_control
        from detectors.value_check import value_check
        from detectors.eth_transfer import detect_eth_transfer

        self.reentrancy = detect_reentrancy(ops) or detect_state_after_call(ops)
        self.unchecked_call = detect_unchecked_call(ops)
        self.delegatecall = detect_delegatecall(ops)
        self.access_control = access_control(ops,self.visibility)
        self.value_check = value_check(ops)
        self.eth_transfer = detect_eth_transfer(ops)

    def apply_modifiers(self, modifiers):

        for mod in modifiers:

            if mod.access_control:
                self.access_control = True

            if mod.whitelist:
                self.access_control = True

            if mod.reentrancy_guard:
                self.reentrancy = False