import argparse
import csv

def transform_csv(input_path, output_path, threshold):
    with open(input_path, 'r') as infile, open(output_path, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if float(row['value']) > threshold:
                writer.writerow(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter CSV by threshold")
    parser.add_argument("input_path", help="Path to input CSV")
    parser.add_argument("output_path", help="Path to write output")
    parser.add_argument("--threshold", type=float, default=100.0, help="Filter threshold")
    args = parser.parse_args()

    transform_csv(args.input_path, args.output_path, args.threshold)
