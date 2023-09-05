variable "role_name" {
  type    = string
  default = "harness_aws_ccm_connector_automation"
}

variable "role_path" {
  type    = string
  default = "/"
}

variable "policy_name" {
  type    = string
  default = "harness_aws_ccm_connector_automation"
}

variable "policy_path" {
  type    = string
  default = "/"
}

variable "function_name" {
  type    = string
  default = "harness_aws_ccm_connector_automation"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "tags to add to created resources"
}

variable "harness_account_id" {
  type        = string
  description = "tags to add to created resources"
}

variable "harness_platform_api_key" {
  type        = string
  description = "tags to add to created resources"
}

variable "cross_account_role_name" {
  type        = string
  description = "tags to add to created resources"
}

variable "external_id" {
  type        = string
  description = "tags to add to created resources"
}

variable "ignore" {
  type        = string
  default     = ""
  description = "tags to add to created resources"
}

variable "role_to_assume" {
  type        = string
  default     = ""
  description = "tags to add to created resources"
}

variable "session_name" {
  type        = string
  default     = ""
  description = "tags to add to created resources"
}

variable "connector_tags" {
  type        = map(string)
  default     = {}
  description = "tags to add to created resources"
}

variable "features" {
  type        = string
  default     = ""
  description = "tags to add to created resources"
}

variable "govcloud" {
  type        = bool
  default     = false
  description = "tags to add to created resources"
}
