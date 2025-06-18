import hcl2


def test_terraform_syntax_validation():
    """Valida sintaxis HCL2 del archivo main.tf"""
    with open("iac/main.tf", 'r') as file:
        terraform_config = hcl2.load(file)
    
    assert terraform_config is not None
