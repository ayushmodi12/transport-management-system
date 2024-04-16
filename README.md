WRITE FOR ASSIGNMENT 4 IS FOUND HERE:--> https://drive.google.com/file/d/1lLgN7pTO_a6krywIUAJEYwMZZ766K1k0/view?usp=sharing  (The file size of greater than 25mb could not be uploaded to github, so the drive link)  
# TRANSPORT MANAGEMENT SYSTEM

## Tools and Skills Used
[![My Skills](https://skillicons.dev/icons?i=flask,html,css,py,vscode,git,mysql)](https://skillicons.dev)  

## Design
![updated_flowchart](https://github.com/ayushmodi12/transport-management-system/assets/113369113/eb11aa59-78fe-40c7-a429-9d7630195c47)

## Running the project

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
## For Non windows users
Access the website by typing `http://127.0.0.1:5000/` on the browser.   

## Screenshots of successful execution of the dynamic operations
### INSERT Operation:
Before inserting, viewing the table on workbench:

![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/8296cec6-cdf7-4d1f-90ac-151388ef3307)

Now, inserting a new value in the table:

![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/4c0a2fd1-9346-4761-9c6e-e1651e425033)

![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/02486ea2-cdcc-47ea-9fd0-7e19eb34fb05)

New value inserted can be seen on workbench:

![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/b2af0c63-f876-49c8-8528-825c3958f2d0)

Showing the Updated and before states of the table on the website:

After (in webApp)
![insert_after](https://github.com/ayushmodi12/transport-management-system/assets/95853168/fe3a8b96-7ac0-4613-8856-5b4814c12da0)
Before (in webApp):
![insert_before](https://github.com/ayushmodi12/transport-management-system/assets/95853168/285c6df4-3745-46ad-abca-e3431ebdecb9)


Now in Admin Terminal for different query:
![Booking a seat](https://github.com/ayushmodi12/transport-management-system/assets/119656326/55cc64bc-a2b0-4e04-b851-8320e6ea58e5)  
We insert entries into the `booking` table upon successful booking.  

![Custom Insert](https://github.com/ayushmodi12/transport-management-system/assets/119656326/5e93f7ab-3cb1-4d59-97e2-53035f855dc1)  
We can also execute custom insert query in the admin terminal. Following is the result.  
![Custom Insert Out](https://github.com/ayushmodi12/transport-management-system/assets/119656326/3700abbf-8fba-40f3-82f3-5277e2a433ca)

### DELETE Operation:
Before Deleting, viewing the table on workbench:

![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/aca95695-2f7f-4ae2-a671-6c42ddc1a40e)

Now, deleting the row where capacity = 20:

![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/8cfdfbd2-4e7e-4b7b-8904-5c68b8bffa5b)

![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/546ed208-2e47-4dce-af81-15e8f59212e1)

We can see on workbench, that the row having capacity = 20 is deleted:

![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/2a1c6cde-08d8-44e8-835f-bde563166a5f)

Showing the Updated and before states of the table on the website:

After (in webApp)
![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/cb334506-165f-4e67-8b9b-a0b0eb785b72)
Before (in webApp):
![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/3beb56c0-192b-4c53-915a-6bbbaebb4a01)


Now in Admin Terminal for **different** query:
![Custom Del](https://github.com/ayushmodi12/transport-management-system/assets/119656326/eef9be9a-88ee-43c9-8d61-19ef90614300)  
We can also execute custom delete query in the admin terminal. Following is the result.  
![Custom Del out](https://github.com/ayushmodi12/transport-management-system/assets/119656326/e56bb0d6-cc92-4e5a-95c5-9bcbe978a67d)

### UPDATE Operation:
Before updating, viewing the table on workbench:

![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/f3595649-86a4-4b22-bc54-053f25a6b549)

Now, updating the capacity to 60 in the row where location="Hostel Parking Area":
NOTE: Only those input fields are to be filled for which we want to update the values, if the field is left empty, the value for that column will not be updated.

![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/1eccd566-c97b-4bcd-aeb4-cbbb8ae17f6b)

![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/b7196a7a-1ee2-4d7d-990c-cd46b5412b04)

This updated row can be seen in the table on workbench:

![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/ceb9f1a8-fea7-452b-a29e-afb861c0573f)

Showing the Updated and before states of the table on the website:

After (in webApp)
![update_after](https://github.com/ayushmodi12/transport-management-system/assets/95853168/511ce72b-181e-4442-a1f5-556836f02da7)
Before (in webApp):
![update_before](https://github.com/ayushmodi12/transport-management-system/assets/95853168/16693cf7-0f07-413f-9f09-02733825832c)


Now in Admin Terminal for different query:
![Custom Update](https://github.com/ayushmodi12/transport-management-system/assets/119656326/27bf73b7-d30b-4560-bae3-d232f390587c)  
We can also execute custom update query in the admin terminal. Following is the result.  
![Custom Update Out](https://github.com/ayushmodi12/transport-management-system/assets/119656326/1077b33a-0149-44d2-b1c1-233efcad8067)

### RENAME Operation:  
Before renaming, viewing the current table on workbench:

![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/91a85cc8-1971-40b0-92db-b6f6458bc331)

Now, updating the table name to parking_space_new:
NOTE: Only those input fields are to be filled for which we want to rename, for rest others, leave the input field empty:

![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/9cd68679-e5d4-448b-b773-f8f70f3ff729)

![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/0fb3c8c8-011a-431a-9c29-493b75523f0a)

As we can see on workbench, the table name has been updated to parking_space_new:

![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/90ea8130-3b03-4ac1-92e2-6c8ff8e4cf06)

![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/dae9c2b1-52c9-4f49-a106-920f80ee0603)

Showing the Updated and before states of the table on website:

After (updating table name):
![rename_1_after](https://github.com/ayushmodi12/transport-management-system/assets/95853168/c61178e2-79ad-4006-aac8-a2e146dc4084)
Before (updating table name):
![rename_1_before](https://github.com/ayushmodi12/transport-management-system/assets/95853168/cdfc2347-fcb9-4c19-89d2-042e91f87c42)

Now, renaming the column **location** to **location_2**:
![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/db01b24b-0d94-45c9-99ef-a074a08552f3)

We can see in the workbench, the table name of location has been changed:

![image](https://github.com/ayushmodi12/transport-management-system/assets/95853168/295bcf3d-8ea1-46e1-94b9-617dc2753335)

Showing the Updated and before states of the table on the website:
After (updating column name):
![rename_2_after](https://github.com/ayushmodi12/transport-management-system/assets/95853168/0998ab0d-0d36-4809-ab93-6c64afcc23ce)
Before (updating column name):
![rename_2_before](https://github.com/ayushmodi12/transport-management-system/assets/95853168/e60cd51f-6d35-424c-8115-a001bb8e54c1)


### Use of WHERE Clause:
Now, the WHERE clause has already been used in the above operations where we have performed UPDATE and DELETE. 
The input field “Condition” in UPDATE and DELETE Operations takes the WHERE Clause as input and accordingly performs the operations. The screenshots for the operations have thus already been shown in the above sections. Below is the snippet of the code for the /update-values api, that creates the sql query for UPDATE operation using WHERE Clause:
![whereclause_final](https://github.com/ayushmodi12/transport-management-system/assets/95853168/0a0ade02-f950-4c37-b2af-bc39eb91f43b)
As we have already added screenshots above in UPDATE and DELETE, which also contain the WHERE Clause, we are not adding screenshots here.

![whereclause_before](https://github.com/ayushmodi12/transport-management-system/assets/95853168/200b4cac-dc7b-4a39-bf14-2ad54dcb9049)
We can also execute custom where where clause in the admin terminal. Following are the results.
![whereclause_After](https://github.com/ayushmodi12/transport-management-system/assets/95853168/68a5f229-4a3c-4bb4-967a-42ff4b9e5ce6)

## Contributors
1) Mithil Pechimuthu
2) Ayush Modi
3) Shreesh Agarwal
4) Anushk Bhana
5) Vedant Kumbhar
