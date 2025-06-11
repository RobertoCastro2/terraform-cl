output "app_server_id" {
  description = "ID da instância EC2 do app"
  value       = aws_instance.app_server.id
}

output "app_server_public_ip" {
  description = "IP público da instância EC2"
  value       = aws_instance.app_server.public_ip
}