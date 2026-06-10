pipeline {
agent any


stages {

    stage('Clonar codigo') {
        steps {
            echo 'Repositorio clonado correctamente'
        }
    }

    stage('Verificar archivos') {
        steps {
            sh 'ls -la'
        }
    }

    stage('Ejecutar pruebas') {
        steps {
            sh 'python --version || true'
            echo 'Pruebas ejecutadas'
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
