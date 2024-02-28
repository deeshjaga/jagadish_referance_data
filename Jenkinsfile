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
    APP_NAME="estimates-data-synthesis-dev"
    DOCKER_REPO="287482246495.dkr.ecr.us-west-2.amazonaws.com"
  }

  stages {
    stage('Checkout') {
      steps {
      checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'app-cirium-ticketsdatasynthesis-jenkins', url: 'https://github.com/LexisNexis-RBA/dsg-cirium-ticketsdatasynthesis-estimate.git']]])
      }     
    }    

    stage('Build') {
      steps {
        sh '''
        mkdir -p ssh
        echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDEe5sxfn5c9TwPaccvNgeoylM4D0Kkq0P8i5q1DXHmzfcnbcvmMGOt+iiK8EMfvsLJ3GrdfGR2zoRFdxmsZuog40Wug/QsXxgTJo5q8JgAo4bunrxLu3MwybbLjhfqu9v8qrDOuZOw7LDBVANL2gIx6iszR0w+8Q1qNaY7CIvGhINSaUXteAxMMJ+LdEbE90OWsTjGY547oRBVf8nabeIDbG8PS8Pm3AYxC/gpmTbkicohc+r9JFjrSyG07Tb8SPb9A2p5w/x6IefhhGphakPFtuEBHxl1zgSUtmIpvNb3QKI6NKDm1Hy069+AfVRNWba8pLW0pUqzdJh1pjKVeEChdOnUwJatzNSd9vd9qMo/aTT+U5jHA/nJNdYAPUPDN7aGpn79BfH8LE2vdOVqP3wBFJ1srkGsXjZ9UZi+PPjgQeiXDvG8jXYEyXwV7+ugkff02yZWzpk3+thaKX4pCs64kmLFekMWCbF2J6i23J9lo82pi+LA+Cjm0+uvU5NE9HU= walkera7@porm201066" > ./authorized_keys
        echo "ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAQEAil9Get4OoG8ckNI5zvrv2KWM8i+0Y3U5zgSO+XfRCB5WMP4T4wuKufna5BfshG+C2xThj3U3f8pbOrxH88aqHo2TqLhbqlZdljTpt71Mpuex8AaJqlo17JZL2PmLPWTHPclGxNqu11LEjuVETaIe/MdYmfdDV5Sgz0kCijrb37RlLjd3rzc83IyVzqzNeFFh+mG+xZu3sdPAWv8kJst6kBEs9cfnNZm3fZyR0aSew3FyhO/PP9FEyFDqxyG2geYJ5UW8CW1izmSJ6kRc795/OSyT6W9YKtVQDCzPl4Lur6NLnkwRNjSzJNF5XEjdxmU8dhkDvjSHYosYu9QfzLUMFw== devudigaria" >> ./authorized_keys
        echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDA9gmrdsdyCXCFPFmtEBLbXjEZ7mpdoH68ueI3ZPQiiT0z7Gt6OCaXmDOgJ8x3/y878+wMw99MjLdgz2d4XXzrz/rZhVrIvUQ4cliiRo2xzP4PpLaPC/7SOgdNaWE5HrMvl1uUG3ZNcJcbnmnwaAUqksyGslPE2l0POHlZ3iStqZ8fBfmi9fXqgjReTW52FJPDGgyuDXMz7v1WnjMtaRfWCzmauE+xNxoAxyun7Kjz+mPFd08GeEdJ71OBC1afKEbiD5dTVVw59PIcsVozQ+w3sTNjdHcuNhsaKlmhQpTiXwnQybrlKxuccj6iZS9HriNUVLv2+joTefoaDrigEeeIIFCnQWzM/Z7Dh1JudYV+SiYSVNMRwN5s0GiVuO0f1iAPYYZV8T+JiBUsTqPZjCVj+5dQEqL/mXiOUA9Nkjsy8lwDbJmyIyDWg3eiou4fp4mw0EoKI2ccwp6hDni/ndM+akNzg6yc40z+IPRp6dQ15r05Z7shaOpUuHjXB2hbRBE= jyothi.nekkalapudi@cirium.com" >> ./authorized_keys
        echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDvoI6Qm96y0YPRFxOaIll10RsSVVAkdbFbUAr/mUKNxVmIKj+HvwVY4Iav1J6g9tYQqSgExgRfpYQ4hrdfDqzUwAVFzPW6XnvGMbjHq60D5undYP3M+Wkp2FuQo/JnYD1/CbHgrg9AbRti0Wh1c3/GrQIPVS/6YOTjk8l8rfAyF309hdAwx3nkvCHi7zQR65B/DtFh/f7KtYX8C2qMoGi2tWpb08vmiJVx2EwrrDXTyswujfMbbFn3cVjqnGJ+/neCP5yMiv8S8fiucM1HEI6p+5rUYe9fF881E/Fn64oca2C2mxJ8v5u1tpi4vgTdeIExn5UWYwHHZ8WIJRk5aRCd08PXtZoKN1ZVEMlC2zKb+bJpihlWvtG54FKR9hj/uK3EMRqG19UDxkeaGnhRjU0H1jivLm9WeTnEoph0vcsoQYA3xy6iezHJdw5nETYqi7ASHFUyTXHjx7NYnnCtkB7gsmbBnmN7oZfQIwcMSqxWso/dVhsDSk+/fBVeKOe6K3xIjUbfk51OVDKw5ay2S0UZQt0g1Ed1smul5tW5E/YyKylb1HNv4kWErcBoX+8sGmrpbI5SjpvWhD4VHHEkxyK/3W9DYTBe+aLXMX60tOX5qd9mdSHqmNSHoEkrDLsDX8xH6z71De32IgpHQs3os/Y9f4OHlclv3z3Xwof+wg2iIw== dave.cruts@flightglobal.com" >> ./authorized_keys
        echo "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAgEAvc1WJTTVOsJggDpn+S8/O93nwBWGjnyfHa7pHdz55EHgf26l13TchGL827a0qR6xmtBGvmKWsHt4ka7Hks3BMSnM2a2oGfGqFRnEXQ3zPYQj2jp4gjIZAa82GpPtYvg0q5HVegchoWUOaMCzl9M9dldAIAUxXg/x2AokJLW2TyjvJqV53u5ypwzLoZOlWxseofQAYce/DMSOFJLek0yKM+ZQZBztW6+KfQ8dSzOV0ebiiuAQYfYGr8BUOOQKUta37TMdMQ2E/CgqffX4iBNGgAaHpyTj54/TVpnHI1bekyuAEVGLAnEPvckgnvkag0GK1rcFiVDiqYulD1mC7QWj+OXbBmqbVnqGA03SYABr5BqSQsvytuRovC0qmyIAmJX3XOe2gtnEy9K2a7rjJTk+uvfw+nVe4nicPCJy5/Bc0pQ6YUo24lqaMGQ6b5j/8NOQhKGRdtzUBoLK8qRV0ovtIFV314d7rtaqv01vtmpphIVIcIKDpfxNFogtZHcka3Y5FYBShBAI1i3V5FbHhp0dtDCSIq5QGGedC+Tw8FRWvXeKGTf3ZpW9ku+3XP3M0YKzLrYb5bTl+LMBIZJS1Wq2VnMbJzqmaldxIc35YSZ/cC/DWPyRjtcvgAZkxK8LVGQItchsxO+6zISmf3TRB0H9tEFMset/82x7WpOfIK7DTwc= crozierm@dentaku" >> ./authorized_keys
        echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDOql+ZPi+cZWnwf5Ug2wq0oA3Hn49GE9g74VCE1EW4kemMRdYEvT+CU44esXBRkfzkgKPahz50LOF6BP/yo7ah8HoRkACE14YNomZJ8VMB4xzonvb8Hf7U6bxKCSkjy2degZ6tl8kczMEMWpO9w7gMP1ah1ZWzm1Oso7KtbeZdZkP+cf0Gph9uH1H4g9eVGKzPLxnJHWigFExtTZuFUg/smtRbrzgUznD0iYGV1f8UD5gEt+XD06MNukMRYOjtgTjuHWYE6xQ0St4hzDLJUb8qTQf9DY+w6iIB9QTinkVUXVCoKhXjApN2lmm0Qo7BoofLYIayFtFFFYhA/8SUxfj0codVGvbN/nR/iXmDC1EWZ5FG7jeH7h349HxDFE+CPXq38XfBhVxgXeFHl4Uz6GI70pfTh26ywFKHrj+WPovXeqQMNkQycAM8YYnUrKlZeQLmleV0VIdlwZuIrSJAQP+o4x6OrmVaEqqK6l1WO2axph9ZHTcZYBYYsvrs+HYQ5os= yuanf@PORMYUANF" >> ./authorized_keys

        docker build -t ${DOCKER_REPO}/$APP_NAME:latest . -f ./Dockerfile
        '''
      }
    }

    stage ('Trivy Scan') {
      steps { 
        sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock -v ${WORKSPACE}/trivy-reports:/output -e TRIVY_NEW_JSON_SCHEMA=true aquasec/trivy image --format json --timeout 15m0s --exit-code 0 --no-progress ${DOCKER_REPO}/${APP_NAME} | tee trivy.out'
        recordIssues enabledForFailure: true, aggregatingResults: true
//        recordIssues enabledForFailure: true, aggregatingResults: true, tool: trivy(pattern: "trivy.out")
      } 
    }

    stage('Publish') {
      steps {
        sh 'aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin ${DOCKER_REPO}'
        sh 'docker push ${DOCKER_REPO}/${APP_NAME}:latest'
      }
    }
  }
  post {
    // Cleanup the workspace
    always {
      cleanWs()
    }
  }
}
