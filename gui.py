import customtkinter as ctk
from tkinter import filedialog, messagebox
from defs import subir_folhas
import sys
import os

# 📌 Detecta se é executável ou script .py
if getattr(sys, 'frozen', False):
    APP_PATH = os.path.dirname(sys.executable)
else:
    APP_PATH = os.path.dirname(os.path.abspath(__file__))

ICO_PATH = os.path.join(APP_PATH, "sp.ico")

# Cria a janela
app = ctk.CTk()
app.title('SmartPonto - Automação de Folhas')

# Aplica o ícone na barra de tarefas e janela
app.iconbitmap(ICO_PATH)

app.geometry('700x700')
ctk.set_appearance_mode("dark")
# --- Informações Iniciais ---
info_text = (
    "Bem-vindo ao SmartPonto!\n\n"
    "Este programa automatiza o processo de envio de folhas de ponto. "
    "Para utilizá-lo, é necessário ter o navegador Microsoft Edge instalado em seu computador.\n"
)

info_label = ctk.CTkLabel(
    app,
    text=info_text,
    wraplength=660,
    justify='left',
    font=ctk.CTkFont(size=14)
)
info_label.pack(anchor='w', padx=20, pady=(20, 10))

# --- Campos de Entrada ---

# Usuário
usuario_label = ctk.CTkLabel(app, text="Usuário:", font=ctk.CTkFont(size=12, weight="bold"))
usuario_label.pack(anchor='w', padx=20, pady=(10, 2))
usuario_entry = ctk.CTkEntry(app, placeholder_text="Digite seu usuário")
usuario_entry.pack(anchor='w', padx=20, pady=5)

# Senha
senha_label = ctk.CTkLabel(app, text="Senha:", font=ctk.CTkFont(size=12, weight="bold"))
senha_label.pack(anchor='w', padx=20, pady=(10, 2))
senha_entry = ctk.CTkEntry(app, placeholder_text="Digite sua senha", show="*")
senha_entry.pack(anchor='w', padx=20, pady=5)

# Local da pasta
pasta_label = ctk.CTkLabel(app, text="Local da Pasta:", font=ctk.CTkFont(size=12, weight="bold"))
pasta_label.pack(anchor='w', padx=20, pady=(10, 2))

# Campo de exibição da pasta
pasta_entry = ctk.CTkEntry(app, placeholder_text="Nenhuma pasta selecionada")
pasta_entry.pack(anchor='w', padx=20, pady=5)

# Botão para selecionar pasta
def selecionar_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        pasta_entry.delete(0, ctk.END)
        pasta_entry.insert(0, pasta)

pasta_button = ctk.CTkButton(app, text="Selecionar Pasta", command=selecionar_pasta)
pasta_button.pack(anchor='w', padx=20, pady=5)

# Observação sobre os arquivos
pasta_info_text = (
    "Observação: Certifique-se de que os arquivos na pasta estejam em formato PDF "
    "e sigam o padrão de nome exigido pelo sistema: 'CPF - Competência' (exemplo: 99999999999 - 03)."
)

pasta_info_label = ctk.CTkLabel(
    app,
    text=pasta_info_text,
    wraplength=660,
    justify='left',
    font=ctk.CTkFont(size=11),
    text_color="gray"
)
pasta_info_label.pack(anchor='w', padx=20, pady=(0, 10))

# Lista suspensa para versão do Edge
opcoes = ["137", "138", "139", "140"]
opcoes_selecionadas = ctk.CTkOptionMenu(app, values=opcoes)
opcoes_selecionadas.set("Selecione a versão do Edge")
opcoes_selecionadas.pack(anchor='w', padx=20, pady=(10, 5))

# Texto explicativo para verificar versão do Edge
texto_explicativo = (
    "Como verificar a versão do Microsoft Edge:\n"
    " - Abra o Microsoft Edge.\n"
    " - Clique em 'Configurações e mais' (três pontos no canto superior direito).\n"
    " - Selecione 'Configurações'.\n"
    " - Clique em 'Sobre o Microsoft Edge' para ver a versão instalada."
)

texto_label = ctk.CTkLabel(
    app,
    text=texto_explicativo,
    wraplength=660,
    justify='left',
    font=ctk.CTkFont(size=12)
)
texto_label.pack(anchor='w', padx=20, pady=(10, 20))

import threading

def enviar_dados():
    # Desativa o botão
    enviar_button.configure(state="disabled")

    def tarefa():
        usuario = usuario_entry.get().strip()
        senha = senha_entry.get().strip()
        pasta = pasta_entry.get().strip()
        driver_option = opcoes_selecionadas.get()

        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Por favor, preencha o usuário e a senha.")
            enviar_button.configure(state="normal")  # Reativa o botão
            return

        if not pasta:
            messagebox.showwarning("Atenção", "Por favor, selecione uma pasta.")
            enviar_button.configure(state="normal")
            return

        if driver_option == "Selecione a versão do Edge":
            messagebox.showwarning("Atenção", "Por favor, selecione a versão do Edge.")
            enviar_button.configure(state="normal")
            return

        try:
            subir_folhas(usuario, senha, driver_option, pasta)
            messagebox.showinfo("Sucesso", "Processo concluído com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro:\n{e}")
        finally:
            enviar_button.configure(state="normal")  # Reativa o botão ao terminar

    # Roda tudo em uma thread separada
    thread = threading.Thread(target=tarefa)
    thread.start()

enviar_button = ctk.CTkButton(app, text="Iniciar Automação", command=enviar_dados)
enviar_button.pack(anchor='w', padx=20, pady=10)

# Rodapé
rodape_label = ctk.CTkLabel(
    app,
    text="© 2025 SmartPonto - Desenvolvido por Mateus Toledo Benkenstein",
    font=ctk.CTkFont(size=10),
    text_color="gray"
)
rodape_label.pack(side='bottom', anchor='center', pady=10)

# Execução da aplicação
app.mainloop()
