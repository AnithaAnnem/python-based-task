pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        PATH = "${env.WORKSPACE}/${env.VENV_DIR}/bin:${env.PATH}"
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
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo "Running Unit Tests with pytest"
                sh '''
                    . $VENV_DIR/bin/activate
                    pytest tests --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Code Quality Checks') {
            steps {
                echo "Running flake8 for code quality"
                sh '''
                    . $VENV_DIR/bin/activate
                    pip install flake8
                    flake8 sample tests
                '''
            }
        }
    }

    post {
        always {
            echo "Cleaning up virtual environment"
            sh "rm -rf $VENV_DIR"
            echo "Pipeline finished"
        }
        success {
            echo "Build succeeded!"
        }
        failure {
            echo "Build failed!"
        }
    }
}
