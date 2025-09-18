pipeline {
    agent any

    parameters {
        string(name: 'GIT_URL', defaultValue: 'https://github.com/AnithaAnnem/python-based-task.git', description: 'Git repository URL')
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch to build')
    }

    environment {
        VENV_DIR = 'venv'
    }

    stages {

        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Checkout') {
            steps {
                git branch: "${params.BRANCH}",
                    url: "${params.GIT_URL}"
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv $VENV_DIR
                . $VENV_DIR/bin/activate
                pip install --upgrade pip
                pip install pytest pytest-cov pip-audit flake8
                '''
            }
        }

        stage('Bug Analysis with SonarQube') {
            steps {
                withSonarQubeEnv('sonar-server') {
                    sh '''
                    . $VENV_DIR/bin/activate
                    sonar-scanner \
                        -Dsonar.projectKey=python-sample \
                        -Dsonar.sources=samplemod \
                        -Dsonar.host.url=$SONAR_HOST_URL \
                        -Dsonar.login=$SONAR_AUTH_TOKEN
                    '''
                }
            }
        }

        stage('Static Code Analysis') {
            steps {
                sh '''
                . $VENV_DIR/bin/activate
                flake8 samplemod --statistics
                '''
            }
        }

        stage('Credential Scanning with Gitleaks') {
            steps {
                sh '''
                gitleaks detect --source . --report-path gitleaks-report.json
                '''
            }
        }

        stage('Dependency Scanning') {
            steps {
                sh '''
                . $VENV_DIR/bin/activate
                pip-audit --output audit-report.json
                '''
            }
        }

        stage('Run Unit Tests with Coverage') {
            steps {
                sh '''
                . $VENV_DIR/bin/activate
                pytest --cov=samplemod tests/
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up virtual environment'
            sh 'rm -rf $VENV_DIR'
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
