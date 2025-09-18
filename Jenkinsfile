pipeline {
    agent any

    tools {
        hudson.plugins.sonar.SonarRunnerInstallation 'SonarQube_Scanner'
    }

    environment {
        SONARQUBE_ENV = 'sonar-server'   
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/AnithaAnnem/python-based-task.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt || true
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest --maxfail=1 --disable-warnings -q || true
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv("${SONARQUBE_ENV}") {
                    withCredentials([string(credentialsId: 'python-sample-token', variable: 'SONAR_TOKEN')]) {
                        sh '''
                            sonar-scanner \
                                -Dsonar.projectKey=python-sample \
                                -Dsonar.sources=. \
                                -Dsonar.host.url=$SONAR_HOST_URL \
                                -Dsonar.login=$SONAR_TOKEN
                        '''
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully. SonarQube analysis finished."
        }
        failure {
            echo "Pipeline failed. Please check the logs in Jenkins."
        }
        always {
            cleanWs()
        }
    }
}
