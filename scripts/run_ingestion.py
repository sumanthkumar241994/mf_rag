# scripts/run_ingestion.py

from ingestion.ingest_sid import ingest_sid


def main():

    ingest_sid(
        pdf_path="/users/sumanth/downloads/1777436013137.pdf",
        scheme_name="Platinum Hybrid Long-Short Fund",
        amc_name="Mirae AMC"
    )


if __name__ == "__main__":
    main()