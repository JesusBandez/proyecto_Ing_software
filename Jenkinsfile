pipeline {
  agent any
  stages {
    stage('Requirements') {
      steps {
        sh ' pip install -r requirements.txt'
      }
    }

    stage('Tests') {
      steps {
        sh 'cd ./tests && python3 -m unittest Tests_*.py -v'
      }
    }

  }
}