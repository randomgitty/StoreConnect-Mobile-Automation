def get_approvers_for_amount(amount, matrix_config, module_name):
    """
    Given an amount and module name, returns the list of required approvers.
    """
    for rule in matrix_config[module_name]:
        min_val, max_val = map(float, rule["range"].split('-'))
        if min_val <= amount <= max_val:
            return rule["approvers"]
    raise ValueError(f"No rule found for amount {amount} in module {module_name}")