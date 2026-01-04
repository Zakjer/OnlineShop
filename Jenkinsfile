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
                withCredentials([file(credentialsId: 'azure-creds', variable: 'AZURE_CRED')]) {
                    sh '''
                            az login --service-principal --username $(jq -r .clientId $AZURE_CRED) \
                                        --password $(jq -r .clientSecret $AZURE_CRED) \
                                        --tenant $(jq -r .tenantId $AZURE_CRED) > /dev/null
                                az account set --subscription $(jq -r .subscriptionId $AZURE_CRED)
                    '''
                }
            }
        }

        stage('Push image to Azure Container Registry') {
            steps {
                withCredentials([file(credentialsId: 'azure-creds', variable: 'AZURE_CRED')]) {
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
}
