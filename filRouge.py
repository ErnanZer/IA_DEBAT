import tkinter as tk
from tkinter import ttk 
from tkinter import scrolledtext
from openai import OpenAI
from threading import Thread

class ChatInterface:
    def __init__(self, master):
        self.master = master
        master.title("GPT-3.5 Boite à débat")

        # Changer l'icône de la fenêtre
        master.iconbitmap("logo_jJJ_icon.ico")  # Remplacez "chemin_vers_votre_icone.ico" par le chemin de votre propre icône
        
        # Définition des couleurs
        bg_color = "#404242"  # Gris
        right_text_color = "white"
        left_text_color = "#5bd3eb"

        # Taille minimale de la fenêtre
        master.minsize(600, 500)

        # Zone de texte déroulante pour l'historique du chat
        self.chat_history = scrolledtext.ScrolledText(master, width=50, height=20, bg=bg_color)
        self.chat_history.pack(fill=tk.BOTH, expand=True)  # Remplir et étendre pour s'adapter à la fenêtre

        # Configuration de la couleur du texte pour les rôles
        self.chat_history.tag_config("right", foreground=right_text_color)
        self.chat_history.tag_config("left", foreground=left_text_color)

        # Champ d'entrée pour saisir le message
        self.message_entry = tk.Entry(master, width=50)
        self.message_entry.pack(fill=tk.BOTH)  # Remplir horizontalement

        # Bouton d'envoi
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack()

        # Barre de progression pour le chargement
        self.progress_bar = ttk.Progressbar(master, orient='horizontal', mode='indeterminate')
        self.progress_bar.pack(fill=tk.X)

    def send_message(self):
        user_message = self.message_entry.get()
        self.chat_history.insert(tk.END, "Sujet du débat : " + user_message + "\n", "right")  # Message de droite

        # Afficher le loader
        self.progress_bar.start()

        # Exécuter les requêtes dans un thread séparé pour éviter de bloquer l'interface utilisateur
        Thread(target=self.process_requests, args=(user_message,)).start()

    def process_requests(self, user_message):
        # Envoyer la première requête
        self.client = OpenAI(api_key='')
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un homme/femme politique Français de Droite. Répond au sujet posé."},
                {"role": "user", "content": user_message}
            ]
        )
        ai_response = completion.choices[0].message.content

        # Mettre à jour l'interface utilisateur
        self.master.after(0, lambda: self.update_interface("GPT DE DROITE", ai_response))

        # Envoyer la deuxième requête
        self.client2 = OpenAI(api_key='')
        completion2 = self.client2.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un homme/femme politique Français de Gauche.Répond au sujet posé."},
                {"role": "user", "content": ai_response }
            ]
        )
        ai_response2 = completion2.choices[0].message.content

        # Mettre à jour l'interface utilisateur
        self.master.after(0, lambda: self.update_interface("GPT DE GAUCHE", ai_response2))

        # Arrêter le loader
        self.progress_bar.stop()

    def update_interface(self, sender, message):
        # Ajout du message avec la couleur appropriée
        if sender == "GPT DE DROITE":
            self.chat_history.insert(tk.END, f"\n\n{sender}: {message}\n", ("right" , "bold"))  # Message de droite
        elif sender == "GPT DE GAUCHE":
            self.chat_history.insert(tk.END, f"\n\n{sender}: {message}\n", ("left" , "bold"))  # Message de gauche
        self.message_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    chat_interface = ChatInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()
