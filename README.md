# hello-aws

I want to resolve my AWS questions.

---

## Getting started with AWS CLI locally

### Prerequisites

- An AWS account with an IAM user that has an **Access Key ID** and **Secret Access Key**
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) installed

### Steps

1. **Configure credentials**

   ```bash
   aws configure
   ```

   Enter your credentials when prompted:

   ```
   AWS Access Key ID [None]: <your-access-key-id>
   AWS Secret Access Key [None]: <your-secret-access-key>
   Default region name [None]: ap-northeast-1
   Default output format [None]: json
   ```

   Credentials are saved to `~/.aws/credentials` and `~/.aws/config`.

2. **Verify the setup**

   ```bash
   # Check the authenticated identity
   aws sts get-caller-identity

   # List S3 buckets
   aws s3 ls

   # List EC2 instances
   aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name]' --output table
   ```

3. **Use multiple profiles (optional)**

   ```bash
   # Add a named profile
   aws configure --profile <profile-name>

   # Use a specific profile
   aws s3 ls --profile <profile-name>

   # Set a default profile via environment variable
   export AWS_PROFILE=<profile-name>
   aws s3 ls
   ```

### References

- [Install or update the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Configuration and credential file settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
