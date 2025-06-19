variable "environment" {
  description = "Entorno de despliegue (dev, test, prod)"
  type        = string
  default     = "dev"
  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "El valor de environment debe ser 'dev', 'test', o 'prod'."
  }
}

variable "project_name" {
  description = "Nombre del proyecto para recursos y etiquetado"
  type        = string
  default     = "calidad-code"
}

variable "enable_debug" {
  description = "Habilita funcionalidades de depuración"
  type        = bool
  default     = false
}