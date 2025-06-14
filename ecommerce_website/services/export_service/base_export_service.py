import logging
from io import StringIO, BytesIO
import csv
import json
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

# Setting up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseExportService:
    def __init__(self, queryset=None, batch_size=50):
        """
        Initializes the export service with a queryset and an optional batch size for logging progress.
        """
        self.queryset = queryset
        self.total_records = queryset.count() if queryset else 0
        self.processed_records = 0  # Track processed records
        self.batch_size = batch_size  # Define the batch size for logging progress

    def log_progress(self):
        """
        Logs progress based on the number of records processed.
        Logs progress every 'batch_size' records.
        """
        self.processed_records += 1
        if self.processed_records % self.batch_size == 0 or self.processed_records == self.total_records:
            logger.info(f"Processed {self.processed_records} of {
                        self.total_records} records.")

    def log_start(self):
        """
        Logs when the export process starts.
        """
        logger.info(f"Export started for {self.total_records} records.")

    def log_finish(self):
        """
        Logs when the export process finishes.
        """
        logger.info(f"Export finished. Total records processed: {
                    self.processed_records}.")

    def process_record(self, record):
        """
        This method is called for each individual record. It should be implemented in subclasses to
        retrieve the data for that specific record.
        """
        raise NotImplementedError(
            "The 'process_record' method must be implemented in subclasses")

    def get_data(self):
        """
        Retrieves the data by processing each record individually and logging the progress after each batch.
        """
        data = []
        for record in self.queryset:
            # Process each record individually and log the progress
            record_data = self.process_record(record)
            data.append(record_data)
            self.log_progress()  # Log progress after each record is processed
        return data

    def export_to_csv(self):
        """
        Export the data to CSV format.
        """
        self.log_start()  # Log start of export process
        data = self.get_data()

        output = StringIO()
        # Use newline='' and disable extrasaction
        writer = csv.DictWriter(output, fieldnames=data[0].keys())

        # Write the header once
        writer.writeheader()

        # Write the rows without any blank lines after each row
        for record in data:
            writer.writerow(record)

        # Use the getvalue() method of StringIO to return the CSV content
        self.log_finish()  # Log end of export process
        return output.getvalue().strip()  # Strip any leading/trailing newlines

    def export_to_json(self):
        """
        Export the data to JSON format.
        """
        self.log_start()  # Log start of export process
        data = self.get_data()
        self.log_finish()  # Log end of export process
        return json.dumps(data, indent=4)

    def export_to_excel(self):
        """
        Export the data to Excel format.
        """
        self.log_start()  # Log start of export process
        data = self.get_data()

        # Create a new Excel workbook and sheet
        wb = Workbook()
        sheet = wb.active
        sheet.title = "Product Data"

        # Use the keys of the first item in the data to create headers
        headers = list(data[0].keys())  # Convert dict_keys to list
        sheet.append(headers)

        # Append the data rows
        for record in data:
            # Convert the dictionary values to a list
            sheet.append(list(record.values()))

        # Save the Excel file to a BytesIO object
        excel_output = BytesIO()
        wb.save(excel_output)
        excel_output.seek(0)

        self.log_finish()  # Log end of export process

        # Return the Excel file as bytes
        return excel_output.getvalue()

    def export_to_google_merchant_excel(self):
        """
        Export the data in Google Merchant-compatible Excel format.
        """

        self.log_start()
        data = self.get_data()

        # Define Google Merchant headers
        headers = [
            "id", "title", "description", "availability", "link", "image link",
            "price", "sale price", "identifier exists", "gtin", "mpn", "brand", "product detail",
            "condition", "color", "size", "gender", "material", "pattern", "age group",
            "multipack", "is bundle", "unit pricing measure", "unit pricing base measure",
            "energy efficiency class", "min energy efficiency class", "max energy efficiency class",
            "item group id", "sell on google quantity"
        ]

        # Create workbook
        wb = Workbook()
        sheet = wb.active
        sheet.title = "Merchant Products"

        # Write header with bold styling
        sheet.append(headers)
        for col_num, _ in enumerate(headers, 1):
            col_letter = get_column_letter(col_num)
            sheet[f"{col_letter}1"].font = Font(bold=True)

        # Expect `process_record()` to return dictionary matching above fields
        for record in data:
            row = [record.get(header, "") for header in headers]
            sheet.append(row)

        # Save to BytesIO
        excel_output = BytesIO()
        wb.save(excel_output)
        excel_output.seek(0)

        self.log_finish()
        return excel_output.getvalue()

    def export(self, file_format="csv"):
        """
        Export the data in the requested file format (CSV, JSON, or Excel).
        """
        if file_format == "csv":
            return self.export_to_csv()
        elif file_format == "json":
            return self.export_to_json()
        elif file_format == "excel":
            return self.export_to_excel()
        elif file_format == "google":
            return self.export_to_google_merchant_excel()
        else:
            raise ValueError(f"Unsupported file format: {file_format}")
