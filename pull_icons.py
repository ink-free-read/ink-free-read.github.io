#!/usr/bin/env python3
"""
Simple icon downloader
"""

import tempfile
import zipfile
import requests
from pathlib import Path

# Config: URL -> filename mapping
ICONS = {
    # https://github.com/apache/airflow/tree/main/airflow-core/docs/img/logos
    "airflow.svg": "https://raw.githubusercontent.com/apache/airflow/refs/heads/main/airflow-core/docs/img/logos/wordmark_2.svg",
    "airflow.png": "https://raw.githubusercontent.com/apache/airflow/refs/heads/main/airflow-core/docs/img/logos/airflow_transparent.png",
    # https://aws.amazon.com/architecture/icons
    "aws": {
        'source': "https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/architecture/approved/architecture-icons/Asset-Package_07312025.49d3aab7f9e6131e51ade8f7c6c8b961ee7d3bb1.zip",
        'files': {
            "aws.svg": "Architecture-Group-Icons_07312025/AWS-Cloud-logo_32_Dark.svg",
            "aws-ec2.svg": "Architecture-Service-Icons_07312025/Arch_Compute/64/Arch_Amazon-EC2_64.svg",
            "aws-sagemaker.svg": "Architecture-Service-Icons_07312025/Arch_Artificial-Intelligence/64/Arch_Amazon-SageMaker-AI_64.svg",
            "aws-s3.svg": "Architecture-Service-Icons_07312025/Arch_Storage/64/Arch_Amazon-Simple-Storage-Service_64.svg",
        }
    },

    # https://brand.databricks.com/databricks-logo
    'databricks.svg': "https://cdn.bfldr.com/9AYANS2F/at/k8bgnnxhb4bggjk88r4x9snf/databricks-symbol-color.svg",
    
    # https://kotlinlang.org/docs/kotlin-brand-assets.html
    'kotlin' : {
        'source': "https://resources.jetbrains.com/storage/products/kotlin/docs/kotlin_logos.zip",
        'files': {
            'kotlin.svg': "Digital/Mark/Full Color/Kotlin Full Color Logo Mark RGB.svg"
        }
    },

    # https://github.com/mlflow/mlflow/blob/master/assets/
    "mlflow.svg": "https://raw.githubusercontent.com/mlflow/mlflow/refs/heads/master/assets/icon.svg",
    
    # https://openai.com/brand/
    "openai": {
        'source': "https://cdn.openai.com/brand/OpenAI-Logos-2025.zip",
        'files': {
            'openai.svg': 'OpenAI-logos(new)/SVGs/OpenAI-black-monoblossom.svg'
        }
    },
    
    # https://www.python.org/community/logos/
    "python.svg": "https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/files/python-logo-only.svg",
    
    # https://github.com/pyg-team/pyg_sphinx_theme/blob/master/pyg_sphinx_theme/static/img/pyg_logo.svg
    "pytorch_geometric.svg": "https://raw.githubusercontent.com/pyg-team/pyg_sphinx_theme/refs/heads/master/pyg_sphinx_theme/static/img/pyg_logo.svg",
    
    # https://github.com/Lightning-AI/pytorch-lightning/blob/master/docs/source-fabric/_static/images
    "pytorch_lightning.svg": "https://raw.githubusercontent.com/Lightning-AI/pytorch-lightning/refs/heads/master/docs/source-fabric/_static/images/icon.svg",
    
    # https://github.com/pytorch/pytorch.github.io/blob/master/assets/images/
    "pytorch.svg": "https://raw.githubusercontent.com/pytorch/pytorch.github.io/refs/heads/master/assets/images/logo-icon.svg",

    # https://www.snowflake.com/brand-guidelines/
    "snowflake" : {
        'source': "https://www.snowflake.com/wp-content/uploads/2021/04/Snowflake-Logo-Package.zip",
        'files': {
            'snowflake.svg': 'Snowflake Logo/Digital/SVG/snowflake-bug-color-rgb.svg',
        }
    },

    # https://brand.hashicorp.com/product_logos
    "hashicorp" : {
        'source': "https://brand.hashicorp.com/file/brand.hashicorp.com/https%3A%2F%2Ffirebasestorage.googleapis.com%2Fv0%2Fb%2Fstandards-site-beta.appspot.com%2Fo%2Fdocuments%252F4a24m5t0li5%252Fantwtl4lq0z%252FProduct%2520Logos-20241118T223201Z-001.zip%3Falt%3Dmedia%26token%3Dc25d9186-ec62-49b9-9633-b8a91aeba77d",
        'files': {
            'terraform.svg': 'Product Logos/01-Terraform/Terraform/Terraform-LogoMark_onLight.svg'
        }
    },
    # https://spark.apache.org/images/
    "spark.svg": "https://spark.apache.org/images/spark-start.svg",
    "spark_pride.png": "https://spark.apache.org/images/spark-logo-pride.png",
    # "python.svg": "https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/files/python-logo-only.svg",
    # "snowflake.svg": "https://www.snowflake.com/wp-content/themes/snowflake/assets/img/logo.svg",
    # "databricks.svg": "https://databricks.com/wp-content/uploads/2021/10/db-navbar-logo.svg",
    # "pytorch.svg": "https://pytorch.org/assets/images/pytorch-logo-dark-text-8ba00000.svg",
    # "pytorch_lightning.svg": "https://lightning.ai/assets/images/logo-dark.svg",
    # "pytorch_geometric.svg": "https://pytorch-geometric.readthedocs.io/en/latest/_images/logo.png",
    # "mlflow.ico": "https://mlflow.org/assets/images/mlflow-logo-dark-text-8ba00000.svg",
    # "openai.svg": "https://openai.com/favicon.ico",
    # "pytorch.webp": "https://pytorch.org/assets/images/pytorch-logo-dark-text-8ba00000.svg",
    # # Add more here...
}

def download_icons():
    platforms_dir = Path("img/platforms")
    platforms_dir.mkdir(parents=True, exist_ok=True)
    
    for filename, url in ICONS.items():
        filepath = platforms_dir / filename
        try:
            if type(url) is dict:
                out_files = list(url["files"].keys())
                if all((platforms_dir / key).exists() for key in out_files):
                    print(f"✅ {filename} assets already exists: {out_files}")
                    continue
                with tempfile.TemporaryDirectory() as temp_dir:
                    print(f"Downloading and unzipping {filename} assets...")
                    temp_dir = Path(temp_dir)
                    response = requests.get(url["source"], timeout=10)
                    response.raise_for_status()
                    temp_zip_path = temp_dir / 'temp.zip'
                    temp_zip_path.write_bytes(response.content)
                    temp_unzip_dir = temp_dir / "unzip"
                    temp_unzip_dir.mkdir(parents=True, exist_ok=True)
                    with zipfile.ZipFile(temp_zip_path, "r") as zip_ref:
                        zip_ref.extractall(temp_unzip_dir)

                    for key, value in url["files"].items():
                        source_path = temp_unzip_dir / value
                        if not source_path.exists():
                            print(f"❌ Source file not found: {source_path}")
                            continue
                        Path(source_path).rename(platforms_dir / key)
                        print(f"✅ Downloaded {key}")
            else:
                if not filepath.exists():
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    Path(filepath).write_bytes(response.content)
                    print(f"✅ Downloaded {filename}")
                else:
                    print(f"✅ {filename} already exists")
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")

if __name__ == "__main__":
    download_icons()
