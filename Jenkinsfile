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
                // EC2에 저장된 .env 파일을 workspace로 복사
                sh 'cp /home/ubuntu/Fhir-Style-Builder/.env $WORKSPACE/.env'
            }
        }
        stage('Deploy') {
            steps {
                // 기존 컨테이너 내리고 재빌드 후 실행
                sh 'docker-compose down'
                sh 'docker-compos\e up -d --build'
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
