# -*- coding: utf-8 -*-
"""CodeObfuscationStrengthMeasurement.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AMsaK5kmRpxZ3-92X8NteIPznLljw9rd

Flowchart Similarity -- > Semantic Similarity
1. Uno Board
2. RPi 4.0
3. ESP 32
"""

#flowchart_a is original
#flowchart_b is reverse engineered
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union else 0.0

def compare_flowcharts(flowchart1, flowchart2):
    description1 = " ".join(flowchart1.values())
    description2 = " ".join(flowchart2.values())

    tokens1 = set(description1.lower().split())
    tokens2 = set(description2.lower().split())

    return jaccard_similarity(tokens1, tokens2)

# Example usage:
flowchart_a = {
    "start": "Start Main Program",
    "step1": "SET GPIO mode BCM",
    "step2": "SET GPIO_TRIGGER 18 as output",
    "step3": "Set GPIO_echo 24 as Input",
    "step4": "Measure distance in loop",
    "step5": "Set trigger pin high",
    "step6": "Set trigger pin low after 0.01ms",
    "step7": "save start time when echo pin goes low",
    "step8": "calculate distance using the formula Time Elapsed * 34300/2",
    "step9": "Display measured distance",
    "step10": "End program",
    "end": "End process"
}

flowchart_b = {
    "start": "Start system initialization",
    "step1": "Initialize signal variables",
    "step2": "Set final output B",
    "step3": "Start interrupt handler",
    "step4": "Read signal value and check signal thresthold",
    "step5": "Set led_state 1 on",
    "step6": "measure start time using micros",
    "step7": "Measure elapsed time",
    "step8": "Reset LED blink delay to 1000 microseconds",
    "step9": "Compare signal with signal threasthold",
    "step10": "Call seria0_available function",
    "end": "Finish"
}

similarity_score = compare_flowcharts(flowchart_a, flowchart_b)
print(f"Flowchart similarity: {similarity_score}")

"""Semantic Similarity"""

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

sentence1 = "End program"
sentence2 = "Call serial_available function"

embedding1 = model.encode(sentence1, convert_to_tensor=True)
embedding2 = model.encode(sentence2, convert_to_tensor=True)

similarity = util.pytorch_cos_sim(embedding1, embedding2)
print(f"Similarity: {similarity.item()}")

"""Binary Similarity


"""

def compare_hex_files(file1_path, file2_path):
    with open(file1_path, 'rb') as file1, open(file2_path, 'rb') as file2:
        data1 = file1.read()
        data2 = file2.read()

    if data1 == data2:
        print("The HEX files are identical.")
    else:
        print("The HEX files are different.")
        min_len = min(len(data1), len(data2))
        for i in range(min_len):
            if data1[i] != data2[i]:
                print(f"Difference at byte {i}: {data1[i]:02X} != {data2[i]:02X}")

        if len(data1) != len(data2):
            print(f"Files have different lengths: {len(data1)} != {len(data2)}")

# Example usage
compare_hex_files('/content/Arduino original.hex', '/content/Arduino reverse eng.hex')

def compare_hex_files(file1_path, file2_path, max_differences=10):
    differences = []
    line_number = 0

    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        while True:
            line1 = file1.readline()
            line2 = file2.readline()
            if not line1 and not line2:
                # End of both files
                break

            line_number += 1
            line1 = line1.strip()
            line2 = line2.strip()

            if line1 != line2:
                differences.append((line_number, line1, line2))
                if len(differences) >= max_differences:
                    break

    if not differences:
        print("✅ The HEX files are identical.")
    else:
        print(f"❌ Files are different! Showing first {len(differences)} differences:\n")
        for diff in differences:
            ln, l1, l2 = diff
            print(f"Line {ln}:")
            print(f"  File1: {l1}")
            print(f"  File2: {l2}\n")

        # Check if there are more differences
        total_lines = sum(1 for _ in open(file1_path))  # or just use line_number
        print(f"Compared {line_number} lines.")
        print(f"Found {len(differences)} differences (showing first {max_differences}).")


# Example usage
compare_hex_files('/content/Arduino original.hex', '/content/Arduino reverse eng.hex', max_differences=10)