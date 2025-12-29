pipeline {
    agent any

    stages {
        stage('Debug container') {
            steps {
                sh '''
                set -eux
                docker build -t debug-image .
                docker run --name debug-container --init debug-image sh -c "sleep 300"
                '''
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
