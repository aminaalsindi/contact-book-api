

from database import *

init_db()
add_user("Ahmed")

users = get_all_users()

print(users)