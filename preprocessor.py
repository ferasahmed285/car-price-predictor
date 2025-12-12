##check levy and 0 volume
import csv
import os
import re

def clean_dataset(input_file):
    """
    Reads input, validates strict rules, and outputs:
    1. [name]_cleaned.csv (Valid data)
    2. [name]_rejected.csv (Rejected rows WITH a 'RejectionReason' column)
    """
    base_name, _ = os.path.splitext(input_file)
    output_clean = f"{base_name}_cleaned.csv"
    output_reject = f"{base_name}_rejected.csv"

    print(f"  > Preprocessing: {input_file}...")

    # Regex: Allow A-Z, a-z, 0-9, space, dot, hyphen, greater-than.
    VALID_PATTERN = re.compile(r'^[a-zA-Z0-9\s\.\-\>]*$')

    try:
        with open(input_file, mode='r', encoding='utf-8') as infile, \
             open(output_clean, mode='w', newline='', encoding='utf-8') as clean_file, \
             open(output_reject, mode='w', newline='', encoding='utf-8') as reject_file:
            
            reader = csv.DictReader(infile)
            
            # --- Setup Clean Writer ---
            clean_headers = [
                'ID', 'Levy', 'Manufacturer', 'Model', 'Prod. year', 'Category', 
                'Leather interior', 'Fuel type', 'Engine volume', 'Mileage', 
                'Cylinders', 'Gear box type', 'Drive wheels', 'Doors', 'Wheel', 
                'Color', 'Airbags', 'Price'
            ]
            writer_clean = csv.DictWriter(clean_file, fieldnames=clean_headers)
            writer_clean.writeheader()

            # --- Setup Reject Writer ---
            # We take the original headers and append 'RejectionReason'
            if reader.fieldnames:
                reject_headers = reader.fieldnames + ['RejectionReason']
            else:
                reject_headers = ['RejectionReason'] # Fallback if empty file
            
            writer_reject = csv.DictWriter(reject_file, fieldnames=reject_headers)
            writer_reject.writeheader()
            
            valid_rows = []
            seen_ids = set()
            
            count_total = 0
            count_rejected = 0
            
            for row in reader:
                count_total += 1
                rejection_reason = None # Reset reason
                
                # ---------------------------
                # A. ID & Deduplication Check
                # ---------------------------
                try:
                    # Strict Integer Check
                    id_val = int(float(row['ID'].strip()))
                    row_id = str(id_val)
                except ValueError:
                    rejection_reason = "Invalid ID format (not an integer)"
                    
                # Only check duplicate if ID format was valid
                if not rejection_reason:
                    if row_id in seen_ids:
                        rejection_reason = "Duplicate ID"

                # If failed ID checks, write immediately
                if rejection_reason:
                    row['RejectionReason'] = rejection_reason
                    writer_reject.writerow(row)
                    count_rejected += 1
                    continue

                # ---------------------------
                # B. Data Cleaning
                # ---------------------------
                
                # Levy
                levy_input = row['Levy'].strip()
                if levy_input == '-':
                    levy_clean = '0'
                else:
                    levy_temp = levy_input.replace(',', '')
                    if levy_temp.isdigit():
                        levy_clean = levy_temp
                    else:
                        levy_clean = "" # Invalid

                # Doors
                doors_raw = row['Doors'].strip()
                doors_lower = doors_raw.lower()
                if 'may' in doors_lower:
                    doors_clean = '4-5'
                elif 'mar' in doors_lower:
                    doors_clean = '2-3'
                elif '>5' in doors_raw:
                    doors_clean = '>5'
                else:
                    doors_clean = doors_raw

                # Engine
                engine_raw = row['Engine volume'].strip()
                if 'Turbo' in engine_raw:
                    parts = engine_raw.split()
                    engine_clean = f"{parts[0]} T" if parts else ""
                else:
                    engine_clean = engine_raw

                # Mileage
                mileage_clean = row['Mileage'].lower().replace('km', '').strip()

                # Airbags
                try:
                    airbags_val = int(float(row['Airbags'].strip()))
                    airbags_clean = str(airbags_val)
                except ValueError:
                    airbags_clean = "" # Invalid

                # Construct Candidate
                candidate_row = {
                    'ID': row_id,
                    'Levy': levy_clean,
                    'Manufacturer': row['Manufacturer'].strip(),
                    'Model': row['Model'].strip(),
                    'Prod. year': row['Prod. year'].strip(),
                    'Category': row['Category'].strip(),
                    'Leather interior': row['Leather interior'].strip(),
                    'Fuel type': row['Fuel type'].strip(),
                    'Engine volume': engine_clean,
                    'Mileage': mileage_clean,
                    'Cylinders': row['Cylinders'].strip(),
                    'Gear box type': row['Gear box type'].strip(),
                    'Drive wheels': row['Drive wheels'].strip(),
                    'Doors': doors_clean,
                    'Wheel': row['Wheel'].strip(),
                    'Color': row['Color'].strip(),
                    'Airbags': airbags_clean,
                    'Price': row['Price'].strip()
                }

                # ---------------------------
                # C. Validation Loop
                # ---------------------------
                # We check every column to find the FIRST error
                
                for key, value in candidate_row.items():
                    # Check 1: Empty Values
                    if value == "":
                        rejection_reason = f"Invalid or Empty value in '{key}'"
                        break
                    
                    # Check 2: Invalid Characters
                    if not VALID_PATTERN.match(value):
                        rejection_reason = f"Illegal characters in '{key}'"
                        break
                
                # ---------------------------
                # D. Final Decision
                # ---------------------------
                if rejection_reason:
                    # Write to rejected file with reason
                    row['RejectionReason'] = rejection_reason
                    writer_reject.writerow(row)
                    count_rejected += 1
                else:
                    # Valid! Add to list
                    seen_ids.add(row_id)
                    valid_rows.append(candidate_row)

            # ---------------------------
            # E. Sort & Save Valid Data
            # ---------------------------
            valid_rows.sort(key=lambda x: int(x['ID']))
            writer_clean.writerows(valid_rows)

        print(f"    - Cleaned File:  {output_clean}")
        print(f"    - Rejected File: {output_reject}")
        print(f"    - Stats: {len(valid_rows)} Valid | {count_rejected} Rejected")
        return output_clean

    except FileNotFoundError:
        print(f"    ! Error: {input_file} not found.")
        return None
    except Exception as e:
        print(f"    ! Error: {e}")
        return None