# Recurso null_resource
resource "null_resource" "qa_platform_setup" {
  triggers = {
    environment  = var.environment
    project_name = var.project_name
    enable_debug = var.enable_debug ? "enabled" : "disabled"
  }
}
