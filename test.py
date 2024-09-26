from Bio import Entrez, SeqIO
import pandas as pd
from io import StringIO

# Set your email
Entrez.email = "your_email@example.com"

assembly_accessions = [
    "GCF_041014305.1",
    "GCF_019703285.1",
    "GCF_026194635.2",
    "GCF_034422775.1",
    "GCF_008931365.1",
    "GCF_012934965.1",
    "GCF_004768705.1",
    "GCF_030168285.1",
    "GCF_012935005.1",
    "GCF_012935105.1",
    "GCF_026062515.1",
    "GCF_036870965.1",
    "GCF_025264005.1",
    "GCF_039545565.1",
    "GCF_012931625.1",
    "GCF_023809705.1",
    "GCF_002210065.1",
    "GCF_038441325.1",
    "GCF_012935085.1",
    "GCF_020912005.1",
    "GCF_004028375.1",
    "GCF_024205285.1",
    "GCF_029909475.1",
    "GCF_014874575.1"
]

results = []

for assembly_accession in assembly_accessions:
    search_handle = Entrez.esearch(db="assembly", term=assembly_accession)
    search_results = Entrez.read(search_handle)
    search_handle.close()

    if search_results["IdList"]:
        assembly_id = search_results["IdList"][0]
        print(f"Found Assembly ID: {assembly_id} for {assembly_accession}")

        elink_handle = Entrez.elink(dbfrom="assembly", db="nuccore", id=assembly_id, linkname="assembly_nuccore_refseq")
        elink_results = Entrez.read(elink_handle)
        elink_handle.close()

        nuccore_ids = [link["Id"] for link in elink_results[0]["LinkSetDb"][0]["Link"]]

        if nuccore_ids:
            print(f"Found Nuccore IDs: {nuccore_ids} for {assembly_accession}")

            for nuccore_id in nuccore_ids:
                fetch_handle = Entrez.efetch(db="nuccore", id=nuccore_id, rettype="gb", retmode="text")
                record = fetch_handle.read()
                fetch_handle.close()
                record_io = StringIO(record)
                genome_record = SeqIO.read(record_io, "genbank")
                results.append({
                    "Assembly ID": assembly_accession,
                    "Nuccore ID": genome_record.id,
                    "Description": genome_record.description,
                    "Sequence Length": len(genome_record.seq)
                })

        else:
            print(f"No nucleotide records found for {assembly_accession}.")
    else:
        print(f"Assembly ID not found for {assembly_accession}.")


df = pd.DataFrame(results)
output_file = "genome_records.xlsx"
df.to_excel(output_file, index=False)

print(f"Results saved to {output_file}.")
