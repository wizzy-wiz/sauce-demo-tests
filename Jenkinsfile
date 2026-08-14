// Jenkins declarative pipeline for this test suite.
// Note: this repo is hosted on GitHub, so this file won't run automatically here —
// it's included to demonstrate Jenkins pipeline authoring. To run it for real,
// point a Jenkins job (Pipeline > Pipeline script from SCM) at this repository.

pipeline {
    agent any

    options {
        timestamps()
    }

    stages {
        stage('Set up environment') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Run tests') {
            steps {
                sh './venv/bin/pytest --html=report.html --self-contained-html'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
        }
        failure {
            echo 'Test suite failed — see report.html for details.'
        }
    }
}
