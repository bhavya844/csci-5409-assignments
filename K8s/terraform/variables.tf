variable "project" {}

variable "credentials_file" {}

variable "region" {
  default = "us-central1"
}

variable "zone" {
  default = "us-central1-c"
}

variable "location" {
  default     = "us-central1-c"
  description = "zone of the cluster nodes"
}