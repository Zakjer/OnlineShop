pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile.ci'
            args '--init -u root:root -e CLIENT_ID -e CLIENT_SECRET -e TENANT_ID -e SUBSCRIPTION_ID -e DB_PASSWORD -e SECRET_KEY -e DB_HOST -e DB_USER -e DB_NAME'
        }
    }

    environment {
        IMAGE_NAME = 'online-shop'
        IMAGE_TAG = "${BUILD_NUMBER}"
        ACR_NAME = 'onlineshopacr'
        ACR_SERVER = "${ACR_NAME}.azurecr.io"
        RESOURCE_GROUP = 'inzynierka'
        ACI_NAME = 'onelineshop-container'
        ACI_REGION = 'eastus'
        MYSQL_SERVER = 'onlineshop-mysql'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Running tests and checks') {
            steps {
                withCredentials([
                    string(credentialsId: 'db-password', variable: 'DB_PASSWORD'),
                    string(credentialsId: 'secret-key', variable: 'SECRET_KEY')
                ]) {
                    sh '''
                        python manage.py check
                        python manage.py test
                    '''
                }
            }
        }

        stage('Build docker image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Azure authentication') {
            steps {
                withCredentials([
                    string(credentialsId: 'azure-client-id', variable: 'CLIENT_ID'),
                    string(credentialsId: 'azure-client-secret', variable: 'CLIENT_SECRET'),
                    string(credentialsId: 'azure-tenant-id', variable: 'TENANT_ID'),
                    string(credentialsId: 'azure-subscription-id', variable: 'SUBSCRIPTION_ID')
                ]) {
                    sh '''
                        set -e

                        az login --service-principal \
                        --username "$CLIENT_ID" \
                        --password "$CLIENT_SECRET" \
                        --tenant "$TENANT_ID"

                        az account set --subscription "$SUBSCRIPTION_ID"

                        check_and_register () {
                        PROVIDER=$1
                        STATE=$(az provider show \
                            --namespace "$PROVIDER" \
                            --query "registrationState" \
                            -o tsv)

                        echo "$PROVIDER state: $STATE"

                        if [ "$STATE" != "Registered" ]; then
                            echo "Registering $PROVIDER..."
                            az provider register --namespace "$PROVIDER"
                            sleep 60
                        fi
                        }

                        check_and_register Microsoft.ContainerRegistry
                        check_and_register Microsoft.ContainerInstance
                        check_and_register Microsoft.DBforMySQL
                    '''
                }
            }
        }

        stage('Push image to Azure Container Registry') {
            steps {
                sh '''
                    az acr login --name $ACR_NAME

                    echo "Tagging Docker image"
                    docker tag $IMAGE_NAME:$IMAGE_TAG $ACR_SERVER/$IMAGE_NAME:$IMAGE_TAG

                    echo "Pushing Docker image to ACR"
                    docker push $ACR_SERVER/$IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }

        stage('Create Azure MySQL') {
            steps {
                sh '''
                set -e

                echo "Checking MySQL server..."
                if ! az mysql flexible-server show \
                    --resource-group $RESOURCE_GROUP \
                    --name $MYSQL_SERVER &>/dev/null; then

                    echo "Creating MySQL Flexible Server..."
                    az mysql flexible-server create \
                        --resource-group $RESOURCE_GROUP \
                        --name $MYSQL_SERVER \
                        --location $ACI_REGION \
                        --admin-user $DB_USER \
                        --admin-password $DB_PASSWORD \
                        --sku-name Standard_B1ms \
                        --storage-size 20 \
                        --version 8.0 \
                        --public-access 0.0.0.0
                        --workload-type Dev

                    echo "Waiting for MySQL server to be ready..."
                    sleep 60
                else
                    echo "MySQL server already exists"
                fi

                echo "Creating database if not exists..."
                az mysql flexible-server db create \
                    --resource-group $RESOURCE_GROUP \
                    --server-name $MYSQL_SERVER \
                    --name $DB_NAME || echo "Database already exists"
                '''
            }
        }

        stage('Deploy app to Azure Container Instance') {
            steps {
			sh '''
                echo "Checking if ACI $ACI_NAME exists..."
                if az container show --resource-group $RESOURCE_GROUP --name $ACI_NAME &>/dev/null; then
                    echo "Deleting existing ACI container..."
                    az container delete --resource-group $RESOURCE_GROUP --name $ACI_NAME --yes
                    echo "Waiting for deletion..."
                    sleep 10
                fi

				echo 'Deploying Image to ACI'
				az container create \
                    --name $ACI_NAME \
                    --resource-group $RESOURCE_GROUP \
                    --image $ACR_SERVER/$IMAGE_NAME:$IMAGE_TAG \
                    --registry-login-server $ACR_SERVER \
                    --registry-username $(az acr credential show --name $ACR_NAME --query username -o tsv) \
                    --registry-password $(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv) \
                    --dns-name-label online-shop-${BUILD_NUMBER} \
                    --ports 9000 \
                    --location $ACI_REGION \
                    --os-type Linux \
                    --cpu 1 \
                    --memory 1.5 \
                    --restart-policy Never

                echo "Waiting for ACI to initialize..."
                sleep 30

                echo "Getting the URL of the ACI app..."
                APP_URL=$(az container show \
                    --resource-group $RESOURCE_GROUP \
                    --name $ACI_NAME \
                    --query ipAddress.fqdn \
                    --output tsv):9000

                echo "Application URL: http://$APP_URL"
    			'''
			}
		}

        stage('Load demo data into Azure MySQL') {
            steps {
                withCredentials([string(credentialsId: 'db-password', variable: 'DB_PASSWORD')]) {
                    sh '''
                    echo "Loading demo data..."
                    mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME < data.sql
                    '''
                }
            }
        }
    }
}
