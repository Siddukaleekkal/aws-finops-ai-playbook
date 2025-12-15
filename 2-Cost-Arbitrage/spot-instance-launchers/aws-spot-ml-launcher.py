import boto3
import json

# --- Configuration for your ML Workload ---
IAM_PROFILE_NAME = "MLTrainingInstanceProfile"
SUBNET_ID = "subnet-xxxxxxxxxxxx"  # Subnet for the GPU instances
KEY_PAIR_NAME = "ml-engineer-key"
TAGS = [
    {'Key': 'ProjectID', 'Value': 'llm-fine-tuning'},
    {'Key': 'ArbitrageStrategy', 'Value': 'Spot/Preemptible'}
]
# --- Boto3 Client ---
ec2 = boto3.client('ec2', region_name='us-east-1')

def launch_spot_fleet(image_id: str, desired_capacity: int):
    """
    Launches a Spot Fleet Request for ML Training.
    Uses a mix of instance types to maximize availability and minimize interruption.
    """
    
    # 1. Define Instance Type Mix (Cost Arbitrage)
    # Target high-demand GPUs with fallback to older generations.
    launch_specifications = [
        {
            'InstanceType': 'p4d.24xlarge', # Highest performance/cost
            'WeightedCapacity': 1,
            'SubnetId': SUBNET_ID,
            'ImageId': image_id,
            'IamInstanceProfile': {'Name': IAM_PROFILE_NAME},
            'KeyName': KEY_PAIR_NAME,
            'TagSpecifications': [{'ResourceType': 'instance', 'Tags': TAGS}]
        },
        {
            'InstanceType': 'p3.8xlarge', # Lower cost fallback
            'WeightedCapacity': 0.5,
            'SubnetId': SUBNET_ID,
            'ImageId': image_id,
            'IamInstanceProfile': {'Name': IAM_PROFILE_NAME},
            'KeyName': KEY_PAIR_NAME,
            'TagSpecifications': [{'ResourceType': 'instance', 'Tags': TAGS}]
        }
    ]

    try:
        response = ec2.request_spot_fleet(
            SpotFleetRequestConfig={
                'AllocationStrategy': 'capacityOptimized', # AWS selects cheapest/most available
                'TargetCapacity': desired_capacity,
                'IamFleetRole': 'arn:aws:iam::123456789012:role/aws-ec2-spot-fleet-role', # Replace with your role ARN
                'LaunchSpecifications': launch_specifications,
                'Type': 'request'
            }
        )
        print("Successfully submitted Spot Fleet Request.")
        print(f"Request ID: {response['SpotFleetRequestId']}")
        return response
    except Exception as e:
        print(f"Error launching Spot Fleet: {e}")
        return None

if __name__ == "__main__":
    # You would typically find a deep learning AMI ID here
    ML_AMI_ID = "ami-0abcdef1234567890" 
    
    # We want the equivalent of one p4d.24xlarge machine's capacity
    launch_spot_fleet(ML_AMI_ID, desired_capacity=1) 
    
    print("\nRemember: Successful FinOps requires a robust checkpointing mechanism (e.g., saving model weights to S3 every 15 minutes) to handle Spot interruptions!")
