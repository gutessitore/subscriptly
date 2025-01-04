import random
import string

class PasswordGenerator:
    def __init__(
        self,
        length: int = 6,
        num_numbers: int = 4,
        num_uppercase: int = 1,
        num_lowercase: int = 0,
        num_special_chars: int = 1,
    ):
        """
        Initialize the password generator with specified options.

        Args:
            length (int): Total length of the password.
            num_numbers (int): Number of numeric characters in the password.
            num_uppercase (int): Number of uppercase letters in the password.
            num_lowercase (int): Number of lowercase letters in the password.
            num_special_chars (int): Number of special characters in the password.
        """
        self.length = length
        self.num_numbers = num_numbers
        self.num_uppercase = num_uppercase
        self.num_lowercase = num_lowercase
        self.num_special_chars = num_special_chars

        total_requested = num_numbers + num_uppercase + num_lowercase + num_special_chars
        if total_requested > length:
            raise ValueError(
                "The sum of character-specific counts exceeds the total password length!"
            )
        self.num_filler_lowercase = length - total_requested  # Remaining length filled with lowercase

    def generate(self) -> str:
        """
        Generate the password based on the specified options.

        Returns:
            str: A randomly generated password.
        """
        password_chars = []

        # Add numbers
        password_chars += random.choices(string.digits, k=self.num_numbers)

        # Add uppercase letters
        password_chars += random.choices(string.ascii_uppercase, k=self.num_uppercase)

        # Add lowercase letters
        password_chars += random.choices(string.ascii_lowercase, k=self.num_lowercase)

        # Add special characters
        # special_chars = "!@#$%&*()-_=+[]{};:.?"
        special_chars = "@#$%&"
        password_chars += random.choices(special_chars, k=self.num_special_chars)

        # Fill the remaining characters with lowercase letters
        password_chars += random.choices(string.ascii_lowercase, k=self.num_filler_lowercase)

        # Shuffle the resulting password to ensure randomness
        random.shuffle(password_chars)

        return ''.join(password_chars)
