pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/AnithaAnnem/python-based-task.git', branch: 'main'
            }
        }

        stage('Setup Python') {
            steps {
                echo "Setting up Python virtual environment"
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
                echo "Running unit tests"
                sh '''
                    . $VENV_DIR/bin/activate
                    pytest samplemod/tests --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Code Quality Checks') {
            steps {
                echo "Running flake8"
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
            echo "Pipeline finished"
        }
        failure {
            echo 'Build failed!'
        }
    }
}
