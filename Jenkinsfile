pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile.ci'
            args '--init -u root:root -e CLIENT_ID -e CLIENT_SECRET -e TENANT_ID -e SUBSCRIPTION_ID'
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
                    ls -la
                    cat .env
                '''
            }
        }

        stage('Running tests and checks') {
            steps {
                sh '''
                    python manage.py check
                    python manage.py test
                '''
            }
        }

        stage('Build docker image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Azure authentication and configuration') {
            steps {
                withCredentials([
                    string(credentialsId: 'azure-client-id', variable: 'CLIENT_ID'),
                    string(credentialsId: 'azure-client-secret', variable: 'CLIENT_SECRET'),
                    string(credentialsId: 'azure-tenant-id', variable: 'TENANT_ID'),
                    string(credentialsId: 'azure-subscription-id', variable: 'SUBSCRIPTION_ID')
                ]) {
                    sh """
                        az login --service-principal \
                            --username "\$CLIENT_ID" \
                            --password "\$CLIENT_SECRET" \
                            --tenant "\$TENANT_ID"

                        az account set --subscription "\$SUBSCRIPTION_ID"

                        echo "Enabling admin user on ACR"
                        az acr update -n $ACR_NAME --admin-enabled true

                        STATE_ACR=\$(az provider show --namespace Microsoft.ContainerRegistry --query "registrationState" -o tsv)
                        STATE_ACI=\$(az provider show --namespace Microsoft.ContainerInstance --query "registrationState" -o tsv)
                        echo "ACR Provider state: \$STATE_ACR"
                        echo "ACI Provider state: \$STATE_ACI"

                        if [ "\$STATE_ACR" = "NotRegistered" ] || [ "\$STATE_ACI" = "NotRegistered" ]; then
                            echo "Registering Azure providers..."
                            az provider register --namespace Microsoft.ContainerRegistry
                            az provider register --namespace Microsoft.ContainerInstance
                            echo "Waiting for registration to complete..."
                            sleep 60
                        fi
                        """
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

        stage('Deploy app to Azure Container Instance') {
            steps {
			sh '''
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
    }
}
