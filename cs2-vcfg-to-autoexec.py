from os import listdir

print("Digite o diretório onde estão os arquivos vcfg")
print("Exemplo: C:\\Program Files (x86)\\Steam\\userdata\\XXXXXXX\\730\\local\\cfg")
diretorio_inicial = input("-> ").strip()
print()
arquivos_total = listdir(diretorio_inicial)

arquivos_filtrados = []
for chave,nome in enumerate(arquivos_total):
    if "vcfg_" not in nome and "vcfg" in nome:
        arquivos_filtrados.append(arquivos_total[chave])
        
print("Digite o diretório onde será criado o arquivo final")
print("Exemplo: C:\\Users\\XXXXXX\\Desktop\\")
diretorio_final = input("-> ").strip()
print()

if diretorio_final[len(diretorio_final) - 1] != "\\" and diretorio_final[len(diretorio_final) - 1] != "/":
    diretorio_final += "\\"

with open(diretorio_final + "autoexec.cfg","w") as autoexec:
    print("Arquivos vcfg encontrados: ")
    for cfg in arquivos_filtrados:
        print(cfg)
        with open("C:\\Users\\Thiago\\Desktop\\userdata\\"+ cfg,"r") as userdata:
            linhas_userdata = userdata.read().splitlines()
            aberto = linhas_userdata.count("}") + linhas_userdata.count("\t}")
            tipo = ""
            if len(linhas_userdata) <=3:
                continue
            while aberto != 0:
                for linha in linhas_userdata:
                    linha = linha.strip()
                    if linha == '"config"' or linha == "{":
                        continue
                    elif linha == "}":
                        aberto -= 1
                        continue
                    elif linha in '"convars""bindings""analogbindings"':
                        tipo = linha
                        continue
                    if tipo == '"convars"':
                        comando_cru = linha.strip().split("\t\t")
                        comando1 = comando_cru[0].strip('"')
                        comando2 = comando_cru[1]
                        autoexec.write(comando1 + " " + comando2 + "\n")
                    else:
                        if "unbound" in linha:
                            continue
                        else:
                            comando_cru = linha.strip().split("\t\t")
                            comando1 = comando_cru[0]
                            comando2 = comando_cru[1]
                            autoexec.write("bind" + " " + comando1 + " " + comando2 + "\n")

print()
print("Arquivo autoexec.cfg gerado em: " + diretorio_final)
                
