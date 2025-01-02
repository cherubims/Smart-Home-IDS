import csv
from django.core.management.base import BaseCommand
from network_traffic.models import NetworkTraffic

# Define a custom Django management command to load network traffic data from CSV  into DB.
class Command(BaseCommand):
    # When running the `help` flag:
    help = "Load network traffic data from a CSV file into the Database."

    # Custom cli arguments to the management command.
    def add_arguments(self, parser):
        # Define a required positional argument named 'csv_file' for the path to the CSV file.
        parser.add_argument('csv_file', type=str, help="The path to the CSV file to be loaded")

    # Main logic
    def handle(self, *args, **options):
        # Retrieve path to CSV file
        csv_file = options['csv_file']

        try:
            # Attempt to open the specified CSV file in read mode.
            with open(csv_file, mode='r') as file:
                # Use the DictReader to parse the CSV file, mapping each row to a dict.
                reader = csv.DictReader(file)
                rows = 0  # Counter for the number of rows successfully processed.

                # Loop through each row
                for row in reader:
                    # Create a new NetworkTraffic object for each row, save to db and increment by 1
                    NetworkTraffic.objects.create(
                        duration=float(row['duration']),  # Duration of the network traffic session.
                        protocol_type=row['protocol_type'],  # Protocol type used in the session (e.g., TCP, UDP).
                        service=row['service'],  # The service or application accessed (e.g., HTTP, FTP).
                        flag=row['flag'],  # Flag status indicating the session state (e.g., SF, REJ).
                        src_bytes=int(row['src_bytes']),  # Number of bytes sent from the source.
                        dst_bytes=int(row['dst_bytes']),  # Number of bytes sent to the destination.
                        land=bool(int(row['land'])),  # Boolean indicating if the source and destination are the same.
                        wrong_fragment=int(row['wrong_fragment']),  # Count of wrong fragments in the session.
                        urgent=int(row['urgent']),  # Number of urgent packets in the session.
                        hot=int(row['hot']),  # Number of "hot" indicators (suspicious activities).
                        logged_in=bool(int(row['logged_in'])),  # Boolean indicating if the session was logged in.
                        num_compromised=int(row['num_compromised']),  # Number of compromised conditions observed.
                        count=int(row['count']),  # Number of connections to the same host as the current session.
                        srv_count=int(row['srv_count']),  # Number of connections to the same service as the current session.
                        serror_rate=float(row['serror_rate']),  # Percentage of connections with SYN errors.
                        rerror_rate=float(row['rerror_rate']),  # Percentage of connections with REJ errors.
                        same_srv_rate=float(row['same_srv_rate']),  # Percentage of connections to the same service.
                        diff_srv_rate=float(row['diff_srv_rate']),  # Percentage of connections to different services.
                        srv_diff_host_rate=float(row['srv_diff_host_rate']),  # Percentage of connections to different hosts.
                        dst_host_count=int(row['dst_host_count']),  # Number of connections to the same destination host.
                        dst_host_srv_count=int(row['dst_host_srv_count']),  # Number of connections to the same service at the destination host.
                        dst_host_same_srv_rate=float(row['dst_host_same_srv_rate']),  # Percentage of same-service connections to the destination host.
                        dst_host_diff_srv_rate=float(row['dst_host_diff_srv_rate']),  # Percentage of different-service connections to the destination host.
                        attack=row['attack'].strip().lower() == 'yes',  # Boolean indicating if this session is an attack.
                    )
                    rows += 1

            # Print success message to console, showing number of rows processed.
            self.stdout.write(self.style.SUCCESS(f"Successfully loaded {rows} rows into the database."))

        # Handle case where the specified file cannot be found.
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File {csv_file} not found."))
        # Catch any other exceptions that might occur and display the error message.
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {str(e)}"))
