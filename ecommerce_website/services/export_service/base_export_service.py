import xml.etree.ElementTree as ET
from io import BytesIO
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

    def export_to_google_merchant_xml(self):
        self.log_start()
        data = self.get_data()

        # Google Merchant XML namespace
        NS = "http://base.google.com/ns/1.0"
        ET.register_namespace('', NS)

        rss = ET.Element("rss", version="2.0", attrib={"xmlns:g": NS})
        channel = ET.SubElement(rss, "channel")

        # Required channel info
        ET.SubElement(channel, "title").text = "Goedkoopstevloerenshop.nl"
        ET.SubElement(
            channel, "link").text = "https://goedkoopstevloerenshop.nl"
        ET.SubElement(
            channel, "description").text = "Product feed for Google Merchant"

        for record in data:
            item = ET.SubElement(channel, "item")
            # Map Google Merchant fields (make sure your records use correct keys or map accordingly)

            def add_g_tag(tag, text):
                if text:
                    ET.SubElement(item, f"{{{NS}}}{tag}").text = str(text)

            add_g_tag("id", record.get("id"))
            add_g_tag("title", record.get("title"))
            add_g_tag("description", record.get("description"))
            add_g_tag("link", record.get("link"))
            add_g_tag("image_link", record.get("image link"))
            add_g_tag("availability", record.get("availability"))
            add_g_tag("price", record.get("price"))
            add_g_tag("sale_price", record.get("sale price"))
            add_g_tag("identifier_exists", record.get("identifier exists"))
            add_g_tag("gtin", record.get("gtin"))
            add_g_tag("mpn", record.get("mpn"))
            add_g_tag("brand", record.get("brand"))
            add_g_tag("condition", record.get("condition"))
            add_g_tag("color", record.get("color"))
            add_g_tag("size", record.get("size"))
            add_g_tag("gender", record.get("gender"))
            add_g_tag("material", record.get("material"))
            add_g_tag("pattern", record.get("pattern"))
            add_g_tag("age_group", record.get("age group"))
            add_g_tag("multipack", record.get("multipack"))
            add_g_tag("is_bundle", record.get("is bundle"))
            add_g_tag("unit_pricing_measure",
                      record.get("unit pricing measure"))
            add_g_tag("unit_pricing_base_measure",
                      record.get("unit pricing base measure"))
            add_g_tag("energy_efficiency_class",
                      record.get("energy efficiency class"))
            add_g_tag("min_energy_efficiency_class",
                      record.get("min energy efficiency class"))
            add_g_tag("max_energy_efficiency_class",
                      record.get("max energy efficiency class"))
            add_g_tag("item_group_id", record.get("item group id"))
            add_g_tag("sell_on_google_quantity",
                      record.get("sell on google quantity"))

        tree = ET.ElementTree(rss)
        output = BytesIO()
        tree.write(output, encoding="utf-8", xml_declaration=True)
        output.seek(0)

        self.log_finish()
        return output.getvalue()

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
            return self.export_to_google_merchant_xml()
        else:
            raise ValueError(f"Unsupported file format: {file_format}")
