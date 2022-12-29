
# Seller API's
Make bids on Auctions created by Admin

## Run Locally

####  Clone the project
> ```  git clone https://github.com/Codeansh/microservices ```


####  Create a new file named .flaskenv inside microservice/auction_service 

##### Structure should look like this :
> ```-> microservices          ```<br>
> ```       -> auction_service   ```<br>
> ```               -> .flaskenv ```
> 
##### Set Environment variables in .flaskenv file :
 ```FLASK_APP=app```<br>
```FLASK_DEBUG=True```<br>
```ADMIN_AUTH_KEY=GENERATE YOUR OWN KEY```<br>
```SECRET_KEY==GENERATE YOUR OWN KEY ```

#### Like above, create a new file named .flaskenv inside microservice/auth_service

##### Structure should look like this :
> ```-> microservices          ```<br>
> ```       -> auth_service      ```<br>
> ```               -> .flaskenv ```

##### Set Environment variables in .flaskenv file :
 ```FLASK_APP=app```<br>
```FLASK_DEBUG=True```<br>
```ADMIN_AUTH_KEY=GENERATE YOUR OWN KEY```<br>
```SECRET_KEY==GENERATE YOUR OWN KEY ```<br>
```UNAUTHENTICATED_ROUTES=['/auth/signup','/auth/login']```

#### Run the script in terminal ( Docker-Compose should be installed )

> ``` docker-compose up --build  ```<br>

###### Auction Service will be listening on http://localhost:5001/<br> Auth Service will be listening on http://localhost:5000/

##### To be Authenticated as Admin and access the Admin API's, create a new header named 'ADMIN_AUTH' and set its value equal to the value  of 'ADMIN_AUTH_KEY' in .flaskenv file
#### If Using Postman, do the same :
![Screenshot (16)](https://user-images.githubusercontent.com/73956838/209978181-9911d829-7eee-4e09-83c6-57e6936ed3b8.png)
