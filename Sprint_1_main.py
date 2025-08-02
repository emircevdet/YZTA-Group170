import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import hashlib
import json
import datetime
import random
from tkinter import font as tkfont
import google.generativeai as genai
import threading
from dotenv import load_dotenv
import os


class DriveMate:
    def __init__(self, root):
        self.root = root
        self.root.title("DriveMate - Yapay Zeka Destekli Ehliyet Eğitmenin")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Gemini API yapılandırması
        self.setup_gemini_api()
        
        # Veritabanı bağlantısı
        self.init_database()
        
        # Kullanıcı durumu
        self.current_user = None
        self.user_level = None
        
        # Asistan penceresi durumu
        self.assistant_window = None
        self.assistant_visible = False
        
        # Ana pencere stilleri
        self.setup_styles()
        
        # Ana menü
        self.show_main_menu()

    def setup_gemini_api(self):
        """Gemini API'sını yapılandırır"""
        load_dotenv()  # .env dosyasını oku
        API_KEY = os.getenv("GEMINI_API_KEY")  # Anahtarı al
        if not API_KEY:
            raise ValueError("API key bulunamadı! Lütfen .env dosyasına GEMINI_API_KEY yaz.")
        genai.configure(api_key=API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def setup_styles(self):
        """Tkinter stilleri ayarlar"""
        pass
    
    def init_database(self):
        """Veritabanını başlatır"""
        self.conn = sqlite3.connect('ehliyet_app.db')
        self.cursor = self.conn.cursor()
        
        # Kullanıcılar tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Kullanıcı seviyeleri tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_levels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                level INTEGER DEFAULT 1,
                test_score INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Konular tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                question_count INTEGER DEFAULT 0
            )
        ''')
        
        # Sorular tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_id INTEGER,
                question_text TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                difficulty INTEGER DEFAULT 1,
                FOREIGN KEY (topic_id) REFERENCES topics (id)
            )
        ''')
        
        # Test sonuçları tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                topic_id INTEGER,
                score INTEGER,
                total_questions INTEGER,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (topic_id) REFERENCES topics (id)
            )
        ''')
        
        # Kullanıcı ayarları tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                exam_date TEXT,
                avatar_id INTEGER DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Örnek veriler ekle
        self.insert_sample_data()
        
        self.conn.commit()
    
    def insert_sample_data(self):
        """Örnek konular ve sorular ekler"""
        # Konular
        topics = [
            ('Trafik İşaretleri', 'Trafik işaretleri ve anlamları', 20),
            ('Trafik Kuralları', 'Temel trafik kuralları', 25),
            ('Motor ve Araç Bilgisi', 'Araç teknik bilgileri', 15),
            ('İlk Yardım', 'Temel ilk yardım bilgileri', 10),
            ('Çevre Bilgisi', 'Çevre ve trafik', 10)
        ]
        
        for topic in topics:
            self.cursor.execute('''
                INSERT OR IGNORE INTO topics (name, description, question_count)
                VALUES (?, ?, ?)
            ''', topic)
        
        # Örnek sorular
        sample_questions = [
            (1, 'Aşağıdaki trafik işaretlerinden hangisi "Yol Ver" anlamındadır?', 
             'Kırmızı üçgen', 'Mavi daire', 'Sarı eşkenar dörtgen', 'Yeşil kare', 'A', 1),
            (1, 'Hangi trafik işareti "Dur" anlamındadır?',
             'Kırmızı sekizgen', 'Mavi daire', 'Sarı üçgen', 'Yeşil kare', 'A', 1),
            (2, 'Şehir içi yollarda azami hız kaç km/saat olmalıdır?',
             '30 km/saat', '50 km/saat', '70 km/saat', '90 km/saat', 'B', 1),
            (2, 'Kavşaklarda ilk geçiş hakkı hangi araçlarındır?',
             'Özel araçların', 'Toplu taşıma araçlarının', 'Acil durum araçlarının', 'Ticari araçların', 'C', 1),
            (3, 'Motor yağı hangi durumda değiştirilmelidir?',
             'Her 1000 km\'de', 'Her 5000 km\'de', 'Her 10000 km\'de', 'Her 20000 km\'de', 'C', 1),
            (3, 'Lastik hava basıncı ne zaman kontrol edilmelidir?',
             'Her gün', 'Her hafta', 'Her ay', 'Her 6 ayda', 'B', 1),
            (4, 'Kazazedenin bilinci kapalı ise ilk yapılacak işlem nedir?',
             'Kalp masajı', 'Sunni teneffüs', 'ABC kontrolü', 'Kanama durdurma', 'C', 1),
            (4, 'Hangi durumda turnike uygulanır?',
             'Her kanamada', 'Sadece atardamar kanamalarında', 'Sadece toplardamar kanamalarında', 'Hiçbir zaman', 'B', 1),
            (5, 'Egzoz gazları hangi çevre sorununa neden olur?',
             'Su kirliliği', 'Hava kirliliği', 'Toprak kirliliği', 'Gürültü kirliliği', 'B', 1),
            (5, 'Araç bakımı hangi çevre sorununu önler?',
             'Su kirliliği', 'Hava kirliliği', 'Toprak kirliliği', 'Gürültü kirliliği', 'B', 1)
        ]
        
        for question in sample_questions:
            self.cursor.execute('''
                INSERT OR IGNORE INTO questions 
                (topic_id, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', question)
        
        self.conn.commit()
    
    def clear_window(self):
        """Pencereyi temizler"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_main_menu(self):
        """Ana menüyü gösterir"""
        self.clear_window()

        # Başlık ve alt başlık
        title_label = tk.Label(self.root, text="DriveMate", font=("Arial", 36, "bold"), fg="#222", bg="#f0f0f0")
        title_label.pack(pady=(40, 0))
        subtitle_label = tk.Label(self.root, text="Yapay Zeka Destekli Ehliyet Eğitmenin", font=("Arial", 18), fg="#444", bg="#f0f0f0")
        subtitle_label.pack(pady=(0, 30))
        # Menü kutusu (Frame)
        menu_box = tk.Frame(self.root, bg="white", bd=0, relief="flat", highlightthickness=0)
        menu_box.pack(pady=10)
        menu_box.place(relx=0.5, rely=0.5, anchor="center", width=400, height=420)
        menu_box.configure(highlightbackground="#ddd", highlightcolor="#ddd")
        menu_box.pack_propagate(False)
        

        if self.current_user:
            # Kullanıcı giriş yapmış
            btn1 = tk.Button(menu_box, text="Konular", command=self.show_topics, font=("Arial", 14, "bold"), bg="#222", fg="white", relief="flat", height=2)
            btn1.pack(fill="x", padx=40, pady=(40, 10))
        
            btn2 = tk.Button(menu_box, text="Seviye Belirleme Testi", command=self.show_level_test, font=("Arial", 14, "bold"), bg="#222", fg="white", relief="flat", height=2)
            btn2.pack(fill="x", padx=40, pady=10)
        
            btn3 = tk.Button(menu_box, text="DriveMate'e Sor", command=self.show_drivemate_chat, font=("Arial", 14, "bold"), bg="#222", fg="white", relief="flat", height=2)
            btn3.pack(fill="x", padx=40, pady=10)
        
            btn4 = tk.Button(menu_box, text="Profil", command=self.show_profile, font=("Arial", 14, "bold"), bg="#222", fg="white", relief="flat", height=2)
            btn4.pack(fill="x", padx=40, pady=10)
        
            btn5 = tk.Button(menu_box, text="Çıkış Yap", command=self.logout, font=("Arial", 14, "bold"), bg="#e74c3c", fg="white", relief="flat", height=2)
            btn5.pack(fill="x", padx=40, pady=(10, 0))
        
        else:
            # Kullanıcı giriş yapmamış
           btn1 = tk.Button(menu_box, text="Giriş Yap", command=self.show_login, font=("Arial", 14, "bold"), bg="#222", fg="white", relief="flat", height=2)
           btn1.pack(fill="x", padx=40, pady=(70, 10))
           btn2 = tk.Button(menu_box, text="Kayıt Ol", command=self.show_register, font=("Arial", 14, "bold"), bg="#222", fg="white", relief="flat", height=2)
           btn2.pack(fill="x", padx=40, pady=10) 
            
    def show_drivemate_chat(self):
        """DriveMate sohbet sayfasını gösterir"""
        self.clear_window()
        
        drivemate_topic = {
            "name": "DriveMate - Ehliyet Asistanı",
            "description": "Ehliyet ve trafik konularında genel yardımcınız",
            "system_prompt": """Sen DriveMate, kapsamlı bir ehliyet ve trafik asistanısın. 
            Kullanıcılara tüm ehliyet konularında yardım edebilirsin:
            - Trafik işaretleri ve kuralları
            - Araç tekniği ve bakımı  
            - İlk yardım bilgileri
            - Trafik adabı ve görgü kuralları
            - Ehliyet sınavı hazırlığı
            - Sürücü kursu süreçleri
            
            Türkiye trafik kurallarına göre doğru, güncel ve anlaşılır bilgiler ver.
            Samimi, yardımsever ve eğitici bir dil kullan. Örneklerle açıkla."""
        }
        
        self.show_chatbot_interface(drivemate_topic)
        # Sohbet arayüzü burada implement edilecek
    

    def show_register(self):
        """Kayıt sayfasını gösterir"""
        self.clear_window()

        # Başlık ve alt başlık
        title_label = tk.Label(self.root, text="DriveMate", font=("Arial", 36, "bold"), fg="#222", bg="#f0f0f0")
        title_label.pack(pady=(40, 0))
        subtitle_label = tk.Label(self.root, text="Yapay Zeka Destekli Ehliyet Eğitmenin", font=("Arial", 18), fg="#444", bg="#f0f0f0")
        subtitle_label.pack(pady=(0, 30))

        # Form kutusu (Frame)
        form_box = tk.Frame(self.root, bg="white", bd=0, relief="flat", highlightthickness=0)
        form_box.pack(pady=10)
        form_box.place(relx=0.5, rely=0.5, anchor="center", width=380, height=340)
        form_box.configure(highlightbackground="#ddd", highlightcolor="#ddd")
        form_box.pack_propagate(False)

        # E-posta
        email_label = tk.Label(form_box, text="E-posta", font=("Arial", 12), bg="white", anchor="w")
        email_label.pack(fill="x", padx=30, pady=(30, 0))
        email_entry = tk.Entry(form_box, font=("Arial", 12), bg="#f7f7f7", relief="flat", highlightthickness=1, highlightbackground="#ccc")
        email_entry.pack(fill="x", padx=30, pady=(0, 10))

        # Şifre
        password_label = tk.Label(form_box, text="Şifre", font=("Arial", 12), bg="white", anchor="w")
        password_label.pack(fill="x", padx=30, pady=(0, 0))
        password_entry = tk.Entry(form_box, font=("Arial", 12), show="*", bg="#f7f7f7", relief="flat", highlightthickness=1, highlightbackground="#ccc")
        password_entry.pack(fill="x", padx=30, pady=(0, 10))

        # Şifre tekrar
        password_confirm_label = tk.Label(form_box, text="Şifre Tekrar)", font=("Arial", 12), bg="white", anchor="w")
        password_confirm_label.pack(fill="x", padx=30, pady=(0, 0))
        password_confirm_entry = tk.Entry(form_box, font=("Arial", 12), show="*", bg="#f7f7f7", relief="flat", highlightthickness=1, highlightbackground="#ccc")
        password_confirm_entry.pack(fill="x", padx=30, pady=(0, 20))

        # Kayıt butonu
        def register():
            email = email_entry.get().strip()
            password = password_entry.get()
            password_confirm = password_confirm_entry.get()
            if not email or not password:
                messagebox.showerror("Hata", "Tüm alanları doldurun!")
                return
            if password != password_confirm:
                messagebox.showerror("Hata", "Şifreler eşleşmiyor!")
                return
            if len(password) < 6:
                messagebox.showerror("Hata", "Şifre en az 6 karakter olmalıdır!")
                return
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            try:
                self.cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
                self.conn.commit()
                messagebox.showinfo("Başarılı", "Kayıt başarıyla tamamlandı!")
                self.show_login()
            except sqlite3.IntegrityError:
                messagebox.showerror("Hata", "Bu e-posta adresi zaten kullanılıyor!")

        register_btn = tk.Button(form_box, text="Sign Up", command=register, font=("Arial", 13, "bold"), bg="#222", fg="white", relief="flat", height=2)
        register_btn.pack(fill="x", padx=30, pady=(0, 10))

        # Girişe dön linki
        login_link = tk.Label(form_box, text="Already have an account? Sign In", font=("Arial", 10, "underline"), fg="#0077cc", bg="white", cursor="hand2")
        login_link.pack(pady=(0, 10))
        login_link.bind("<Button-1>", lambda e: self.show_login())

    def show_login(self):
        """Giriş sayfasını gösterir"""
        self.clear_window()

        # Başlık ve alt başlık
        title_label = tk.Label(self.root, text="DriveMate", font=("Arial", 36, "bold"), fg="#222", bg="#f0f0f0")
        title_label.pack(pady=(40, 0))
        subtitle_label = tk.Label(self.root, text="Yapay Zeka Destekli Ehliyet Eğitmenin", font=("Arial", 18), fg="#444", bg="#f0f0f0")
        subtitle_label.pack(pady=(0, 30))

        # Form kutusu (Frame)
        form_box = tk.Frame(self.root, bg="white", bd=0, relief="flat", highlightthickness=0)
        form_box.pack(pady=10)
        form_box.place(relx=0.5, rely=0.5, anchor="center", width=380, height=270)
        form_box.configure(highlightbackground="#ddd", highlightcolor="#ddd")
        form_box.pack_propagate(False)

        # E-posta
        email_label = tk.Label(form_box, text="E-posta", font=("Arial", 12), bg="white", anchor="w")
        email_label.pack(fill="x", padx=30, pady=(30, 0))
        email_entry = tk.Entry(form_box, font=("Arial", 12), bg="#f7f7f7", relief="flat", highlightthickness=1, highlightbackground="#ccc")
        email_entry.pack(fill="x", padx=30, pady=(0, 10))

        # Şifre
        password_label = tk.Label(form_box, text="Şifre", font=("Arial", 12), bg="white", anchor="w")
        password_label.pack(fill="x", padx=30, pady=(0, 0))
        password_entry = tk.Entry(form_box, font=("Arial", 12), show="*", bg="#f7f7f7", relief="flat", highlightthickness=1, highlightbackground="#ccc")
        password_entry.pack(fill="x", padx=30, pady=(0, 20))

        # Giriş butonu
        def login():
            email = email_entry.get().strip()
            password = password_entry.get()
            if not email or not password:
                messagebox.showerror("Hata", "Tüm alanları doldurun!")
                return
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.cursor.execute('SELECT id, email FROM users WHERE email = ? AND password = ?', (email, hashed_password))
            user = self.cursor.fetchone()
            if user:
                self.current_user = {'id': user[0], 'email': user[1]}
                messagebox.showinfo("Başarılı", f"Hoş geldiniz, {user[1]}!")
                self.show_main_menu()
            else:
                messagebox.showerror("Hata", "E-posta veya şifre hatalı!")

        login_btn = tk.Button(form_box, text="Giriş Yap", command=login, font=("Arial", 13, "bold"), bg="#222", fg="white", relief="flat", height=2)
        login_btn.pack(fill="x", padx=30, pady=(0, 10))

        # Şifremi unuttum linki 
        forgot_link = tk.Label(form_box, text="Şifremi Unuttum", font=("Arial", 10, "underline"), fg="#0077cc", bg="white", cursor="hand2")
        forgot_link.pack(pady=(0, 10))
        forgot_link.bind("<Button-1>", lambda e: self.show_forgot_password())

    def show_forgot_password(self):
        """Şifremi unuttum sayfasını gösterir"""
        self.clear_window()

        # Başlık ve alt başlık
        title_label = tk.Label(self.root, text="DriveMate", font=("Arial", 36, "bold"), fg="#222", bg="#f0f0f0")
        title_label.pack(pady=(40, 0))
        subtitle_label = tk.Label(self.root, text="Şifre Sıfırlama", font=("Arial", 18), fg="#444", bg="#f0f0f0")
        subtitle_label.pack(pady=(0, 30))

        # Form kutusu
        form_box = tk.Frame(self.root, bg="white", bd=0, relief="flat", highlightthickness=0)
        form_box.pack(pady=10)
        form_box.place(relx=0.5, rely=0.5, anchor="center", width=380, height=300)
        form_box.configure(highlightbackground="#ddd", highlightcolor="#ddd")
        form_box.pack_propagate(False)

        # Açıklama
        info_label = tk.Label(form_box, text="E-posta adresinizi girin, yeni şifrenizi belirleyin:", 
                         font=("Arial", 12), bg="white", fg="#666", wraplength=320)
        info_label.pack(pady=(30, 20), padx=30)

        # E-posta
        email_label = tk.Label(form_box, text="Email", font=("Arial", 12), bg="white", anchor="w")
        email_label.pack(fill="x", padx=30, pady=(0, 0))
        email_entry = tk.Entry(form_box, font=("Arial", 12), bg="#f7f7f7", relief="flat", highlightthickness=1, highlightbackground="#ccc")
        email_entry.pack(fill="x", padx=30, pady=(0, 10))

        # Yeni şifre
        new_password_label = tk.Label(form_box, text="Yeni Şifre", font=("Arial", 12), bg="white", anchor="w")
        new_password_label.pack(fill="x", padx=30, pady=(0, 0))
        new_password_entry = tk.Entry(form_box, font=("Arial", 12), show="*", bg="#f7f7f7", relief="flat", highlightthickness=1, highlightbackground="#ccc")
        new_password_entry.pack(fill="x", padx=30, pady=(0, 20))

        # Şifre sıfırlama butonu
        def reset_password():
            email = email_entry.get().strip()
            new_password = new_password_entry.get()
            
            if not email or not new_password:
                messagebox.showerror("Hata", "Tüm alanları doldurun!")
                return
            
            if len(new_password) < 6:
                messagebox.showerror("Hata", "Şifre en az 6 karakter olmalıdır!")
                return
            
            # Kullanıcının var olup olmadığını kontrol et
            self.cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
            user = self.cursor.fetchone()
            
            if not user:
                messagebox.showerror("Hata", "Bu e-posta adresi kayıtlı değil!")
                return
            
            # Şifreyi güncelle
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            self.cursor.execute('UPDATE users SET password = ? WHERE email = ?', (hashed_password, email))
            self.conn.commit()
            
            messagebox.showinfo("Başarılı", "Şifreniz başarıyla güncellendi!")
            self.show_login()

        reset_btn = tk.Button(form_box, text="Şifreyi Sıfırla", command=reset_password, 
                             font=("Arial", 13, "bold"), bg="#0077cc", fg="white", relief="flat", height=2)
        reset_btn.pack(fill="x", padx=30, pady=(0, 10))

        # Kayıt ol linki
        register_link = tk.Label(form_box, text="Don't have an account? Sign Up", font=("Arial", 10, "underline"), fg="#0077cc", bg="white", cursor="hand2")
        register_link.pack(pady=(0, 10))
        register_link.bind("<Button-1>", lambda e: self.show_register())
        # Girişe dön linki
        login_link = tk.Label(form_box, text="← Giriş sayfasına dön", font=("Arial", 10, "underline"), 
                             fg="#0077cc", bg="white", cursor="hand2")
        login_link.pack(pady=(0, 10))
        login_link.bind("<Button-1>", lambda e: self.show_login())

        
    
    def logout(self):
        """Çıkış yapar"""
        self.current_user = None
        self.user_level = None
        self.show_main_menu()
    
    def show_topics(self):
        """Konuların listelendiği sayfayı gösterir"""
        self.clear_window()

        # Başlık ve alt başlık
        title_label = tk.Label(self.root, text="Konular", font=("Arial", 32, "bold"), fg="#222", bg="#f0f0f0")
        title_label.pack(pady=(40, 0))
        subtitle_label = tk.Label(self.root, text="Hedefine bir adım daha yaklaş! Konulardan birini seç, öğrenmeye başla.", font=("Arial", 16), fg="#444", bg="#f0f0f0")
        subtitle_label.pack(pady=(0, 30))

        # Ana çerçeve - Ortalama için relx, rely kullanıyoruz
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8, relheight=0.6)

        # Canvas ve scrollbar
        canvas = tk.Canvas(main_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        
        # Scrollable frame
        scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")
        
        # Canvas içeriğini yapılandır
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Canvas ve scrollbar'ı yerleştir
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Canvas içine scrollable frame'i yerleştir
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mouse wheel ile scroll etmeyi etkinleştir
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Konu bilgileri - Yeni konular ve açıklamalar
        topics = [
            {
                "id": 1,
                "name": "Trafik ve Çevre Bilgisi",
                "description": "Trafik levhalarını sadece ezberleme, ne anlama geldiklerini öğren ve yolda bir adım önde ol!",
                "question_count": 25,
                "color": "#3498db",  # Mavi
                "icon": "🛣️"
            },
            {
                "id": 2,
                "name": "Araç Tekniği",
                "description": "Motorun nasıl çalıştığını, araç bakımını ve teknik detayları sade anlatımlarla öğren.",
                "question_count": 20,
                "color": "#e74c3c",  # Kırmızı
                "icon": "🔧"
            },
            {
                "id": 3,
                "name": "İlk Yardım Bilgisi",
                "description": "Kazalarda ilk müdahaleyi nasıl yapacağını, temel ilk yardım adımlarını pratik bilgilerle öğren.",
                "question_count": 15,
                "color": "#2ecc71",  # Yeşil
                "icon": "🚑"
            },
            {
                "id": 4,
                "name": "Trafik Adabı",
                "description": "Görgü kurallarını öğren, sadece iyi bir sürücü değil, örnek bir vatandaş ol!",
                "question_count": 10,
                "color": "#9b59b6",  # Mor
                "icon": "📋"
            }
        ]
        
        # Her konu için kart oluştur - Ekran görüntüsüne benzer düzen
        for topic in topics:
            # Kart çerçevesi - Genişliği sabit tutuyoruz
            card_frame = tk.Frame(scrollable_frame, bg=topic["color"], bd=0)
            card_frame.pack(fill="x", pady=10, padx=10)
            
            # İç içerik çerçevesi - Yüksekliği sabit
            inner_frame = tk.Frame(card_frame, bg=topic["color"], padx=20, pady=15)
            inner_frame.pack(fill="x")
            
            # Sol taraf (ikon)
            icon_frame = tk.Frame(inner_frame, bg=topic["color"], width=60)
            icon_frame.pack(side="left", fill="y")
            icon_frame.pack_propagate(False)  # Sabit genişlik için
            
            # İkon
            icon_label = tk.Label(
                icon_frame, 
                text=topic["icon"], 
                font=("Arial", 24), 
                bg=topic["color"], 
                fg="white"
            )
            icon_label.pack(expand=True)
            
            # Başlık ve açıklama kısmı
            content_frame = tk.Frame(inner_frame, bg=topic["color"])
            content_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
            
            # Konu adı - Tam genişlikte
            name_label = tk.Label(
                content_frame, 
                text=topic["name"], 
                font=("Arial", 18, "bold"), 
                bg=topic["color"], 
                fg="white",
                anchor="w"
            )
            name_label.pack(fill="x", anchor="w")
            
            # Konu açıklaması
            desc_label = tk.Label(
                content_frame, 
                text=topic["description"], 
                font=("Arial", 12), 
                bg=topic["color"], 
                fg="white",
                wraplength=500,
                justify="left",
                anchor="w"
            )
            desc_label.pack(fill="x", anchor="w", pady=(5, 0))
            
            # Soru sayısı
            question_label = tk.Label(
                content_frame, 
                text=f"Soru Sayısı: {topic['question_count']}", 
                font=("Arial", 12, "italic"), 
                bg=topic["color"], 
                fg="white",
                anchor="w"
            )
            question_label.pack(fill="x", anchor="w", pady=(5, 0))
            
            # Sağ taraf (butonlar)
            right_frame = tk.Frame(inner_frame, bg=topic["color"], width=100)
            right_frame.pack(side="right", fill="y")
            
            # Butonlar
            study_btn = tk.Button(
                right_frame, 
                text="Öğren", 
                command=lambda t=topic["id"]: self.show_topic_content(t),
                font=("Arial", 12, "bold"), 
                bg="white", 
                fg=topic["color"], 
                relief="flat",
                width=8
            )
            study_btn.pack(pady=(0, 5))
            
            test_btn = tk.Button(
                right_frame, 
                text="Pratik Yap", 
                command=lambda t=topic["id"]: self.start_topic_test(t),
                font=("Arial", 12, "bold"), 
                bg="white", 
                fg=topic["color"], 
                relief="flat",
                width=8
            )
            test_btn.pack()
        
        # Alt menü - Sabit pozisyonda
        bottom_frame = tk.Frame(self.root, bg="#f0f0f0")
        bottom_frame.place(relx=0.5, rely=0.9, anchor="center")
        
        # Ana menüye dön butonu
        back_btn = tk.Button(
            bottom_frame, 
            text="Ana Menüye Dön", 
            command=self.show_main_menu,
            font=("Arial", 12, "bold"), 
            bg="#222", 
            fg="white", 
            relief="flat",
            height=2,
            width=15
        )
        back_btn.pack(pady=10)
    
    def show_topic_content(self, topic_id):
        """Konu içeriğini chatbot ile gösterir"""
        # Konu bilgilerini al
        topic_info = {
            1: {
                "name": "Trafik ve Çevre Bilgisi",
                "description": "Trafik işaretleri, yol kuralları ve çevre bilgisi",
                "system_prompt": """Sen bir ehliyet kursu eğitmenisin. Trafik ve Çevre Bilgisi konusunda uzmanlaşmışsın. 
                Kullanıcılara trafik işaretleri, yol kuralları, çevre bilgisi konularında yardım edeceksin.
                Açıklamalarını sade, anlaşılır ve örneklerle destekleyerek yap. Türkiye trafik kurallarına göre bilgi ver."""
            },
            2: {
                "name": "Araç Tekniği",
                "description": "Motor bilgisi, araç bakımı ve teknik konular",
                "system_prompt": """Sen bir ehliyet kursu eğitmenisin. Araç Tekniği konusunda uzmanlaşmışsın.
                Kullanıcılara motor çalışması, araç bakımı, teknik arızalar konularında yardım edeceksin.
                Teknik konuları basit dille anlatarak herkesin anlayabileceği şekilde açıkla."""
            },
            3: {
                "name": "İlk Yardım Bilgisi",
                "description": "Temel ilk yardım ve acil durum müdahaleleri",
                "system_prompt": """Sen bir ehliyet kursu eğitmenisin. İlk Yardım konusunda uzmanlaşmışsın.
                            Kullanıcılara temel ilk yardım, kaza anında müdahale, yaralı taşıma konularında yardım edeceksin.
                Hayati önem taşıyan bilgileri net ve uygulanabilir şekilde anlat."""
            },
            4: {
                "name": "Trafik Adabı",
                "description": "Trafik görgü kuralları ve etik davranışlar",
                "system_prompt": """Sen bir ehliyet kursu eğitmenisin. Trafik Adabı konusunda uzmanlaşmışsın.
                Kullanıcılara trafik görgüsü, saygılı sürücülük, etik davranışlar konularında yardım edeceksin.
                Toplumsal sorumluluk bilincini geliştirici örnekler ver."""
            }
        }
        
        if topic_id not in topic_info:
            messagebox.showerror("Hata", "Konu bulunamadı!")
            return
        
        topic = topic_info[topic_id]
        self.show_chatbot_interface(topic)
    
    def show_chatbot_interface(self, topic):
        """Chatbot arayüzünü gösterir"""
        self.clear_window()
        
        # Başlık
        title_label = tk.Label(self.root, text=f"🤖 {topic['name']} Öğretmeni", 
                              font=("Arial", 24, "bold"), fg="#222", bg="#f0f0f0")
        title_label.pack(pady=(20, 10))
        
        # Alt başlık
        subtitle_label = tk.Label(self.root, text=topic['description'], 
                                 font=("Arial", 14), fg="#444", bg="#f0f0f0")
        subtitle_label.pack(pady=(0, 20))
        
        # Ana çerçeve
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Chat geçmişi alanı
        chat_frame = tk.Frame(main_frame, bg="white", relief="solid", bd=1)
        chat_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Scrollable text widget
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, 
            wrap=tk.WORD, 
            font=("Arial", 11),
            bg="white",
            fg="#333",
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.chat_display.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Mesaj giriş alanı
        input_frame = tk.Frame(main_frame, bg="#f0f0f0")
        input_frame.pack(fill="x", pady=(0, 10))
        
        # Mesaj giriş kutusu
        self.message_entry = tk.Text(
            input_frame, 
            height=3, 
            font=("Arial", 11),
            wrap=tk.WORD,
            relief="solid",
            bd=1
        )
        self.message_entry.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Gönder butonu
        send_btn = tk.Button(
            input_frame,
            text="Gönder",
            command=lambda: self.send_message(topic),
            font=("Arial", 12, "bold"),
            bg="#0077cc",
            fg="white",
            relief="flat",
            width=10,
            height=3
        )
        send_btn.pack(side="right")
        
        # Enter tuşu ile gönderme
        self.message_entry.bind("<Control-Return>", lambda e: self.send_message(topic))
        
        # Alt butonlar
        bottom_frame = tk.Frame(main_frame, bg="#f0f0f0")
        bottom_frame.pack(fill="x")
        
        # Konulara dön butonu
        back_btn = tk.Button(
            bottom_frame,
            text="← Konulara Dön",
            command=self.show_topics,
            font=("Arial", 12),
            bg="#666",
            fg="white",
            relief="flat",
            padx=20
        )
        back_btn.pack(side="left")
        
        # Sohbeti temizle butonu
        clear_btn = tk.Button(
            bottom_frame,
            text="Sohbeti Temizle",
            command=self.clear_chat,
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            relief="flat",
            padx=20
        )
        clear_btn.pack(side="right")
        
        # Chat geçmişini başlat
        self.chat_history = []
        self.current_topic = topic
        
        # Hoş geldin mesajı
        welcome_msg = f"Merhaba! Ben {topic['name']} konusunda size yardımcı olacak sanal eğitmeninizim. 🎓\n\nBu konuda merak ettiğiniz her şeyi sorabilirsiniz. Hangi konudan başlamak istersiniz?"
        self.add_message_to_chat("Eğitmen", welcome_msg, "#0077cc")
        
        # Focus'u mesaj kutusuna ver
        self.message_entry.focus()
    
    def add_message_to_chat(self, sender, message, color="#333"):
        """Chat'e mesaj ekler"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Zaman damgası
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        # Gönderen bilgisi
        self.chat_display.insert(tk.END, f"\n{sender} ({timestamp}):\n", "sender")
        self.chat_display.tag_config("sender", font=("Arial", 10, "bold"), foreground=color)
        
        # Mesaj içeriği
        self.chat_display.insert(tk.END, f"{message}\n", "message")
        self.chat_display.tag_config("message", font=("Arial", 11), foreground="#333")
        
        # Ayırıcı çizgi
        self.chat_display.insert(tk.END, "─" * 50 + "\n", "separator")
        self.chat_display.tag_config("separator", foreground="#ddd")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def send_message(self, topic):
        """Kullanıcı mesajını gönderir ve AI yanıtı alır"""
        user_message = self.message_entry.get("1.0", tk.END).strip()
        
        if not user_message:
            return
        
        # Kullanıcı mesajını chat'e ekle
        self.add_message_to_chat("Siz", user_message, "#27ae60")
        
        # Mesaj kutusunu temizle
        self.message_entry.delete("1.0", tk.END)
        
        # "Yazıyor..." mesajı göster
        self.add_message_to_chat("Eğitmen", "Yazıyor... ⏳", "#999")
        
        # AI yanıtını ayrı thread'de al
        threading.Thread(target=self.get_ai_response, args=(user_message, topic), daemon=True).start()
    
    def get_ai_response(self, user_message, topic):
        """AI'dan yanıt alır"""
        try:
            # Chat geçmişini oluştur
            conversation = f"{topic['system_prompt']}\n\n"
            
            # Önceki mesajları ekle (son 10 mesaj)
            for msg in self.chat_history[-10:]:
                conversation += f"{msg['role']}: {msg['content']}\n"
            
            # Mevcut kullanıcı mesajını ekle
            conversation += f"Kullanıcı: {user_message}\nEğitmen:"
            
            # Gemini'den yanıt al
            response = self.model.generate_content(conversation)
            ai_response = response.text
            
            # Chat geçmişine ekle
            self.chat_history.append({"role": "Kullanıcı", "content": user_message})
            self.chat_history.append({"role": "Eğitmen", "content": ai_response})
            
            # UI'ı ana thread'de güncelle
            self.root.after(0, self.update_chat_with_response, ai_response)
            
        except Exception as e:
            error_msg = f"Üzgünüm, bir hata oluştu: {str(e)}\nLütfen tekrar deneyin."
            self.root.after(0, self.update_chat_with_response, error_msg)
    
    def update_chat_with_response(self, response):
        """AI yanıtı ile chat'i günceller"""
        # "Yazıyor..." mesajını kaldır
        self.chat_display.config(state=tk.NORMAL)
        content = self.chat_display.get("1.0", tk.END)
        lines = content.split('\n')
        
        # Son "Yazıyor..." mesajını bul ve kaldır
        for i in range(len(lines)-1, -1, -1):
            if "Yazıyor... ⏳" in lines[i]:
                # Bu satırdan itibaren sil
                line_start = len('\n'.join(lines[:i]))
                self.chat_display.delete(f"1.0+{line_start}c", tk.END)
                break
        
        self.chat_display.config(state=tk.DISABLED)
        
        # AI yanıtını ekle
        self.add_message_to_chat("Eğitmen", response, "#0077cc")
    
    def clear_chat(self):
        """Sohbet geçmişini temizler"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete("1.0", tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # Chat geçmişini sıfırla
        self.chat_history = []
        
        # Hoş geldin mesajını tekrar göster
        welcome_msg = f"Merhaba! Ben {self.current_topic['name']} konusunda size yardımcı olacak sanal eğitmeninizim. 🎓\n\nBu konuda merak ettiğiniz her şeyi sorabilirsiniz. Hangi konudan başlamak istersiniz?"
        self.add_message_to_chat("Eğitmen", welcome_msg, "#0077cc")
    
    def show_level_test(self):
        """Seviye belirleme testini gösterir"""
        self.clear_window()
        
        # Başlık
        title_label = tk.Label(self.root, text="Seviye Belirleme Testi", font=("Arial", 32, "bold"), fg="#222", bg="#f0f0f0")
        title_label.pack(pady=20)
        
        # Test açıklaması
        desc_label = tk.Label(self.root, text="Bu test 20 sorudan oluşur ve seviyenizi belirler.\nSorular Gemini AI tarafından özel olarak hazırlanır.", font=("Arial", 16), fg="#444", bg="#f0f0f0")
        desc_label.pack(pady=10)
        
        # Test başlatma butonu - start_level_test metodunu çağır
        start_btn = tk.Button(self.root, text="Teste Başla", command=self.start_level_test, font=("Arial", 14, "bold"), bg="#0077cc", fg="white", relief="flat", height=2, width=15)
        start_btn.pack(pady=30)

        # Geri dön butonu
        back_btn = tk.Button(self.root, text="Ana Menüye Dön", command=self.show_main_menu, font=("Arial", 12), bg="#666", fg="white", relief="flat", height=2, width=15)
        back_btn.pack(pady=20)
    
    def start_level_test(self):
        """Seviye belirleme testini başlatır - Gemini AI ile"""
        # Kullanıcı kontrolü
        if not self.current_user:
            messagebox.showerror("Hata", "Lütfen önce giriş yapın!")
            self.show_login()
            return
        
        # Loading mesajı göster
        self.show_loading_screen("Sorular hazırlanıyor...")
        
        # AI'dan soruları ayrı thread'de al
        threading.Thread(target=self.generate_level_test_questions, daemon=True).start()

    def generate_level_test_questions(self):
        """Gemini AI ile seviye belirleme testi soruları üretir"""
        try:
            prompt = """
            Türkiye ehliyet sınavı için 20 adet çoktan seçmeli soru hazırla. Sorular şu konulardan olsun:
            - Trafik işaretleri ve kuralları (8 soru)
            - Araç tekniği ve bakımı (4 soru) 
            - İlk yardım bilgisi (4 soru)
            - Trafik adabı ve çevre bilgisi (4 soru)
            
            Her soru için:
            - Soru metni
            - 4 seçenek (A, B, C, D)
            - Doğru cevap harfi
            - Zorluk seviyesi (1-3 arası)
            
            JSON formatında döndür:
            {
                "questions": [
                    {
                        "question": "Soru metni",
                        "options": {
                            "A": "Seçenek A",
                            "B": "Seçenek B", 
                            "C": "Seçenek C",
                            "D": "Seçenek D"
                        },
                        "correct": "A",
                        "difficulty": 2,
                        "topic": "Trafik İşaretleri"
                    }
                ]
            }
            
            Soruları Türkiye trafik kurallarına göre hazırla. Güncel ve doğru bilgiler kullan.
            """
            
            response = self.model.generate_content(prompt)
            
            # JSON parse et
            import json
            import re
            
            # JSON kısmını çıkar
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                questions_data = json.loads(json_str)
                
                # Soruları uygun formata çevir
                formatted_questions = []
                for q in questions_data.get('questions', []):
                    formatted_q = (
                        0,  # id
                        q['question'],  # question_text
                        q['options']['A'],  # option_a
                        q['options']['B'],  # option_b
                        q['options']['C'],  # option_c
                        q['options']['D'],  # option_d
                        q['correct'],  # correct_answer
                        q.get('difficulty', 2)  # difficulty
                    )
                    formatted_questions.append(formatted_q)
                
                # UI'ı ana thread'de güncelle
                self.root.after(0, self.start_generated_test, formatted_questions)
            else:
                raise Exception("JSON formatı bulunamadı")
                
        except Exception as e:
            error_msg = f"Sorular oluşturulurken hata: {str(e)}"
            self.root.after(0, self.show_test_error, error_msg)

    def show_loading_screen(self, message):
        """Modern yükleme ekranı gösterir"""
        self.clear_window()
        
        # Ana container
        main_container = tk.Frame(self.root, bg="#f0f0f0")
        main_container.pack(fill="both", expand=True)
        
        # Ortalama frame
        center_frame = tk.Frame(main_container, bg="#f0f0f0")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Modern kart tasarımı
        card_frame = tk.Frame(center_frame, bg="white", relief="flat", bd=0)
        card_frame.pack(padx=40, pady=40)
        
        # Gölge efekti için arka plan
        shadow_frame = tk.Frame(center_frame, bg="#e0e0e0", relief="flat", bd=0)
        shadow_frame.place(in_=card_frame, x=3, y=3, relwidth=1, relheight=1)
        card_frame.lift()
        
        # İçerik alanı
        content_frame = tk.Frame(card_frame, bg="white", padx=60, pady=50)
        content_frame.pack()
        
        # AI ikonu
        ai_icon = tk.Label(content_frame, text="🤖", font=("Arial", 48), bg="white", fg="#0077cc")
        ai_icon.pack(pady=(0, 20))
        
        # Başlık
        title_label = tk.Label(content_frame, text="Sınava hazır mısın?", 
                              font=("Arial", 24, "bold"), fg="#222", bg="white")
        title_label.pack(pady=(0, 10))
        
        # Alt başlık
        subtitle_label = tk.Label(content_frame, text="DriveMate sana özel sorular hazırlıyor", 
                                 font=("Arial", 14), fg="#666", bg="white")
        subtitle_label.pack(pady=(0, 30))
        
        # Modern progress bar container
        progress_container = tk.Frame(content_frame, bg="white")
        progress_container.pack(pady=(0, 20))
        
        # Progress bar arka planı
        progress_bg = tk.Canvas(progress_container, width=300, height=6, bg="#e9ecef", 
                               highlightthickness=0, relief="flat")
        progress_bg.pack()
        
        # Progress bar
        self.progress_fill = progress_bg.create_rectangle(0, 0, 0, 6, fill="#ffa600", width=0)
        
        # Loading mesajı
        self.loading_message = tk.Label(content_frame, text=message, 
                                       font=("Arial", 12), fg="#666", bg="white")
        self.loading_message.pack(pady=(10, 0))
        
        # Animasyon değişkenleri
        self.loading_dots = 0
        self.progress_width = 0
        self.progress_direction = 1
        
        # Animasyonları başlat
        self.animate_modern_loading(progress_bg)

    def animate_modern_loading(self, progress_bg):
        """Modern loading animasyonu"""
        if hasattr(self, 'loading_message') and self.loading_message.winfo_exists():
            # Dots animasyonu
            dots = "." * (self.loading_dots % 4)
            base_message = "Bu işlem 1 dakika sürebilir."
            self.loading_message.config(text=f"{base_message}{dots}")
            self.loading_dots += 1
            
            # Progress bar animasyonu (sürekli hareket eden)
            self.progress_width += self.progress_direction * 15
            if self.progress_width >= 300:
                self.progress_width = 300
                self.progress_direction = -1
            elif self.progress_width <= 0:
                self.progress_width = 0
                self.progress_direction = 1
            
            # Progress bar'ı güncelle
            progress_bg.coords(self.progress_fill, 0, 0, self.progress_width, 6)
            
            # Renk geçişi efekti
            colors = ["#0077cc", "#00a8ff", "#0077cc", "#005bb5"]
            color_index = (self.loading_dots // 2) % len(colors)
            progress_bg.itemconfig(self.progress_fill, fill=colors[color_index])
            
            self.root.after(200, lambda: self.animate_modern_loading(progress_bg))

    def start_generated_test(self, questions):
        """Üretilen sorularla testi başlatır"""
        if len(questions) < 10:
            self.show_test_error("Yeterli soru oluşturulamadı. Lütfen tekrar deneyin.")
            return
        
        # Test ekranını göster
        self.show_test_screen(questions, self.finish_level_test)

    def show_test_error(self, error_message):
        """Modern hata ekranı gösterir"""
        self.clear_window()
        
        # Ana container
        main_container = tk.Frame(self.root, bg="#f0f0f0")
        main_container.pack(fill="both", expand=True)
        
        # Ortalama frame
        center_frame = tk.Frame(main_container, bg="#f0f0f0")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Modern kart tasarımı
        card_frame = tk.Frame(center_frame, bg="white", relief="flat", bd=0)
        card_frame.pack(padx=40, pady=40)
        
        # Gölge efekti
        shadow_frame = tk.Frame(center_frame, bg="#e0e0e0", relief="flat", bd=0)
        shadow_frame.place(in_=card_frame, x=3, y=3, relwidth=1, relheight=1)
        card_frame.lift()
        
        # İçerik alanı
        content_frame = tk.Frame(card_frame, bg="white", padx=60, pady=50)
        content_frame.pack()
        
        # Hata ikonu
        error_icon = tk.Label(content_frame, text="⚠️", font=("Arial", 48), bg="white")
        error_icon.pack(pady=(0, 20))
        
        # Hata başlığı
        title_label = tk.Label(content_frame, text="Bir Sorun Oluştu", 
                              font=("Arial", 24, "bold"), fg="#e74c3c", bg="white")
        title_label.pack(pady=(0, 10))
        
        # Hata mesajı
        error_label = tk.Label(content_frame, text=error_message, 
                              font=("Arial", 12), fg="#666", bg="white",
                              wraplength=400, justify="center")
        error_label.pack(pady=(0, 30))
        
        # Buton container
        button_container = tk.Frame(content_frame, bg="white")
        button_container.pack()
        
        # Modern butonlar
        retry_btn = tk.Button(button_container, text="🔄 Tekrar Dene", 
                             command=self.start_level_test,
                             font=("Arial", 12, "bold"), bg="#0077cc", fg="white", 
                             relief="flat", padx=20, pady=10, cursor="hand2")
        retry_btn.pack(side="left", padx=(0, 10))
        
        # Hover efekti
        def on_enter(e):
            retry_btn.config(bg="#005bb5")
        def on_leave(e):
            retry_btn.config(bg="#0077cc")
        
        retry_btn.bind("<Enter>", on_enter)
        retry_btn.bind("<Leave>", on_leave)
        
        # Ana menü butonu
        back_btn = tk.Button(button_container, text="🏠 Ana Menü", 
                            command=self.show_main_menu,
                            font=("Arial", 12), bg="#6c757d", fg="white", 
                            relief="flat", padx=20, pady=10, cursor="hand2")
        back_btn.pack(side="left")
        
        # Hover efekti
        def on_enter_back(e):
            back_btn.config(bg="#5a6268")
        def on_leave_back(e):
            back_btn.config(bg="#6c757d")
        
        back_btn.bind("<Enter>", on_enter_back)
        back_btn.bind("<Leave>", on_leave_back)
    
    def start_topic_test(self, topic_id):
        """Konu testini başlatır"""
        # Konuya ait soruları getir
        self.cursor.execute('''
            SELECT id, question_text, option_a, option_b, option_c, option_d, correct_answer 
            FROM questions 
            WHERE topic_id = ? 
            ORDER BY RANDOM() 
            LIMIT 10
        ''', (topic_id,))
        questions = self.cursor.fetchall()
    
        if len(questions) < 5:
            messagebox.showerror("Hata", "Bu konu için yeterli soru bulunamadı!")
            return
    
        self.show_test(questions, f"Konu Testi", lambda score, total: self.finish_topic_test(topic_id, score, total), has_timer=False)

    def show_test_screen(self, questions, finish_callback):
        """Test arayüzünü gösterir"""
        self.show_test(questions, "Seviye Belirleme Testi", finish_callback, has_timer=True)

    def show_test(self, questions, title, finish_callback, has_timer=False):
        """Test arayüzünü gösterir"""
        self.clear_window()

        # Başlık
        title_label = tk.Label(self.root, text=title, font=("Arial", 28, "bold"), fg="#222", bg="#f0f0f0")
        title_label.pack(pady=(20, 0))
        subtitle_label = tk.Label(self.root, text="Soruları cevaplayın ve ilerlemenizi takip edin", font=("Arial", 14), fg="#444", bg="#f0f0f0")
        subtitle_label.pack(pady=(0, 15))

        # Kronometre (sadece seviye testi için)
        if has_timer:
            timer_frame = tk.Frame(self.root, bg="#f0f0f0")
            timer_frame.pack(pady=(0, 10))
        
            # Kronometre container - modern tasarım
            timer_container = tk.Frame(timer_frame, bg="#e74c3c", relief="flat", bd=0)
            timer_container.pack()
        
            # Kronometre ikonu ve metin
            timer_content = tk.Frame(timer_container, bg="#e74c3c", padx=20, pady=8)
            timer_content.pack()
        
            timer_icon = tk.Label(timer_content, text="⏰", font=("Arial", 16), bg="#e74c3c", fg="white")
            timer_icon.pack(side="left", padx=(0, 8))
        
            self.timer_label = tk.Label(timer_content, text="10:00", font=("Arial", 16, "bold"), bg="#e74c3c", fg="white")
            self.timer_label.pack(side="left")
        
            # Timer değişkenleri
            self.time_remaining = 600  # 10 dakika = 600 saniye
            self.timer_running = True
        
            # Timer'ı başlat
            self.update_timer()

        # Test kutusu (Frame) - Yüksekliği artırıldı
        test_box = tk.Frame(self.root, bg="white", bd=0, relief="flat", highlightthickness=0)
        test_box.pack(pady=10)
        test_box.place(relx=0.5, rely=0.5, anchor="center", width=650, height=520)
        test_box.configure(highlightbackground="#ddd", highlightcolor="#ddd")
        test_box.pack_propagate(False)

        # Test durumu
        self.current_question = 0
        self.test_questions = questions
        self.test_answers = []
        self.finish_callback = finish_callback
        self.has_timer = has_timer

        # İlerleme çubuğu - Daha kompakt
        progress_container = tk.Frame(test_box, bg="white")
        progress_container.pack(fill="x", pady=(10, 5), padx=30)
        
        self.progress_var = tk.DoubleVar()
        progress_bar = tk.Canvas(progress_container, width=580, height=12, bg="#eee", highlightthickness=0)
        progress_bar.pack()
        self.progress_bar = progress_bar
        self.progress_bar_rect = progress_bar.create_rectangle(0, 0, 0, 12, fill="#0077cc", width=0)

        # Soru frame - Yüksekliği optimize edildi
        self.question_frame = tk.Frame(test_box, bg="white")
        self.question_frame.pack(pady=(5, 10), padx=30, fill="both", expand=True)

        # İlk soruyu göster
        self.show_question()
    
    def update_timer(self):
        """Kronometreyi günceller"""
        if not hasattr(self, 'timer_running') or not self.timer_running:
            return
    
        if not hasattr(self, 'timer_label') or not self.timer_label.winfo_exists():
            return
    
        if self.time_remaining <= 0:
        # Süre doldu - testi bitir
            self.timer_running = False
            self.timer_label.config(text="00:00", bg="#c0392b")
            messagebox.showwarning("Süre Doldu!", "Test süresi doldu. Mevcut cevaplarınız değerlendirilecek.")
            self.finish_test()
            return
        # Dakika ve saniyeyi hesapla
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
    
        # Zamanı formatla
        time_text = f"{minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=time_text)
    
        # Renk uyarıları
        if self.time_remaining <= 60:  # Son 1 dakika
            self.timer_label.config(bg="#c0392b")  # Koyu kırmızı
        elif self.time_remaining <= 180:  # Son 3 dakika
            self.timer_label.config(bg="#e67e22")  # Turuncu
    
        # Süreyi azalt
        self.time_remaining -= 1
    
        # 1 saniye sonra tekrar çağır
        self.root.after(1000, self.update_timer)

    def finish_test(self):
        """Testi bitirir ve sonuçları hesaplar"""
        # Timer'ı durdur
        if hasattr(self, 'timer_running'):
            self.timer_running = False
    
        # Son cevabı kaydet (eğer varsa)
        if hasattr(self, 'selected_answer') and self.selected_answer.get():
            if self.current_question < len(self.test_answers):
                self.test_answers[self.current_question] = self.selected_answer.get()
            else:
                self.test_answers.append(self.selected_answer.get())
    
        # Cevapsız soruları boş olarak işaretle
        while len(self.test_answers) < len(self.test_questions):
            self.test_answers.append("")
    
        # Puanı hesapla
        score = 0
        for i, answer in enumerate(self.test_answers):
            if i < len(self.test_questions) and answer == self.test_questions[i][6]:  # correct_answer
                score += 1
    
        # Callback'i çağır
        self.finish_callback(score, len(self.test_questions))

    def show_question(self):
        """Mevcut soruyu gösterir"""
        # Önceki soru frame'ini temizle
        for widget in self.question_frame.winfo_children():
            widget.destroy()

        if self.current_question >= len(self.test_questions):
            # Test bitti
            self.finish_test()
            return

        question = self.test_questions[self.current_question]

        # Soru numarası ve ilerleme
        header_frame = tk.Frame(self.question_frame, bg="white")
        header_frame.pack(fill="x", pady=(5, 0))
        
        question_num_label = tk.Label(header_frame, 
                                      text=f"Soru {self.current_question + 1}/{len(self.test_questions)}", 
                                      font=("Arial", 14, "bold"), bg="white", fg="#0077cc")
        question_num_label.pack(anchor="w")

        # Soru metni
        question_container = tk.Frame(self.question_frame, bg="white")
        question_container.pack(fill="x", pady=(10, 15))
        
        question_label = tk.Label(question_container, text=question[1], 
                                 font=("Arial", 13), wraplength=550, bg="white", fg="#222",
                                 justify="left")
        question_label.pack(anchor="w")

        # Cevap seçenekleri
        options = [question[2], question[3], question[4], question[5]]
        self.selected_answer = tk.StringVar()

        # Eğer daha önce bu soruya cevap verilmişse, onu seç
        if self.current_question < len(self.test_answers):
            self.selected_answer.set(self.test_answers[self.current_question])

        # Seçenekler container
        options_container = tk.Frame(self.question_frame, bg="white")
        options_container.pack(fill="x", pady=(0, 15))

        self.option_frames = []
        for i, option in enumerate(options):
            option_frame = tk.Frame(options_container, bg="#f8f9fa", relief="flat", bd=1,
                                   highlightbackground="#dee2e6", highlightthickness=1)
            option_frame.pack(fill="x", pady=2, padx=5)
            
            def on_click(event, value=chr(65 + i)):
                self.selected_answer.set(value)
                self.update_option_styles()
            
            option_frame.bind("<Button-1>", on_click)
            
            content_frame = tk.Frame(option_frame, bg="#f8f9fa")
            content_frame.pack(fill="x", padx=12, pady=8)
            content_frame.bind("<Button-1>", on_click)
            
            letter_label = tk.Label(content_frame, text=f"{chr(65 + i)}", 
                                   font=("Arial", 11, "bold"), bg="#f8f9fa", fg="#0077cc",
                                   width=2)
            letter_label.pack(side="left")
            letter_label.bind("<Button-1>", on_click)
            
            option_label = tk.Label(content_frame, text=option, 
                                   font=("Arial", 11), bg="#f8f9fa", fg="#333",
                                   anchor="w", justify="left", wraplength=480)
            option_label.pack(side="left", fill="x", expand=True, padx=(8, 0))
            option_label.bind("<Button-1>", on_click)
            
            self.option_frames.append((option_frame, content_frame, letter_label, option_label))

        # Butonlar
        bottom_frame = tk.Frame(self.question_frame, bg="white")
        bottom_frame.pack(fill="x", side="bottom", pady=(10, 0))
        
        button_container = tk.Frame(bottom_frame, bg="white")
        button_container.pack(fill="x")
        
        # Önceki butonu
        left_frame = tk.Frame(button_container, bg="white")
        left_frame.pack(side="left")
        
        if self.current_question > 0:
            prev_btn = tk.Button(left_frame, text="← Önceki", command=self.previous_question, 
                               font=("Arial", 10, "bold"), bg="#6c757d", fg="white", 
                               relief="flat", padx=15, pady=6, cursor="hand2")
            prev_btn.pack()
        
        # Sonraki/Bitir butonu
        right_frame = tk.Frame(button_container, bg="white")
        right_frame.pack(side="right")
        
        if self.current_question < len(self.test_questions) - 1:
            next_btn = tk.Button(right_frame, text="Sonraki →", command=self.next_question, 
                               font=("Arial", 10, "bold"), bg="#0077cc", fg="white", 
                               relief="flat", padx=15, pady=6, cursor="hand2")
            next_btn.pack()
        else:
            finish_btn = tk.Button(right_frame, text="Testi Bitir ✓", command=self.finish_test, 
                                   font=("Arial", 10, "bold"), bg="#27ae60", fg="white", 
                                   relief="flat", padx=15, pady=6, cursor="hand2")
            finish_btn.pack()

        # İlerleme çubuğunu güncelle
        total = len(self.test_questions)
        done = self.current_question + 1
        width = int(580 * done / total)
        self.progress_bar.coords(self.progress_bar_rect, 0, 0, width, 12)
        
        # Seçenek stillerini güncelle
        self.update_option_styles()

    def update_option_styles(self):
        """Seçili seçeneğin stilini günceller"""
        if not hasattr(self, 'option_frames'):
            return
        
        selected = self.selected_answer.get()
        
        for i, (frame, content, letter, option) in enumerate(self.option_frames):
            if selected == chr(65 + i):
                # Seçili stil
                frame.config(bg="#e3f2fd", highlightbackground="#0077cc", highlightthickness=2)
                content.config(bg="#e3f2fd")
                letter.config(bg="#e3f2fd", fg="#0077cc")
                option.config(bg="#e3f2fd", fg="#0d47a1")
            else:
                # Normal stil
                frame.config(bg="#f8f9fa", highlightbackground="#dee2e6", highlightthickness=1)
                content.config(bg="#f8f9fa")
                letter.config(bg="#f8f9fa", fg="#0077cc")
                option.config(bg="#f8f9fa", fg="#333")
    
    def next_question(self):
        """Sonraki soruya geçer"""
        # Cevabı kaydet
        if self.current_question < len(self.test_answers):
            self.test_answers[self.current_question] = self.selected_answer.get()
        else:
            self.test_answers.append(self.selected_answer.get())
        
        self.current_question += 1
        self.show_question()
    
    def previous_question(self):
        """Önceki soruya döner"""
        # Cevabı kaydet
        if self.current_question < len(self.test_answers):
            self.test_answers[self.current_question] = self.selected_answer.get()
        else:
            self.test_answers.append(self.selected_answer.get())
        
        self.current_question -= 1
        self.show_question()
    
    def finish_test(self):
        """Testi bitirir ve sonuçları hesaplar"""
        # Son cevabı kaydet
        if self.current_question < len(self.test_answers):
            self.test_answers[self.current_question] = self.selected_answer.get()
        else:
            self.test_answers.append(self.selected_answer.get())
        
        # Puanı hesapla
        score = 0
        for i, answer in enumerate(self.test_answers):
            if answer == self.test_questions[i][6]:  # correct_answer
                score += 1
        
        # Callback'i çağır
        self.finish_callback(score, len(self.test_questions))
    
    def finish_level_test(self, score, total):
        """Seviye belirleme testini bitirir"""
        # Kullanıcı kontrolü
        if not self.current_user:
            messagebox.showerror("Hata", "Kullanıcı oturumu bulunamadı!")
            self.show_main_menu()
            return
            
        # Seviyeyi hesapla
        percentage = (score / total) * 100
        
        if percentage >= 80:
            level = 3  # İleri
        elif percentage >= 60:
            level = 2  # Orta
        else:
            level = 1  # Başlangıç
        
        # Kullanıcı seviyesini kaydet
        self.cursor.execute('''
            INSERT OR REPLACE INTO user_levels (user_id, level, test_score)
            VALUES (?, ?, ?)
        ''', (self.current_user['id'], level, score))
        self.conn.commit()
        
        self.user_level = level
        
        # Sonuç sayfasını göster
        self.show_test_result("Seviye Belirleme Testi", score, total, level)
    
    def finish_topic_test(self, topic_id, score, total):
        """Konu testini bitirir"""
        # Kullanıcı kontrolü
        if not self.current_user:
            messagebox.showerror("Hata", "Kullanıcı oturumu bulunamadı!")
            self.show_main_menu()
            return
            
        # Test sonucunu kaydet
        self.cursor.execute('''
            INSERT INTO test_results (user_id, topic_id, score, total_questions)
            VALUES (?, ?, ?, ?)
        ''', (self.current_user['id'], topic_id, score, total))
        self.conn.commit()
        
        # Sonuç sayfasını göster
        self.show_test_result("Konu Testi", score, total)
    
    def show_test_result(self, test_type, score, total, level=None):
        """Test sonuç sayfasını gösterir"""
        self.clear_window()

        # Başlık ve alt başlık
        title_label = tk.Label(self.root, text=f"{test_type} Sonucu", font=("Arial", 32, "bold"), fg="#222", bg="#f0f0f0")
        title_label.pack(pady=(40, 0))
        subtitle_label = tk.Label(self.root, text="Test performansınızı inceleyin", font=("Arial", 16), fg="#444", bg="#f0f0f0")
        subtitle_label.pack(pady=(0, 30))

        # Sonuç kutusu (Frame)
        result_box = tk.Frame(self.root, bg="white", bd=0, relief="flat", highlightthickness=0)
        result_box.pack(pady=10)
        result_box.place(relx=0.5, rely=0.5, anchor="center", width=420, height=320)
        result_box.configure(highlightbackground="#ddd", highlightcolor="#ddd")
        result_box.pack_propagate(False)

        percentage = (score / total) * 100

        tk.Label(result_box, text=f"Doğru: {score}/{total}", font=("Arial", 18, "bold"), bg="white", fg="#222").pack(pady=10)
        tk.Label(result_box, text=f"Başarı Oranı: %{percentage:.1f}", font=("Arial", 15), bg="white", fg="#444").pack(pady=10)

        if level:
            level_names = {1: "Başlangıç", 2: "Orta", 3: "İleri"}
            tk.Label(result_box, text=f"Seviyeniz: {level_names[level]}", font=("Arial", 15, "bold"), bg="white", fg="#0077cc").pack(pady=10)

        # Değerlendirme
        if percentage >= 80:
            evaluation = "Mükemmel! Çok iyi bir performans gösterdiniz."
        elif percentage >= 60:
            evaluation = "İyi! Biraz daha çalışarak daha iyi sonuçlar alabilirsiniz."
        else:
            evaluation = "Daha fazla çalışmanız gerekiyor. Konuları tekrar gözden geçirin."

        tk.Label(result_box, text=evaluation, font=("Arial", 12), wraplength=350, bg="white", fg="#444").pack(pady=20)

        # Butonlar
        button_frame = tk.Frame(result_box, bg="white")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Ana Menüye Dön", command=self.show_main_menu, font=("Arial", 12, "bold"), bg="#0077cc", fg="white", relief="flat", width=14).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Konulara Dön", command=self.show_topics, font=("Arial", 12, "bold"), bg="#222", fg="white", relief="flat", width=14).pack(side=tk.LEFT, padx=10)
    
    def show_profile(self):
        """Profil sayfasını gösterir"""
        self.clear_window()
        
        # Kullanıcı kontrolü
        if not hasattr(self, 'current_user') or not self.current_user:
            messagebox.showerror("Hata", "Kullanıcı oturumu bulunamadı!")
            self.show_main_menu()
            return

        # Ana menüye dön butonu (üst kısımda)
        back_btn = tk.Button(
            self.root, 
            text="← Ana Menüye Dön", 
            command=self.show_main_menu,
            font=("Arial", 12), 
            bg="#0077cc", 
            fg="white", 
            relief="flat",
            padx=10,
            pady=5
        )
        back_btn.place(x=20, y=20)

        # Başlık ve alt başlık
        title_label = tk.Label(self.root, text="Profil", font=("Arial", 32, "bold"), fg="#222", bg="#f0f0f0")
        title_label.pack(pady=(40, 0))
        subtitle_label = tk.Label(self.root, text="Kullanıcı bilgileri ve istatistikler", font=("Arial", 16), fg="#444", bg="#f0f0f0")
        subtitle_label.pack(pady=(0, 30))

        # Profil kutusu (Frame)
        profile_box = tk.Frame(self.root, bg="white", bd=1, relief="solid", highlightthickness=0)
        profile_box.place(relx=0.5, rely=0.5, anchor="center", width=500, height=500)
        profile_box.configure(highlightbackground="#ddd", highlightcolor="#ddd")
        profile_box.pack_propagate(False)

        # Kullanıcı bilgileri bölümü
        user_frame = tk.Frame(profile_box, bg="white", padx=20, pady=15)
        user_frame.pack(fill="x")
        
        # Kullanıcı avatarı
        avatar_id = 1  # Varsayılan avatar
        
        # Veritabanından kullanıcının avatar seçimini al
        try:
            self.cursor.execute('''
                SELECT avatar_id FROM user_settings 
                WHERE user_id = ?
            ''', (self.current_user.get('id', 0),))
            result = self.cursor.fetchone()
            if result and result[0]:
                avatar_id = result[0]
        except Exception as e:
            print(f"Veritabanı sorgusu hatası: {e}")
        
        # Avatar emojileri
        avatars = {
            1: "👤", 2: "👩", 3: "👨", 4: "🧑", 5: "🦸",
            6: "🧠", 7: "🚗", 8: "🎓", 9: "🌟", 10: "🐱"
        }
        
        # Avatar çerçevesi
        avatar_frame = tk.Frame(user_frame, bg="white")
        avatar_frame.pack(side="left", padx=(0, 15))
        
        # Seçilen avatar
        avatar_label = tk.Label(
            avatar_frame, 
            text=avatars.get(avatar_id, "👤"), 
            font=("Arial", 36), 
            bg="white", 
            fg="#0077cc"
        )
        avatar_label.pack()
        
        # Avatar değiştirme butonu
        change_avatar_btn = tk.Button(
            avatar_frame, 
            text="Değiştir", 
            command=lambda: self.change_avatar(avatar_label, avatars),
            font=("Arial", 8), 
            bg="#f0f0f0", 
            fg="#444", 
            relief="flat",
            padx=5,
            pady=2
        )
        change_avatar_btn.pack(pady=(5, 0))
        
        # Kullanıcı bilgileri
        user_info_frame = tk.Frame(user_frame, bg="white")
        user_info_frame.pack(side="left", fill="both", expand=True)
        
        # Kullanıcı adı ve e-posta
        username = self.current_user.get('email', '').split('@')[0] if self.current_user.get('email') else "Kullanıcı"
        email = self.current_user.get('email', 'E-posta bulunamadı')
        
        tk.Label(user_info_frame, text=f"Kullanıcı Adı: {username}", 
                 font=("Arial", 14, "bold"), bg="white", fg="#222", anchor="w").pack(fill="x", pady=(0, 5))
        
        tk.Label(user_info_frame, text=f"E-posta: {email}", 
                 font=("Arial", 12), bg="white", fg="#666", anchor="w").pack(fill="x")
        
        # Seviye bilgisi
        level_text = "Henüz belirlenmedi"
        if hasattr(self, 'user_level') and self.user_level:
            level_names = {1: "Başlangıç", 2: "Orta", 3: "İleri"}
            level_text = level_names.get(self.user_level, "Bilinmiyor")
        
        tk.Label(user_info_frame, text=f"Seviye: {level_text}", 
                 font=("Arial", 12, "bold"), bg="white", fg="#0077cc", anchor="w").pack(fill="x", pady=(10, 0))
        
        # İstatistikler bölümü
        stats_frame = tk.Frame(profile_box, bg="white", padx=20, pady=15)
        stats_frame.pack(fill="x")
        
        # İstatistik başlığı
        tk.Label(stats_frame, text="📊 İstatistikler", 
                 font=("Arial", 16, "bold"), bg="white", fg="#222").pack(anchor="w", pady=(0, 10))
        
        # Test istatistikleri
        try:
            # Toplam test sayısı
            self.cursor.execute('''
                SELECT COUNT(*) FROM test_results 
                WHERE user_id = ?
            ''', (self.current_user.get('id', 0),))
            total_tests = self.cursor.fetchone()[0]
            
            # Ortalama puan
            self.cursor.execute('''
                SELECT AVG(CAST(score AS FLOAT) / total_questions * 100) 
                FROM test_results 
                WHERE user_id = ?
            ''', (self.current_user.get('id', 0),))
            avg_score = self.cursor.fetchone()[0]
            avg_score = round(avg_score, 1) if avg_score else 0
            
            # En yüksek puan
            self.cursor.execute('''
                SELECT MAX(CAST(score AS FLOAT) / total_questions * 100) 
                FROM test_results 
                WHERE user_id = ?
            ''', (self.current_user.get('id', 0),))
            max_score = self.cursor.fetchone()[0]
            max_score = round(max_score, 1) if max_score else 0
            
        except Exception as e:
            print(f"İstatistik sorgusu hatası: {e}")
            total_tests = 0
            avg_score = 0
            max_score = 0
        
        # İstatistik bilgileri
        stats_info = [
            ("Toplam Test:", str(total_tests)),
            ("Ortalama Başarı:", f"%{avg_score}"),
            ("En Yüksek Puan:", f"%{max_score}")
        ]
        
        for label, value in stats_info:
            stat_row = tk.Frame(stats_frame, bg="white")
            stat_row.pack(fill="x", pady=2)
            
            tk.Label(stat_row, text=label, font=("Arial", 12), 
                     bg="white", fg="#666", anchor="w").pack(side="left")
            tk.Label(stat_row, text=value, font=("Arial", 12, "bold"), 
                     bg="white", fg="#222", anchor="e").pack(side="right")
         
         # Sınav tarihi bölümü (İstatistikler bölümünden sonra eklenecek)
        countdown_frame = tk.Frame(profile_box, bg="white", padx=20, pady=15)
        countdown_frame.pack(fill="x")
        
        # Sınav tarihi başlığı
        tk.Label(countdown_frame, text="📅 Sınav Tarihi", 
                 font=("Arial", 16, "bold"), bg="white", fg="#222").pack(anchor="w", pady=(0, 10))

        # Sınav tarihi bilgileri
        countdown_info_frame = tk.Frame(countdown_frame, bg="white")
        countdown_info_frame.pack(side="left", fill="both", expand=True)
        
        # Kullanıcının sınav tarihini veritabanından al veya varsayılan tarih kullan
        if hasattr(self, 'conn') and hasattr(self, 'cursor'):
            try:
                self.cursor.execute('''
                    SELECT exam_date FROM user_settings 
                    WHERE user_id = ?
                ''', (self.current_user.get('id', 0),))
                result = self.cursor.fetchone()
                if result and result[0]:
                    exam_date = datetime.datetime.strptime(result[0], "%Y-%m-%d")
                else:
                    # Varsayılan tarih (30 gün sonrası)
                    exam_date = datetime.datetime.now() + datetime.timedelta(days=30)
            except Exception as e:
                print(f"Veritabanı sorgusu hatası: {e}")
                exam_date = datetime.datetime.now() + datetime.timedelta(days=30)
        else:
            exam_date = datetime.datetime.now() + datetime.timedelta(days=30)
        
        days_left = (exam_date - datetime.datetime.now()).days
        
        # Sınav tarihi ve kalan süre
        exam_date_label = tk.Label(countdown_info_frame, text=f"Sınav Tarihi: {exam_date.strftime('%d.%m.%Y')}", 
                 font=("Arial", 14, "bold"), bg="white", fg="#e74c3c", anchor="w")
        exam_date_label.pack(fill="x", pady=2)
        
        days_left_label = tk.Label(countdown_info_frame, text=f"Kalan Süre: {days_left} gün", 
                 font=("Arial", 12), bg="white", fg="#444", anchor="w")
        days_left_label.pack(fill="x", pady=2)
        
        # Motivasyon mesajı
        if days_left <= 7:
            motivation = "Son düzlüktesin! Şimdi daha çok çalışma zamanı!"
        elif days_left <= 14:
            motivation = "İki haftadan az kaldı! Eksiklerini tamamla."
        else:
            motivation = "Düzenli çalışarak başarıya ulaşabilirsin!"
        
        motivation_label = tk.Label(countdown_info_frame, text=motivation, 
                 font=("Arial", 12, "italic"), bg="white", fg="#e74c3c", anchor="w")
        motivation_label.pack(fill="x", pady=2)
        
        # Sınav tarihi değiştirme butonu
        change_date_btn = tk.Button(
            countdown_info_frame, 
            text="Sınav Tarihini Değiştir", 
            command=lambda: self.change_exam_date(exam_date_label, days_left_label, motivation_label),
            font=("Arial", 10), 
            bg="#e74c3c", 
            fg="white", 
            relief="flat",
            height=1
        )
        change_date_btn.pack(anchor="e", pady=(5, 0))
        
        # Alt butonlar
        button_frame = tk.Frame(profile_box, bg="white", pady=20)
        button_frame.pack(fill="x")
        
        # Seviye testi butonu
        level_test_btn = tk.Button(
            button_frame,
            text="Seviye Testi Yap",
            command=self.show_level_test,
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            relief="flat",
            width=15
        )
        level_test_btn.pack(side="left", padx=(20, 10))
        
        # Çıkış butonu
        logout_btn = tk.Button(
            button_frame,
            text="Çıkış Yap",
            command=self.logout,
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            relief="flat",
            width=15
        )
        logout_btn.pack(side="right", padx=(10, 20))
    
    def change_avatar(self, avatar_label, avatars):
        """Avatar değiştirme penceresini açar"""
        avatar_window = tk.Toplevel(self.root)
        avatar_window.title("Avatar Seç")
        avatar_window.geometry("400x300")
        avatar_window.configure(bg="white")
        avatar_window.resizable(False, False)
        
        # Pencereyi ortala
        avatar_window.transient(self.root)
        avatar_window.grab_set()
        
        tk.Label(avatar_window, text="Avatar Seçin", 
                 font=("Arial", 16, "bold"), bg="white", fg="#222").pack(pady=20)
        
        # Avatar grid
        avatar_frame = tk.Frame(avatar_window, bg="white")
        avatar_frame.pack(pady=20)
        
        for i, (avatar_id, emoji) in enumerate(avatars.items()):
            row = i // 5
            col = i % 5
            
            avatar_btn = tk.Button(
                avatar_frame,
                text=emoji,
                font=("Arial", 24),
                bg="#f0f0f0",
                relief="flat",
                width=3,
                height=2,
                command=lambda aid=avatar_id, e=emoji: self.select_avatar(aid, e, avatar_label, avatar_window)
            )
            avatar_btn.grid(row=row, column=col, padx=5, pady=5)
    
    def select_avatar(self, avatar_id, emoji, avatar_label, window):
        """Avatar seçimini kaydeder"""
        try:
            # Veritabanına kaydet
            self.cursor.execute('''
                INSERT OR REPLACE INTO user_settings (user_id, avatar_id)
                VALUES (?, ?)
            ''', (self.current_user.get('id', 0), avatar_id))
            self.conn.commit()
            
            # UI'ı güncelle
            avatar_label.config(text=emoji)
            
            # Pencereyi kapat
            window.destroy()
            
        except Exception as e:
            print(f"Avatar kaydetme hatası: {e}")
            messagebox.showerror("Hata", "Avatar kaydedilemedi!")

    def change_exam_date(self, date_label, days_label, motivation_label):
        """Kullanıcının sınav tarihini değiştirmesini sağlar"""
        # Tarih seçme penceresi
        date_window = tk.Toplevel(self.root)
        date_window.title("Sınav Tarihi Seçin")
        date_window.geometry("400x300")
        date_window.configure(bg="white")
        date_window.resizable(False, False)
        
        # Pencereyi ana pencerenin ortasına konumlandır
        date_window.transient(self.root)
        date_window.grab_set()
        
        # Başlık
        tk.Label(date_window, text="Sınav Tarihinizi Seçin", font=("Arial", 16, "bold"), 
                 bg="white", fg="#222").pack(pady=(20, 10))
        
        # Açıklama
        tk.Label(date_window, text="Lütfen ehliyet sınavınızın tarihini seçin.", 
                 font=("Arial", 12), bg="white", fg="#444").pack(pady=(0, 20))
        
        # Tarih seçici çerçeve
        date_frame = tk.Frame(date_window, bg="white")
        date_frame.pack(pady=10)
        
        # Bugünün tarihi
        today = datetime.datetime.now()
        
        # Gün, ay, yıl seçicileri
        day_var = tk.StringVar(value=str(today.day))
        month_var = tk.StringVar(value=str(today.month))
        year_var = tk.StringVar(value=str(today.year))
        
        # Gün seçici
        day_frame = tk.Frame(date_frame, bg="white")
        day_frame.pack(side="left", padx=10)
        tk.Label(day_frame, text="Gün", font=("Arial", 12), bg="white").pack()
        day_menu = ttk.Combobox(day_frame, textvariable=day_var, width=5)
        day_menu['values'] = tuple(range(1, 32))
        day_menu.pack(pady=5)
        
        # Ay seçici
        month_frame = tk.Frame(date_frame, bg="white")
        month_frame.pack(side="left", padx=10)
        tk.Label(month_frame, text="Ay", font=("Arial", 12), bg="white").pack()
        month_menu = ttk.Combobox(month_frame, textvariable=month_var, width=5)
        month_menu['values'] = tuple(range(1, 13))
        month_menu.pack(pady=5)
        
        # Yıl seçici
        year_frame = tk.Frame(date_frame, bg="white")
        year_frame.pack(side="left", padx=10)
        tk.Label(year_frame, text="Yıl", font=("Arial", 12), bg="white").pack()
        year_menu = ttk.Combobox(year_frame, textvariable=year_var, width=7)
        year_menu['values'] = tuple(range(today.year, today.year + 5))
        year_menu.pack(pady=5)
        
        # Hata mesajı için label
        error_label = tk.Label(date_window, text="", font=("Arial", 12), bg="white", fg="red")
        error_label.pack(pady=10)
        
        # Kaydet butonu
        def save_date():
            try:
                # Seçilen tarihi al
                day = int(day_var.get())
                month = int(month_var.get())
                year = int(year_var.get())
                
                # Geçerli bir tarih mi kontrol et
                try:
                    selected_date = datetime.datetime(year, month, day)
                except ValueError:
                    error_label.config(text="Geçersiz tarih! Lütfen tekrar kontrol edin.")
                    return
                
                # Bugünden önceki bir tarih mi kontrol et
                if selected_date < today:
                    error_label.config(text="Geçmiş bir tarih seçemezsiniz!")
                    return
                
                # Tarihi veritabanına kaydet
                if hasattr(self, 'conn') and hasattr(self, 'cursor'):
                    try:
                        # user_settings tablosu var mı kontrol et
                        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS user_settings (
                                user_id INTEGER PRIMARY KEY,
                                exam_date TEXT
                            )
                        ''')
                        
                        # Kullanıcının ayarı var mı kontrol et
                        self.cursor.execute('''
                            SELECT * FROM user_settings WHERE user_id = ?
                        ''', (self.current_user.get('id', 0),))
                        
                        if self.cursor.fetchone():
                            # Güncelle
                            self.cursor.execute('''
                                UPDATE user_settings SET exam_date = ? WHERE user_id = ?
                            ''', (selected_date.strftime("%Y-%m-%d"), self.current_user.get('id', 0)))
                        else:
                            # Yeni kayıt ekle
                            self.cursor.execute('''
                                INSERT INTO user_settings (user_id, exam_date) VALUES (?, ?)
                            ''', (self.current_user.get('id', 0), selected_date.strftime("%Y-%m-%d")))
                        
                        self.conn.commit()
                    except Exception as e:
                        print(f"Veritabanı hatası: {e}")
                
                # Arayüzü güncelle
                days_left = (selected_date - datetime.datetime.now()).days
                date_label.config(text=f"Sınav Tarihi: {selected_date.strftime('%d.%m.%Y')}")
                days_label.config(text=f"Kalan Süre: {days_left} gün")
                
                # Motivasyon mesajını güncelle
                if days_left <= 7:
                    motivation = "Son düzlüktesin! Şimdi daha çok çalışma zamanı!"
                elif days_left <= 14:
                    motivation = "İki haftadan az kaldı! Eksiklerini tamamla."
                else:
                    motivation = "Düzenli çalışarak başarıya ulaşabilirsin!"
                
                motivation_label.config(text=motivation)
                
                # Pencereyi kapat
                date_window.destroy()
                
            except Exception as e:
                error_label.config(text=f"Hata oluştu: {e}")
        
        save_btn = tk.Button(
            date_window, 
            text="Tarihi Kaydet", 
            command=save_date,
            font=("Arial", 12, "bold"), 
            bg="#e74c3c", 
            fg="white", 
            relief="flat",
            height=2,
            width=15
        )
        save_btn.pack(pady=20)
        
        # İptal butonu
        cancel_btn = tk.Button(
            date_window, 
            text="İptal", 
            command=date_window.destroy,
            font=("Arial", 12), 
            bg="#ccc", 
            fg="#444", 
            relief="flat"
        )
        cancel_btn.pack()

    def run(self):
        """Uygulamayı başlatır"""
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = DriveMate(root)
    app.run()
