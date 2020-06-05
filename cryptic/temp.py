from cryptic import app,db
from cryptic.models import User
all_users = User.query.all()
print(all_users)
