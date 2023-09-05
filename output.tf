output "role" {
  description = "Lambda execution role"
  value       = aws_iam_role.this.arn
}

output "function" {
  description = "Lambda function role"
  value       = aws_lambda_function.this.arn
}