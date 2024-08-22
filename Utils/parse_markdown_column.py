from markdown_it import MarkdownIt
import Utils.category as c

# Funzione per trovare i titoli nelle sezioni del file Markdown
def find_titles_md(link_md, path_file):
    try:
        with open(path_file, 'r', encoding='utf-8') as file:
                md_text = file.read()
    except UnicodeDecodeError:
                md_text = ""

    md = MarkdownIt()
    tokens = md.parse(md_text)

    h1_titles = [link_md]
    for i, token in enumerate(tokens):
        if token.type == 'heading_open':
            if i + 1 < len(tokens) and tokens[i + 1].type == 'inline':
                h1_titles.append(tokens[i + 1].content)
                h1_titles.append(str(int(token.tag[1:])))
    return h1_titles

def initialize_data_table(num_file_md, link_list, path_md_file):
    data_table = []
    for i in range(num_file_md):
        file_data = {
            "file_name": f"{i}.md",
            "link": link_list[i],
            "sections": []
        }
        data_table.append(file_data)
    return data_table


def extract_sections(data_table, path_md_file):
    for i, file_data in enumerate(data_table):
        titles = find_titles_md(file_data["link"], path_md_file + file_data["file_name"])

        try:
            with open(path_md_file + file_data["file_name"], 'r', encoding='utf-8') as file:
                md_lines = file.readlines()
        except:
            md_lines = ""

        md_text = "".join(md_lines)

        for j in range(1, len(titles), 2):
            section_title = titles[j]
            normalized_title = section_title.strip().lower()

            start_index = md_text.lower().find(normalized_title)
            if start_index == -1:
                continue

            if j + 2 < len(titles):
                next_section_title = titles[j + 2].strip().lower()
                end_index = md_text.lower().find(next_section_title, start_index + len(normalized_title))
            else:
                end_index = len(md_text)

            section_text = md_text[start_index:end_index]

            section_info = {
                "section_title": titles[j],
                "section_text": section_text
            }

            file_data["sections"].append(section_info)

    return data_table

def add_section_levels(data_table, path_md_file):
    for i, file_data in enumerate(data_table):
        titles = find_titles_md(file_data["link"], path_md_file + file_data["file_name"])

        for j in range(1, len(titles), 2):
            section_level = titles[j + 1]  # Assumendo che il livello sia nel titolo successivo
            file_data["sections"][j // 2]["level"] = section_level  # Inserisce il livello nella sezione corrispondente

    return data_table

def add_word_count(data_table):
    for file_data in data_table:
        for section in file_data["sections"]:
            word_count = section["section_text"].count(" ")
            section["word_count"] = word_count
    return data_table

def categorize_sections(data_table):
    for file_data in data_table:
        for section in file_data["sections"]:
            keys = [key for key, values in c.tipologia.items() if section["section_title"].strip().lower() in [v.strip().lower() for v in values]]
            if keys:
                section["category"] = keys[0]
            else:
                section["category"] = "Uncategorized"
    return data_table

def count_images_in_sections(data_table):
    for file_data in data_table:
        for section in file_data["sections"]:
            # Esempio di codice che conta le immagini (ipotetico)
            image_count = section["section_text"].count("![")
            section["image_count"] = image_count
    return data_table

#aggiungere qui altre statistiche



def data_table(num_file_md, link_list, path_md_file):
    data_table = initialize_data_table(num_file_md, link_list, path_md_file)
    data_table = extract_sections(data_table, path_md_file)  # Estrazione delle sezioni
    data_table = add_section_levels(data_table, path_md_file)  # Aggiunta dei livelli
    data_table = add_word_count(data_table)  # Aggiunta del conteggio delle parole
    data_table = categorize_sections(data_table)  # Categorizzazione delle sezioni
    data_table = count_images_in_sections(data_table)
    data_table = add_score(data_table)  # Calcolo e aggiunta del punteggio
    #data_table = find_image_for_section(data_table)

    return data_table


def add_score(data_table):
    for file_data in data_table:
        for section in file_data["sections"]:
            # Parametri per il calcolo del punteggio (esempio):
            # - Conteggio parole
            # - Livello della sezione
            # - Categoria

            word_count = section.get("word_count", 0)
            level = section.get("level", "")
            category = section.get("category", "Uncategorized")

            # Esempio di calcolo del punteggio basato su parametri ipotetici
            score = 0

            # Aumenta il punteggio in base al conteggio delle parole
            score += word_count / 100  # 1 punto ogni 100 parole

            # Aumenta/diminuisci il punteggio in base al livello del titolo e quindi della sezione
            if level == 1:
                score += 5
            elif level == 2:
                score += 3
            elif level == 3:
                score += 1

            # Aumenta il punteggio in base alla categoria
            if category == "Uncategorized":
                score -= 2
            else:
                score += 2

            section["score"] = score
    return data_table


def sum_scores_by_file(data_table):
    score_summary = {}

    for file_data in data_table:
        file_name = file_data["file_name"]
        total_score = sum(section.get("score", 0) for section in file_data["sections"])

        score_summary[file_name] = total_score

    return score_summary