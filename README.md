# TRANSPORT MANAGEMENT SYSTEM

## Tools and Skills Used
[![My Skills](https://skillicons.dev/icons?i=flask,html,css,py,vscode,git,mysql)](https://skillicons.dev)  

## Design
![updated_flowchart](https://github.com/ayushmodi12/transport-management-system/assets/113369113/eb11aa59-78fe-40c7-a429-9d7630195c47)

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
Before (in webApp):
![insert_before](https://github.com/ayushmodi12/transport-management-system/assets/95853168/285c6df4-3745-46ad-abca-e3431ebdecb9)
After (in webApp)
![insert_after](https://github.com/ayushmodi12/transport-management-system/assets/95853168/fe3a8b96-7ac0-4613-8856-5b4814c12da0)

Now in Admin Terminal for different query:
![Booking a seat](https://github.com/ayushmodi12/transport-management-system/assets/119656326/55cc64bc-a2b0-4e04-b851-8320e6ea58e5)  
We insert entries into the `booking` table upon successful booking.  

![Custom Insert](https://github.com/ayushmodi12/transport-management-system/assets/119656326/5e93f7ab-3cb1-4d59-97e2-53035f855dc1)  
We can also execute custom insert query in the admin terminal. Following is the result.  
![Custom Insert Out](https://github.com/ayushmodi12/transport-management-system/assets/119656326/3700abbf-8fba-40f3-82f3-5277e2a433ca)

### DELETE Operation:
Before (in webApp):
![insert_after](https://github.com/ayushmodi12/transport-management-system/assets/95853168/00bc9d3b-089e-4429-bc81-432f8bcb9429)
After (in webApp)
![delete_after](https://github.com/ayushmodi12/transport-management-system/assets/95853168/ac8ca8fd-1774-4ddb-95dc-a0988adedbe6)

Now in Admin Terminal for different query:
![Custom Del](https://github.com/ayushmodi12/transport-management-system/assets/119656326/eef9be9a-88ee-43c9-8d61-19ef90614300)  
We can also execute custom insert query in the admin terminal. Following is the result.  
![Custom Del out](https://github.com/ayushmodi12/transport-management-system/assets/119656326/e56bb0d6-cc92-4e5a-95c5-9bcbe978a67d)

### UPDATE Operation:
Before (in webApp):
![update_before](https://github.com/ayushmodi12/transport-management-system/assets/95853168/16693cf7-0f07-413f-9f09-02733825832c)
After (in webApp)
![update_after](https://github.com/ayushmodi12/transport-management-system/assets/95853168/511ce72b-181e-4442-a1f5-556836f02da7)

Now in Admin Terminal for different query:
![Custom Update](https://github.com/ayushmodi12/transport-management-system/assets/119656326/27bf73b7-d30b-4560-bae3-d232f390587c)  
We can also execute custom update query in the admin terminal. Following is the result.  
![Custom Update Out](https://github.com/ayushmodi12/transport-management-system/assets/119656326/1077b33a-0149-44d2-b1c1-233efcad8067)

### RENAME Operation:  
Before (updating table name):
![rename_1_before](https://github.com/ayushmodi12/transport-management-system/assets/95853168/cdfc2347-fcb9-4c19-89d2-042e91f87c42)
After (updating table name):
![rename_1_after](https://github.com/ayushmodi12/transport-management-system/assets/95853168/c61178e2-79ad-4006-aac8-a2e146dc4084)

Before (updating column name):
![rename_2_before](https://github.com/ayushmodi12/transport-management-system/assets/95853168/e60cd51f-6d35-424c-8115-a001bb8e54c1)
After (updating column name):
![rename_2_after](https://github.com/ayushmodi12/transport-management-system/assets/95853168/0998ab0d-0d36-4809-ab93-6c64afcc23ce)

### Use of WHERE Clause:
![whereclause_before](https://github.com/ayushmodi12/transport-management-system/assets/95853168/200b4cac-dc7b-4a39-bf14-2ad54dcb9049)
We can also execute custom where where clause in the admin terminal. Following are the results.
![whereclause_After](https://github.com/ayushmodi12/transport-management-system/assets/95853168/68a5f229-4a3c-4bb4-967a-42ff4b9e5ce6)

## Contributors
1) Mithil Pechimuthu
2) Ayush Modi
3) Shreesh Agarwal
4) Anushk Bhana
5) Vedant Kumbhar
