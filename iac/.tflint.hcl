plugin "terraform" {
  enabled = true
}

rule "terraform_deprecated_interpolation" {
  enabled = true  
}

rule "terraform_deprecated_index" {
  enabled = true 
}

rule "terraform_unused_declarations" {
  enabled = true
}

rule "terraform_comment_syntax" {
  enabled = true
}

rule "terraform_required_version" {
  enabled = true
}

rule "terraform_required_providers" {
  enabled = true
}
