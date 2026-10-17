pipeline {
    agent any

    environment {
        IMAGE_NAME = 'gemini-chatbot'
        CONTAINER_NAME = 'gemini-chatbot'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker rm -f ${CONTAINER_NAME} || true'
            }
        }

        stage('Run Container') {
            steps {
                withCredentials([string(
                    credentialsId: 'GEMINI_API_KEY',
                    variable: 'GEMINI_API_KEY'
                )]) {
                    sh '''
                        docker run -d \
                            --name ${CONTAINER_NAME} \
                            -p 5000:5000 \
                            -e GEMINI_API_KEY="$GEMINI_API_KEY" \
                            ${IMAGE_NAME}:latest
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Gemini Chatbot deployed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the Jenkins console output.'
        }
    }
}
