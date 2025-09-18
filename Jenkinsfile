pipeline {
    agent any

    parameters {
        string(name: 'GIT_URL', defaultValue: 'https://github.com/AnithaAnnem/python-based-task.git', description: 'Git repository URL')
        string(name: 'BRANCH', defaultValue: 'main', description: 'Branch to build')
        string(name: 'SONAR_HOST_URL', defaultValue: 'http://54.173.57.76:9000', description: 'SonarQube server URL')
    }

    environment {
        VENV_DIR = 'venv'
        SONARQUBE_ENV = 'sonar-server1'  
        SONAR_SCANNER_TOOL = 'SonarQube_Scanner' 
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
                                -Dsonar.login=${SONAR_AUTH_TOKEN}
                            deactivate
                        """
                    }
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

        stage('Credential Scanning') {
            steps {
                sh 'gitleaks detect --source . --report-path gitleaks-report.json || true'
            }
        }

        stage('Dependency Scanning') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate

                    # Run pip-audit and generate HTML report
                    pip-audit --output-format html --output-file pip-audit-report.html || true

                    deactivate
                '''

                // Archive the report in Jenkins so you can view it
                archiveArtifacts artifacts: 'pip-audit-report.html', allowEmptyArchive: true
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
            echo 'Pipeline finished successfully!'
        }
        failure {
            echo 'Build failed!'
        }
    }
}
