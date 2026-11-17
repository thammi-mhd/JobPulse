from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()

def test_create_user():
    try:

        email_to_check = "thameez@example.com"

        # 1. CHECK FIRST: See if the user already exists
        statement = select(User).where(User.email == email_to_check)
        existing_user = db.execute(statement).scalar_one_or_none()

        if existing_user:
            print(f"User already exists: {existing_user.username}, Email: {existing_user.email}, ID: {existing_user.id}")
            return


        # Create a new user
        new_user = User(
            username="Thameez",
        email="thameez@example.com",
        hashed_password="temporary_hash_for_testing"
        )

        #add user to the session
        db.add(new_user)

        #commit the changes to the database
        db.commit()

        #refresh the instance to get the updated data from the database
        db.refresh(new_user)

        print(f"Created user: {new_user.username}, Email: {new_user.email}, ID: {new_user.id}")

        #retrieve the user using email
        statement = select(User).where(User.email == "thameez@example.com")

        result = db.execute(statement)

        user = result.scalar_one_or_none()

        if user:
            print(f"Retrieved user: {user.username}, Email: {user.email}, ID: {user.id}")
        else:
            print("User not found.")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
        raise

    finally:
        db.close()

if __name__ == "__main__":
    test_create_user()