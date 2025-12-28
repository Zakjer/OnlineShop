pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'jenkins_test',
                url: 'git@github.com:Zakjer/OnlineShop.git',
                credentialsId: 'github-ssh'
                }
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

