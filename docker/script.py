# script.py
import os
from collections import Counter
import subprocess

def list_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.txt')]

def count_words_in_file(filepath):
    with open(filepath, 'r') as file:
        words = file.read().split()
    return len(words)

def top_three_words(filepath):
    with open(filepath, 'r') as file:
        words = file.read().split()
    counter = Counter(words)
    return counter.most_common(3)

def main():
    directory = "/home/data"
    output_directory = "/home/output"
    os.makedirs(output_directory, exist_ok=True)
    output_file = os.path.join(output_directory, "result.txt")
    
    files = list_files(directory)
    total_words = 0
    with open(output_file, 'w') as out:
        out.write(f"List of text files in /home/data: {', '.join(files)}\n")
        for file in files:
            filepath = os.path.join(directory, file)
            word_count = count_words_in_file(filepath)
            out.write(f"Total words in {file}: {word_count}\n")
            total_words += word_count
        out.write(f"Grand total of words in both the files: {total_words}\n")
        top_words = top_three_words(os.path.join(directory, "IF.txt"))
        for word, count in top_words:
            out.write(f"Top word in IF.txt: {word}, its count: {count}\n")
        result = subprocess.check_output(['hostname', '-I'])
        ip_address = result.decode('utf-8').strip()
        out.write(f"IP Address of the machine: {ip_address}\n")
    
    # Print the content of the /home/data/result.txt
    with open(output_file, 'r') as result:
        print(result.read())

if __name__ == "__main__":
    main()
