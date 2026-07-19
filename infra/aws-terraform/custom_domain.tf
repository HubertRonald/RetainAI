resource "aws_acm_certificate" "retainai_api" {
  domain_name       = var.api_custom_domain
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = merge(var.tags, {
    Name      = var.api_custom_domain
    component = "api-custom-domain"
    sprint    = "7-6-2"
  })
}

resource "aws_acm_certificate_validation" "retainai_api" {
  certificate_arn = aws_acm_certificate.retainai_api.arn

  validation_record_fqdns = [
    for option in aws_acm_certificate.retainai_api.domain_validation_options :
    option.resource_record_name
  ]

  timeouts {
    create = "45m"
  }
}

resource "aws_apigatewayv2_domain_name" "backend" {
  domain_name = var.api_custom_domain

  domain_name_configuration {
    certificate_arn = aws_acm_certificate_validation.retainai_api.certificate_arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }

  tags = merge(var.tags, {
    Name      = var.api_custom_domain
    component = "api-custom-domain"
    sprint    = "7-6-2"
  })
}

resource "aws_apigatewayv2_api_mapping" "backend" {
  api_id      = aws_apigatewayv2_api.backend.id
  domain_name = aws_apigatewayv2_domain_name.backend.id
  stage       = aws_apigatewayv2_stage.default.id
}
