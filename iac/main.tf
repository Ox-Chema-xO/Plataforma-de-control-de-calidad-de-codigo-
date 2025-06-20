# Recurso null_resource
resource "null_resource" "qa_platform_setup" {
  triggers = {
    environment  = var.environment
    project_name = var.project_name
    enable_debug = var.enable_debug ? "enabled" : "disabled"
  }
}

# Recurso para crear archivo de prueba
resource "null_resource" "file_creator" {
  # Aseguramos que se ejecute después del recurso principal
  depends_on = [null_resource.qa_platform_setup]

  # Provisioner que crea un archivo de texto
  provisioner "local-exec" {
    command = <<-EOT
      echo "Este archivo fue creado por Terraform como parte de las pruebas de infraestructura." > iac_dummy.txt
      echo "Configuración de Infraestructura:" >> iac_dummy.txt
      echo "- Entorno: ${var.environment}" >> iac_dummy.txt
      echo "- Proyecto: ${var.project_name}" >> iac_dummy.txt
      echo "- Debug: ${var.enable_debug ? "enabled" : "disabled"}" >> iac_dummy.txt
      echo "- Timestamp: $(date)" >> iac_dummy.txt
    EOT
  }
}
