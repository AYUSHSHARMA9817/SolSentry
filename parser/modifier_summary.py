class ModifierSummary:
    def __init__(self,name,mod):
        self.name = name
        self.access_control = False
        self.role_variable = None
        self.whitelist = False
        self.pause_guard = False
        self.reentrancy_guard = False

        for _,op,var in mod:
            if op == "require_condition":
                if "msg.sender ==" in var:
                    self.access_control = True
                    self.role_variable = var.split("==")[1].strip()

                if "[msg.sender]" in var:
                    self.whitelist = True

                if "!paused" in var:
                    self.pause_guard = True
                
    