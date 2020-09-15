import tabula

df = tabula.read_pdf("/home/joantas/Downloads/precatorios.pdf", pages='all')

print(df)
