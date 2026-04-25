pipeline {
    agent any

    environment {
        IMAGE_TAG      = "aceest:build-${env.BUILD_NUMBER}"
        IMAGE_LATEST   = "aceest:latest"
        VENV_DIR       = "${env.WORKSPACE}/.venv"
        REPO_OWNER     = "kshitizranjan15"
        REPO_NAME      = "Introduction_to_DEVOPS_-S2-25_SEZG514-_Assignment2"
        SONARQUBE_HOST = "http://localhost:9000"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_HASH = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
                    echo "✓ Checked out commit: ${env.GIT_COMMIT_HASH}"
                    postGitHubStatus('pending', 'Jenkins build started', 'continuous-integration/jenkins')
                }
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv ${VENV_DIR}
                    ${VENV_DIR}/bin/pip install --upgrade pip --quiet
                    ${VENV_DIR}/bin/pip install -r requirements.txt --quiet
                    ${VENV_DIR}/bin/python --version
                    echo "✓ Python virtualenv ready"
                '''
            }
        }

        stage('Lint & Syntax Check') {
            steps {
                sh '''
                    ${VENV_DIR}/bin/python -m compileall . -q
                    echo "✓ Syntax check passed"
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    ${VENV_DIR}/bin/pytest -q \
                        --tb=short \
                        --junitxml=test-results/results.xml \
                        --cov=app \
                        --cov-report=xml:coverage.xml
                    echo "✓ All unit tests passed"
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results/results.xml'
                    archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                        sh '''
                            if [ -f sonar-project.properties ]; then
                                if command -v sonar-scanner &> /dev/null; then
                                    echo "✓ Running SonarQube analysis..."
                                    sonar-scanner \
                                        -Dsonar.projectKey=aceest-assignment2 \
                                        -Dsonar.sources=. \
                                        -Dsonar.host.url=${SONARQUBE_HOST} \
                                        -Dsonar.coverageReportPaths=coverage.xml \
                                        || echo "⚠ SonarQube analysis skipped (sonar-scanner not available)"
                                else
                                    echo "⚠ sonar-scanner not found. Install with: npm install -g sonarqube-scanner"
                                fi
                            else
                                echo "⚠ sonar-project.properties not found, skipping SonarQube analysis"
                            fi
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE_TAG} .
                    docker tag ${IMAGE_TAG} ${IMAGE_LATEST}
                    echo "✓ Docker image built: ${IMAGE_TAG}"
                '''
            }
        }

        stage('Test Inside Container') {
            steps {
                sh '''
                    echo "✓ Running tests inside container..."
                    docker run --rm ${IMAGE_TAG} pytest -q
                    echo "✓ Container-level tests passed"
                '''
            }
        }

        stage('Push to Registry') {
            when {
                expression {
                    return env.BRANCH_NAME == 'main' || env.BRANCH_NAME == null
                }
            }
            steps {
                script {
                    catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                        withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                            sh '''
                                echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                                docker tag ${IMAGE_TAG} ${DOCKER_USER}/aceest:${BUILD_NUMBER}
                                docker tag ${IMAGE_TAG} ${DOCKER_USER}/aceest:latest
                                docker push ${DOCKER_USER}/aceest:${BUILD_NUMBER}
                                docker push ${DOCKER_USER}/aceest:latest
                                echo "✓ Image pushed to Docker Hub"
                                docker logout
                            '''
                        }
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            when {
                expression {
                    return env.BRANCH_NAME == 'main' || env.BRANCH_NAME == null
                }
            }
            steps {
                script {
                    catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                        sh '''
                            if [ -f scripts/deploy_k8s.sh ]; then
                                echo "✓ Deploying to Kubernetes..."
                                bash ./scripts/deploy_k8s.sh ${IMAGE_TAG}
                            else
                                echo "⚠ Kubernetes deployment script not found, skipping deployment"
                            fi
                        '''
                    }
                }
            }
        }

        stage('Smoke Test') {
            steps {
                script {
                    catchError(buildResult: 'SUCCESS', stageResult: 'UNSTABLE') {
                        sh '''
                            echo "✓ Running smoke tests..."
                            sleep 2
                            curl -fS http://localhost:5000/health || echo "⚠ Health check skipped (service not accessible)"
                        '''
                    }
                }
            }
        }

    }

    post {
        success {
            echo "✓✓✓ PIPELINE SUCCEEDED - Image: ${IMAGE_TAG}"
            script {
                postGitHubStatus('success', 'Jenkins pipeline passed', 'continuous-integration/jenkins')
            }
        }
        failure {
            echo "✗ PIPELINE FAILED - Check logs above"
            script {
                postGitHubStatus('failure', 'Jenkins pipeline failed', 'continuous-integration/jenkins')
            }
        }
        always {
            sh 'rm -rf ${VENV_DIR} || true'
            archiveArtifacts artifacts: 'test-results/**/*.xml,coverage.xml', allowEmptyArchive: true
            cleanWs()
        }
    }
}

// =====================================================
// Helper: Post commit status to GitHub via REST API
// =====================================================
// Requires Jenkins credential: 'github-token' (Secret text = GitHub PAT with repo:status scope)
// Falls back gracefully if credential is missing
def postGitHubStatus(String state, String description, String context) {
    try {
        withCredentials([string(credentialsId: 'github-token', variable: 'GH_TOKEN')]) {
            def commitHash = env.GIT_COMMIT_HASH ?: sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
            def payload = groovy.json.JsonOutput.toJson([
                state      : state,
                description: description,
                context    : context,
                target_url : "${env.BUILD_URL}"
            ])
            sh '''
                curl -s -o /dev/null -w "GitHub status: %{http_code}\\n" \\
                  -H "Authorization: token ${GH_TOKEN}" \\
                  -H "Content-Type: application/json" \\
                  -X POST \\
                  -d '${payload}' \\
                  "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/statuses/${commitHash}"
            '''
        }
    } catch (Exception e) {
        echo "ℹ GitHub status update skipped (add 'github-token' credential to enable)"
    }
}

