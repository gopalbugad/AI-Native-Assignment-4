provider "aws" {
  region = var.region
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"
  cluster_name    = var.cluster_name
  subnet_ids      = var.subnet_ids
  vpc_id          = var.vpc_id
  cluster_enabled_log_types = []
  create_cloudwatch_log_group = false

  eks_managed_node_groups = {
    default = {
      desired_size = 1
      max_size     = 1
      min_size     = 1
      instance_types = ["t3.medium"]
    }
  }
}
