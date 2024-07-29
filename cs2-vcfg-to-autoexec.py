from os import listdir

arquivos = listdir("C:\\Users\\Thiago\\Desktop\\userdata\\")

for chave,nome in enumerate(arquivos):
    if "vcfg_" in nome or "vcfg" not in nome:
        arquivos.pop(chave)
        
with open("C:\\Users\\Thiago\\Desktop\\userdata\\resultado\\autoexec.cfg","w") as autoexec:
    for cfg in arquivos:
        print(cfg + " Ok!")
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
                        
print("Pronto!")
                
