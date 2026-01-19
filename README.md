OnlineShop is a Django-based e-commerce web application built with DevOps practices.  
The project is fully containerized, uses a Jenkins CI/CD pipeline, and is deployed to Microsoft Azure using Azure Container Instances (ACI).

## Features

- Django backend covered with unit tests (Python)
- Product catalog and admin panel
- CI/CD pipeline with Jenkins (configured with JCasC)
- Deployment to Azure Container Instances (ACI)
- MySQL database with persistent storage
- Email sending
- Environment-based configuration

## Accessing the app
There are basically two ways to access the app. First one is to visit the link hosted on Azure but it may be slow or temporary unavailable due to cost reduction. The second option is to run the app locally with steps explained below.

### App link: http://onlineshopsite.eastus.azurecontainer.io:9000

### Running app locally

#### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git
- Gunicorn

#### Clone Repository
```
git clone https://github.com/Zakjer/OnlineShop.git  
cd OnlineShop
```

#### Create database and populate it with dummy data
```
CREATE DATABASE shop_database CHARACTER SET utf8mb4;
mysql -u root -p shop_database < db_dump.sql
```

#### Create a `.env` file in the project root
```
SECRET_KEY="generate using Django's get_random_secret_key()" 
DB_NAME=shop_database  
DB_USER=root  
DB_PASSWORD="your_db_password"
DB_HOST=127.0.0.1  
DB_PORT=3306  
```

#### Run Locally with gunicorn
```
pip install -r requirements.txt
python -m gunicorn OnlineShop.wsgi:application --bind 0.0.0.0:9000
```

Application should now be available at:  
http://localhost:9000/


## CI/CD Pipeline

The Jenkins pipeline performs:

1. Code checkout
2. Django checks and tests
3. Docker image build
4. Security scan using Trivy
5. Push image to Azure Container Registry
6. Deploy to Azure Container Instances
7. Run Django migrations
8. Import database data
![alt text](https://github.com/Zakjer/OnlineShop/blob/master/media/shop/images/pipeline.png)

