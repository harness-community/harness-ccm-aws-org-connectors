# harness-ccm-aws-org-connectors

create harness ccm aws connectors for all accounts in an organization

## Python

### Settings

- CROSS_ACCOUNT_ROLE_NAME: Name of the role provisioned into member accounts, example: `HarnessCERole`
- EXTERNAL_ID: External ID specified in the trust relationship of member account roles, example: `harness:012345678901:awsajh91h2k`
- IGNORE: Account Ids to skip creating connectors for, you should add your master account id here, example: `012345678901,112345678901`
- ROLE_TO_ASSUME (optional): Role to assume for organizations access, example: `arn:aws:iam::012345678901:role/orgaccess`
- SESSION_NAME (optional): Session name for assuming role, example: `harnessautomation`
- TAGS (optional): Tags in a json format to add to the connectors, example: `{"key":"value"}`
- FEATURES (optional): Features to enable for accounts, example: `GOVERNANCE,VISIBILITY`
- GOVCLOUD (optional): If the account is in aws govcloud, example: `true`

### Run

```python
pip install requirements.txt
python main.py
```

## Terraform

### Requirements

No requirements.

### Providers

| Name | Version |
|------|---------|
| <a name="provider_archive"></a> [archive](#provider\_archive) | 2.4.0 |
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.14.0 |

### Modules

No modules.

### Resources

| Name | Type |
|------|------|
| [aws_cloudwatch_event_rule.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_rule) | resource |
| [aws_cloudwatch_event_target.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudwatch_event_target) | resource |
| [aws_iam_policy.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_policy) | resource |
| [aws_iam_role.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy_attachment.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_lambda_function.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_lambda_permission.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_permission) | resource |
| [archive_file.this](https://registry.terraform.io/providers/hashicorp/archive/latest/docs/data-sources/file) | data source |
| [aws_iam_policy_document.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |

### Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_connector_tags"></a> [connector\_tags](#input\_connector\_tags) | tags to add to created resources | `map(string)` | `{}` | no |
| <a name="input_cross_account_role_name"></a> [cross\_account\_role\_name](#input\_cross\_account\_role\_name) | tags to add to created resources | `string` | n/a | yes |
| <a name="input_external_id"></a> [external\_id](#input\_external\_id) | tags to add to created resources | `string` | n/a | yes |
| <a name="input_features"></a> [features](#input\_features) | tags to add to created resources | `string` | `""` | no |
| <a name="input_function_name"></a> [function\_name](#input\_function\_name) | n/a | `string` | `"harness_aws_ccm_connector_automation"` | no |
| <a name="input_govcloud"></a> [govcloud](#input\_govcloud) | tags to add to created resources | `bool` | `false` | no |
| <a name="input_harness_account_id"></a> [harness\_account\_id](#input\_harness\_account\_id) | tags to add to created resources | `string` | n/a | yes |
| <a name="input_harness_platform_api_key"></a> [harness\_platform\_api\_key](#input\_harness\_platform\_api\_key) | tags to add to created resources | `string` | n/a | yes |
| <a name="input_ignore"></a> [ignore](#input\_ignore) | tags to add to created resources | `string` | `""` | no |
| <a name="input_policy_name"></a> [policy\_name](#input\_policy\_name) | n/a | `string` | `"harness_aws_ccm_connector_automation"` | no |
| <a name="input_policy_path"></a> [policy\_path](#input\_policy\_path) | n/a | `string` | `"/"` | no |
| <a name="input_role_name"></a> [role\_name](#input\_role\_name) | n/a | `string` | `"harness_aws_ccm_connector_automation"` | no |
| <a name="input_role_path"></a> [role\_path](#input\_role\_path) | n/a | `string` | `"/"` | no |
| <a name="input_role_to_assume"></a> [role\_to\_assume](#input\_role\_to\_assume) | tags to add to created resources | `string` | `""` | no |
| <a name="input_session_name"></a> [session\_name](#input\_session\_name) | tags to add to created resources | `string` | `""` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | tags to add to created resources | `map(string)` | `{}` | no |

### Outputs

| Name | Description |
|------|-------------|
| <a name="output_function"></a> [function](#output\_function) | Lambda function role |
| <a name="output_role"></a> [role](#output\_role) | Lambda execution role |
