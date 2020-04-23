
## example of pdf from url, convert to html, xpath search and export to Dataframe
def scrap_pdf():
    input_bytes = BytesIO()
    output_string = StringIO()
    response = requests.get('https://covid19.min-saude.pt/wp-content/uploads/2020/04/51_DGS_boletim_20200422.pdf')
    input_bytes.write(response.content)
   
    extract_text_to_fp(input_bytes, output_string, laparams=LAParams(),output_type='html', codec=None)  
    
    tree = html.fromstring(output_string.getvalue())
    cases_string = tree.xpath("//span")


    list_values = [t.text_content().strip().replace('\n',' ') for t in cases_string]
    list_values.remove('laboratorial')
    list_values.remove('(desde 1 de janeiro  2020)')

    index_start = list_values.index("Total de casos suspeitos")
    index_end =  list_values.index("Óbitos")+1

    keys = list_values[index_start:index_end]

    values = list_values[index_end:index_end+(index_end-index_start)]

    df_first_page = pd.DataFrame({'key':keys,'value':values})

    ix_hospitalization_icu =[(i,t) for i,t in enumerate(list_values)  if 'NÚMERO  DE CASOS' in t]

    hospitalized = list_values[ix_hospitalization_icu[0][0]+1]
    icu = list_values[ix_hospitalization_icu[1][0]+1]

    df_hospi_icu = pd.DataFrame({'key':['hospitalizations','icu'],'value':[hospitalized,icu]})

    df = pd.concat([df_first_page,df_hospi_icu],axis=0)


def save_to_file():
    with open("output.html", "w") as text_file:
        print(output_string.getvalue(), file=text_file)