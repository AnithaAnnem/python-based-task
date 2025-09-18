pipeline {
    agent any

    parameters {
        string(name: 'GIT_URL', defaultValue: 'https://github.com/AnithaAnnem/python-based-task.git', description: 'Git repository URL')
        string(name: 'BRANCH', defaultValue: 'main', description: 'Branch to build')
    }

    environment {
        VENV_DIR = 'venv'
        SONARQUBE_ENV = 'sonar-server1' 
    }

    stages {

        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Checkout') {
            steps {
                git branch: "${params.BRANCH}", url: "${params.GIT_URL}"
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -r samplemod/requirements.txt
                pip install pytest pytest-cov pip-audit flake8
                deactivate
                '''
            }
        }

        stage('Bug Analysis with SonarQube') {
            steps {
                withSonarQubeEnv("${SONARQUBE_ENV}") {
                    sh '''
                    . ${VENV_DIR}/bin/activate
                    sonar-scanner \
                        -Dsonar.projectKey=python-sample \
                        -Dsonar.sources=samplemod \
                        -Dsonar.host.url=${SONAR_HOST_URL} \
                        -Dsonar.login=${SONAR_AUTH_TOKEN}
                    deactivate
                    '''
                }
            }
        }

        stage('Static Code Analysis') {
            steps {
                sh '''
                . ${VENV_DIR}/bin/activate
                flake8 samplemod
                deactivate
                '''
            }
        }

        stage('Credential Scanning with Gitleaks') {
            steps {
                sh 'gitleaks detect --source . --report-path gitleaks-report.json'
            }
        }

        stage('Dependency Scanning') {
            steps {
                sh '''
                . ${VENV_DIR}/bin/activate
                pip-audit
                deactivate
                '''
            }
        }

        stage('Run Unit Tests with Coverage') {
            steps {
                sh '''
                . ${VENV_DIR}/bin/activate
                pytest --cov=samplemod tests/
                deactivate
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up virtual environment'
            sh 'rm -rf ${VENV_DIR}'
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Build failed!'
        }
    }
}
