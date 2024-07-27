import streamlit as st
import pandas as pd
import json
from io import BytesIO, StringIO

def converter_para_json(df):
    """Converte DataFrame para JSON."""
    return df.to_json(orient="records", lines=True)

def converter_para_excel(df):
    """Converte DataFrame para Excel e retorna como bytes."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)  # Move o ponteiro para o início do BytesIO
    return output.getvalue()

def converter_para_csv(df):
    """Converte DataFrame para CSV e retorna como string."""
    output = StringIO()
    df.to_csv(output, index=False)
    output.seek(0)  # Move o ponteiro para o início do StringIO
    return output.getvalue()

def processar_arquivo(arquivo):
    """Processa o arquivo carregado com base no tipo MIME."""
    if arquivo.type == "text/csv":
        df = pd.read_csv(arquivo)
    elif arquivo.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(arquivo)
    elif arquivo.type == "application/json":
        df = pd.read_json(arquivo)
    else:
        raise ValueError("Tipo de arquivo não suportado.")
    return df

def cadastrar():
    """Função para a página de cadastro."""
    st.title("Cadastro")
    email = st.text_input("Digite seu e-mail")
    senha = st.text_input("Digite sua senha", type="password")
    telefone = st.text_input("Digite seu telefone")
    cadastro_btn = st.button("Cadastrar")

    if cadastro_btn:
        st.success(f"Cadastro realizado com sucesso para {email}!")
        st.session_state.pagina_atual = "login"  

def login():
    """Função para a página de login."""
    st.title("Login")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    login_btn = st.button("Logar")
    
    if st.button("Não Tenho Conta?"):
        st.session_state.pagina_atual = "cadastrar"

    if login_btn:
        verificar(email, senha)

def verificar(email, senha):
    """Verifica as credenciais do usuário."""
    if email == "Admin@gmail.com" and senha == "Admin123":
        st.session_state.logged_in = True
        st.success("Login bem-sucedido!")
        st.session_state.pagina_atual = "tela_inicial"
    else:
        st.session_state.logged_in = False
        st.error("Senha ou e-mail inválido!")

def tela_inicial():
    """Função para a página inicial após login."""
    st.header("AutoBot2.0")
    st.subheader("Conheça Nossos Trabalhos!")
    st.text("Trabalhamos com automações de tarefas com o objetivo de facilitar sua rotina.")    
    st.subheader("Arquivos para Conversão")

    arquivo = st.file_uploader("Compartilhe o arquivo", type=["csv", "xlsx", "json"])

    """Verifica se possui arquivo vazio"""
    if arquivo is not None:
        
        try:
            df = processar_arquivo(arquivo)
            opcao = st.selectbox("Escolha o formato de saída:", ["JSON", "Excel", "CSV"])
            """Converte os arquivos coforme o escolhido pelo usuario, mostrando o arquivo com uma opção de baixar pra o ususario!"""
            if opcao == "JSON":
                json_data = converter_para_json(df)
                st.text("JSON convertido:")
                st.text(json_data) 
                st.download_button(label="Baixar Arquivo Json", data=json_data, file_name="arquivo convertido.json")
            elif opcao == "CSV":
                csv_data = converter_para_csv(df)
                st.text("CSV convertido:")
                st.text(csv_data)  
                st.download_button(
                    label="Baixar arquivo CSV",
                    data=csv_data,
                    file_name='arquivo_convertido.csv',
                    mime='text/csv'
                )
            elif opcao == "Excel":
             
                    excel_data = converter_para_excel(df)
                    st.download_button(
                    label="Baixar arquivo Excel",
                    data=excel_data,
                    file_name='arquivo_convertido.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
            else: 
                st.error("Não é possivel Converta o arquivo da mesma origem!")
    
                    
            """Caso o arquivo seja repetido, será mostrado que não pode converter o arquivo"""
        except Exception:
            st.error(f"Erro ao processar o arquivo de mesma origem! ")

def main():
    """Função principal para controlar a navegação entre páginas."""
    if 'pagina_atual' not in st.session_state:
        st.session_state.pagina_atual = "login"

    if st.session_state.pagina_atual == "login":
        login()
    elif st.session_state.pagina_atual == "cadastrar":
        cadastrar()
    elif st.session_state.pagina_atual == "tela_inicial":
        tela_inicial()

if __name__ == "__main__":
    main()
