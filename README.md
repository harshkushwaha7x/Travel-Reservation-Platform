# Travel Reservation Platform (Django)

A web-based travel reservation platform built with Django, designed to provide users with an easy way to search for and book travel destinations. The platform features user authentication, destination browsing, and real-time booking management, offering a seamless and efficient travel experience.

## Features

- **User Authentication**: Secure sign-up, login, and user profile management.
- **Search and Browse Destinations**: Easily search for travel destinations and view detailed information.
- **Booking System**: Users can book travel packages and manage reservations in real-time.
- **Admin Dashboard**: Administrators can manage destinations, bookings, and users.
- **Responsive Design**: The platform is mobile-friendly and works across devices.

## Technologies Used

- Django (Python framework)
- MySQL (Database)
- HTML/CSS/JavaScript (Frontend)
- Bootstrap (UI framework)

## Installation

1. Clone the repository.
2. Install dependencies using pip:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up your `.env` file with your database credentials and other configurations.
4. Run migrations to set up the database:
    ```bash
    python manage.py migrate
    ```
5. Create a superuser for admin access:
    ```bash
    python manage.py createsuperuser
    ```
6. Start the Django server:
    ```bash
    python manage.py runserver
    ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
