import os
import platform
import pkg_resources
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework import __version__ as drf_version
from django.db.models import Q
from .models import NetworkTraffic
from .serializers import NetworkTrafficSerializer

# View admin credentials
def admin_credentials(request):
    admin_user = User.objects.filter(is_superuser=True).first()
    context = {
        "admin_username": admin_user.username if admin_user else "Not configured",
        "admin_password": "password",
    }
    return render(request, "../templates/credentials.html", context)

# Index view to display general information and API endpoints
def index(request):
    # Fetch the Python version being used
    python_version = platform.python_version()
    
    # Fetch the Django and DRF versions being used
    django_version = pkg_resources.get_distribution("Django").version
    drf_version == drf_version

    # Read the `requirements.txt` file to list installed dependencies
    requirements_path = os.path.join(settings.BASE_DIR, 'requirements.txt')
    with open(requirements_path, 'r') as file:
        requirements = file.readlines()
    
    #Filter relevant packages
    relevant_packages = ['Django', 'drf', 'psycopg2']
    filtered_requirements = [
        req.strip() for req in requirements if any(pkg in req for pkg in relevant_packages)
        ]

    # Fetch the first superuser account (admin details)
    admin_user = User.objects.filter(is_superuser=True).first()
    admin_username = admin_user.username if admin_user else "Not configured"
    admin_password = "Admin password is confidential"

    # Define a list of API endpoints available in the application
    api_endpoints = [
        {"name": "Traffic List", "url": reverse('traffic-list'), "description": "List all network traffic data."},
        {"name": "Traffic Detail", "url": reverse('traffic-detail', kwargs={"pk": 1}), "description": "View detailed information of a single traffic record."},
        {"name": "Traffic Create", "url": reverse('traffic-create'), "description": "Create a new traffic record."},
        {"name": "Anomalous Traffic", "url": reverse('anomalous-traffic'), "description": "Identify anomalous traffic patterns."},
        {"name": "Traffic Filter by Service", "url": reverse('traffic-filter-service', kwargs={"service": "http"}), "description": "Filter traffic by service type e.g. http."},
        {"name": "Traffic Filter by Attack", "url": reverse('traffic-filter-attack'), "description": "Filter traffic by attack type."},

        # These are commented from the main view but was tested via cURL on the CLI
        # {"name": "Traffic Update", "url": reverse('traffic-update', kwargs={"pk": 1}), "description": "Endpoint to update an existing traffic record."},
        # {"name": "Traffic Delete", "url": reverse('traffic-delete', kwargs={"pk": 1}), "description": "Endpoint to delete a traffic record."},
    ]

    # Context data to be passed to the template for rendering
    context = {
        "python_version": python_version,
        "django_version": django_version,
        "drf_version": drf_version,
        "requirements": requirements,
        "admin_username": admin_username,
        "admin_password": admin_password,
        "api_endpoints": api_endpoints,
    }
    return render(request, "../templates/index.html", context)  # Render the HTML template with context data

# Direct API Views to handle NetworkTraffic-related operations

# 1. Retrieve the list of all network traffic records
class NetworkTrafficListView(APIView):
    def get(self, request):
        traffic_data = NetworkTraffic.objects.all()  # Fetch all records from the database
        serializer = NetworkTrafficSerializer(traffic_data, many=True)  # Serialize multiple records
        return Response(serializer.data, status=status.HTTP_200_OK)  # Return serialized data as a JSON response


# 2. Retrieve details of a single record by its primary key (ID)
class NetworkTrafficDetailView(APIView):
    def get(self, request, pk):
        try:
            traffic_data = NetworkTraffic.objects.get(pk=pk)  # Fetch the record by ID
            serializer = NetworkTrafficSerializer(traffic_data)  # Serialize the single record
            return Response(serializer.data, status=status.HTTP_200_OK)  # Return serialized data
        except NetworkTraffic.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)  # Handle record not found


# 3. Create a new record in the database
class NetworkTrafficCreateView(APIView):
    def post(self, request):
        serializer = NetworkTrafficSerializer(data=request.data)  # Deserialize incoming data
        if serializer.is_valid():
            serializer.save()  # Save the valid data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return the created record
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors


# 4. Update an existing record identified by its ID
class NetworkTrafficUpdateView(APIView):
    def put(self, request, pk):
        try:
            traffic_data = NetworkTraffic.objects.get(pk=pk)  # Fetch the existing record
            serializer = NetworkTrafficSerializer(traffic_data, data=request.data)  # Update with new data
            if serializer.is_valid():
                serializer.save()  # Save the updated record
                return Response(serializer.data, status=status.HTTP_200_OK)  # Return updated data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors
        except NetworkTraffic.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)  # Handle record not found


