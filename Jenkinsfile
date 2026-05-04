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
                    mkdir resources\\app
                    curl -L -o %APK_PATH% "%APK_URL%"
                    if exist "%APK_PATH%" (
                        echo APK downloaded successfully!
                        for %%A in (%APK_PATH%) do echo File size: %%~zA bytes
                    ) else (
                        echo APK download failed!
                        exit /b 1
                    )
                '''
            }
        }
        stage('Start Appium') {
            steps {
                echo '🚀 Starting Appium server...'
                // Start Appium in background, redirect output to log file
                bat 'cmd /c "start /b appium --address 127.0.0.1 --port 4723 > appium.log 2>&1"'
                // Use ping as a reliable sleep command on Windows (avoids timeout redirection issues)
                bat 'ping 127.0.0.1 -n 11 > nul'
                echo '✅ Appium server started and ready'
            }
        }
        
        
        stage('Run Product Facing Test') {
            steps {
                echo '🧪 Running Product Facing automation test...'
                bat '''
                    call %PYTHON_ENV%\\Scripts\\activate.bat
                    mkdir reports logs
                    pytest test_cases/tc_ProductFacingFlow.py::test_product_facing_flow --alluredir=%ALLURE_RESULTS% --html=reports/pytest-report.html --self-contained-html -v -s --log-cli-level=INFO
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'reports/*.html, logs/*.log, appium.log', allowEmptyArchive: true
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
            echo '✅ Pipeline completed!'
            bat 'taskkill /F /IM node.exe || echo Done'
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