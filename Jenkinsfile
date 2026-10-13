pipeline {
    agent any

    options {
        timeout(time: 15, unit: 'MINUTES')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare .env') {
            steps {
                // .env is git-ignored, so the pipeline builds it from the template.
                // Throwaway credentials for a short-lived test stack.
                sh 'cp .env.example .env'
            }
        }

        stage('Validate Compose file') {
            steps {
                sh 'docker compose config -q'
            }
        }

        stage('Build and start') {
            steps {
                sh 'docker compose up -d --build'
            }
        }

        stage('Health check') {
            steps {
                // Runs the request inside the app container, so it works even when
                // Jenkins itself runs in a container and cannot reach the host's localhost.
                sh '''
                    for i in $(seq 1 30); do
                        if docker compose exec -T flask-app python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"; then
                            echo "App is healthy"
                            exit 0
                        fi
                        echo "Waiting for app... ($i/30)"
                        sleep 5
                    done
                    echo "App did not become healthy in time"
                    exit 1
                '''
            }
        }

        stage('Home page check') {
            steps {
                // Fails on HTTP 500, so it covers app + database + template.
                sh '''docker compose exec -T flask-app python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')"'''
            }
        }
    }

    post {
        failure {
            sh 'docker compose logs'
        }
        always {
            sh 'docker compose down -v'
        }
    }
}
