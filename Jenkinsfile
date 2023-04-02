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
        sh 'cd ./tests && xvfb-run -an 90 -s "-screen 0 1280x1024x24" python3 -m unittest Tests_*.py -v'
      }
    }

  }
}