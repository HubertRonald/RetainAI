output "api_custom_domain" {
  description = "Branded RetainAI API domain."
  value       = aws_apigatewayv2_domain_name.backend.domain_name
}

output "api_custom_url" {
  description = "Branded HTTPS URL for the RetainAI backend."
  value       = "https://${aws_apigatewayv2_domain_name.backend.domain_name}"
}

output "api_custom_domain_target" {
  description = "Regional API Gateway hostname used by the external DNS CNAME."
  value       = aws_apigatewayv2_domain_name.backend.domain_name_configuration[0].target_domain_name
}

output "api_custom_domain_hosted_zone_id" {
  description = "API Gateway Regional hosted zone ID. Informational because Namecheap remains the DNS provider."
  value       = aws_apigatewayv2_domain_name.backend.domain_name_configuration[0].hosted_zone_id
}

output "api_certificate_arn" {
  description = "ACM certificate ARN for the branded API domain."
  value       = aws_acm_certificate.retainai_api.arn
}

output "api_certificate_dns_validation" {
  description = "DNS validation records that must be added manually to Namecheap."

  value = {
    for option in aws_acm_certificate.retainai_api.domain_validation_options :
    option.domain_name => {
      name  = option.resource_record_name
      type  = option.resource_record_type
      value = option.resource_record_value
    }
  }
}
