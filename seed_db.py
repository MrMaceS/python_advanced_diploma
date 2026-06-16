from backend.database import SessionLocal
from backend.models import User, Tweet, Follow, Like, Media


def clear_db(session):
    """Опционально: очистить данные перед seed'ом."""
    session.query(Like).delete()
    session.query(Follow).delete()
    session.query(Media).delete()
    session.query(Tweet).delete()
    session.query(User).delete()
    session.commit()


def seed_users(session):
    """Создаём пользователей"""
    users_data = [
        {"name": "Mr.Mace",    "api_key": "test"},
        {"name": "SpongeBob",  "api_key": "bob-key"},
        {"name": "Lev",        "api_key": "lev-key"},
        {"name": "Alice",      "api_key": "alice-key"},
        {"name": "Bob",        "api_key": "bob2-key"},
        {"name": "Charlie",    "api_key": "charlie-key"},
        {"name": "Dana",       "api_key": "dana-key"},
        {"name": "Екатерина",  "api_key": "katya-key"},
        {"name": "Иван",       "api_key": "ivan-key"},
        {"name": "Николай",    "api_key": "nik-key"},
    ]

    users = []
    for data in users_data:
        user = User(name=data["name"], api_key=data["api_key"])
        session.add(user)
        users.append(user)

    session.commit()

    for user in users:
        session.refresh(user)

    return users


def seed_follows(session, users):
    """
    Связи фолловинга (пример):

    - Mr.Mace фолловит SpongeBob и Lev
    - Alice фолловит Bob и Charlie
    - Bob фолловит Alice
    - Lev фолловит Mr.Mace
    - Иван фолловит Екатерину и Николая
    """
    mace = next(u for u in users if u.name == "Mr.Mace")
    spongebob = next(u for u in users if u.name == "SpongeBob")
    lev = next(u for u in users if u.name == "Lev")
    alice = next(u for u in users if u.name == "Alice")
    bob = next(u for u in users if u.name == "Bob")
    charlie = next(u for u in users if u.name == "Charlie")
    ivan = next(u for u in users if u.name == "Иван")
    katya = next(u for u in users if u.name == "Екатерина")
    nik = next(u for u in users if u.name == "Николай")

    follows = [
        Follow(user_id=mace.id,     following_user_id=spongebob.id),
        Follow(user_id=mace.id,     following_user_id=lev.id),

        Follow(user_id=alice.id,    following_user_id=bob.id),
        Follow(user_id=alice.id,    following_user_id=charlie.id),
        Follow(user_id=bob.id,      following_user_id=alice.id),

        Follow(user_id=lev.id,      following_user_id=mace.id),

        Follow(user_id=ivan.id,     following_user_id=katya.id),
        Follow(user_id=ivan.id,     following_user_id=nik.id),
    ]

    session.add_all(follows)
    session.commit()


def seed_tweets(session, users):
    """
    Создадим твиты от разных пользователей
    """
    mace = next(u for u in users if u.name == "Mr.Mace")
    spongebob = next(u for u in users if u.name == "SpongeBob")
    lev = next(u for u in users if u.name == "Lev")
    alice = next(u for u in users if u.name == "Alice")
    bob = next(u for u in users if u.name == "Bob")
    charlie = next(u for u in users if u.name == "Charlie")
    dana = next(u for u in users if u.name == "Dana")
    katya = next(u for u in users if u.name == "Екатерина")
    ivan = next(u for u in users if u.name == "Иван")
    nik = next(u for u in users if u.name == "Николай")

    tweets = [

        Tweet(
            content="Mr.Mace: утро началось с дождя, но настроение боевое.",
            author_id=mace.id
        ),
        Tweet(
            content="Mr.Mace: дописал фичу, выхожу на улицу — солнце, как награда.",
            author_id=mace.id
        ),

        Tweet(
            content="SpongeBob: за окном пасмурно, но в голове полный штиль и идеи.",
            author_id=spongebob.id
        ),
        Tweet(
            content="SpongeBob: после работы иду гулять по городу, люблю свежий воздух после дождя.",
            author_id=spongebob.id
        ),

        Tweet(
            content="Lev: сегодня весь день шёл снег, идеально, чтобы сидеть дома и кодить.",
            author_id=lev.id
        ),
        Tweet(
            content="Lev: сделал перерыв, вышел на балкон — воздух холодный, но голова очистилась.",
            author_id=lev.id
        ),

        Tweet(
            content="Alice: утренний кофе и лёгкий туман за окном — лучший старт дня.",
            author_id=alice.id
        ),
        Tweet(
            content="Alice: весь день в офисе, зато вечером будет прогулка под звёздами.",
            author_id=alice.id
        ),

        Tweet(
            content="Bob: странная погода, то солнце, то ветер, а задачи всё равно ждать не будут.",
            author_id=bob.id
        ),
        Tweet(
            content="Bob: закончил дебажить, и как назло — начался ливень. Домой поеду под дождём.",
            author_id=bob.id
        ),

        Tweet(
            content="Charlie: утренний дождь смыл весь сон, теперь можно спокойно пилить фронт.",
            author_id=charlie.id
        ),
        Tweet(
            content="Charlie: вечером было ясное небо, сел на лавочку и подумал, что люблю свою работу.",
            author_id=charlie.id
        ),

        Tweet(
            content="Dana: целый день облачно, зато ни солнце, ни жара не отвлекают от тестов.",
            author_id=dana.id
        ),
        Tweet(
            content="Dana: дождь за окном — идеальный фон, чтобы писать юнит-тесты и слушать музыку.",
            author_id=dana.id
        ),

        Tweet(
            content="Екатерина: утром лёгкий мороз и ясное небо, еду на работу и думаю о докладе.",
            author_id=katya.id
        ),
        Tweet(
            content="Екатерина: вернулась домой, за окном снег, а я дописываю слайды к презентации.",
            author_id=katya.id
        ),

        Tweet(
            content="Иван: сильный ветер напомнил, что лучше сидеть в офисе и не забывать про бэкапы.",
            author_id=ivan.id
        ),
        Tweet(
            content="Иван: вечером пошёл лёгкий дождь, а я как раз закончил деплой и выключил ноут.",
            author_id=ivan.id
        ),

        Tweet(
            content="Николай: утром серое небо, но с новым проектом день всё равно начинается интересно.",
            author_id=nik.id
        ),
        Tweet(
            content="Николай: ночь выдалась тёплой, сидел на балконе и думал над архитектурой сервиса.",
            author_id=nik.id
        ),
    ]

    session.add_all(tweets)
    session.commit()

    for t in tweets:
        session.refresh(t)

    return tweets


