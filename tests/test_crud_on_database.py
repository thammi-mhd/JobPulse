from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()

def test_crud_op():
    try:

        email_to_check = "thameez@example.com"

        # 1. CHECK FIRST: See if the user already exists
        user = db.execute(select(User).where(User.email == email_to_check)).scalar_one_or_none()

        if user:
            print(f"user found: {user.username}, Email: {user.email}, ID: {user.id}")

            user.username = "Thameez Updated"
            db.commit()

            print("username updated successfully.")

            #verify the update by retrieving the user again
            db.refresh(user)
            print(f"updated username to : {user.username}")

        #delete the user
            db.delete(user)
            db.commit()

            print("user deleted successfully.")



    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
        raise

    finally:
        db.close()

if __name__ == "__main__":
    test_crud_op()