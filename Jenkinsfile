pipeline {
  agent {
    kubernetes {
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    command:
    - cat
    tty: true
    volumeMounts:
    - name: kaniko-volume
      mountPath: /kaniko/.docker
  volumes:
  - name: kaniko-volume
    emptyDir: {}
"""
      defaultContainer 'kaniko'
    }
  }

  environment {
    IMAGE = "Ruben-Delgado-23/Simple-Juniper-SRX-VPN-Site-to-Site-Configurator-docker"
  }

  stages {
    stage('Clonar repositorio') {
      steps {
        git 'https://github.com/Ruben-Delgado-23/Simple-Juniper-SRX-VPN-Site-to-Site-Configurator-docker.git'
      }
    }

    stage('Crear config.json con credenciales codificadas') {
      steps {
        sh '''
          mkdir -p /kaniko/.docker
          cat <<EOF > /kaniko/.docker/config.json
{
  "auths": {
    "https://index.docker.io/v1/": {
      "auth": "/N@yRJatLSqW87K"  // <== Reemplaza con tu base64 real
    }
  }
}
EOF
        '''
      }
    }

    stage('Construir y subir imagen con Kaniko') {
      steps {
        sh '''
        /kaniko/executor \
          --context `pwd` \
          --dockerfile `pwd`/Dockerfile \
          --destination=${IMAGE}:latest \
          --verbosity=info
        '''
      }
    }
  }
}
