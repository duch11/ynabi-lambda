//State and provider
provider "aws" {
  region = local.region
  default_tags {
    tags = {
      project = local.project_name
    }
  }
}

locals {
  region = "eu-north-1"
  project_name = "YNAB-Spiir-Sync-Terraform"
  log_retention_in_days = "30"
  schedule_expression = "rate(3 hours)" #every 3 hours do a sync
  #See https://docs.aws.amazon.com/lambda/latest/dg/services-cloudwatchevents-expressions.html for more
}

//Lambda
resource "aws_lambda_function" "YNAB-Spiir-Sync-Lambda" {
  function_name                  = local.project_name
  filename                       = "${path.module}/../extras/aws_lambda_code.zip"
  handler                        = "lambda_function.lambda_handler"
  memory_size                    = "128"
  package_type                   = "Zip"
  reserved_concurrent_executions = "-1"
  role                           = "${aws_iam_role.YSS-Lambda-Role.arn}"
  runtime                        = "python3.9"
  timeout                        = "180"
  source_code_hash               = filebase64sha256("${path.module}/../extras/aws_lambda_code.zip")

  tracing_config {
    mode = "PassThrough"
  }
}

resource "aws_iam_role" "YSS-Lambda-Role" {
  name                 = "YSS-Lambda-Role"
  managed_policy_arns  = ["${aws_iam_policy.YSS-Lambda-Allow-Logging.arn}"]
  max_session_duration = "3600"
  
  path                 = "/service-role/"
  assume_role_policy = data.aws_iam_policy_document.sts_assume_role.json
}

data "aws_iam_policy_document" "sts_assume_role" {
  statement {
    actions = [
      "sts:AssumeRole",
    ]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

// Logging
resource "aws_cloudwatch_log_group" "YSS-Lambda-Log-Group" {
  name              = "/aws/lambda/${local.project_name}"
  retention_in_days = local.log_retention_in_days
}

resource "aws_iam_role_policy_attachment" "YSS-Lambda-Role_YSS_lambda-Allow-Logging" {
  policy_arn = "${aws_iam_policy.YSS-Lambda-Allow-Logging.arn}"
  role       = "${aws_iam_role.YSS-Lambda-Role.name}"
}

resource "aws_iam_policy" "YSS-Lambda-Allow-Logging" {
  name = "YSS-Lambda-Allow-Logging"
  path = "/service-role/"

  policy = data.aws_iam_policy_document.allow_logging.json

}

data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "allow_logging" {
  statement {
    actions = [
      "logs:CreateLogGroup",
    ]
    resources = [
      "arn:aws:logs:${local.region}:${data.aws_caller_identity.current.account_id}:*",
    ]
  }

  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = [
      "${aws_cloudwatch_log_group.YSS-Lambda-Log-Group.arn}",
    ]
  }
}

// Triggering with cloudwatch
resource "aws_cloudwatch_event_rule" "sync-ynab-trigger" {
  event_bus_name      = "default"
  is_enabled          = "true"
  name                = "sync-ynab-trigger-test"
  schedule_expression = local.schedule_expression
}

resource "aws_cloudwatch_event_target" "YSS-target" {
  arn = aws_lambda_function.YNAB-Spiir-Sync-Lambda.arn
  rule      = aws_cloudwatch_event_rule.sync-ynab-trigger.id
  retry_policy {
    maximum_event_age_in_seconds = "600"
    maximum_retry_attempts       = "2"
  }
}
