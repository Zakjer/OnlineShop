pipeline {
    agent any

    stages {
        stage('Manual docker run') {
            steps {
                sh '''
                docker build -t debug-image .
                docker run --name debug-container -it debug-image bash
                '''
            }
        }

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
    }
}