# 5. Delete a record by its ID
class NetworkTrafficDeleteView(APIView):
    def delete(self, request, pk):
        try:
            traffic_data = NetworkTraffic.objects.get(pk=pk)  # Fetch the record to delete
            traffic_data.delete()  # Delete the record
            return Response({"message": "Record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)  # Success message
        except NetworkTraffic.DoesNotExist:
            return Response({"error": "Record not found"}, status=status.HTTP_404_NOT_FOUND)  # Handle record not found


# 6. Identify anomalous traffic records based on byte thresholds
class AnomalousTrafficView(APIView):
    def get(self, request):
        threshold = int(request.query_params.get('threshold', 1000))  # Retrieve threshold or use default
        traffic_data = NetworkTraffic.objects.filter(
            Q(src_bytes__gte=threshold) | Q(dst_bytes__gte=threshold)  # Filter based on source/destination bytes
        )
        serializer = NetworkTrafficSerializer(traffic_data, many=True)  # Serialize filtered records
        return Response(serializer.data, status=status.HTTP_200_OK)  # Return filtered data


# 7. Filter traffic records based on the service type
class NetworkTrafficFilterByServiceView(APIView):
    def get(self, request, service):  # The 'service' argument comes directly from the URL
        if service:
            traffic_data = NetworkTraffic.objects.filter(service=service)  # Filter by service type
            serializer = NetworkTrafficSerializer(traffic_data, many=True)  # Serialize filtered records
            return Response(serializer.data, status=status.HTTP_200_OK)  # Return filtered data
        return Response({"error": "Service is required"}, status=status.HTTP_400_BAD_REQUEST)  # Handle missing parameter

# 8. Filter traffic records based on attack type
class NetworkTrafficFilterByAttackView(APIView):
    def get(self, request):
        # Convert attack type query parameter to boolean
        attack_value = request.query_params.get('attack', 'yes').strip().lower()
        if attack_value == 'yes':
            attack_value = True
        elif attack_value == 'no':
            attack_value = False
        else:
            return Response({"error": "Invalid attack type. Use 'yes' or 'no'."}, status=status.HTTP_400_BAD_REQUEST)

        # Filter records based on attack value
        traffic_data = NetworkTraffic.objects.filter(attack=attack_value)
        if traffic_data.exists():
            serializer = NetworkTrafficSerializer(traffic_data, many=True)  # Serialize filtered records
            return Response(serializer.data, status=status.HTTP_200_OK)  # Return filtered data

        return Response({"error": "No records match the provided attack type."}, status=status.HTTP_404_NOT_FOUND)  # Handle no matches


class NetworkTrafficComplexFiltersView(APIView):
    """
    Advanced filtering for network traffic data based on fields in the dataset.
    """
    def get(self, request):
        # Parse query parameters
        protocol_type = request.query_params.get('protocol_type', None)
        service = request.query_params.get('service', None)
        flag = request.query_params.get('flag', None)
        src_bytes_min = request.query_params.get('src_bytes_min', None)
        src_bytes_max = request.query_params.get('src_bytes_max', None)
        dst_bytes_min = request.query_params.get('dst_bytes_min', None)
        dst_bytes_max = request.query_params.get('dst_bytes_max', None)
        land = request.query_params.get('land', None)
        attack = request.query_params.get('attack', None)
        serror_rate_min = request.query_params.get('serror_rate_min', None)
        serror_rate_max = request.query_params.get('serror_rate_max', None)

        # Build filter query
        query = Q()
        if protocol_type:
            query &= Q(protocol_type__iexact=protocol_type)
        if service:
            query &= Q(service__iexact=service)
        if flag:
            query &= Q(flag__iexact=flag)
        if src_bytes_min:
            query &= Q(src_bytes__gte=int(src_bytes_min))
        if src_bytes_max:
            query &= Q(src_bytes__lte=int(src_bytes_max))
        if dst_bytes_min:
            query &= Q(dst_bytes__gte=int(dst_bytes_min))
        if dst_bytes_max:
            query &= Q(dst_bytes__lte=int(dst_bytes_max))
        if land:
            land_bool = land.lower() == 'yes'
            query &= Q(land=land_bool)
        if attack:
            attack_bool = attack.lower() == 'yes'
            query &= Q(attack=attack_bool)
        if serror_rate_min:
            query &= Q(serror_rate__gte=float(serror_rate_min))
        if serror_rate_max:
            query &= Q(serror_rate__lte=float(serror_rate_max))

        # Fetch and serialize filtered data
        traffic_data = NetworkTraffic.objects.filter(query)
        serializer = NetworkTrafficSerializer(traffic_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
