pipeline {
    agent {
        node {
            label 'dockerEC2'
        }
    }

  options {
    timeout(time: 1, unit: 'HOURS')   // timeout on whole pipeline job
  }
  environment {
    APP_NAME="bts-reference"
    DOCKER_REPO="287482246495.dkr.ecr.us-west-2.amazonaws.com"
  }

  stages {
    stage('Checkout') {
      steps {
      checkout([$class: 'GitSCM', branches: [[name: '*/main']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'app-cirium-ticketsdatasynthesis-jenkins', url: 'https://github.com/LexisNexis-RBA/dsg-cirium-ticketsdatasynthesis-bts-reference.git']]])
      }     
    }    

    stage('Build') {
      steps {
        sh '''
          echo " building bts-reference"
          docker build -t $APP_NAME . -f ./Dockerfile 
#        docker build -t ${DOCKER_REPO}/$APP_NAME:latest . -f ./Dockerfile
          echon "build complete"
        '''
      }
    }

//    stage ('Trivy Scan') {
//      steps { 
//        sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v ${WORKSPACE}/trivy-reports:/output -e TRIVY_NEW_JSON_SCHEMA=true aquasec/trivy image --format json --timeout 15m0s --exit-code 0 --no-progress ${DOCKER_REPO}/${APP_NAME} | tee trivy.out'
//        recordIssues enabledForFailure: true, aggregatingResults: true
////        recordIssues enabledForFailure: true, aggregatingResults: true, tool: trivy(pattern: "trivy.out")
//      } 
//    }

//    stage('Publish') {
//      steps {
//        sh 'aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin ${DOCKER_REPO}'
//        sh 'docker push ${DOCKER_REPO}/${APP_NAME}:latest'
//      }
//    }
  }
  post {
    // Cleanup the workspace
    always {
      cleanWs()
    }
  }
}
