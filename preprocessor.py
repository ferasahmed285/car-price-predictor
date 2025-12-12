##it allows 0 engine volume??
import csv
import os
import re

def clean_dataset(input_file):
    """
    Reads input, sorts by ID, applies strict formatting,
    and removes rows with non-English/non-digit characters 
    (except strictly necessary formatting like . - > and space).
    """
    base_name, _ = os.path.splitext(input_file)
    output_file = f"{base_name}_cleaned.csv"

    print(f"  > Preprocessing: {input_file}...")

    # Regex: Allow A-Z, a-z, 0-9, space, dot, hyphen, greater-than.
    # Anchors ^ and $ ensure the WHOLE string matches this.
    # If a string contains '?', '!', '@', or non-ascii, it fails.
    VALID_PATTERN = re.compile(r'^[a-zA-Z0-9\s\.\-\>]*$')

    try:
        with open(input_file, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            
            valid_rows = []
            seen_ids = set()
            rows_dropped_empty = 0
            rows_dropped_chars = 0
            
            for row in reader:
                # --- 1. Clean & Format ---
                
                # ID
                row_id = row['ID'].strip()
                if row_id in seen_ids:
                    continue 

                # Levy: Digits only
                levy_raw = row['Levy'].replace(',', '').strip()
                if levy_raw.isdigit():
                    levy_clean = levy_raw
                else:
                    levy_clean = "" 

                # Doors: 4-5, 2-3, >5
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

                # Engine: 2.0 T
                engine_raw = row['Engine volume'].strip()
                if 'Turbo' in engine_raw:
                    parts = engine_raw.split()
                    engine_clean = f"{parts[0]} T" if parts else ""
                else:
                    engine_clean = engine_raw

                # Mileage: Digits only
                mileage_clean = row['Mileage'].lower().replace('km', '').strip()

                # --- 2. Construct Candidate ---
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
                    'Airbags': row['Airbags'].strip(),
                    'Price': row['Price'].strip()
                }

                # --- 3. Strict Filters ---

                # Filter A: Empty Values
                if any(value == "" for value in candidate_row.values()):
                    rows_dropped_empty += 1
                    continue 

                # Filter B: Illegal Characters (English/Digits Check)
                # We check every single value in the row against the regex.
                has_invalid_char = False
                for value in candidate_row.values():
                    if not VALID_PATTERN.match(value):
                        has_invalid_char = True
                        break # Stop checking this row, it's already bad
                
                if has_invalid_char:
                    rows_dropped_chars += 1
                    continue

                # --- 4. Keep Valid Row ---
                seen_ids.add(row_id)
                valid_rows.append(candidate_row)

        # --- 5. Sort by ID ---
        try:
            valid_rows.sort(key=lambda x: int(x['ID']))
        except ValueError:
            valid_rows.sort(key=lambda x: x['ID'])

        # --- 6. Write to File ---
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            fieldnames = [
                'ID', 'Levy', 'Manufacturer', 'Model', 'Prod. year', 'Category', 
                'Leather interior', 'Fuel type', 'Engine volume', 'Mileage', 
                'Cylinders', 'Gear box type', 'Drive wheels', 'Doors', 'Wheel', 
                'Color', 'Airbags', 'Price'
            ]
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(valid_rows)

        print(f"    - Saved to: {output_file}")
        print(f"    - Valid rows: {len(valid_rows)}")
        print(f"    - Dropped (Empty values): {rows_dropped_empty}")
        print(f"    - Dropped (Bad characters): {rows_dropped_chars}")
        return output_file

    except FileNotFoundError:
        print(f"    ! Error: {input_file} not found.")
        return None
    except Exception as e:
        print(f"    ! Error: {e}")
        return None