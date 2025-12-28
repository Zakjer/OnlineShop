pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Python') {
            steps {
                sh '''
                    sudo apt-get update
                    sudo apt-get install -y python3.11 python3.11-venv python3-pip
                '''
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
    }
}
