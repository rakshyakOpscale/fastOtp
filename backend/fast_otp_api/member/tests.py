from django.test import TestCase

# Create your tests here.
contact = {
    "id": 1,
    "phone_number": "1234567890",
    "label": "family",
    "first_name": "Rahul",
    "last_name": "Sharma",
}
app = {
    "id": 1,
    "display_name": "amazone",
    "package_name": "com.package.amazone",
    "label": "ecomarce",
}
config = {
    "id": 1,
    "set_duration": "2h",
    "profile": 1,
    "contact": [
        1,
        2
    ],
    "selected_apps": [
        1
    ]
}