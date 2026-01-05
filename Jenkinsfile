pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile.ci'
            args '--init -u root:root'
        }
    }

    environment {
        IMAGE_NAME = 'online-shop'
        IMAGE_TAG = "${BUILD_NUMBER}"
        ACR_NAME = 'onlineshopacr'
        ACR_SERVER = "${ACR_NAME}.azurecr.io"
        RESOURCE_GROUP = 'inzynierka'
        ACI_NAME = 'xxx'
        ACI_REGION = 'xxx'
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
                sh '''
                    python manage.py check
                    python manage.py test
                '''
            }
        }

        stage('Build docker image') {
            steps {
                script {
                        sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .'
                }
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
                        env
                        az login --service-principal \
                            --username "$CLIENT_ID" \
                            --password "$CLIENT_SECRET" \
                            --tenant "$TENANT_ID"

                        az account set --subscription "$SUBSCRIPTION_ID"
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
    }
}
