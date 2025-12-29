pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build debug image') {
            steps {
                sh '''
                    set -euxo pipefail
                    docker build -t debug-image .
                '''
            }
        }

        stage('Run tests in container') {
            steps {
                sh '''
                    set -euxo pipefail

                    docker run --name debug-container --init debug-image sh -c "
                        pip install --upgrade pip &&
                        pip install -r requirements.txt &&
                        python manage.py check &&
                        python manage.py test
                    "
                '''
            }
        }
    }

    post {
        failure {
            echo 'Pipeline failed — keeping container alive for debugging'
            sh '''
                docker ps -a | grep debug-container || true
                echo "You can now inspect the container:"
                echo "  docker logs debug-container"
                echo "  docker exec -it debug-container sh"
            '''
        }

        always {
            echo 'Pipeline finished'
        }
    }
}
