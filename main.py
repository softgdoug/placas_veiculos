from importlib.resources import files
import os
from dotenv import load_dotenv
import streamlit as st
import requests

# Função para limpar a tela do terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
# Função para retornar a lista de clientes (mockup)    
def get_client_list():
    _cliente_list = [{"nome": "Doug", "idade":50, "placa":"FDX9B94"}, {"nome": "Ana", "idade": 25, "placa":"OZL7H33"}, {"nome": "Jorge", "idade": 35,"placa":"ABC0123"}, {"nome": "Adriana", "idade": 28,"placa":"INR8137"}]
    
    return _cliente_list

#Função para buscar clientes através de campo e valor 
def fcSearch_client(field, value):
    _field = field.lower() 
    _value = value.lower() 
   

    if _field and _value:
        _cliente_list = get_client_list()
        _value = _value.replace(" ","").replace("\n","").lower()
        print("_cliente_list", _cliente_list)
        print(f"Buscando clientes onde {_field} = {_value}...")
        return [_cliente for _cliente in _cliente_list if  str(_cliente[_field]).lower() == str(_value).lower() ]
    else: 
        return []
        

# Monta a tela principal no streamlit
def main_screen():
    st.title("Avaliar placas de carros")
    with st.expander("Clientes"):
        st.json(get_client_list())
        
    with st.expander("Placa"):
        _file = st.file_uploader("Selecione o arquivo", type=["jpg", "jpeg", "png", "webp", "gif"])
            
            
    if st.button("Processar imagem"):
        if _file:
            files = {
                "file": (_file.name, _file.getvalue(), _file.type)
            }
                        
            #enviar a imagem e obter a descrição com a LLM 
            response = requests.post("https://flow-hml.plusoftomni.com.br/webhook/image_describe", files=files)                
            
            print("response", response.json())
            _placa = response.json().get("placa", "N/A")
            
            #Se identificou a placa
            if _placa != "N/A":
                st.toast(f"Placa {_placa} detectada com sucesso!", icon="✅")
                _client = fcSearch_client("placa", _placa) 
                print("_client", _client)
                st.write("Placa detectada: ", _placa)
                st.write("cliente: ", _client[0]["nome"] if _client else "Cliente não encontrado.")                        
            else:
                st.toast(f"Não foi possível identificar a placa na imagem", icon="❌") 
                
        else:
            # ícones para o toast "✅" "⚠️" "❌" "ℹ️" "🚀"
            st.toast("Selecione uma imagem para enviar.", icon="⚠️")

    # Carrega a imagem se carregada                  
    if _file:
        st.image(_file)
            
# Não está em uso no streamlit, permite testes com os dados do cliente via terminal
def main():
    load_dotenv()
    _cliente_list = [{"nome": "Doug", "idade":50, "placa":"FDX9B94"}, {"nome": "Ana", "idade": 25, "placa":"OZL7H33"}, {"nome": "Jorge", "idade": 35,"placa":"ABC0123"}, {"nome": "Adriana", "idade": 28,"placa":"INR8137"}]
    _campo = "nome"

    _field_list = ", ".join(_cliente_list[0].keys())
    # print("Campos disponíveis: ", _field_list)
    while True:
        _campo = input(f"Digite o campo a ser buscado: [{_field_list}]: ")
        
        if _campo not in _field_list:
            print(f"Selecione um dos itens: [{_field_list}]")
            continue
        
        while True:            
            _valor = input("Digite o valor a ser buscado: ")
            clear_screen() 

            _result = [_cliente for _cliente in _cliente_list if str(_valor).lower() in str(_cliente[_campo]).lower() ]
            print("Registros: ",_result if _result else "Nenhum registro encontrado.")    
            

if __name__ == "__main__":
    # main()
    main_screen()
