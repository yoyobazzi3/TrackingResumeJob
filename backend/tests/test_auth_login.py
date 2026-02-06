"""Auth service tests."""

import os
import sys
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import Base  # noqa: E402
from app.services.auth_service import create_user, authenticate_user  # noqa: E402


class TestAuthLoginEmailNormalization(unittest.TestCase):
    def setUp(self) -> None:
        # Use an in-memory SQLite DB for fast tests.
        self.engine = create_engine(
            "sqlite+pysqlite:///:memory:",
            connect_args={"check_same_thread": False},
        )
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def tearDown(self) -> None:
        # Clean up DB schema after each test.
        Base.metadata.drop_all(self.engine)
        self.engine.dispose()

    def test_login_normalizes_email(self) -> None:
        # Signup and login should normalize the email the same way.
        db = self.SessionLocal()
        try:
            create_user(db, "  Test@Example.com  ", "password123")
            user = authenticate_user(db, " test@EXAMPLE.com ", "password123")
            self.assertIsNotNone(user)
            self.assertEqual(user.email, "test@example.com")
        finally:
            db.close()
