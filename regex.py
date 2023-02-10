complete_name = r"\b([a-zñáéíóúA-ZÑÁÉÍÓÚ',.-]+( [a-zñáéíóúA-ZÑÁÉÍÓÚ',.-]+)*){2,30}"
complete_name_comma = r"\b([a-zñáéíóúA-ZÑÁÉÍÓÚ',.-]+( [a-zñáéíóúA-ZÑÁÉÍÓÚ',.-]+)*){2,30}"
# Esta es la normal 
date = r'\b\d{2}/\d{2}/\d{4}\b'
# La siguiente es la de los inscritos del cto de españa absoluto
date_dash = r'\b\d{2}[-]\d{2}[-]\d{4}\b'
mark = r'\b(\d{1,2}\.\d{2}|\d{1,2}:\d{2}\.\d{2})\b'
combi_mark = r'\b(\d{1}\.\d{3})\b'
licens = r'[A-Z]{1,2}\d+'
licens_abs = r'\b[A-Z]+[-]{1,2}\d+'
category = r'(?i)\bsub\d{2}'
