provider "aws" {
  region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "your-terraform-state-bucket"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "lambda_policy"
  role = aws_iam_role.iam_for_lambda.id

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
EOF
}

resource "aws_cognito_user_pool" "main" {
  name = "my_user_pool"
}

resource "aws_cognito_user_pool_client" "client" {
  name = "my_user_pool_client"
  user_pool_id = aws_cognito_user_pool.main.id
  
  # Add this to your user pool client
  explicit_auth_flows = ["USER_PASSWORD_AUTH"]
}

resource "aws_api_gateway_rest_api" "MyDemoAPI" {
  name        = "MyDemoAPI"
  description = "This is my API for demonstration purposes"
}

resource "aws_api_gateway_resource" "MyDemoResource" {
  rest_api_id = aws_api_gateway_rest_api.MyDemoAPI.id
  parent_id   = aws_api_gateway_rest_api.MyDemoAPI.root_resource_id
  path_part   = "mydemoresource"
}

resource "aws_api_gateway_method" "MyDemoMethod" {
  rest_api_id   = aws_api_gateway_rest_api.MyDemoAPI.id
  resource_id   = aws_api_gateway_resource.MyDemoResource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "MyDemoIntegration" {
  rest_api_id = aws_api_gateway_rest_api.MyDemoAPI.id
  resource_id = aws_api_gateway_resource.MyDemoResource.id
  http_method = aws_api_gateway_method.MyDemoMethod.http_method

  type = "MOCK"
}

resource "aws_lambda_function" "test_lambda" {
  filename      = "lambda_function_payload.zip"
  function_name = "lambda_function_name"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_function.lambda_handler" 

  source_code_hash = filebase64sha256("lambda_function_payload.zip")

  runtime = "python3.8"

  environment {
    variables = {
      foo = "bar"
    }
  }
}

resource "aws_iam_role_policy" "ses_send_email" {
  name = "ses_send_email"
  role = aws_iam_role.iam_for_lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ses:SendEmail",
          "ses:SendRawEmail"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}
resource "aws_iam_role_policy" "cognito_admin_create_user" {
  name = "cognito_admin_create_user"
  role = aws_iam_role.iam_for_lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "cognito-idp:AdminCreateUser"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

resource "aws_ssm_parameter" "cognito_client_id" {
  name  = "/app/parameters/cognito_client_id"
  type  = "SecureString"
  value = aws_cognito_user_pool_client.client.id
}