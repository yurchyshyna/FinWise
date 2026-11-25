output "server_public_ip" {
  description = "Публічна IP-адреса сервера"
  value       = aws_instance.server.public_ip
}

output "server_public_dns" {
  description = "Публічне DNS-ім'я сервера"
  value       = aws_instance.server.public_dns
}

output "ssh_command" {
  description = "Команда для входу на сервер"
  value       = "ssh -i ~/.ssh/finwise-key ubuntu@${aws_instance.server.public_ip}"
}