# Simple cloud solution for trained UNET neural network
In recent years, the integration of Artificial Intelligence (AI) models in various applications has become increasingly prevalent. AI models require substantial computational resources, making efficient deployment a critical consideration. One powerful solution is leveraging cloud hosting, which provides scalability, flexibility, and ease of access to computational power. In this tutorial, we will explore the benefits of using cloud hosting for AI model deployment using a human segmentation binary classification UNET model as a practical example.\
Thank you chatGPT for the introduction, now let's get a little in depth.
### Building diagram for our solution
For this example we will use the simplest possible architecture, which nevertheless could be scaled easily for higher demand. Of course, it could be addapted for clients demands, like availability in case of local power offs, lower latence for remote regions or integration of on-site resources.
When migrating any project to the cloud every one in a team should be informed and have an idea on what exactly cloud technologies could provide for them. Therefore this short reading could be used as a great starting point for people that are yet to be familiarized with AWS.

_In this detailed step-by-step tutorial we would only use the following repo, therefore readers are welcomed to follow the instructions!_

![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/Updated_diagram.png)

Here we can see the **EC2 instance** connected to **S3 database** which is used to store collected user data. External database provide an opportunity to collect users data that could used for furter model training or fine-tunning. Obviously, the EC2 virtual machine itself has the memory, however after a machine termination its data gets erased. An example of such case could be growth in demand that will launch additional instances and after deman gets back to normal extra instances would be demolished with all theirs valuable data. That's the case we're avoiding with provided architecture. Having created the architecture diagram the next step would be to open the AWS console and implement it!

### Creating EC2 instance 
At first glance the AWS might look overwhelming, but you will get use to it, trust me. 

![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/console.png)

For now screenshots sre self-sufficient therefore I will share one very important advice I got from one senior cloud engineer - **keep it simple** and stick to the most basic recources you possibly can. Using one extremely specialized tool provided by AWS (that there are **tons of**) may cause an unexpected need to replace it with anything because the _exact tool_ is no longer supported or the versions are no longer competable with one another. 

![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/ec2_creation.png)
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/choosing_processor.png)\
For simpler projects the free tier processor should be sufficient, hovewer Pytorch that we are using is much more that free tier **1GB** RAM could take.\
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/instance_created.png)

### Creating S3 instance
Is a pretty straightforward process. Have a look.\
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/database_creation.png)
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/s3_bucket_options.png)
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/s3_acess_option.png)\
We will configure the access later in this tutorial.
### Creating the IAM role
In oreder to be able to access the S3 instance from EC2 we need a role that will provide all the necessarry rights to it.
![image]()
