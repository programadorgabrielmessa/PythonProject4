import os
import tkinter as tk
from tkinter import messagebox
import webbrowser

class WordPressSearcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscador de Páginas WordPress")
        self.root.geometry("600x400")

        # Frame para caixas de seleção dos discos
        self.drives_frame = tk.Frame(root)
        self.drives_frame.pack(pady=10)

        # Label para os discos
        tk.Label(self.drives_frame, text="Selecione os discos para buscar:").pack()

        # Lista de discos disponíveis
        self.available_drives = [f"{d}:\\" for d in 'CDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(f"{d}:\\")]

        # Dicionário para armazenar as variáveis das caixas de seleção
        self.drive_vars = {}
        for drive in self.available_drives:
            var = tk.BooleanVar(value=True)
            cb = tk.Checkbutton(self.drives_frame, text=drive, variable=var)
            cb.pack(anchor='w')
            self.drive_vars[drive] = var

        # Botões para selecionar todos e desmarcar todos
        self.select_all_button = tk.Button(self.drives_frame, text="Selecionar Todos", command=self.select_all)
        self.select_all_button.pack(side='left', padx=5)

        self.deselect_all_button = tk.Button(self.drives_frame, text="Desmarcar Todos", command=self.deselect_all)
        self.deselect_all_button.pack(side='left', padx=5)

        # Botão para iniciar a busca
        self.search_button = tk.Button(root, text="Buscar Páginas WordPress", command=self.search_wordpress)
        self.search_button.pack(pady=5)

        # Frame para o listbox e barra de rolagem
        self.listbox_frame = tk.Frame(root)
        self.listbox_frame.pack(pady=10, fill='both', expand=True)

        # Barra de rolagem
        self.scrollbar = tk.Scrollbar(self.listbox_frame)
        self.scrollbar.pack(side='right', fill='y')

        # Listbox para mostrar os links
        self.listbox = tk.Listbox(self.listbox_frame, yscrollcommand=self.scrollbar.set, height=10, width=70)
        self.listbox.pack(side='left', fill='both', expand=True)
        self.scrollbar.config(command=self.listbox.yview)

        # Botão para abrir o link selecionado
        self.open_button = tk.Button(root, text="Abrir Selecionado", command=self.open_selected, state='disabled')
        self.open_button.pack(pady=5)

        # Label para status
        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=5)

        # Caminho base do XAMPP (ajuste se necessário)
        self.htdocs_path = r"C:\xampp\htdocs"

    def select_all(self):
        for var in self.drive_vars.values():
            var.set(True)

    def deselect_all(self):
        for var in self.drive_vars.values():
            var.set(False)

    def search_wordpress(self):
        # Limpa os resultados anteriores
        self.listbox.delete(0, tk.END)
        self.open_button.config(state='disabled')
        self.status_label.config(text="Buscando...")

        # Obtém os discos selecionados
        selected_drives = [drive for drive, var in self.drive_vars.items() if var.get()]

        if not selected_drives:
            messagebox.showinfo("Aviso", "Nenhum disco selecionado!")
            self.status_label.config(text="")
            return

        # Diretórios a serem ignorados
        ignore_dirs = ['Windows', 'Program Files', 'Program Files (x86)', 'System Volume Information']

        # Conjunto para armazenar os links únicos
        links_set = set()

        for drive in selected_drives:
            try:
                for root, dirs, files in os.walk(drive, topdown=True):
                    # Pula diretórios ignorados
                    dirs[:] = [d for d in dirs if d not in ignore_dirs]

                    if 'wp-config.php' in files:
                        # Verifica se está dentro de htdocs
                        if root.startswith(self.htdocs_path):
                            # Calcula o caminho relativo a htdocs
                            relative_path = os.path.relpath(root, self.htdocs_path).replace('\\', '/')
                            # Gera os URLs
                            base_url = f"http://localhost/{relative_path}/"
                            admin_url = f"http://localhost/{relative_path}/wp-admin/"
                            links_set.add((base_url, admin_url))
            except Exception as e:
                # Ignora erros e continua
                continue

        # Adiciona os links ao listbox
        for base_url, admin_url in links_set:
            self.listbox.insert(tk.END, f"Página Pública: {base_url}")
            self.listbox.insert(tk.END, f"Área de Admin: {admin_url}")
            self.listbox.insert(tk.END, "")  # Linha em branco para separar

        if links_set:
            self.open_button.config(state='normal')
            self.status_label.config(text="Busca concluída!")
        else:
            self.listbox.insert(tk.END, "Nenhuma instalação do WordPress encontrada.")
            self.status_label.config(text="Nenhuma instalação encontrada.")

    def open_selected(self):
        try:
            selected_index = self.listbox.curselection()[0]
            selected_text = self.listbox.get(selected_index)
            # Extrai o URL após o prefixo
            if "Página Pública: " in selected_text:
                url = selected_text.split("Página Pública: ")[1]
            elif "Área de Admin: " in selected_text:
                url = selected_text.split("Área de Admin: ")[1]
            else:
                raise ValueError("Selecione um link válido.")
            webbrowser.open(url)
        except IndexError:
            messagebox.showinfo("Aviso", "Selecione um link para abrir.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o link: {str(e)}")

def main():
    root = tk.Tk()
    app = WordPressSearcherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()