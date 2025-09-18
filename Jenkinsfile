pipeline {
    agent any

    parameters {
        string(name: 'GIT_URL', defaultValue: 'https://github.com/AnithaAnnem/python-based-task.git', description: 'Git repository URL')
        string(name: 'BRANCH', defaultValue: 'main', description: 'Branch to build')
        string(name: 'SONAR_HOST_URL', defaultValue: 'http://54.197.45.84:9000', description: 'SonarQube server URL')
    }

    environment {
        VENV_DIR = 'venv'
        SONARQUBE_ENV = 'sonar-server1'      // Jenkins SonarQube server config
        SONAR_SCANNER_TOOL = 'SonarQube_Scanner' // Jenkins tool name
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
                    pip install -r requirements.txt
                    pip install pytest pytest-cov pip-audit flake8 bandit
                '''
            }
        }

        stage('Credential Scanning') {
            steps {
                sh 'gitleaks detect --source . --report-path gitleaks-report.json || true'
            }
        }

        stage('Static Code Analysis (flake8)') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    flake8 samplemod
                '''
            }
        }

        stage('Security Scan (bandit)') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    bandit -r samplemod -f json -o bandit-report.json
                '''
            }
        }

        stage('Dependency Scanning') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pip-audit -r requirements.txt -f json > dependency-report.json || true
                '''
            }
        }

        stage('Run Unit Tests with Coverage') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pytest --cov=samplemod --cov-report=xml --cov-report=term
                '''
            }
        }

        stage('Bug Analysis with SonarQube') {
            steps {
                withSonarQubeEnv("${SONARQUBE_ENV}") {
                    script {
                        def scannerHome = tool "${SONAR_SCANNER_TOOL}"
                        sh """
                            . ${VENV_DIR}/bin/activate
                            ${scannerHome}/bin/sonar-scanner \
                              -Dsonar.projectKey=python-sample \
                              -Dsonar.sources=samplemod \
                              -Dsonar.host.url=${params.SONAR_HOST_URL} \
                              -Dsonar.python.coverage.reportPaths=coverage.xml
                        """
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
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
            echo 'Pipeline finished successfully!'
        }
        failure {
            echo 'Build failed!'
        }
    }
}