def seed_likes(session, users, tweets):
    """
    Немного лайков для активности.
    """
    mace = next(u for u in users if u.name == "Mr.Mace")
    spongebob = next(u for u in users if u.name == "SpongeBob")
    lev = next(u for u in users if u.name == "Lev")
    alice = next(u for u in users if u.name == "Alice")
    bob = next(u for u in users if u.name == "Bob")
    ivan = next(u for u in users if u.name == "Иван")

    mace_tweets = [t for t in tweets if t.author_id == mace.id]
    spongebob_tweets = [t for t in tweets if t.author_id == spongebob.id]
    lev_tweets = [t for t in tweets if t.author_id == lev.id]
    alice_tweets = [t for t in tweets if t.author_id == alice.id]
    bob_tweets = [t for t in tweets if t.author_id == bob.id]
    ivan_tweets = [t for t in tweets if t.author_id == ivan.id]

    tweet_spongebob_1 = spongebob_tweets[0]
    tweet_mace_1 = mace_tweets[0]
    tweet_bob_1 = bob_tweets[0]
    tweet_lev_1 = lev_tweets[0]
    tweet_alice_1 = alice_tweets[0]
    tweet_ivan_1 = ivan_tweets[0]

    likes = [
        Like(user_id=mace.id,      tweet_id=tweet_bob_1.id),
        Like(user_id=mace.id,      tweet_id=tweet_lev_1.id),

        Like(user_id=spongebob.id, tweet_id=tweet_mace_1.id),
        Like(user_id=alice.id,     tweet_id=tweet_mace_1.id),

        Like(user_id=bob.id,       tweet_id=tweet_alice_1.id),

        Like(user_id=ivan.id,      tweet_id=tweet_ivan_1.id),
        Like(user_id=ivan.id,      tweet_id=tweet_spongebob_1.id),
    ]

    session.add_all(likes)
    session.commit()

    for l in likes:
        session.refresh(l)

    return likes


def seed_media(session, tweets):
    """
    Пример: привяжем картинки к нескольким твитам.
    Пути должны соответствовать тому, что лежит в backend/media.
    """
    tweet_mace_1 = next(t for t in tweets if t.content.startswith("Mr.Mace:"))
    tweet_lev_1 = next(t for t in tweets if t.content.startswith("Lev: сегодня"))
    tweet_bob_1 = next(t for t in tweets if t.content.startswith("Bob: странная погода"))

    media_objects = [
        Media(file_path="media/1_image2.jpg",  tweet_id=tweet_mace_1.id),
        Media(file_path="media/1_images.jpg",  tweet_id=tweet_lev_1.id),
        Media(file_path="media/1_images3.jpg", tweet_id=tweet_bob_1.id),
    ]

    session.add_all(media_objects)
    session.commit()

    for m in media_objects:
        session.refresh(m)

    return media_objects


def main() -> None:
    session = SessionLocal()
    try:
        print("Clearing existing data...")
        clear_db(session)

        print("Seeding users...")
        users = seed_users(session)

        print("Seeding follows...")
        seed_follows(session, users)

        print("Seeding tweets...")
        tweets = seed_tweets(session, users)

        print("Seeding media...")
        seed_media(session, tweets)

        print("Seeding likes...")
        seed_likes(session, users, tweets)

        print("Seed completed.")
        print("Используйте api-key одного из пользователей:")
        for u in users:
            print(f"- {u.name}: api-key = {u.api_key}")

    finally:
        session.close()


if __name__ == "__main__":
    main()