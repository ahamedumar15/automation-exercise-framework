
from faker import Faker
from datetime import datetime
from config.config import TEST_EMAIL_DOMAIN

fake = Faker()


class UserData:
    """Generate test user data"""

    @staticmethod
    def generate_user():
        """Generate random user data"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        return {
            'name': fake.first_name(),
            'email': f"test_{timestamp}{TEST_EMAIL_DOMAIN}",
            'password': 'Test@12345',
            'title': fake.random_element(['Mr', 'Mrs']),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'company': fake.company(),
            'address1': fake.street_address(),
            'address2': fake.secondary_address(),
            'country': 'India',
            'state': fake.state(),
            'city': fake.city(),
            'zipcode': fake.zipcode(),
            'mobile': fake.phone_number()[:15],
            'day': str(fake.random_int(1, 28)),
            'month': str(fake.random_int(1, 12)),
            'year': str(fake.random_int(1980, 2000)),
            'newsletter': True,
            'special_offers': True
        }

    @staticmethod
    def generate_multiple_users(count=3):
        """Generate multiple users"""
        return [UserData.generate_user() for _ in range(count)]


class ProductData:
    """Product related test data"""

    @staticmethod
    def get_sample_products():
        """Get sample product names for testing"""
        return [
            "Blue Top",
            "Men Tshirt",
            "Sleeveless Dress",
            "Stylish Dress",
            "Winter Top"
        ]

    @staticmethod
    def get_search_terms():
        """Get search terms for product search"""
        return {
            'valid': ['top', 'dress', 'jeans', 'tshirt'],
            'invalid': ['xyz123', 'nonexistent'],
            'partial': ['blu', 'men', 'kid']
        }


class ContactData:
    """Contact form test data"""

    @staticmethod
    def get_contact_info():
        """Generate contact form data"""
        return {
            'name': fake.name(),
            'email': fake.email(),
            'subject': fake.sentence(nb_words=5),
            'message': fake.text(max_nb_chars=200)
        }


class LoginCredentials:
    """Login credentials for testing"""

    VALID_USER = {
        'email': 'testuser@example.com',
        'password': 'Test@12345'
    }

    INVALID_USER = {
        'email': 'invalid@example.com',
        'password': 'WrongPassword'
    }

    EMPTY_CREDENTIALS = {
        'email': '',
        'password': ''
    }