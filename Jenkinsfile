pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'jenkins_test', url: 'https://github.com/Zakjer/OnlineShop.git'
            }
        }

        stage('Testing') {
            steps {
                script {
                        sh 'echo hello'
                }
            }
        }
    }
}
