import json
import sys
import pandas as pd
from argparse import ArgumentParser
from pprint import pprint
from pathlib import Path


if sys.version_info[0] == 2:
    raise Exception("Please, use Python 3.")

# md_model = "metadata_model.xlsx"
# col_old_label = "Label as exists in legacy metadata (BEAM spreadsheet, metadata field)"
# col_new_label = "New local label"
# sheet_name = "Pre-ingest"


def xls_to_key_list(md_model_path, sheet_name, col_old_label, col_new_label):
    """
        reads the new and old keys for our metadata migration from a spreadsheet
        and returns them in a list as json.
        :param md_model:
        :param col_old_label:
        :param col_new_label:
        :return:
    """

    if md_model_path.endswith(".xlsx"):
        try:
            md_df = pd.read_excel(md_model_path, sheet_name)
        except ValueError:
            raise Exception(f"Please check if {md_model_path} is the correct path,"
                            f" and that {sheet_name} exists in that spreadsheet. ")
        try:
            labels_df = md_df[[col_old_label, col_new_label]]
        except KeyError:
            raise Exception(f"Please ensure that the column names {col_old_label},"
                            f" and {col_new_label} exists. "
                            f"Or adjust the given arguments.")
        labels_df["id"] = labels_df.index + 1
        labels_df.dropna(subset=[col_new_label, col_old_label], inplace=True)
        labels_dict = labels_df.set_index("id").T.to_dict("dict")
        labels_dict_list = list(labels_dict.values())
        return labels_dict_list
    else:
        false_file = Path(md_model_path).suffix
        raise Exception(
            f" {false_file} is not an xlsx document. Please use a xlsx document")


def clean_up_keys(list_of_labels, col_old_label, col_new_label):
    cleaned_list = []
    for label in list_of_labels:
        label = {k: v for k, v in label.items() if v != "DO NOT MIGRATE"}
        if col_new_label in label and col_old_label in label:
            label["new_label"] = label.pop(col_new_label)
            label["old_labels"] = label.pop(col_old_label)
            label["old_label"] = label['old_labels'].split(",")[-1].strip().lower()
            cleaned_list.append(label)
    return cleaned_list


def main(md_model_path, sheet_name, col_old_label, col_new_label, output_file=None):
    key_list = xls_to_key_list(md_model_path, sheet_name, col_old_label,
                               col_new_label)
    cleaned_list = clean_up_keys(key_list, col_old_label, col_new_label)
    if output_file in ("-", "", None):
        sys.stdout.write(" ".join(str(x) for x in cleaned_list))
        return cleaned_list
    else:
        with open(output_file, "w") as fh:
            json.dump(cleaned_list, fh)


if __name__ == '__main__':
    parser = ArgumentParser(description="...")
    parser.add_argument("md_model",
                        help="Path to the md_model.xlsx")
    parser.add_argument("sheet_name", metavar="sheet_name",
                        help="Name of the worksheet")
    parser.add_argument("col_old_label", metavar="col_old_label",
                        help="Name of the column where the old keys are stored")
    parser.add_argument("col_new_label", metavar="col_new_label",
                        help="Name of the column where the new keys are stored")
    parser.add_argument("-o", "--output", dest="output_file",
                        help="Write location")
    args = parser.parse_args()
    pprint(main(args.md_model, args.sheet_name, args.col_old_label, args.col_new_label,
         args.output_file))
