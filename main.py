import Utils.in_out_csv as ioc, Utils.download_from_urls as dfu, Utils.parse_markdown_column as pmc

name_file_csv_in = "./in/jaqs.csv"
name_file_csv_out = "./out/output_sections.csv"
path_md_file = "./md_file/"


# Esecuzione principale del programma
site_list = ioc.read_urls(name_file_csv_in)
print(".. imported from url ..")
link_list = dfu.rename_urls(site_list)
print(link_list) ##############
print(".. renamed urls ..")
num_file_md = dfu.download_md_file(link_list, path_md_file)
print(f".. downloaded md file in {path_md_file}..")
data_table = pmc.get_data_table(num_file_md, link_list,path_md_file)
print(".. created data table ..")
ioc.get_csv_tab(data_table, name_file_csv_out)
print(f".. table exported to csv in {name_file_csv_out} ..")
#ioc.export_scores_to_csv(data_table, name_file_csv_out_score)
#print(f".. score exported in {name_file_csv_out_score} ..")
print("END")
