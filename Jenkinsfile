pipeline {
    agent any
    
    environment {
        PYTHON_ENV = 'my_env'
        ALLURE_RESULTS = 'allure-results'
        APK_URL = 'https://a3.files.diawi.com/app-file/BuJRXBtidTLhCT5bULK1.apk'
        APK_PATH = 'resources/app/app-release.apk'
        PYTHONIOENCODING = 'utf-8'
        PYTHONUTF8 = '1'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from GitHub...'
                checkout scm
            }
        }
        
        stage('Setup Python') {
            steps {
                echo 'Setting up Python environment...'
                bat '''
                    @echo off
                    chcp 65001 > nul
                    python -m venv %PYTHON_ENV%
                    call %PYTHON_ENV%\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Download APK') {
            steps {
                echo 'Downloading APK from Diawi...'
                bat '''
                    @echo off
                    chcp 65001 > nul
                    if not exist resources\\app mkdir resources\\app
                    curl -L -o %APK_PATH% "%APK_URL%"
                    if exist "%APK_PATH%" (
                        echo APK downloaded successfully
                        for %%A in (%APK_PATH%) do echo File size: %%~zA bytes
                    ) else (
                        echo APK download failed
                        exit /b 1
                    )
                '''
            }
        }
        
        stage('Start Appium') {
            steps {
                echo 'Starting Appium server...'
                bat '''
                    @echo off
                    chcp 65001 > nul
                    start /b appium --address 127.0.0.1 --port 4723 > appium.log 2>&1
                    timeout /t 10 /nobreak > nul
                    echo Appium server started on port 4723
                '''
            }
        }
        
        stage('Run Product Facing Test') {
            steps {
                echo 'Running Product Facing automation test...'
                bat '''
                    @echo off
                    chcp 65001 > nul
                    set PYTHONIOENCODING=utf-8
                    set PYTHONUTF8=1
                    
                    call %PYTHON_ENV%\\Scripts\\activate.bat
                    mkdir reports logs
                    
                    pytest test_cases/tc_ProductFacingFlow.py::test_product_facing_flow ^
                        --alluredir=%ALLURE_RESULTS% ^
                        --html=reports/pytest-report.html ^
                        --self-contained-html ^
                        -v ^
                        -s ^
                        --log-cli-level=INFO ^
                        --tb=short
                '''
            }
            post {
                always {
                    echo 'Archiving test artifacts...'
                    archiveArtifacts artifacts: 'reports/*.html,logs/*.log,appium.log', allowEmptyArchive: true
                }
                success {
                    echo 'Product Facing test PASSED!'
                }
                failure {
                    echo 'Product Facing test FAILED - check console output'
                }
            }
        }
        
        stage('Generate Allure Report') {
            steps {
                echo 'Generating Allure report...'
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
            echo 'Pipeline execution completed!'
            bat '''
                @echo off
                taskkill /F /IM node.exe 2>nul || echo Appium process closed
            '''
            cleanWs()
        }
        success {
            echo 'BUILD SUCCESSFUL!'
        }
        failure {
            echo 'BUILD FAILED!'
        }
    }
}