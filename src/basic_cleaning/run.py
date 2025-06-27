import argparse
import pandas as pd
import wandb
import os
from datetime import datetime

def go(args):
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    # Drop outliers
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    # Drop rows with missing values
    df.dropna(inplace=True)

    # Save cleaned data to a uniquely named file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"clean_sample_{timestamp}.csv"
    df.to_csv(output_filename, index=False)

    # Log artifact with unique name
    artifact = wandb.Artifact(
        name=output_filename,
        type=args.output_type,
        description=args.output_description
    )
    artifact.add_file(output_filename)
    run.log_artifact(artifact)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean the dataset")

    parser.add_argument("--input_artifact", type=str, required=True, help="Name of the raw dataset artifact")
    parser.add_argument("--output_artifact", type=str, required=True, help="Name of the output (cleaned) artifact")
    parser.add_argument("--output_type", type=str, required=True, help="Type of the output artifact")
    parser.add_argument("--output_description", type=str, required=True, help="Description for the output artifact")
    parser.add_argument("--min_price", type=float, required=True, help="Minimum valid price")
    parser.add_argument("--max_price", type=float, required=True, help="Maximum valid price")

    args = parser.parse_args()

    go(args)