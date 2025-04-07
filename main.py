import instaloader
import tkinter as tk
from tkinter import messagebox
import os

def download_data():
    username = entry_username.get().strip()
    password = entry_password.get().strip()
    if not username or not password:
        messagebox.showerror("Błąd", "Wprowadź nazwę użytkownika i hasło.")
        return

    L = instaloader.Instaloader()
    try:
        # Logowanie do Instagrama
        L.login(username, password)
        profile = instaloader.Profile.from_username(L.context, username)
        
        # Pobranie listy obserwujących
        followers_list = [follower.username for follower in profile.get_followers()]
        # Pobranie listy obserwowanych
        following_list = [followee.username for followee in profile.get_followees()]

        # Zapis do plików
        with open("followers.txt", "w", encoding="utf-8") as f:
            for user in followers_list:
                f.write(user + "\n")
        with open("following.txt", "w", encoding="utf-8") as f:
            for user in following_list:
                f.write(user + "\n")

        messagebox.showinfo("Sukces", "Dane zostały pobrane i zapisane do plików!")
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")

def compare_data():
    if not os.path.exists("followers.txt") or not os.path.exists("following.txt"):
        messagebox.showerror("Błąd", "Nie znaleziono plików z danymi. Najpierw pobierz dane!")
        return

    # Odczyt danych z plików
    with open("followers.txt", "r", encoding="utf-8") as f:
        followers = set(line.strip() for line in f if line.strip())
    with open("following.txt", "r", encoding="utf-8") as f:
        following = set(line.strip() for line in f if line.strip())
    
    # Porównanie – wyłonienie różnic
    not_following_back = following - followers
    not_followed_by_you = followers - following

    result_text = "Osoby, które obserwujesz, a które nie obserwują Ciebie:\n"
    result_text += "\n".join(sorted(not_following_back)) if not_following_back else "Brak danych\n"
    result_text += "\n\nOsoby, które obserwują Ciebie, a Ty ich nie obserwujesz:\n"
    result_text += "\n".join(sorted(not_followed_by_you)) if not_followed_by_you else "Brak danych"

    # Wyświetlenie wyniku w nowym oknie
    result_window = tk.Toplevel(root)
    result_window.title("Wynik porównania")
    txt = tk.Text(result_window, wrap="word", width=60, height=20)
    txt.insert("1.0", result_text)
    txt.config(state="disabled")
    txt.pack()

# Konfiguracja głównego okna GUI
root = tk.Tk()
root.title("Instagram API - Pobieranie danych")

# Pola na dane logowania
tk.Label(root, text="Nazwa użytkownika:").grid(row=0, column=0, padx=10, pady=10)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Hasło:").grid(row=1, column=0, padx=10, pady=10)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=10)

# Przyciski do pobierania i porównywania danych
download_button = tk.Button(root, text="Pobierz dane", command=download_data)
download_button.grid(row=2, column=0, padx=10, pady=10)

compare_button = tk.Button(root, text="Porównaj dane", command=compare_data)
compare_button.grid(row=2, column=1, padx=10, pady=10)

root.mainloop()
