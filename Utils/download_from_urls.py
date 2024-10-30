import urllib.request

"""
Rinomina gli URL nella lista fornita e restituisce una nuova lista di URL.
Args:
    site_list (list): Lista di URL da rinominare.
Returns:
    list: Lista di URL rinominati.
"""
def rename_urls(site_list):
    s_raw = []
    for id, s in enumerate(site_list):
        a = s.split('.com')[0] + 'usercontent.com'
        b = s.split('.com')[1]
        c = 'http://raw.' + a.split('//')[1] + b + '/master/README.md'
        s_raw.append(c)
    return s_raw


"""
Scarica i file Markdown dai link forniti e li salva nella directory specificata.
Args:
    link_list (list): Lista di link dei file Markdown da scaricare.
    path_md_file (str): Percorso della directory in cui salvare i file.
Returns:
    int: Numero di file scaricati con successo.
"""
def download_md_file(link_list, path_md_file):
    i = 0
    for link in link_list:
        try:
            urllib.request.urlretrieve(link, path_md_file + str(i) + ".md")
            i += 1
        except:
            pass
    return i

