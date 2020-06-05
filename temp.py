from cryptic import app,db
from cryptic.models import User

all_users = User.query.all()
for user in all_users:
    print(user.fname)
