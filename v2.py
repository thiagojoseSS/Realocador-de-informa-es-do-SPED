import os.path
import os
from tkinter import filedialog


def campo7(linha_0200):
    try:
        tabela_campo7 = [b"00", b"01", b"02", b"03", b"04", b"05", b"06", b"07", b"08", b"09", b"10", b"99"]

        tab7 = [b"00-Mercadoria para Revenda",
                b"01-Materia prima",
                b"02-Embalagem",
                b"03-Produto em Processo",
                b"04-Produto Acabado",
                b"05-Subproduto",
                b"06-Produto Intermediario",
                b"07-Material de Uso e Consumo",
                b"08-Ativo Imobilizado",
                b"09-Servicos",
                b"10-Outros insumos",
                b"99-Outras"]

        atual_linha = linha_0200.split(b"|")
        for i, elem in enumerate(tabela_campo7):
            if elem == atual_linha[7]:
                atual_linha[7] = tab7[i]

        nova_linha = b''
        for y, en in enumerate(atual_linha):
            if y > 0:
                nova_linha += b"|"
                nova_linha += en

        return nova_linha
    except ValueError:
        return b"Erro tabela campo 7"


def ler_e_extrair(sped):
    try:
        cabecalho = b"|REG|NUM_ITEM|COD_ITEM|DESCR_COMPL|QTD|UNID|VL_ITEM|VL_DESC|IND_MOV|CST_ICMS|CFOP|COD_NAT|VL_BC_ICMS|ALIQ_ICMS|VL_ICMS|VL_BC_ICMS_ST|ALIQ_ST|VL_ICMS_ST|IND_APUR|CST_IPI|COD_ENQ|VL_BC_IPI|ALIQ_IPI|VL_IPI|CST_PIS|VL_BC_PIS|ALIQ_PIS|QUANT_BC_PIS|ALIQ_PIS|VL_PIS|CST_COFINS|VL_BC_COFINS|ALIQ_COFINS|QUANT_BC_CO INS|ALIQ_COFINS|VL_COFINS|COD_CTA|VL_ABAT_NT|CHV_NFE|REG2|COD_INF_ITEM|x|.|REG3|COD_ITEM|DESCR_ITEM|COD_BARRA|COD_ANT_ITEM|UNID_INV|TIPO_ITEM|COD_NCM|EX_IPI|COD_GEN|COD_LST|ALIQ_ICMS|CEST|obs\n"

        retorna_final_sped = []
        indice_da_linha_0200 = []
        lista_c170_temp = []
        concatenar = b''
        num_c170_da_nota = 0
        chave = b''
        retorna_final_sped.append(cabecalho)
        ipe = 0

        # For geral percorrer o SPED
        for i, e in enumerate(sped):
            x = e
            x = x.replace(b'\n', b'')
            x = x.replace(b'\r', b'')
            linha_atual = x.split(b'|')
            if linha_atual[1] == b"0200":
                indice_da_linha_0200.append((linha_atual[2], e))

            if linha_atual[1] == b"C100":
                num_c170_da_nota = 0
                chave = b"'" + linha_atual[9]

            if linha_atual[1] == b"C170":
                num_c170_da_nota += 1
                # concatenar = x + chave
                lista_c170_temp.append((linha_atual[3], x))

            if linha_atual[1] == b"C177":
                ipe = 1
                for f in lista_c170_temp:
                    for q in indice_da_linha_0200:
                        if f[0] == q[0]:
                            linha_q = campo7(q[1])
                            retorna_final_sped.append(f[1] + chave + x + linha_q)

            if ipe == 1:
                lista_c170_temp.clear()
                chave = b''
                ipe = 0

        return retorna_final_sped

    except ValueError:
        # Retorna uma lista com uma mensagem de erro, pois alguma coisa deu errado
        # no processo
        return ["Erro na geração da lista do SPED final C170!", "Conferir o 'modulo ler_e_extrair'."]


arq_sped = filedialog.askopenfilename(filetypes=(("txt files", "*.txt"), ("all files", "*.*")))

if arq_sped != "()":

    arq = open(arq_sped, 'rb')
    lista_das_linhas_sped = arq.readlines()

    final_sped = ler_e_extrair(lista_das_linhas_sped)

    arq.close()

    novo = filedialog.asksaveasfile(mode="wb", defaultextension=".txt",
                                    filetypes=(("txt files", "*.txt"), ("all files", "*.*")))

    if novo != "()":
        novo.writelines(final_sped)
        novo.close()
