# Simple cloud solution for trained UNET neural network
In recent years, the integration of Artificial Intelligence (AI) models in various applications has become increasingly prevalent. AI models require substantial computational resources, making efficient deployment a critical consideration. One powerful solution is leveraging cloud hosting, which provides scalability, flexibility, and ease of access to computational power. In this tutorial, we will explore the benefits of using cloud hosting for AI model deployment using a human segmentation binary classification UNET model as a practical example.\
Thank you chatGPT for the introduction, now let's get a little in depth.
### Building diagram for our solution
For this example we will use the simplest possible architecture, which nevertheless could be scaled easily for higher demand. Of course, it could be addapted for clients demands, like availability in case of local power offs, lower latence for remote regions or integration of on-site resources.
When migrating any project to the cloud every one in a team should be informed and have an idea on what exactly cloud technologies could provide for them. Therefore this short reading could be used as a great starting point for people that are yet to be familiarized with AWS.

_In this detailed step-by-step tutorial we would only use the following repo, therefore readers are welcomed to follow the instructions!_

![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/Updated_diagram.png)

Here we can see the **EC2 instance** connected to **S3 database** which is used to store collected user data. External database provide an opportunity to collect users data that could used for furter model training or fine-tunning. Obviously, the EC2 virtual machine itself has the memory, however after a machine termination its data gets erased. An example of such case could be growth in demand that will launch additional instances and after deman gets back to normal extra instances would be demolished with all theirs valuable data. That's the case we're avoiding with provided architecture. Having created the architecture diagram the next step would be to open the AWS console and implement it!

## Creating EC2 instance 
At first glance the AWS might look overwhelming, but you will get use to it, trust me. 

![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/console.png)

For now screenshots sre self-sufficient therefore I will share one very important advice I got from one senior cloud engineer - **keep it simple** and stick to the most basic recources you possibly can. Using one extremely specialized tool provided by AWS (that there are **tons of**) may cause an unexpected need to replace it with anything because the _exact tool_ is no longer supported or the versions are no longer competable with one another. 

![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/ec2_creation.png)
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/choosing_processor.png)\
For simpler projects the free tier processor should be sufficient, hovewer Pytorch that we are using is much more that free tier **1GB** RAM could take.\
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/instance_created.png)

## Creating S3 instance
Is a pretty straightforward process. Have a look.\
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/database_creation.png)
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/s3_bucket_options.png)
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/s3_acess_option.png)\
We will configure the access later in this tutorial.
## Creating the IAM role
In oreder to be able to access the S3 instance from EC2 we need a role that will provide all the necessarry rights to it.
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/create_iam_policy.png)\
In production we should always follow the **principle of least privilege**, however for the demonstration purposes we will stick to simplest solutions.\
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/adding_policies.png)
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/adding_policies2.png)
## Connecting and configuring the system
In the EC2 options menu we can see the "connect" option. That's what we are klicking.\
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/connecting_to_instance.png)\
_This action could be also performed with a direct TCP connection which would require an oppened connection port in EC2 instance settings._
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/connection_establioshed.png)\
**Congratulations!**\
```aws configure```\
```aws s3 ls```\
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/opened_ec2_console.png)\
```git pull -b aws https://github.com/C1l1r/unet_human_segmentation.git``` \
```git lfs pull``` Yep, the neural network weights are too heavy for github.\
Now we can simply launch necessary files with simple commands!\
```python inference.py```\
here we should use the ```bg``` command in order to run the second file that will send files to S3 instance.\
```python  s3_file_uploader.py```
Now when we have the server running we can connect to it from our local machine. Also woth mentioning that this API uses Flask, however it could be switched to **AWS ApiGateway**
## Launching UI and testing
In order to perform the next step you should pull the github folder on machine you want to connect to api and change the default variable to **public IpV4** of EC2 instance. 
Then you can simply use the ```streamlit run UI.py``` to run the UI and upload the file!\
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/UI_with_uploaded_video.png)
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/video_saved.png)
![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/file_on_s3.png)
## Conclusion
This arcticle should provide you with the general idea on cloud computing and AWS implementation ideas. However, despite being a powerful resource it should be used with great caution. As an example of suboptimal desisions that have led to unwnted expenses could be used this [case](https://devclass.com/2023/05/05/reduce-costs-by-90-by-moving-from-microservices-to-monolith-amazon-internal-case-study-raises-eyebrows/) Thank you for your attention!
