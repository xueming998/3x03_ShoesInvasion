pipeline {
	agent {
            docker { image 'python:3.9-alpine' }
        }
/*
	environment{
		test_dir ="./ShoesInvasion"
	}

	parameters{
		booleanParam(name:"RUN_TEST", defaultValue: true, description: "Run Test Stage")
	}

*/
	stages {
		stage('Build') {
			steps {
				echo 'Building the application ...'
				sh 'pip install -r requirements.txt'
			}
		}

		stage('OWASP DependencyCheck') {
			/*
			when{
				expression {
					params.RUN_TEST 
					//Only run DependencyCheck in development or master branch, this should only work if you have a multibranch pipeline
					env.BRANCH_NAME == 'Development' 
				}

			}*/
			steps {
				echo 'OWASP DependencyCheck ...'
				//Disable yarn audit as not in used
				dependencyCheck additionalArguments: '--format HTML --format XML --disableYarnAudit', odcInstallation: 'Default'
			}
		} 

		stage('Test') {
			/*
			when{
				expression {
					params.RUN_TEST 
					//Only run unit test in development or master branch, this should only work if you have a multibranch pipeline
					env.BRANCH_NAME == 'Development'
				}

			}*/

            steps {
                //echo 'Testing the application ...'
				echo 'JUnit Test ...'
				sh 'python manage.py test'
				/*
				dir("${test_dir}"){
					sh "python manage.py test"
				} */
				
            }
	}
	}	
	post {
		success {
			dependencyCheckPublisher pattern: 'dependency-check-report.xml'
			// junit '**/target/*.xml'
		}
	}
}
