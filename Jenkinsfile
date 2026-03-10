pipeline {
    agent any

    stages {
        stage('Clone') {
            steps {
                // GitHub에서 최신 코드 가져오기
                git branch: 'main',
                    url: 'git@github.com:cwd3469/Fhir-Style-Builder.git'
            }
        }
        stage('Prepare') {
            steps {
                // Jenkins Credentials에서 .env 파일 주입
                withCredentials([file(credentialsId: 'fhir-env-file-back-product', variable: 'ENV_FILE')]) {
                    sh 'cp $ENV_FILE $WORKSPACE/.env'
                }
            }
        }
        stage('Deploy') {
            steps {
                // 기존 컨테이너 내리고 재빌드 후 실행
                sh 'docker-compose down'
                sh 'docker-compose up -d --build'
            }
        }
    }

    post {
        success {
            echo '배포 성공'
        }
        failure {
            echo '배포 실패'
        }
    }
}
