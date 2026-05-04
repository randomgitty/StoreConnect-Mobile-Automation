pipeline {
    agent any
    
    environment {
        PYTHON_ENV = 'my_env'
        ALLURE_RESULTS = 'allure-results'
        APK_URL = 'https://a3.files.diawi.com/app-file/BuJRXBtidTLhCT5bULK1.apk'
        APK_PATH = 'resources/app/app-release.apk'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Checking out code from GitHub...'
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo '🐍 Setting up Python virtual environment...'
                bat '''
                    python -m venv %PYTHON_ENV%
                    call %PYTHON_ENV%\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Download APK') {
            steps {
                echo '📱 Downloading APK from Diawi...'
                bat '''
                    echo Downloading APK from hosted URL...
                    echo URL: %APK_URL%
                    
                    mkdir resources\\app
                    
                    curl -L -o %APK_PATH% "%APK_URL%"
                    
                    if exist "%APK_PATH%" (
                        echo APK downloaded successfully!
                        dir %APK_PATH%
                    ) else (
                        echo APK download failed - file not found!
                        exit /b 1
                    )
                '''
            }
        }
        
        stage('Run Product Facing Test') {
            steps {
                echo '🧪 Running Product Facing automation test...'
                bat '''
                    call %PYTHON_ENV%\\Scripts\\activate.bat
                    mkdir reports logs
                    pytest test_cases/tc_ProductFacingFlow.py::test_product_facing_flow ^
                        --alluredir=%ALLURE_RESULTS% ^
                        --html=reports/pytest-report.html ^
                        --self-contained-html ^
                        -v ^
                        -s ^
                        --log-cli-level=INFO
                '''
            }
            post {
                always {
                    echo 'Archiving test artifacts...'
                    archiveArtifacts artifacts: 'reports/*.html, logs/*.log', allowEmptyArchive: true
                }
                success {
                    echo '🎉 Product Facing test passed!'
                }
                failure {
                    echo '❌ Product Facing test failed - check console output'
                }
            }
        }
        
        stage('Generate Allure Report') {
            steps {
                echo '📊 Generating Allure report...'
                script {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: "${ALLURE_RESULTS}"]]
                    ])
                }
            }
        }
    }
    
    post {
        always {
            echo '✅ Pipeline execution completed!'
            cleanWs()
        }
        success {
            echo '🏆 BUILD SUCCESSFUL!'
        }
        failure {
            echo '💥 BUILD FAILED!'
        }
    }
}