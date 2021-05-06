# TravelAlly-Android
Android app to join the travelers visiting the same destination.

Implemented around Model-View-ViewModel (MVVM) Architecture. Architecture component Libraries from Google are used.
Learn more about it here: https://developer.android.com/topic/libraries/architecture

Navigation Component library is used to navigate around the app.
Learn more about it here: https://developer.android.com/guide/navigation

Dagger is used for Dependency Injection.
Learn about it: https://developer.android.com/training/dependency-injection/dagger-basics

Retrofit is used as the networking library.
Learn it here: https://square.github.io/retrofit/

Kotlin Coroutines are used for providing asynchronous programming.
Read about them here: https://kotlinlang.org/docs/reference/coroutines-overview.html

# Building the Code

- Clone the repository using HTTP: `git clone https://github.com/SkroX/Software-Engineering-TravelAlly.git`

- Open Android Studio.

- Click on 'Open an existing Android Studio project'

- Browse to the directory where you cloned the mobile-wallet repo and click OK.

- Let Android Studio import the project.

- Build the application in your device by clicking run button.

# Contribution

- Fork the project to your own account.

- Create your new branch using 
`git checkout -b [your branch name]`
  
- Make sure the changes you made are of good quality and the project is building successfully.
  
- Commit your changes to this branch with `git commit -m "meaningful message"`

- Make a pull request.


# TravelAlly Backend

Server side code written in Django rest framework for an android app TravelAlly.

Docker and Docker-Compose is used for containerization.

Postgres is used as Database.

Google auth is used to verify and get data from idtoken

# Building The Project

- Docker & Docker-Compose must be setup before building the project.
- Clone the repository with `git clone https://github.com/SkroX/Software-Engineering-TravelAlly.git`
- Navigate to the root directory of project.
- Run `sudo docker-compose build .` to build the image.
- Run `sudo docker-compose up` to run the server at port 8080. You can visit http://127.0.0.1:8080 to view the endpoints.
- You can run `sudo docker-compose run --rm app sh -c "python manage.py makemigrations"` to create the db migrations.
- You can run `sudo docker-compose run --rm app sh -c "python manage.py migrate"` to apply the migrations.
- You can run `sudo docker-compose run --rm app sh -c "python manage.py test"` to run the tests.

# Contribution

- Fork the project to your own account.

- Create your new branch using 
`git checkout -b [your branch name]`
  
- Make sure the changes you made are of good quality and the project is building successfully.
  
- Commit your changes to this branch with `git commit -m "meaningful message"`

- Make a pull request.


