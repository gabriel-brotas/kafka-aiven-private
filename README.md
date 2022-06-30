
aiven private link arn = arn:aws:iam::977777161073:root

```bash
# aws ec2 --region eu-east-1 create-vpc-endpoint --vpc-endpoint-type Interface --vpc-id $your_vpc_id --subnet-ids $space_separated_list_of_subnet_ids --security-group-ids $security_group_ids --service-name com.amazonaws.vpce.eu-west-1.vpce-svc-0b16e88f3b706aaf1

aws ec2 --region us-east-1 create-vpc-endpoint --vpc-endpoint-type Interface --vpc-id vpc-067c6648bf7ce437c --subnet-ids subnet-0f4974308ecb149cc subnet-0e8517fe66c19f7ea  --service-name com.amazonaws.vpce.us-east-1.vpce-svc-0f3d4bb7ca973f76b
```

The security groups determine the instances that are allowed to connect to the endpoint network interfaces created by AWS into the specified subnets.

the security group for the VPC endpoint must allow ingress in the port range 10000-31000 to accommodate the pool of Kafka broker ports used in our PrivateLink implementation.

Once the AWS endpoint state changes to available, the connection is visible in Aiven.


security group =
10000 - 31000 -> 10.10.0.0/16