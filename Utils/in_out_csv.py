import csv
from Utils import parse_markdown_column as pmc

# Funzione per leggere gli URL dal file CSV
def read_urls(path):
    site_list = []
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for raw in csv_reader:
            if raw[1].startswith('http'):
                site_list.append(raw[1])
    return site_list


def get_csv_tab(data_table, name_file_csv_out):
    with open(name_file_csv_out, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["File Name", "Link", "Section Title", "Level", "Category", "Word Count", "Image", "Score"])
        #writer.writerow(["File Name", "Link", "Section Title", "Level", "Category", "Word Count", "Image"])

        for file_data in data_table:
            for section in file_data["sections"]:
                writer.writerow([
                    file_data["file_name"],
                    file_data["link"],
                    section["section_title"],
                    section["level"],
                    section["category"],
                    section["word_count"],
                    section["image_count"], #stessa parola della funzione da parse_mk_clm
                    section["score"]
                    #section["image"]
                ])


def export_scores_to_csv(data_table, output_csv_path):
    # Calcolare la somma degli score per ogni file
    score_summary = pmc.sum_scores_by_file(data_table)

    # Scrivere i risultati in un file CSV
    with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # Scrivere l'intestazione
        writer.writerow(["file_name", "total_score"])

        # Scrivere i dati
        for file_name, total_score in score_summary.items():
            writer.writerow([file_name, total_score])

