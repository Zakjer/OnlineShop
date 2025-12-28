pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            args '-u root:root'
            reuseNode true
        }
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
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Running tests and checks') {
            steps {
                script {
                    try {
                        sh '''
                            python manage.py check
                            python manage.py test
                        '''
                    } catch (err) {
                        if (!err.toString().contains("Failed to kill container")) {
                            throw err
                        } else {
                            echo "Warning: Jenkins failed to stop Docker container, ignoring."
                        }
                    }
                }
            }
        }
    }
}
