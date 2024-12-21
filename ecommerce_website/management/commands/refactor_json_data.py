from django.core.management.base import BaseCommand
import importlib
import os
import sys


class Command(BaseCommand):
    help = 'Run the multiply_price_data script to update product prices'

    def handle(self, *args, **options):
        while True:
            self.stdout.write(self.style.SUCCESS(
                'Available Refactor Script:'))

            # Get the refactor script (specifically looking for 'multiply_price_data.py')
            refactor_script = self.get_refactor_scripts()

            # Display the script choice
            for idx, script in enumerate(refactor_script, start=1):
                self.stdout.write(f'{idx}. {script}')

            self.stdout.write('0. Exit')
            choice = input(
                'Select the script to run (1-{}, 0 to exit): '.format(len(refactor_script)))

            if choice == '0':
                self.stdout.write(self.style.SUCCESS('Exiting...'))
                sys.exit()

            try:
                script_index = int(choice) - 1
                if 0 <= script_index < len(refactor_script):
                    script_name = refactor_script[script_index]
                    self.run_refactor_script(script_name)
                else:
                    self.stdout.write(self.style.ERROR(
                        'Invalid choice, please try again.'))
            except ValueError:
                self.stdout.write(self.style.ERROR(
                    'Invalid input, please enter a number.'))

    def get_refactor_scripts(self):
        # Get all Python files in the import_data_refactor directory
        refactor_dir = os.path.join(
            os.path.dirname(__file__), 'import_data_refactor')
        scripts = [
            f[:-3] for f in os.listdir(refactor_dir) if f.endswith('.py') and f != '__init__.py']
        return scripts

    def run_refactor_script(self, script_name):
        # Dynamically import and run the refactor script
        module_path = f'ecommerce_website.management.commands.import_data_refactor.{
            script_name}'
        try:
            module = importlib.import_module(module_path)

            # List all available functions in the module
            available_functions = [func for func in dir(module) if callable(
                getattr(module, func)) and not func.startswith("__")]

            self.stdout.write(self.style.SUCCESS(f'Available functions in {
                              script_name}: {available_functions}'))

            # Execute the update_prices_in_json method if available
            if 'update_prices_in_json' in available_functions:
                print(f'Executing method: update_prices_in_json')
                # Call the method with the necessary arguments (adjust as needed)

                # Correct the path to your JSON file using os.path.join
                base_dir = os.path.dirname(
                    os.path.dirname(os.path.dirname(__file__)))
                file_path = os.path.join(
                    base_dir, 'db_mapper', 'data', 'final_data', 'finalized_combined.json')

                # Ensure the file exists
                if not os.path.exists(file_path):
                    self.stdout.write(self.style.ERROR(
                        f"File not found: {file_path}"))
                    return

                # Specify the multiplier for price updates
                multiplier = 0.475  # Specify the multiplier you need
                getattr(module, 'update_prices_in_json')(file_path, multiplier)
                print(f'Successfully ran update_prices_in_json.')
            else:
                print(f'Method update_prices_in_json not found in {
                      script_name}.')

        except ImportError as e:
            self.stdout.write(self.style.ERROR(
                f'Error importing {script_name}: {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Error running {script_name}: {str(e)}'))
