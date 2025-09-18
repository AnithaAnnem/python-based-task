pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        SONARQUBE_ENV = 'sonar-server' // Jenkins SonarQube server config
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
                    pytest samplemod/tests --maxfail=1 --disable-warnings -q --cov=samplemod --cov-report=xml
                '''
            }
            post {
                always {
                    junit 'samplemod/tests/test-results.xml'
                    echo "JUnit results published"
                }
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

        stage('SonarQube Analysis') {
            steps {
                echo "Running SonarQube code quality analysis..."
                withSonarQubeEnv("${SONARQUBE_ENV}") {
                    script {
                        def scannerHome = tool 'SonarQube_Scanner'
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                              -Dsonar.projectKey=python-sample \
                              -Dsonar.sources=. \
                              -Dsonar.python.version=3 \
                              -Dsonar.python.coverage.reportPaths=coverage.xml
                        """
                    }
                }
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
