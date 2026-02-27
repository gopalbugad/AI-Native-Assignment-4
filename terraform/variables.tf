variable "region" {}
variable "vpc_id" {}
variable "subnet_ids" {
  type = list(string)
}
variable "cluster_name" {}