pipeline {
    agent any

    parameters {
        string(name: 'GIT_URL', defaultValue: 'https://github.com/AnithaAnnem/python-based-task.git', description: 'Git repository URL')
        string(name: 'BRANCH', defaultValue: 'main', description: 'Branch to build')
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
                git url: "${params.GIT_URL}", branch: "${params.BRANCH}"
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -r samplemod/requirements.txt
                    pip install pytest pytest-cov pip-audit gitleaks flake8
                '''
            }
        }

        stage('Credential Scanning with Gitleaks') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    gitleaks detect --source=. --no-git --report-format sarif --report-path gitleaks-report.sarif || true
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'gitleaks-report.sarif', allowEmptyArchive: true
                }
            }
        }

        stage('Dependency Scanning') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    pip-audit -r samplemod/requirements.txt || true
                '''
            }
        }

        stage('Run Unit Tests with Coverage') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    pytest samplemod/tests --cov=samplemod/sample --cov-report=xml --cov-report=term --junitxml=results.xml
                '''
            }
            post {
                always {
                    junit 'results.xml'
                    // Use publishCoverage instead of cobertura
                    publishCoverage adapters: [coberturaAdapter('coverage.xml')], sourceFileResolver: sourceFiles('**/*.py')
                }
            }
        }

        stage('Code Quality Checks') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    flake8 samplemod/sample
                '''
            }
        }

    }

    post {
        always {
            echo "Cleaning up virtual environment"
            sh 'rm -rf $VENV_DIR'
            cleanWs()
            echo "Pipeline finished"
        }
        failure {
            echo 'Build failed!'
        }
    }
}
