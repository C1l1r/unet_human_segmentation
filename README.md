# Simple cloud solution for trained UNET neural network
In recent years, the integration of Artificial Intelligence (AI) models in various applications has become increasingly prevalent. AI models require substantial computational resources, making efficient deployment a critical consideration. One powerful solution is leveraging cloud hosting, which provides scalability, flexibility, and ease of access to computational power. In this tutorial, we will explore the benefits of using cloud hosting for AI model deployment using a human segmentation binary classification UNET model as a practical example.
### Building diagram for our solution
For this example we will use the simplest possible architecture, which nevertheless could be scaled easily for higher demand. Of course, it could be addapted for clients demands, like availability in case of local power offs, lower latence for remote regions or integration of on-site resources.

_In this detailed step-by-step tutorial we would only use the following repo, therefore readers are welcomed to follow the instructions!_

![image](https://github.com/C1l1r/unet_human_segmentation/blob/aws/images/Updated_diagram.png)

Here we can see the **EC2 instance** connected to **S3 database** which is used to store collected user data. External database provide an opportunity to collect users data that could used for furter model training or fine-tunning. Obviously, the EC2 virtual machine itself has the memory, however after a machine termination its data gets erased. An example of such case could be growth in demand that will launch additional instances and after deman gets back to normal extra instances would be demolished with all theirs valuable data. That's the case we're avoiding with provided architecture. Having created the architecture the next step would be to open the AWS console and implement it!

### Creating EC2 instance 
At first glance the 
