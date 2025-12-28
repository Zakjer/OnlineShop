pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Testing') {
            steps {
                sh 'echo hello'
            }
        }
    }
}
