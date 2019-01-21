"""
You will need a Postgres DB to run this. For development, you can run using Docker:
docker pull postgres
    docker run -p 5432:5432 --name data_coll_db \
        -e POSTGRES_PASSWORD=mypassword \
        -e POSTGRES_USER=user\
        -d postgres

If you want an easy way to interact with DB:
    docker pull dpage/pgadmin4
    docker run -p 80:80 \
        -e "PGADMIN_DEFAULT_EMAIL=user@domain.com" \
        -e "PGADMIN_DEFAULT_PASSWORD=mypassword" \
        -d dpage/pgadmin4

Please ensure you have environment variables set for:
USER_REG_USER
USER_REG_PASSWORD
USER_REG_SERVICE
USER_REG_DB
"""


from flask import render_template, Flask, request
from flask_sqlalchemy import SQLAlchemy
import os

application = Flask(__name__)
#application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:mypassword@localhost/user_reg'
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + os.environ['USER_REG_USER'] + ":" + os.environ['USER_REG_PASSWORD'] + "@" + os.environ['USER_REG_SERVICE'] + "/" + os.environ['USER_REG_DB']
db = SQLAlchemy(application)

class User(db.Model):
    __tablename__ = 'workshop_users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    #user_id = db.Column(db.String(7), unique=True, nullable=False)

    def __init__(self, user_name):
        self.user_name = user_name
        print("user init ran")
    # def __repr__(self):
    #     #return self.user_id
    #     return self.user_name

db.create_all()

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        user_name = request.form['real_name']
        print(user_name)
        if db.session.query(User).filter(User.user_name == user_name).count() == 0:
            data = User(user_name)
            db.session.add(data)
            db.session.commit()
            if data.id <= 200:
                return render_template('success.html', workshop_user_id="user" + str(data.id))
            else:
                return render_template("index.html", text="Sorry, we're out of user IDs. Please ask trainer for help.")
        else:
            workshop_user_id = db.session.query(User).filter(User.user_name == user_name).first()
            return render_template("index.html", text="You already have a user assigned: user" + str(workshop_user_id.id))



if __name__ == "__main__":
    application.run(debug=True)