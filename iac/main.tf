# Variable
variable "environment" {
  description = "Nombre del entorno"
  type        = string
  default     = "dev"
}

# Recurso null_resource
resource "null_resource" "qa_platform_setup" {
  triggers = {
    environment = var.environment
  }
}
