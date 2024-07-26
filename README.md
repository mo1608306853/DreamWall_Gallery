
### project introduction
This system innovatively integrates scheduled tasks, large language models, and Stable Diffusion image generation technology. It automatically generates personalized text introductions based on preset preferences and converts them into vivid images. An intuitive interface is built with Tkinter to satisfy users' unique text and photo experiences.

### Adjustment Methods
1.Modify the IP in the user_setup.json file located in the client_code folder to the actual IP address of your WSL (Windows Subsystem for Linux) environment. 
2.Users can customize their preferred style and like text. 
3.Users can set the value of always_display to true to keep the page displayed continuously. If set to false, the system will generate text introductions, photos, and display them according to the configured run_interval time.

### Deployment Process
## Server-side Deployment Process
1.Install Vitis AI Docker Container in Windows 11 using WSL (Windows Subsystem for Linux):
Ensure WSL is enabled and configured on your Windows 11 system.
Use WSL to install the Vitis AI Docker container.
2.Select Linux Distribution (Ubuntu 20.04):
Choose Ubuntu 20.04 as the Linux distribution for your Docker container.
3.Use the ryzen-ai-pytorch Image:
Pull or select the ryzen-ai-pytorch Docker image for your container.
4.Container Port Mapping:
Map the container's port 9630 to the host's port 9630 for communication.
5.Docker Commands:
Use the following Docker commands for running, starting, accessing, and managing your container:

	docker run -p 9630:9630 -it container_id_or_name 
	docker start container_id_or_name 
	docker exec -it container_id_or_name /bin/bash 
	docker ps -a 
	docker cp [options] source_path container_id_or_name:destination_path

6.Download Large Language Model:
Download the large language model to server_code/model/Index_1_9B from the specified address: https://hf-mirror.com/IndexTeam/Index-1.9B/tree/main or https://huggingface.co/IndexTeam/Index-1.9B/tree/main.
 be careful! The directory cannot contain "." and can be replaced with "_"


7.Download Stable Diffusion Model:
Download the Stable Diffusion model to server_code/model/chilloutmix-fp16 from the provided model address: https://hf-mirror.com/sharpbai/chilloutmix-onnx-rocm-fp16/tree/main or https://huggingface.co/sharpbai/chilloutmix-onnx-rocm-fp16/tree/main .

8.Copy server_code Folder to the Docker Container:
Copy the server_code folder containing your server-side code into the running Docker container.
Install any necessary dependencies within the container.
9.Run tcp_server.py:
Within the Docker container, navigate to the server_code directory and execute python tcp_server.py to start the server.

## Client-side Deployment Process
1.Install Python 3 Environment:
Ensure Python 3 is installed on the client machine.
2.Install Required Dependencies:
Use pip to install any necessary Python libraries and dependencies for the client application.
3.Run the Client Program:
Navigate to the client_code folder on the client machine.
Open a command prompt or terminal and run python run.py to start the client application.
