from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .security import hash_password
from .models import User, Transaction, SubscriberPlan, Subscription
from .schemas import UserCreate, TransactionCreate, SubscriberPlanCreate, SubscriptionCreate

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    db_transaction = Transaction(**transaction.dict(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def get_transactions(db: Session, user_id: int):
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()


def create_subscriber_plan(db: Session, subscriber_plan: SubscriberPlanCreate):
    db_subscriber_plan = SubscriberPlan(**subscriber_plan.dict())
    db.add(db_subscriber_plan)
    db.commit()
    db.refresh(db_subscriber_plan)
    return db_subscriber_plan


def get_subscriber_plans(db: Session):
    return db.query(SubscriberPlan).all()


def create_subscription(db: Session, subscription: SubscriptionCreate, user_id: int):
    db_subscription = Subscription(**subscription.dict(), user_id=user_id)
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription
