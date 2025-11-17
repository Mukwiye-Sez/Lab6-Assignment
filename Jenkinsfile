pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins/label: docker-agent
spec:
  containers:
  - name: docker
    image: docker:27.1.2-cli
    command:
      - cat
    tty: true
    volumeMounts:
      - name: docker-sock
        mountPath: /var/run/docker.sock
  volumes:
  - name: docker-sock
    hostPath:
      path: /var/run/docker.sock
      type: Socket
"""
            defaultContainer 'docker'
        }
    }

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds')
        IMAGE_NAME = "mukkris/lab6-app"
    }

    stages {
        stage("Build Docker Image") {
            steps {
                sh "docker version"
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
            }
        }

        stage("Login to Docker Hub") {
            steps {
                sh """
                echo "${DOCKERHUB_CREDENTIALS_PSW}" \
                  | docker login -u "${DOCKERHUB_CREDENTIALS_USR}" --password-stdin
                """
            }
        }

        stage("Push Image") {
            steps {
                sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
            }
        }
    }
}
