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
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    pytest samplemod/tests --maxfail=1 --disable-warnings -q --junitxml=results.xml
                '''
            }
            post {
                always {
                    junit 'results.xml'
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
