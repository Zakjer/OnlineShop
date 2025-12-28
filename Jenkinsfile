pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Running unit tests') {
            steps {
                sh 'python manage.py test'
            }
        }
    }
}
