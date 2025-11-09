# Data Processing Utility
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

"""
type safety, documentation, error-handling
1. Type hinting and safety
2. Docstrings
3. Defined exceptions
4. logic in clean_data looks verbose
5. check if processed data is empty
6. Exceptions should not be simple print statements
7. __name__==__main__
8. Do we need the loading methods?
9. may be some means of filtering and aggregate being combined
"""

class DataProcessor:
    def __init__(self):
        self.data = []
        self.processed_data = []
    
    def load_csv_data(self, filename, encoding: str = 'utf-8', append: bool = False, delimiter: str = ',',
                  max_rows: Optional[int] = None):
        """Load data from csv path provided by filename."""
        if not filename or not isinstance(filename, str):
            raise ValueError("Filename must be non-empty string")
        
        file_path = Path(filename)
        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {filename}")
        
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {filename}")

        try:
            with open(filename, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.data.append(row)
            print(f"Loaded {len(self.data)} records from {filename}")
        except UnicodeDecodeError:
            """add some logic to handle this error"""
            pass
        
        if not append:
            self.data = []

        records_loaded = 0

        try:
            encodings = [encoding]
            if encoding != 'utf-8':
                encodings.extend(['utf-8', 'latin-1', 'cp1252'])

            csv_data = None
            successful_encoding = None

            for enc in encodings:
                try:
                    with open(file_path, 'r', encoding=enc, newline='') as file:
                        # Detect if file has headers
                        sample = file.read(1024)
                        file.seek(0)
                        
                        # Create CSV reader with specified delimiter
                        reader = csv.DictReader(file, delimiter=delimiter)
                        
                        # Validate that we have headers
                        if not reader.fieldnames:
                            raise ValueError("CSV file has no headers or is invalid")
                    
                        # Load data with optional row limit
                        for row_num, row in enumerate(reader, 1):
                            if max_rows and row_num > max_rows:
                                break
                            
                            # Skip empty rows
                            if not any(value.strip() for value in row.values() if value):
                                continue
                            
                            self.data.append(row)
                            records_loaded += 1
                            
                            # Progress feedback for large files
                            if records_loaded % 10000 == 0:
                                print(f"Loaded {records_loaded} records...")

                        successful_encoding = enc
                        break
                        
                except UnicodeDecodeError:
                    if enc == encodings[-1]:  # Last encoding failed
                        raise UnicodeDecodeError(
                            f"Could not decode file with any of these encodings: {encodings}"
                        )
                    continue
            
            if successful_encoding != encoding:
                logging.warning(f"File loaded with {successful_encoding} encoding instead of {encoding}")
            
            print(f"Successfully loaded {records_loaded} records from {filename}")
            return records_loaded
            
        except PermissionError:
            raise PermissionError(f"Permission denied accessing file: {filename}")
        
        except csv.Error as e:
            raise ValueError(f"CSV parsing error in {filename}: {str(e)}")
        
        except Exception as e:
            raise RuntimeError(f"Unexpected error loading {filename}: {str(e)}")

    
    def load_json_data(self, filename: str) -> None:
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    self.data.extend(data)
                else:
                    self.data.append(data)
            print(f"Loaded data from {filename}")
        except:
            print("Error loading JSON file")
    
    def clean_data(self):
        cleaned_data = []
        for record in self.data:
            cleaned_record = {}
            for key, value in record.items():
                # Remove leading/trailing whitespace
                if isinstance(value, str):
                    cleaned_value = value.strip()
                else:
                    cleaned_value = value
                
                # Convert empty strings to None
                if cleaned_value == "":
                    cleaned_value = None
                
                # Convert numeric strings to numbers
                if isinstance(cleaned_value, str):
                    if cleaned_value.isdigit():
                        cleaned_value = int(cleaned_value)
                    else:
                        try:
                            cleaned_value = float(cleaned_value)
                        except:
                            pass
                
                cleaned_record[key] = cleaned_value
            
            cleaned_data.append(cleaned_record)
        
        self.processed_data = cleaned_data
        print(f"Cleaned {len(self.processed_data)} records")
    
    def filter_data(self, field: str, value: str) -> list[dict]:
        if not isinstance(field, str) or not field.strip():
            raise ValueError(f"Input field not compatible.")
        
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Input value not compatable")
        
        filtered_data = []
        for record in self.processed_data:
            if record.get(field, None) == value:
                filtered_data.append(record)
        return filtered_data
    
    def sort_data(self, field, reverse=False):
        try:
            self.processed_data = sorted(self.processed_data, key=lambda x: x.get(field, 0), reverse=reverse)
            print(f"Data sorted by {field}")
        except:
            print("Error sorting data")
    
    def aggregate_data(self, group_field, agg_field, operation):
        if not self.processed_data:
            raise ValueError("Processed data must be non-empty array.")
        
        valid_operations = {'sum', 'avg', 'count', 'max', 'min'}
        if operation not in valid_operations:
            raise ValueError(f"Invalid operation '{operation}'. Must be one of: {valid_operations}")
        # Single-pass aggregation using defaultdict for efficiency
        if operation == 'count':
            # For count, we don't need to store values, just increment counters
            groups = defaultdict(int)
            for record in self.processed_data:
                group_key = record.get(group_field)
                if group_key is not None:
                    groups[group_key] += 1
            return dict(groups)
        
        elif operation in {'sum', 'avg'}:
            # For sum/avg, track both sum and count to avoid multiple iterations
            groups = defaultdict(lambda: {'sum': 0, 'count': 0})
            for record in self.processed_data:
                group_key = record.get(group_field)
                agg_value = record.get(agg_field)
                
                if group_key is not None and agg_value is not None and isinstance(agg_value, (int, float)):
                    groups[group_key]['sum'] += agg_value
                    groups[group_key]['count'] += 1
            
            if operation == 'sum':
                return {k: v['sum'] for k, v in groups.items()}
            else:  # avg
                return {k: v['sum'] / v['count'] if v['count'] > 0 else 0 for k, v in groups.items()}
        
        elif operation in {'max', 'min'}:
            # For min/max, use single-pass tracking
            groups = {}
            for record in self.processed_data:
                group_key = record.get(group_field)
                agg_value = record.get(agg_field)
                
                if group_key is not None and agg_value is not None and isinstance(agg_value, (int, float)):
                    if group_key not in groups:
                        groups[group_key] = agg_value
                    else:
                        if operation == 'max':
                            groups[group_key] = max(groups[group_key], agg_value)
                        else:  # min
                            groups[group_key] = min(groups[group_key], agg_value)
            
            return groups
    
    def export_to_csv(self, filename):
        try:
            if len(self.processed_data) > 0:
                fieldnames = self.processed_data[0].keys()
                with open(filename, 'w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    for record in self.processed_data:
                        writer.writerow(record)
                print(f"Data exported to {filename}")
            else:
                print("No data to export")
        except:
            print("Error exporting to CSV")
    
    def export_to_json(self, filename):
        try:
            with open(filename, 'w') as file:
                json.dump(self.processed_data, file, indent=2)
            print(f"Data exported to {filename}")
        except:
            print("Error exporting to JSON")
    
    def get_summary_stats(self, field):
        values = []
        for record in self.processed_data:
            value = record.get(field)
            if value is not None and isinstance(value, (int, float)):
                values.append(value)
        
        if len(values) == 0:
            return None
        
        stats = {
            'count': len(values),
            'sum': sum(values),
            'avg': sum(values) / len(values),
            'min': min(values),
            'max': max(values)
        }
        
        return stats
    
    def find_duplicates(self, field):
        seen = {}
        duplicates = []
        
        for i, record in enumerate(self.processed_data):
            value = record.get(field)
            if value in seen:
                duplicates.append({'index': i, 'value': value, 'record': record})
            else:
                seen[value] = i
        
        return duplicates


if __name__ == '__main__':
    # Example usage
    processor = DataProcessor()

    # Sample data for testing
    sample_data = [
        {'name': 'John Doe', 'age': '25', 'salary': '50000', 'department': 'Engineering'},
        {'name': 'Jane Smith', 'age': '30', 'salary': '60000', 'department': 'Marketing'},
        {'name': 'Bob Johnson', 'age': '35', 'salary': '55000', 'department': 'Engineering'},
        {'name': ' Alice Brown ', 'age': '28', 'salary': '52000', 'department': 'Marketing'}
    ]

    processor.data = sample_data
    processor.clean_data()

    # Aggregate salaries by department
    dept_salaries = processor.aggregate_data('department', 'salary', 'avg')
    print("Average salaries by department:", dept_salaries)