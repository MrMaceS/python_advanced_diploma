from backend.database import Base, engine
from backend.models import User, Tweet, Media, Like, Follow

def main():
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")

if __name__ == "__main__":
    main()