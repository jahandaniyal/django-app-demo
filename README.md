# django-app-demo

## Features
* JWT Token based authentication
* User Management API to create new users
* A default Admin `{'name': 'admin', 'password': '12345'}` is created automatically during build (only for local testing purposes).
* Authenticated Users can create orders and view a history of their orders.
* Supports a list-view for products with additional features like:
   * Paginated view example - `BASE_URL/api/product?limit=5&offset=5`
   * Filter product by keyword (for example `keyword=redbull`)
   * Filter products by max_price (for example `max_price=1.5` will return all products that have unit price <= 1.5)
* Once an order is made, the quantity of a product is deducted from its actual stock:
   * If requested quantity is less than available stock -> Order is placed succesfully.
   * If requested quantity is more than available stock -> Order is declined and no database transactions are rolled back.
* Users can filter products - This is acheived using query params `max_price=<value>` and `keywords=<name>`. 
   * For example, `BASE_URL/api/product?max_price=5.3&keyword=yellow` will filter products containing the word 'yellow' and price less tha
* Targets in Makefile to ease local development - more details in the Local Development Setup section.

## Local Development Setup
* Use Make to build, run, test and clean the local development environment (assumes a linux-like environment - Tested on ubuntu).
* build - This target will build the docker containers, install all dependencies in requirements.txt and make the initial migrations to the DB. 
   * `make build`
* run - Run the server for testing locally.
   * `make run`
* test - Runs pytests on the test suites for JWT token, User and Orders operations.
   * `make test`
* clean - Removes generated files
   * `make clean`

## Running Locally

### Endpoints
* /api/token/
   * POST
* /api/register/
   * POST
* /api/product/?max_price=<value>&keyword=<name>&limit=<value>&offset=<value>
   * GET, POST
* /api/product/{id}
   * GET, PUT, DELETE
* /api/order/
  *  GET, POST
   
### Create an Admin
* Ideally, you would want to create a SuperUser/Admin for your application. This is already done in `make build` step.
   * A default Admin `{'name': 'admin', 'password': '12345'}` with these credentials is created for testing.
   
### Create new users:
* Use API endpoint `BASE_URL/api/register/` to create a new user. Where `BASE_URL` could be for example - `http://127.0.0.1:8000/`
   * Body structure is similar to - `{"name": "user1", "password": "123abc#$%"}`. Remember your password obviously! 

### Get a Web Token
* Use API endpoint `BASE_URL/api/token/` to get 'access' and 'refresh' token. 
   * Body - `{"name": "user1", "password": "123abc#$%"}`.

### Create a new Product
*  Use API endpoint `BASE_URL/api/product/` to create a new product. You will need 'access' token from the previous step.
   * Body -  Example `{
    "name": "RedBull",
    "price": "2.2",
    "stock": "100"
} `
   * Headers - Authorization: Bearer <ACCESS_TOKEN>

### Get Product list
* Use API endpoint `BASE_URL/api/product/` to fetch a list of products. Optionally pass query params max_price, keyword.
* User Authorization header.

### Get, Update and Delete a Product
* Use API endpoint `BASE_URL/api/product/{id}`. You will need 'access' token from the previous step.
* Body and Header if required is same as described earlier.
  
### Create a new Order
*  Use API endpoint `BASE_URL/api/order/` to create a new order. You will need 'access' token from the previous step.
   * Body -  Example `{
    "products": [
                  {"id": 1, "quantity": 15},
                  {"id": 2, "quantity": 13}
                ]
} `
   * Headers - Authorization: Bearer <ACCESS_TOKEN>

### Get Orders
* Use API endpoint `BASE_URL/api/order/` to fetch a list of orders.
* User Authorization header.



ToDos:
* [ ] Use nginx + gunicorn/uwsgi instead of django built-in server.
* [ ] Use OpenAPI for documenting the API instead of writing it here in README.
* [ ] Use Prometheus + Grafana for monitoring health of services.
* [ ] Add Custom error handling page for example, handler404 & handler500.
* [ ] Deploy on K8s cluster.

## Deployment strategies
Here we dicuss one of the many ways for deployment in production. We will be using AWS ECS.
   *  First create and configure EC2 instance
   *  Assign static IP through AWS Elastic IP service.
   *  Optionally create IAM Roles if it is not available already.
   *  Register your docker images with AWS ECR. We will use it to push our docker images and make it available to AWS ECS.
   *  Configure AWS RDS (recommended) with postgres, or skip this step and use dockerised self hosted postgres server.
   *  Configure all security groups for exposing required ports.
   *  Finally spin up the ECS resources.
