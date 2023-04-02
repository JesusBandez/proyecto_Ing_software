pipeline {
  agent any
  stages {
    stage('Requirements') {
      parallel {
        stage('Requirements') {
          steps {
            sh ' pip install -r requirements.txt'
          }
        }

        stage('git checkout') {
          steps {
            git(url: 'https://github.com/JesusBandez/proyecto_Ing_software', branch: 'produccion')
          }
        }

      }
    }

    stage('Tests') {
      steps {
        sh 'cd ./tests && xvfb-run python3 -m unittest Tests_*.py -v -k  Departments'
      }
    }

  }
}