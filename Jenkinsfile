pipeline {
agent any

stages {

    stage('Clonar codigo') {
        steps {
            echo 'Repositorio clonado correctamente'
        }
    }

    stage('Construir Docker') {
        steps {
            bat 'docker compose build'
        }
    }

    stage('Levantar Contenedores') {
        steps {
            bat 'docker compose up -d'
        }
    }

    stage('Verificar Contenedores') {
        steps {
            bat 'docker ps'
        }
    }
}

post {
    success {
        echo 'Pipeline ejecutado correctamente'
    }

    failure {
        echo 'La ejecucion fallo'
    }
}

}
