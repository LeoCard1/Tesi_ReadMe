import re
from markdown_it import MarkdownIt
from Utils.category import tipologia

"""
Inizializza una struttura dati per memorizzare informazioni sui file Markdown.
Args:
    num_file_md (int): Numero di file Markdown.
    link_list (list): Lista di link corrispondenti a ciascun file Markdown.
Returns:
    list: Una lista di dizionari contenenti i dati inizializzati per ogni file.
"""
def initialize_data_table(num_file_md, link_list):
    data_table = []
    for i in range(num_file_md):
        file_data = {
            "file_name": f"{i}.md",
            "h1_titles": [],
            "category": [],
            "char_counts": [],
            "h2_h3_titles": [],
            "h2_h3_counts": [],
            "link": link_list[i]
        }
        data_table.append(file_data)
    return data_table

    """
    Estrae i titoli H1 e H2/H3 da un file Markdown e restituisce il testo ripulito.
    Args:
        md_file (str): Percorso del file Markdown.
    Returns:
        tuple: Una tupla contenente:
            - lista di titoli H1 con il loro livello e categoria,
            - lista di titoli H2/H3 con i loro livelli,
            - testo Markdown ripulito.
    """
def find_titles_md(md_file):
    try:
        with open(md_file, 'r', encoding='utf-8') as file:
            md_text = file.read()
    except UnicodeDecodeError:
        md_text = ""

    md = MarkdownIt()
    tokens = md.parse(md_text)

    h1_titles = []
    h2_3_titles = []

    for i, token in enumerate(tokens):
        if token.type == 'heading_open':
            level = int(token.tag[1:])
            title_content = tokens[i + 1].content

            cleaned_title = clean_text(title_content)  # Pulizia del titolo
            category = categorize_title(cleaned_title)  # Categorizzazione titolo

            if level == 1:
                h1_titles.append((cleaned_title, level, category))
            else:
                h2_3_titles.append((cleaned_title, level))
    #print(clean_text(md_text))
    return h1_titles, h2_3_titles, md_text

"""
Calcola la lunghezza in caratteri della sezione tra due titoli H1.
Args:
    md_text (str): Il testo completo del Markdown.
    h1_title (str): Il titolo H1 corrente.
    next_h1_title (str): Il titolo H1 successivo.
Returns:
    int: Il conteggio dei caratteri della sezione.
"""
def calculate_section_length(md_text, h1_title, next_h1_title):
    section_start = md_text.find(h1_title) + len(h1_title)
    # Trova l'indice di fine (fixed: ultimo h1_title == next_h1_title non veniva aggiornato)
    if next_h1_title and next_h1_title!=h1_title:
        section_end = md_text.find("# " + next_h1_title)
    else:
        section_end = len(md_text)  # Se non c'è next_h1_title, prendi la lunghezza totale
    # Estrai il testo della sezione
    section_text = md_text[section_start:section_end].strip()
    # Ripulisci e conta caratteri
    cleaned_text = clean_text(section_text)
    return len(cleaned_text)

"""
 Popola la tabella dei dati con sezioni e informazioni sui titoli dai file Markdown.
 Args:
     data_table (list): La tabella dei dati inizializzata.
     path_md_file (str): Percorso della directory contenente i file Markdown.
 Returns:
     list: Tabella dei dati aggiornata con le informazioni estratte.
 """
def extract_sections(data_table, path_md_file):

    for file_data in data_table:

        h1_titles, h2_3_titles, md_text = find_titles_md(path_md_file + file_data["file_name"])

        for i, (title, _,_) in enumerate(h1_titles):

            file_data["h1_titles"].append(title)

            if i + 1 < len(h1_titles):
                next_h1_title = h1_titles[i+1][0]
            else: None

            char_count = calculate_section_length(md_text, title, next_h1_title)
            file_data["char_counts"].append(char_count)

            file_data["category"].append(h1_titles[i][2])

        # Popola la colonna h2_h3_titles
        for i, (title, _) in enumerate(h2_3_titles):
            file_data["h2_h3_titles"].append(title)
        # Popola la colonna h2_h3_counts
        file_data["h2_h3_counts"]= len(h2_3_titles)
    return data_table

    """
    Funzione principale per raccogliere e restituire la tabella dei dati dai file Markdown.
    Args:
        num_file_md (int): Numero di file Markdown.
        link_list (list): Lista di link corrispondenti a ciascun file Markdown.
        path_md_file (str): Percorso della directory contenente i file Markdown.
    Returns:
        list: Tabella finale dei dati con tutte le informazioni estratte.
    """

def get_data_table(num_file_md, link_list,path_md_file):
    data_table=initialize_data_table(num_file_md,link_list)
    return extract_sections(data_table, path_md_file)

    """
    Pulisce il testo Markdown rimuovendo elementi indesiderati.
    Args:
        md_text (str): Il testo Markdown da pulire.
    Returns:
        str: Testo pulito con link, tag HTML e caratteri indesiderati rimossi.
    """
def clean_text(md_text):
    # Rimuove i link Markdown (es. [test](http://example.com))
    md_text = re.sub(r'\[.*?\]\(.*?\)', '', md_text)
    # Rimuove i tag HTML
    md_text = re.sub(r'<.*?>', '', md_text)
    # Rimuove link a siti web
    md_text = re.sub(r'http[s]?://\S+', '', md_text)
    # Rimuove emoji e caratteri non alfanumerici
    md_text = re.sub(r'[^\x00-\x7F]+', '', md_text)
    # Rimuove punteggiatura, caratteri di a capo e spazi
    md_text = re.sub(r'[^\w]', '', md_text)
    return md_text


    """
    Classifica un titolo ripulito in base a categorie predefinite.
    Args:
        cleaned_title (str): Il titolo da classificare.
    Returns:
        str or None: La categoria del titolo se trovata, altrimenti None.
    """
def categorize_title(cleaned_title):
    # Controlla se il cleaned_title corrisponde a una chiave
    for key in tipologia.keys():
        if key.lower() == cleaned_title.lower():
            return key

    # Controlla tra le keywords
    for key, keywords in tipologia.items():
        if any(keyword.lower() in cleaned_title.lower() for keyword in keywords):
            return key

    return None