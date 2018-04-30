import boto3
import time
import sys
global str
Tags = []
Instances = []
Service_Name = []
Instance_Name = []
vpc_id = []
private_ip = []
subnet_id = []
Availability_zone = []
instance_name = []
Instance_id = []

servicename=sys.argv[1]
emailaddress = sys.argv[2]
ccaddr = sys.argv[3]
customer = sys.argv[4]
cmd = sys.argv[5]

regiontable = "us-west-2"
client = boto3.client('dynamodb',regiontable)
response1 = client.scan(TableName='SSM-TEST')
count = response1['Count']
count += 1
for client in response1['Items']:
   print client
   customername = str(client['Client']['S'])
   print customername
   if customername == customer:
        client1 = str(client['Client']['S'])
        cross_acc_arn = str(client['crossaccount']['S'])
        print cross_acc_arn + "  "+client1
        client = boto3.client('sts')
        response1 = client.assume_role(RoleArn=cross_acc_arn,RoleSessionName='Demo')
        access_key = response1['Credentials']['AccessKeyId']
        secret_key = response1['Credentials']['SecretAccessKey']
        session_token = response1['Credentials']['SessionToken']

        print access_key
        print secret_key
        ec2 = boto3.client('ec2',regiontable)
        response = ec2.describe_regions()
        len = len(response['Regions'])
        for i in range(0,len):
                print i
                response = ec2.describe_regions()
                #print response
                regionname=response['Regions'][i]['RegionName']
                region_name=regionname
                print region_name
                client = boto3.client('dynamodb',regiontable)
                response1 = client.scan(TableName='SSM-TEST')
                count = response1['Count']
                count += 1
                #print servicename
                subject = str(client1) +(':List of Linux Instances without ') +(str(servicename))

                ec2 = boto3.client("ec2", aws_access_key_id=access_key,aws_secret_access_key=secret_key,aws_session_token=session_token,region_name=region_name)
                ## Filtering all instancesTypeError: 'str' object is not callable
                all_instances = ec2.describe_instances(Filters=[ {'Name': 'instance-state-name', 'Values': ['running',]}, ])
                windows_instances = ec2.describe_instances( Filters=[  { 'Name': 'platform', 'Values': ['windows',] }, {'Name': 'instance-state-name', 'Values': ['running',]}, ])

                ## Declaring empty sets to filter linux instances
                instance_list = set()
                win_inst_list = set()

                ## Getting windows instances
                for reservation in windows_instances["Reservations"] :
                  for instance in reservation["Instances"]:
                    win_inst_list.add(instance['InstanceId'])
                #print win_inst_list

                ## Getting all instances running within the repective region
                for reservation in all_instances["Reservations"] :
                  for instance in reservation["Instances"]:
                    instance_list.add(instance['InstanceId'])
                #print instance_list
                ## Declaring empty lists to store VPC_id, Private_IP & Subnet_id

                ## Fetching only Linux based instances discarding windows one's
                iamclient = boto3.client('iam', aws_access_key_id=access_key,aws_secret_access_key=secret_key,aws_session_token=session_token,region_name=region_name)
                linux_inst_list = instance_list - win_inst_list
                #print linux_inst_list
                #print type(linux_inst_list)
                ids = []
                final_list = []
                for i in list(linux_inst_list):
                #   print type(i)
                    linuxssm =  ec2.describe_instances(InstanceIds=[i])
                    for reservation1 in linuxssm['Reservations']:
                       try:
                        result = reservation1['Instances'][0]['IamInstanceProfile']['Arn']
                        a = result.split('/')
                        print a[1]
                        iamresponse = iamclient.list_attached_role_policies(RoleName= a[1])
                        policyname = iamresponse['AttachedPolicies']
                        for policy in policyname:
                            try:
                                print policy
                                if (policy['PolicyName'] == "AmazonEC2RoleforSSM" or  "AmazonSSMFullAccess"):
                                   ids.append(i)
                                   print ids
                            except:
                                pass
                        for num in ids:
                            if num not in final_list:
                               final_list.append(num)
                #        print ids
                        print final_list
                       except:
                        pass

                #def Remove(duplicate):
                #    final_list = []
                #    for num in ids:
                #        if num not in final_list:
                #            final_list.append(num)
                #    return final_list
                #print result

                ## Declarig empty list of failed ssm RunCommand instances

                failed_id_list = []
                ## Function to execute RunCommand
                def command_status():
                  response = ssm.get_command_invocation(
                     CommandId=Command_id,
                     InstanceId=member
                  )
                  print response
                  if response['Status'] == 'InProgress':
                    time.sleep(30)
                    command_status()
                  else:
                     if response['StandardErrorContent'] != '':
                         failed_id_list.append(member)

                ## Declaring ssm RunCommand
                for member in final_list:
                    try:
                        print member
                        ssm = boto3.client('ssm', aws_access_key_id=access_key,aws_secret_access_key=secret_key,aws_session_token=session_token,region_name=region_name)
                        testCommand = ssm.send_command( InstanceIds=[member], DocumentName='AWS-RunShellScript', Comment='Testing the boto3 cmd', Parameters={ "commands":[ command ]  } )
                        Command_id = (testCommand['Command']['CommandId'])
                        print Command_id
                        response = ssm.get_command_invocation(
                            CommandId=Command_id,
                            InstanceId=member
                        )
                        print response
                        command_status()
                    except Exception as e:
                        print e #"The instance is not having ssm"

                print failed_id_list
                ec2_describe = boto3.client('ec2', aws_access_key_id=access_key,aws_secret_access_key=secret_key,aws_session_token=session_token,region_name=region_name)
                command = "service" +" "+(str(cmd))+" " + "status"
                print command
                for member in failed_id_list:
                  test =  ec2_describe.describe_instances(InstanceIds=[member])
                  print test
                  vpc_id.append(test['Reservations'][0]['Instances'][0]['VpcId'])
                  private_ip.append(test['Reservations'][0]['Instances'][0]['PrivateIpAddress'])
                  subnet_id.append(test['Reservations'][0]['Instances'][0]['SubnetId'])
                  Availability_zone.append(test['Reservations'][0]['Instances'][0]['Placement']['AvailabilityZone'])
                  Instance_id.append(test['Reservations'][0]['Instances'][0]['InstanceId'])

                  Service_Name.append ("Not Running")
                  print private_ip
                  instance_name1 = test['Reservations']
                #  print instance_name
                  for i in instance_name1:
                     Instances=i['Instances'][0]['Tags']
                #     print Instances['Key']
                     for n in Instances:
                       print n['Key']
                       if n['Key'] == 'Name':
                         instance_name.append(n['Value'])
                         print instance_name

        ## Converting the lists into Table which supports HTML
        table_list = ['Instance_name', 'Instance_id', 'VPC_id', 'Private_IP', 'Subnet_id', 'Availability_zone',servicename]
        html = '<table border="1" style="width:15%"><tr><th>' + '</th><th>'.join(table_list) + '</th></tr>'

        for row in zip(instance_name, Instance_id ,vpc_id, private_ip, subnet_id, Availability_zone, Service_Name):
        #   print '\t'.join(row)
           html +=  '<tr><td>' + '</td><td>'.join(row) + '</td></tr>'
        html += '</table>'
        print html


        ## Sending EMAIL using SES
        client1 = boto3.client('ses', aws_access_key_id=access_key,aws_secret_access_key=secret_key,aws_session_token=session_token,region_name='us-west-2')
        response = client1.send_email(Source=emailaddress,Destination={'ToAddresses': [emailaddress], 'CcAddresses': [ccaddr]},Message={'Subject': {'Data': subject}, 'Body': {'Html': {'Data': html}}}, ReplyToAddresses=['alsa.thuruthel@reancloud.com'])
