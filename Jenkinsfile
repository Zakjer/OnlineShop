pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile.ci'
            args '--init -u root:root -e CLIENT_ID -e CLIENT_SECRET -e TENANT_ID -e SUBSCRIPTION_ID -e DB_PASSWORD -e SECRET_KEY -e DB_HOST -e DB_USER -e DB_NAME -e SENDGRID_API_KEY'
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

        stage('Security scan') {
            steps {
                sh '''
                trivy image --severity CRITICAL --exit-code 1 --ignore-unfixed ${IMAGE_NAME}:${IMAGE_TAG}
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

                    echo "Tagging Docker image..."
                    docker tag $IMAGE_NAME:$IMAGE_TAG $ACR_SERVER/$IMAGE_NAME:$IMAGE_TAG

                    echo "Pushing Docker image to ACR..."
                    docker push $ACR_SERVER/$IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }

        stage('Deploy App + MySQL to ACI') {
            steps {
                withCredentials([
                    string(credentialsId: 'db-password', variable: 'DB_PASSWORD'),
                    string(credentialsId: 'secret-key', variable: 'SECRET_KEY')
                ]) {
                    sh '''
                    set -e

                    ACI_GROUP_NAME=onlineshop-group
                    FILE_SHARE_NAME=mysql-data
                    STORAGE_ACCOUNT=onlineshopstorage2

                    if ! az storage account show \
                        --name $STORAGE_ACCOUNT \
                        --resource-group $RESOURCE_GROUP >/dev/null 2>&1; then

                    echo "Creating storage account: $STORAGE_ACCOUNT"
                    az storage account create \
                        --name $STORAGE_ACCOUNT \
                        --resource-group $RESOURCE_GROUP \
                        --location $ACI_REGION \
                        --sku Standard_LRS
                    else
                    echo "Storage account already exists, reusing it"
                    fi

                    STORAGE_KEY=$(az storage account keys list \
                        --resource-group $RESOURCE_GROUP \
                        --account-name $STORAGE_ACCOUNT \
                        --query '[0].value' -o tsv)

                    echo "Creating file share..."
                    az storage share create \
                        --account-name $STORAGE_ACCOUNT \
                        --account-key $STORAGE_KEY \
                        --name $FILE_SHARE_NAME


                    echo "Deleting existing ACI group (if any)"
                    az container delete \
                        --resource-group $RESOURCE_GROUP \
                        --name $ACI_GROUP_NAME \
                        --yes || true
                    sleep 10

                    ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
                    ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)
                    echo "Generating aci-group.yaml"
                    cat > aci-group.yaml <<EOF
apiVersion: 2021-09-01
location: ${ACI_REGION}
name: ${ACI_GROUP_NAME}
properties:
  osType: Linux
  restartPolicy: Always

  imageRegistryCredentials:
    - server: onlineshopacr.azurecr.io
      username: ${ACR_USERNAME}
      password: ${ACR_PASSWORD}
  containers:
    - name: mysql
      properties:
        image: onlineshopacr.azurecr.io/mysql:8.0
        resources:
          requests:
            cpu: 1
            memoryInGB: 1.5
        environmentVariables:
          - name: MYSQL_ROOT_PASSWORD
            value: ${DB_PASSWORD}
          - name: MYSQL_DATABASE
            value: ${DB_NAME}

    - name: django
      properties:
        image: ${ACR_SERVER}/${IMAGE_NAME}:${IMAGE_TAG}
        ports:
          - port: 9000
        resources:
          requests:
            cpu: 1
            memoryInGB: 2
        environmentVariables:
          - name: DB_HOST
            value: 127.0.0.1
          - name: DB_PORT
            value: "3306"
          - name: DB_NAME
            value: ${DB_NAME}
          - name: DB_USER
            value: root
          - name: DB_PASSWORD
            value: ${DB_PASSWORD}
          - name: SECRET_KEY
            value: ${SECRET_KEY}
          - name: SENDGRID_API_KEY
            secureValue: ${SENDGRID_API_KEY}

  ipAddress:
    type: Public
    dnsNameLabel: onlineshopsite
    ports:
      - protocol: tcp
        port: 9000

  volumes:
    - name: mysql-volume
      azureFile:
        shareName: ${FILE_SHARE_NAME}
        storageAccountName: ${STORAGE_ACCOUNT}
        storageAccountKey: ${STORAGE_KEY}
EOF

            echo "Deploying ACI group..."
            az container create \
                --resource-group $RESOURCE_GROUP \
                --file aci-group.yaml

            APP_FQDN=$(az container show \
                --resource-group $RESOURCE_GROUP \
                --name $ACI_GROUP_NAME \
                --query ipAddress.fqdn -o tsv)

            echo "Application URL: http://$APP_FQDN:9000"
            '''
                }
            }
        }
        stage('Run Django migrations') {
            steps {
                sh '''
                    echo "Running Django migrations inside the container..."
                    az container exec \
                        --resource-group $RESOURCE_GROUP \
                        --name onlineshop-group \
                        --container-name django \
                        --exec-command "python manage.py migrate"
                '''
            }
        }

        stage('Import database data') {
            steps {
                withCredentials([
                    string(credentialsId: 'db-password', variable: 'DB_PASSWORD')
                ]) {
                    sh '''
                    echo "Importing SQL data into MySQL container..."

                    az container exec \
                    --resource-group $RESOURCE_GROUP \
                    --name onlineshop-group \
                    --container-name mysql \
                    --exec-command "mysql -u root -p$DB_PASSWORD shop_database" < db_dump.sql &

                    sleep 45
                    '''
                }
            }
        }
    }
}
