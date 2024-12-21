from django.core.management.base import BaseCommand
import importlib
import os
import sys


class Command(BaseCommand):
    help = 'Seed product data and run refactor scripts'

    def handle(self, *args, **options):
        while True:
            self.stdout.write(self.style.SUCCESS(
                'Available Refactor Scripts:'))

            # Discover all refactor scripts in the db_refactor directory
            refactor_scripts = self.get_refactor_scripts()
            for idx, script in enumerate(refactor_scripts, start=1):
                self.stdout.write(f'{idx}. {script}')

            self.stdout.write('0. Exit')
            choice = input(
                'Select a script to run (1-{}, 0 to exit): '.format(len(refactor_scripts)))

            if choice == '0':
                self.stdout.write(self.style.SUCCESS('Exiting...'))
                sys.exit()

            try:
                script_index = int(choice) - 1
                if 0 <= script_index < len(refactor_scripts):
                    script_name = refactor_scripts[script_index]
                    self.run_refactor_script(script_name)
                else:
                    self.stdout.write(self.style.ERROR(
                        'Invalid choice, please try again.'))
            except ValueError:
                self.stdout.write(self.style.ERROR(
                    'Invalid input, please enter a number.'))

    def get_refactor_scripts(self):
        # Get all Python files in the db_refactor directory
        refactor_dir = os.path.join(os.path.dirname(__file__), 'db_refactor')
        scripts = [
            f[:-3] for f in os.listdir(refactor_dir) if f.endswith('.py') and f != '__init__.py']
        return scripts

    def run_refactor_script(self, script_name):
        # Dynamically import and run the refactor script
        module_path = f'ecommerce_website.management.commands.db_refactor.{
            script_name}'
        try:
            module = importlib.import_module(module_path)

            # List all available functions in the module
            available_functions = [func for func in dir(module) if callable(
                getattr(module, func)) and not func.startswith("__")]

            self.stdout.write(self.style.SUCCESS(f'Available functions in {
                script_name}: {available_functions}'))

            # Define the list of refactor methods
            refactor_methods = [
                'add_product_attribute_to_product',
                'refactor_product_attributes_for_all_products',
                'refactor_product_filters_for_all_products',
                'refactor_product_attributes_to_numeric_values',
                'deliver_return_order_lines', 'deliver_order_lines',
                'update_vat', 'update_selling_percentage', 'update_prices_for_peitsman'
            ]

            # Execute each refactor method that exists in available functions
            for method_name in refactor_methods:
                if method_name in available_functions:
                    print(f'Executing method: {method_name}')
                    getattr(module, method_name)()
                    print(f'Successfully ran {method_name}.')
                else:
                    print(f'Method {method_name} not found in {script_name}.')

        except ImportError as e:
            self.stdout.write(self.style.ERROR(
                f'Error importing {script_name}: {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Error running {script_name}: {str(e)}'))
