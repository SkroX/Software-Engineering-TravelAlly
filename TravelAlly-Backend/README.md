# TravelAlly Backend

Server side code written in Django rest framework for an android app TravelAlly.
App can be found at : [TravelAlly Android](https://github.com/SkroX/TravelAlly-Android)

Docker and Docker-Compose is used for containerization.

Postgres is used as Database.

Google auth is used to verify and get data from idtoken

# Building The Project

- Docker & Docker-Compose must be setup before building the project.
- Clone the repository with `git clone https://github.com/SkroX/TravelAlly-Backend.git`
- Navigate to the root directory of project.
- Run `sudo docker-compose build .` to build the image.
- Run `sudo docker-compose up` to run the server at port 8080. You can visit http://127.0.0.1:8080 to view the endpoints.
- You can run `sudo docker-compose run --rm app sh -c "python manage.py makemigrations"` to create the db migrations.
- You can run `sudo docker-compose run --rm app sh -c "python manage.py migrate"` to apply the migrations.
- You can run `sudo docker-compose run --rm app sh -c "python manage.py test"` to run the tests.

# Contribution

- I will be happy to invite new contributors.

- Fork the project to your own account.

- Create your new branch using 
`git checkout -b [your branch name]`
  
- Make sure the changes you made are of good quality and the project is building successfully.
  
- Commit your changes to this branch with `git commit -m "meaningful message"`

- Make a pull request.
