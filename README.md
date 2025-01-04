# Smart-Home-IDS Network Traffic Detection

## Overview
This project is a web-based application designed for analyzing network traffic data and identifying potential security threats. Built using Django and Django REST Framework (DRF), the application provides a RESTful API for CRUD operations and filtering, making it a valuable tool for cybersecurity analysts and researchers.

## Features
- **Database Design**: Robust model representing network traffic data fields.
- **Data Seeding**: Load data into the database using a custom management command.
- **RESTful Endpoints**:
  - `/api/traffic`: Retrieve all network traffic records.
  - `/api/traffic/<id>/`: Retrieve, update, or delete specific records.
- **Filtering and Queries**: Filter traffic data by attributes like protocol type, service, and attack status.
- **Unit Testing**: Comprehensive tests for models and views to ensure application integrity.

## Installation and Setup
To set up and run the application locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/network-traffic-detection.git
   cd network-traffic-detection
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations to set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Load the dataset into the database:
   ```bash
   python manage.py load_csv
   ```

6. Run the application:
   ```bash
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000`.

## Usage
- Access the API endpoints to interact with network traffic data.
- Use filters to query specific subsets of data, such as all traffic flagged as attacks.
- Utilize the provided unit tests to validate the integrity of models and views.

## Testing
Run the tests using:
```bash
python manage.py test
```

## Dataset
The dataset includes fields like `duration`, `protocol_type`, `service`, `src_bytes`, `dst_bytes`, and `attack`, which collectively represent network traffic behavior. The data is crucial for simulating real-world network monitoring scenarios.

## Future Improvements
- Enhanced filtering and querying capabilities.
- Integration with live network traffic monitoring systems.
- Advanced visualizations for data analysis.

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.
```

---
