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

        stage('Deploy App + MySQL to ACI') {
            steps {
                withCredentials([string(credentialsId: 'db-password', variable: 'DB_PASSWORD')]) {
                    sh '''
                    set -e

                    # Fetch ACR credentials
                    ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
                    ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)

                    # Storage account for MySQL persistence
                    STORAGE_ACCOUNT=onlineshopdb$(date +%s | tail -c 5)
                    az storage account create --name $STORAGE_ACCOUNT --resource-group $RESOURCE_GROUP --location $ACI_REGION --sku Standard_LRS || true
                    STORAGE_KEY=$(az storage account keys list --resource-group $RESOURCE_GROUP --account-name $STORAGE_ACCOUNT --query '[0].value' -o tsv)

                    # Create file share for MySQL
                    FILE_SHARE_NAME=mysql-data
                    az storage share create --account-name $STORAGE_ACCOUNT --account-key $STORAGE_KEY --name $FILE_SHARE_NAME || true

                    # Delete existing ACI group if exists
                    az container delete --resource-group $RESOURCE_GROUP --name onlineshop-group --yes || true
                    sleep 10

                    # Upload data.sql
                    az storage file upload --account-name $STORAGE_ACCOUNT --account-key $STORAGE_KEY --share-name $FILE_SHARE_NAME --source data.sql --path data.sql

                    # Upload data.sql
                    az storage file upload \
                    --account-name $STORAGE_ACCOUNT \
                    --account-key $STORAGE_KEY \
                    --share-name $FILE_SHARE_NAME \
                    --source data.sql \
                    --path data.sql

                    # Deploy Django + MySQL
                    az container create \
                    --resource-group $RESOURCE_GROUP \
                    --name onlineshop-group \
                    --location $ACI_REGION \
                    --dns-name-label online-shop-${BUILD_NUMBER} \
                    --os-type Linux \
                    --cpu 2 --memory 3.5 \
                    --restart-policy Always \
                    --container-name django \
                    --image $ACR_SERVER/$IMAGE_NAME:$IMAGE_TAG \
                    --registry-login-server $ACR_SERVER \
                    --registry-username $ACR_USERNAME \
                    --registry-password $ACR_PASSWORD \
                    --environment-variables \
                        DB_HOST=127.0.0.1 \
                        DB_USER=$DB_USER \
                        DB_PASSWORD=$DB_PASSWORD \
                        DB_NAME=$DB_NAME \
                        SECRET_KEY=$SECRET_KEY \
                    --ports 9000 \
                    --container-name mysql \
                    --image mysql:8.0 \
                    --environment-variables \
                        MYSQL_ROOT_PASSWORD=$DB_PASSWORD \
                        MYSQL_DATABASE=$DB_NAME \
                    --azure-file-volume-share-name $FILE_SHARE_NAME \
                    --azure-file-volume-account-name $STORAGE_ACCOUNT \
                    --azure-file-volume-account-key $STORAGE_KEY \
                    --azure-file-volume-mount-path /docker-entrypoint-initdb.d

                    # Wait for MySQL
                    sleep 40

                    # Get app URL
                    APP_URL=$(az container show --resource-group $RESOURCE_GROUP --name onlineshop-group --query ipAddress.fqdn -o tsv):9000
                    echo "Application URL: http://$APP_URL"
                    '''
                }
            }
        }




    }
}
