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
