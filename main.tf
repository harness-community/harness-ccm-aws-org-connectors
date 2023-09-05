data "aws_iam_policy_document" "this" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "this" {
  name               = var.role_name
  path               = var.role_path
  tags               = var.tags
  assume_role_policy = data.aws_iam_policy_document.this.json
}

resource "aws_iam_policy" "this" {
  name        = var.policy_name
  path        = var.policy_path
  description = "Policy for ${var.role_name} for ${var.function_name}"
  tags        = var.tags

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "organizations:ListAccounts",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "this" {
  role       = aws_iam_role.this.name
  policy_arn = aws_iam_policy.this.arn
}

data "archive_file" "this" {
  type        = "zip"
  source_file = "main.py"
  output_path = "${path.module}/${var.function_name}.zip"
}

resource "aws_lambda_function" "this" {
  filename      = data.archive_file.this.output_path
  function_name = var.function_name
  role          = aws_iam_role.this.arn
  handler       = "main.lambda_handler"

  source_code_hash = data.archive_file.this.output_base64sha256

  # last python version with requests vendored within botocore
  runtime = "python3.7"

  timeout = 900

  environment {
    variables = {
      HARNESS_ACCOUNT_ID       = var.harness_account_id
      HARNESS_PLATFORM_API_KEY = var.harness_platform_api_key,
      CROSS_ACCOUNT_ROLE_NAME  = var.cross_account_role_name,
      EXTERNAL_ID              = var.external_id,
      IGNORE                   = var.ignore,
      ROLE_TO_ASSUME           = var.role_to_assume,
      SESSION_NAME             = var.session_name,
      TAGS                     = tostring(jsonencode(var.connector_tags)),
      FEATURES                 = var.features,
      GOVCLOUD                 = var.govcloud,
    }
  }

  tags = var.tags
}


resource "aws_cloudwatch_event_rule" "this" {
  name                = "${aws_lambda_function.this.function_name}_schedule"
  description         = "Schedule for ${aws_lambda_function.this.function_name} Lambda Function"
  schedule_expression = "cron(0 * ? * * *)"
}

resource "aws_cloudwatch_event_target" "this" {
  rule = aws_cloudwatch_event_rule.this.name
  arn  = aws_lambda_function.this.arn
}


resource "aws_lambda_permission" "this" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "events.amazonaws.com"
}
