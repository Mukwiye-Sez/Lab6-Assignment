pipeline {
    agent {
        kubernetes {
            label "lab6-pipeline-${env.BUILD_ID}"
            defaultContainer 'jnlp'
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins/label: "lab6-pipeline-${env.BUILD_ID}"
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
        - name: workspace-volume
          mountPath: /home/jenkins/agent
          readOnly: false
    - name: jnlp
      image: jenkins/inbound-agent:3345.v03dee9b_f88fc-1
      env:
        - name: JENKINS_URL
          value: "http://jenkins.jenkins.svc.cluster.local:8080/"
      resources:
        requests:
          memory: "256Mi"
          cpu: "100m"
      volumeMounts:
        - name: workspace-volume
          mountPath: /home/jenkins/agent
          readOnly: false
  volumes:
    - name: docker-sock
      hostPath:
        path: /var/run/docker.sock
        type: Socket
    - name: workspace-volume
      emptyDir: {}
            """
        }
    }

    environment {
        DOCKER_IMAGE = "mukkri5/lab6-app:${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Mukwiye-Sez/Lab6-Assignment'
            }
        }

        stage('Build Docker Image') {
            steps {
                container('docker') {
                    sh """
                      docker version
                      docker build -t ${DOCKER_IMAGE} .
                    """
                }
            }
        }

        stage('Test') {
            steps {
                container('docker') {
                    sh """
                      docker run --rm ${DOCKER_IMAGE} pytest -q
                    """
                }
            }
        }

        stage('Static Analysis') {
            steps {
                container('docker') {
                    sh """
                      docker run --rm ${DOCKER_IMAGE} flake8 app.py
                    """
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                container('docker') {
                    withCredentials([usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_PASSWORD'
                    )]) {
                        sh '''
                          echo "$DOCKERHUB_PASSWORD" | docker login -u "$DOCKERHUB_USERNAME" --password-stdin
                        '''
                    }
                }
            }
        }

        stage('Push Image') {
            steps {
                container('docker') {
                    sh """
                      docker push ${DOCKER_IMAGE}
                    """
                }
            }
        }
    }
}
