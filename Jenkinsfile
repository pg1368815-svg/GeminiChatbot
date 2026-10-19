pipeline {
agent any

```
environment {
    AWS_REGION = 'ap-south-1'
    AWS_ACCOUNT_ID = '657231015453'
    ECR_REPOSITORY = 'gemini-chatbot'
    ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
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

    stage('ECR Login') {
        steps {
            sh '''
                aws ecr get-login-password --region ${AWS_REGION} |
                docker login --username AWS --password-stdin ${ECR_REGISTRY}
            '''
        }
    }

    stage('Tag Image for ECR') {
        steps {
            sh '''
                docker tag ${IMAGE_NAME}:latest \
                ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest
            '''
        }
    }

    stage('Push Image to ECR') {
        steps {
            sh '''
                docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest
            '''
        }
    }

    stage('Stop Old Container') {
        steps {
            sh 'docker rm -f ${CONTAINER_NAME} || true'
        }
    }

    stage('Run Container') {
        steps {
            withCredentials([
                string(
                    credentialsId: 'GEMINI_API_KEY',
                    variable: 'GEMINI_API_KEY'
                )
            ]) {
                sh '''
                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p 5000:5000 \
                        -e GEMINI_API_KEY="${GEMINI_API_KEY}" \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest
                '''
            }
        }
    }
}

post {
    success {
        echo 'Gemini Chatbot built, pushed to ECR, and deployed on EC2 successfully!'
    }

    failure {
        echo 'Pipeline failed. Check Console Output for the failing stage.'
    }
}
```

}
