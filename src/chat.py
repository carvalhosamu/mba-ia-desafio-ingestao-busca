from search import search_prompt

def main():
    
    print("Bem-vindo ao Chat! Faça suas perguntas e obtenha respostas.")
    while True:
        user_input = input("Faça sua pergunta (ou digite 'sair' para encerrar): ")
        if user_input.lower() == 'sair':
            print("Encerrando o chat. Até mais!")
            break
        
        try:
            response = search_prompt(user_input)
            print("Resposta:", response.content)
        except Exception as e:
            print("Ocorreu um erro ao processar sua pergunta:", str(e))

    pass

if __name__ == "__main__":
    main()