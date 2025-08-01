output "meilisearch_public_ip" {
  description = "The public IP address of the MeiliSearch server."
  value       = aws_instance.meilisearch_server.public_ip
} 