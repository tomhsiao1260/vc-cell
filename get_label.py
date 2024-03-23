import argparse
import tifffile
import numpy as np

# inklabels generate
def getInklabel(sdf_path, label_path, output_path):
    # z, y, x
    dStack = tifffile.imread(sdf_path)
    labelStack = tifffile.imread(label_path)

    # debug
    # drawImage(output_path)

# python get_label.py --sdf output/sdf.png --label output/label.png --o output/inklabels.png
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate volume via boudning box')
    parser.add_argument('--sdf', type=str, help='SDF input path')
    parser.add_argument('--label', type=str, help='Labels input path')
    parser.add_argument('--o', type=str, help='Inklabels output path')
    args = parser.parse_args()

    getInklabel(args.sdf, args.label, args.o)