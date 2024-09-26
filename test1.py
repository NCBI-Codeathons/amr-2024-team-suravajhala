# # file = './isolates.tsv'
# # n = 0; amrd = {}; amrc = 0
# # for line in open(file, 'r'):
# #     n = n + 1
# #     if n == 1: continue
# #     line = line.strip().split('\t') # len(line) == 16
# #     ID = line[14] + '#' + line[13]

# #     for amr in line[15].split(','):
# #         assert('=' in amr)
# #         amrc = amrc + 1
# #         amrd[amr] = amrd.get(amr, 0) + 1

# # print(n, amrc, len(amrd))
# # # n=36498, amr=1152, amr#=570673

# # for k, v in amrd.items():
# #     print(k, '\t')
# #     pass
# from Bio import Entrez, SeqIO

Entrez.email = "your_email@example.com"

assembly_accession = "GCF_019703285.1"

search_handle = Entrez.esearch(db="assembly", term=assembly_accession)
search_results = Entrez.read(search_handle)
search_handle.close()

if search_results["IdList"]:
    assembly_id = search_results["IdList"][0]
    print(f"Found Assembly ID: {assembly_id}")

    elink_handle = Entrez.elink(dbfrom="assembly", db="nuccore", id=assembly_id, linkname="assembly_nuccore_refseq")
    elink_results = Entrez.read(elink_handle)
    elink_handle.close()

    nuccore_ids = [link["Id"] for link in elink_results[0]["LinkSetDb"][0]["Link"]]
    
    if nuccore_ids:
        print(f"Found Nuccore IDs: {nuccore_ids}")

        fetch_handle = Entrez.efetch(db="nuccore", id=nuccore_ids, rettype="gb", retmode="text")
        
        output_file = f"{assembly_accession}_nuccore.gb"
        with open(output_file, "w") as f:
            f.write(fetch_handle.read())
        
        fetch_handle.close()

        with open(output_file, "r") as f:
            for genome_record in SeqIO.parse(f, "genbank"):
                print(f"Downloaded: {genome_record.id}")
                print(f"Description: {genome_record.description}")
                print(f"Sequence length: {len(genome_record.seq)}")

    else:
        print("No nucleotide records found.")
else:
    print("Assembly ID not found.")
