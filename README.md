# TRANSPRT MANAGEMENT SYSTEM

## Tools and Skills Used
[![My Skills](https://skillicons.dev/icons?i=flask,html,css,py,vscode,git,mysql)](https://skillicons.dev)  

## Design
![Website Design](https://github.com/ayushmodi12/transport-management-system/assets/138511229/68260c57-bf9f-4842-8a97-d58a617a78aa)


## Running the project
Currently, this project is supported in Windows devices only.  

## Setting up the Server
First, change the working directory to `transport-management-system` after cloning this repository.  
``` git clone https://github.com/ayushmodi12/transport-management-system.git```

### Installing all the dependencies
Please run the following command with the cloned repository as the current working directory to install all the required modules and packages.
```
pip install -r requirements.txt
```

### Create Database & Launch Web Server
Please run the `setup.py` to instantiate the database and launch the web server.  
Make sure that you don't have the database before running `setup.py`. Else directly launch the web server by executing `tms.py`. 

## Setting up the Client
### Add DNS Entry
1) Go to the hosts file. It can be typically found here `C:\Windows\System32\drivers\etc\hosts`.  
2) Add the following translation `127.0.0.1   tms.iitgn.ac.in` if the client and server are hosted on the same machine. Else add the public of the server machine. After that, your hosts file should look like this.  
![Hosts File](hosts.png)  

Now `tms.iitgn.ac.in` is mapped to `127.0.0.1`, i.e. the local host and now we can access it like an actual website. So if we type `http://tms.iitgn.ac.in:5000/` on our browser, we will be able to access the webpage!  
We can also create our own personal local network, and set up the server in one computer, and access the webpage from another computer. This can be shown as a demo to the TA when requested.  

### Access the Webpage
Access the website by typing `http://tms.iitgn.ac.in:5000/` on the browser.  

## Screenshots of successful execution of the dynamic operations
### INSERT Operation:
![Booking a seat](https://github.com/ayushmodi12/transport-management-system/assets/119656326/55cc64bc-a2b0-4e04-b851-8320e6ea58e5)  
We insert entries into the `booking` table upon successful booking.  

![Custom Insert](https://github.com/ayushmodi12/transport-management-system/assets/119656326/5e93f7ab-3cb1-4d59-97e2-53035f855dc1)  
We can also execute custom insert query in the admin terminal. Following is the result.  
![Custom Insert Out](https://github.com/ayushmodi12/transport-management-system/assets/119656326/3700abbf-8fba-40f3-82f3-5277e2a433ca)

### DELETE Operation:
![Custom Del](https://github.com/ayushmodi12/transport-management-system/assets/119656326/eef9be9a-88ee-43c9-8d61-19ef90614300)  
We can also execute custom insert query in the admin terminal. Following is the result.  
![Custom Del out](https://github.com/ayushmodi12/transport-management-system/assets/119656326/e56bb0d6-cc92-4e5a-95c5-9bcbe978a67d)

### UPDATE Operation:
![Custom Update](https://github.com/ayushmodi12/transport-management-system/assets/119656326/27bf73b7-d30b-4560-bae3-d232f390587c)  
We can also execute custom update query in the admin terminal. Following is the result.  
![Custom Update Out](https://github.com/ayushmodi12/transport-management-system/assets/119656326/1077b33a-0149-44d2-b1c1-233efcad8067)

### RENAME Operation:  

### Use of WHERE Clause:

## Contributors
1) Mithil Pechimuthu
2) Ayush Modi
3) Shreesh Agarwal
4) Anushk Bhana
5) Vedant Kumbhar
