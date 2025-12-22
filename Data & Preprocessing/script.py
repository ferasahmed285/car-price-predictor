import preprocessor

FILES_TO_CLEAN = ['train_data.csv', 'test_data.csv']

def main():
    print("=== Starting Project Pipeline ===\n")
    print("--- Phase 1: Data Cleaning ---")
    
    cleaned_files = []
    for file_name in FILES_TO_CLEAN:
        result_file = preprocessor.clean_dataset(file_name)
        if result_file:
            cleaned_files.append(result_file)
            
    print("\nCleaning finished.")
    print(f"Cleaned files available: {cleaned_files}")
    print("\n=== Pipeline Execution Complete ===")

if __name__ == "__main__":
    main()