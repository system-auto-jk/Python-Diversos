from gtts import gTTS
import os

def texto_para_audio(texto, nome_arquivo='saida.mp3', idioma='pt'):
    """
    Converte texto em áudio usando a API gTTS e salva o resultado em um arquivo MP3.

    Parâmetros:
    - texto: O texto que será convertido em áudio.
    - nome_arquivo: O nome do arquivo de saída MP3 (padrão: 'saida.mp3').
    - idioma: O idioma do texto (padrão: 'pt' para português).
    """
    try:
        # Cria um objeto gTTS
        tts = gTTS(text=texto, lang=idioma, slow=False)

        # Salva o áudio em um arquivo MP3
        tts.save(nome_arquivo)
        print(f'Áudio salvo com sucesso em {nome_arquivo}')

        # Reproduz o áudio usando o player padrão do sistema
        os.system(f'start {nome_arquivo}')  # funciona no Windows
        # Para Linux ou macOS, você pode usar:
        # os.system(f'xdg-open {nome_arquivo}')  # para Linux
        # os.system(f'open {nome_arquivo}')  # para macOS

    except Exception as e:
        print(f"Erro ao converter texto em áudio: {e}")

# Exemplo de uso
texto = input('Qual o texto: ')
texto_para_audio(texto, 'saida.mp3', 'pt')
