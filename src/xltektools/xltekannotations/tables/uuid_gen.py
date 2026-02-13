# Header #
__package_name__ = "xltektools"

__author__ = "Anthony Fong"
__credits__ = ["Anthony Fong"]
__copyright__ = "Copyright 2022, Anthony Fong"
__license__ = "MIT"

__version__ = "0.6.0"


import uuid

def generate_uuid_for_token(token):
    # Use a fixed namespace UUID (can be any constant UUID)
    # namespace = uuid.UUID('12345678-1234-5678-1234-567812345678')
    # return str(uuid.uuid4(namespace, str(token)))
    return str(uuid.uuid4()) # Generate a random UUID for each instance

# Example usage
# token = 345672
# unique_id_1 = generate_uuid_for_token(token)
# unique_id_2 = generate_uuid_for_token(token)

# print(f"UUID for token instance '{token}': {unique_id_1}")
# print(f"UUID for token instance '{token}': {unique_id_2}")
