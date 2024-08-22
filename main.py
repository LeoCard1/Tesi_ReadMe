from Utils import in_out_csv as ioc, download_from_url as dfu, parse_markdown_column as pmc

path_md_file = "./md_file/"
name_file_csv_out = "./out/output_sections.csv"
name_file_csv_out_score = "./out/score.csv"
name_file_csv_in = "./in/mini_apps.csv"


# Esecuzione principale del programma
site_list = ioc.read_urls(name_file_csv_in)
print(".. imported from url ..")
link_list = dfu.rename_urls(site_list)
print(".. renamed urls ..")
num_file_md = dfu.download_md_file(link_list, path_md_file)
print(f".. downloaded md file in {path_md_file}..")
data_table = pmc.data_table(num_file_md, link_list, path_md_file)
print(".. created data table ..")
ioc.get_csv_tab(data_table, name_file_csv_out)
print(f".. table exported in csv in {name_file_csv_out} ..")
ioc.export_scores_to_csv(data_table, name_file_csv_out_score)
print(f".. score exported in {name_file_csv_out_score} ..")
print("END")
