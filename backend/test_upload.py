from file_processor import FileProcessor

fp = FileProcessor()
with open('test_data.txt', 'rb') as f:
    result = fp.process_file(f.read(), 'txt')
    print(f"Success: {len(result)} parameters found")
    print(result)