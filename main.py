import Utils.in_out_csv as ioc  # Modulo per la gestione di file CSV
import Utils.download_from_urls as dfu  # Modulo per scaricare file da URL
import Utils.parse_markdown_column as pmc  # Modulo per analizzare file Markdown

# Percorsi dei file di input e output
name_file_csv_in = "./in/apps.csv"  # File CSV da cui leggere gli URL #Usa 'miniapps.csv' per un test veloce
name_file_csv_out = "./out/output_sections.csv"  # File CSV dove salvare l'output
path_md_file = "./md_file/"  # Directory per salvare i file Markdown scaricati

# Esecuzione principale del programma
if __name__ == "__main__":
    """
    Esegue il flusso principale del programma:
    1. Legge gli URL da un file CSV.
    2. Rinomina gli URL per preparare il download.
    3. Scarica i file Markdown dagli URL.
    4. Analizza i file Markdown e crea una tabella dei dati.
    5. Esporta i dati in un file CSV di output.
    """

    # Legge gli URL dal file CSV di input
    site_list = ioc.read_urls(name_file_csv_in)
    print(".. imported from url ..")

    # Rinomina gli URL per il download
    link_list = dfu.rename_urls(site_list)
    print(".. renamed urls ..")

    # Scarica i file Markdown dagli URL rinominati
    num_file_md = dfu.download_md_file(link_list, path_md_file)
    print(f".. downloaded md file in {path_md_file}..")

    # Crea una tabella dei dati analizzando i file Markdown scaricati
    data_table = pmc.get_data_table(num_file_md, link_list, path_md_file)
    print(".. created data table ..")

    # Esporta la tabella dei dati in un file CSV di output
    ioc.get_csv_tab(data_table, name_file_csv_out)
    print(f".. table exported to csv in {name_file_csv_out} ..")

    # Segnala la fine dell'esecuzione del programma
    print("END")