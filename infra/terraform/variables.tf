variable "aws_region" {
  description = "Регіон AWS"
  type        = string
  default     = "eu-north-1"
}

variable "project_name" {
  description = "Назва проєкту, використовується в іменах ресурсів"
  type        = string
  default     = "finwise"
}

variable "instance_type" {
  description = "Тип віртуальної машини"
  type        = string
  default     = "t3.small"
}

variable "root_volume_size" {
  description = "Розмір диска сервера, ГБ"
  type        = number
  default     = 20
}

variable "vpc_cidr" {
  description = "Адресний простір віртуальної мережі"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "Адресний простір публічної підмережі"
  type        = string
  default     = "10.0.1.0/24"
}

variable "ssh_allowed_cidr" {
  description = "Адреса, з якої дозволено SSH (наприклад, 203.0.113.10/32)"
  type        = string
}

variable "ssh_public_key" {
  description = "Публічний SSH-ключ для входу на сервер"
  type        = string
}

variable "ami_id" {
  description = "ID образу Ubuntu 24.04 (AMI) у вибраному регіоні"
  type        = string
}