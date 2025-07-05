import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
import json
import datetime
import random
from tkinter import font as tkfont

class EhliyetGoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EhliyetGo - Ehliyet Sınavı Hazırlık Uygulaması")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Veritabanı bağlantısı
        self.init_database()
        
        # Kullanıcı durumu
        self.current_user = None
        self.user_level = None
        
        # Ana pencere stilleri
        self.setup_styles()
        
        # Ana menü
        self.show_main_menu()
    
    def setup_styles(self):
        """Uygulama stillerini ayarlar"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Özel stiller
        style.configure('Title.TLabel', font=('Arial', 24, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Arial', 14), foreground='#34495e')
        style.configure('Button.TButton', font=('Arial', 12, 'bold'), padding=10)
        style.configure('Menu.TButton', font=('Arial', 14, 'bold'), padding=15)
    
    def init_database(self):
        """Veritabanını başlatır ve gerekli tabloları oluşturur"""
        self.conn = sqlite3.connect('ehliyetgo.db')
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
        title_label = tk.Label(self.root, text="EhliyetGO", font=("Arial", 36, "bold"), fg="#222", bg="#f0f0f0")
        title_label.pack(pady=(40, 0))
        subtitle_label = tk.Label(self.root, text="Teorik Ehliyet Asistanı", font=("Arial", 18), fg="#444", bg="#f0f0f0")
        subtitle_label.pack(pady=(0, 30))

        # Menü kutusu (Frame)
        menu_box = tk.Frame(self.root, bg="white", bd=0, relief="flat", highlightthickness=0)
        menu_box.pack(pady=10)
        menu_box.place(relx=0.5, rely=0.5, anchor="center", width=400, height=340)
        menu_box.configure(highlightbackground="#ddd", highlightcolor="#ddd")
        menu_box.pack_propagate(False)

        if self.current_user:
            # Kullanıcı giriş yapmış
            btn1 = tk.Button(menu_box, text="Konular", command=self.show_topics, font=("Arial", 14, "bold"), bg="#222", fg="white", relief="flat", height=2)
            btn1.pack(fill="x", padx=40, pady=(40, 10))
            btn2 = tk.Button(menu_box, text="Seviye Belirleme Testi", command=self.show_level_test, font=("Arial", 14, "bold"), bg="#222", fg="white", relief="flat", height=2)
            btn2.pack(fill="x", padx=40, pady=10)
            btn3 = tk.Button(menu_box, text="Profil", command=self.show_profile, font=("Arial", 14, "bold"), bg="#222", fg="white", relief="flat", height=2)
            btn3.pack(fill="x", padx=40, pady=10)
            btn4 = tk.Button(menu_box, text="Çıkış Yap", command=self.logout, font=("Arial", 14, "bold"), bg="#e74c3c", fg="white", relief="flat", height=2)
            btn4.pack(fill="x", padx=40, pady=(10, 0))
        else:
            # Kullanıcı giriş yapmamış
            btn1 = tk.Button(menu_box, text="Giriş Yap", command=self.show_login, font=("Arial", 14, "bold"), bg="#222", fg="white", relief="flat", height=2)
            btn1.pack(fill="x", padx=40, pady=(70, 10))
            btn2 = tk.Button(menu_box, text="Kayıt Ol", command=self.show_register, font=("Arial", 14, "bold"), bg="#222", fg="white", relief="flat", height=2)
            btn2.pack(fill="x", padx=40, pady=10)

    def show_register(self):
        """Kayıt sayfasını gösterir"""
        self.clear_window()

        # Başlık ve alt başlık
        title_label = tk.Label(self.root, text="EhliyetGO", font=("Arial", 36, "bold"), fg="#222", bg="#f0f0f0")
        title_label.pack(pady=(40, 0))
        subtitle_label = tk.Label(self.root, text="Teorik Ehliyet Asistanı", font=("Arial", 18), fg="#444", bg="#f0f0f0")
        subtitle_label.pack(pady=(0, 30))

        # Form kutusu (Frame)
        form_box = tk.Frame(self.root, bg="white", bd=0, relief="flat", highlightthickness=0)
        form_box.pack(pady=10)
        form_box.place(relx=0.5, rely=0.5, anchor="center", width=380, height=340)
        form_box.configure(highlightbackground="#ddd", highlightcolor="#ddd")
        form_box.pack_propagate(False)

        # E-posta
        email_label = tk.Label(form_box, text="Email", font=("Arial", 12), bg="white", anchor="w")
        email_label.pack(fill="x", padx=30, pady=(30, 0))
        email_entry = tk.Entry(form_box, font=("Arial", 12), bg="#f7f7f7", relief="flat", highlightthickness=1, highlightbackground="#ccc")
        email_entry.pack(fill="x", padx=30, pady=(0, 10))

        # Şifre
        password_label = tk.Label(form_box, text="Password", font=("Arial", 12), bg="white", anchor="w")
        password_label.pack(fill="x", padx=30, pady=(0, 0))
        password_entry = tk.Entry(form_box, font=("Arial", 12), show="*", bg="#f7f7f7", relief="flat", highlightthickness=1, highlightbackground="#ccc")
        password_entry.pack(fill="x", padx=30, pady=(0, 10))

        # Şifre tekrar
        password_confirm_label = tk.Label(form_box, text="Password (again)", font=("Arial", 12), bg="white", anchor="w")
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
        title_label = tk.Label(self.root, text="EhliyetGO", font=("Arial", 36, "bold"), fg="#222", bg="#f0f0f0")
        title_label.pack(pady=(40, 0))
        subtitle_label = tk.Label(self.root, text="Teorik Ehliyet Asistanı", font=("Arial", 18), fg="#444", bg="#f0f0f0")
        subtitle_label.pack(pady=(0, 30))

        # Form kutusu (Frame)
        form_box = tk.Frame(self.root, bg="white", bd=0, relief="flat", highlightthickness=0)
        form_box.pack(pady=10)
        form_box.place(relx=0.5, rely=0.5, anchor="center", width=380, height=270)
        form_box.configure(highlightbackground="#ddd", highlightcolor="#ddd")
        form_box.pack_propagate(False)

        # E-posta
        email_label = tk.Label(form_box, text="Email", font=("Arial", 12), bg="white", anchor="w")
        email_label.pack(fill="x", padx=30, pady=(30, 0))
        email_entry = tk.Entry(form_box, font=("Arial", 12), bg="#f7f7f7", relief="flat", highlightthickness=1, highlightbackground="#ccc")
        email_entry.pack(fill="x", padx=30, pady=(0, 10))

        # Şifre
        password_label = tk.Label(form_box, text="Password", font=("Arial", 12), bg="white", anchor="w")
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

        login_btn = tk.Button(form_box, text="Sign In", command=login, font=("Arial", 13, "bold"), bg="#222", fg="white", relief="flat", height=2)
        login_btn.pack(fill="x", padx=30, pady=(0, 10))

        # Şifremi unuttum linki (şimdilik işlevsiz)
        forgot_link = tk.Label(form_box, text="Forgot password?", font=("Arial", 10, "underline"), fg="#0077cc", bg="white", cursor="hand2")
        forgot_link.pack(pady=(0, 10))
        # forgot_link.bind("<Button-1>", lambda e: self.show_forgot_password())

        # Kayıt ol linki
        register_link = tk.Label(form_box, text="Don't have an account? Sign Up", font=("Arial", 10, "underline"), fg="#0077cc", bg="white", cursor="hand2")
        register_link.pack(pady=(0, 10))
        register_link.bind("<Button-1>", lambda e: self.show_register())
    
    def logout(self):
        """Çıkış yapar"""
        self.current_user = None
        self.user_level = None
        self.show_main_menu()
    
    def show_topics(self):
        """Konular sayfasını gösterir"""
        self.clear_window()

        # Başlık ve alt başlık
        title_label = tk.Label(self.root, text="Konular", font=("Arial", 32, "bold"), fg="#222", bg="#f0f0f0")
        title_label.pack(pady=(40, 0))
        subtitle_label = tk.Label(self.root, text="Çalışmak istediğiniz konuyu seçin", font=("Arial", 16), fg="#444", bg="#f0f0f0")
        subtitle_label.pack(pady=(0, 30))

        # Konuları getir
        self.cursor.execute('SELECT id, name, description, question_count FROM topics')
        topics = self.cursor.fetchall()

        # Konular kutusu (Frame)
        topics_box = tk.Frame(self.root, bg="white", bd=0, relief="flat", highlightthickness=0)
        topics_box.pack(pady=10)
        topics_box.place(relx=0.5, rely=0.5, anchor="center", width=500, height=420)
        topics_box.configure(highlightbackground="#ddd", highlightcolor="#ddd")
        topics_box.pack_propagate(False)

        # Scrollable alan
        canvas = tk.Canvas(topics_box, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(topics_box, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Konu kartları
        for i, topic in enumerate(topics):
            topic_frame = tk.Frame(scrollable_frame, bg="#f7f7f7", bd=1, relief="solid")
            topic_frame.pack(pady=10, padx=20, fill="x")
            tk.Label(topic_frame, text=topic[1], font=("Arial", 15, "bold"), bg="#f7f7f7", fg="#222").pack(pady=(10, 0), anchor="w", padx=10)
            tk.Label(topic_frame, text=topic[2], font=("Arial", 11), bg="#f7f7f7", fg="#444").pack(pady=(0, 5), anchor="w", padx=10)
            tk.Label(topic_frame, text=f"Soru Sayısı: {topic[3]}", font=("Arial", 10), bg="#f7f7f7", fg="#888").pack(pady=(0, 5), anchor="w", padx=10)
            tk.Button(topic_frame, text="Teste Başla", command=lambda t=topic: self.start_topic_test(t[0], t[1]), font=("Arial", 11, "bold"), bg="#222", fg="white", relief="flat", height=1).pack(pady=(0, 10), padx=10, anchor="e")

        # Geri dön butonu
        back_btn = tk.Button(self.root, text="Ana Menüye Dön", command=self.show_main_menu, font=("Arial", 12, "bold"), bg="#0077cc", fg="white", relief="flat", height=2)
        back_btn.pack(pady=20)
    
    def show_level_test(self):
        """Seviye belirleme testini gösterir"""
        self.clear_window()
        
        # Başlık
        title_label = ttk.Label(self.root, text="Seviye Belirleme Testi", style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Test açıklaması
        desc_label = ttk.Label(self.root, text="Bu test 10 sorudan oluşur ve seviyenizi belirler.", style='Subtitle.TLabel')
        desc_label.pack(pady=10)
        
        # Test başlatma butonu
        ttk.Button(self.root, text="Teste Başla", command=self.start_level_test, style='Menu.TButton').pack(pady=30)
        
        # Geri dön butonu
        ttk.Button(self.root, text="Ana Menüye Dön", command=self.show_main_menu, style='Button.TButton').pack(pady=20)
    
    def start_level_test(self):
        """Seviye belirleme testini başlatır"""
        # Rastgele 10 soru seç
        self.cursor.execute('''
            SELECT id, question_text, option_a, option_b, option_c, option_d, correct_answer 
            FROM questions 
            ORDER BY RANDOM() 
            LIMIT 10
        ''')
        questions = self.cursor.fetchall()
        
        if len(questions) < 10:
            messagebox.showerror("Hata", "Yeterli soru bulunamadı!")
            return
        
        self.show_test(questions, "Seviye Belirleme Testi", self.finish_level_test)
    
    def start_topic_test(self, topic_id, topic_name):
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
        
        self.show_test(questions, f"{topic_name} Testi", lambda score, total: self.finish_topic_test(topic_id, score, total))
    
    def show_test(self, questions, title, finish_callback):
        """Test arayüzünü gösterir"""
        self.clear_window()

        # Başlık
        title_label = tk.Label(self.root, text=title, font=("Arial", 32, "bold"), fg="#222", bg="#f0f0f0")
        title_label.pack(pady=(40, 0))
        subtitle_label = tk.Label(self.root, text="Soruları cevaplayın ve ilerlemenizi takip edin", font=("Arial", 16), fg="#444", bg="#f0f0f0")
        subtitle_label.pack(pady=(0, 30))

        # Test kutusu (Frame)
        test_box = tk.Frame(self.root, bg="white", bd=0, relief="flat", highlightthickness=0)
        test_box.pack(pady=10)
        test_box.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)
        test_box.configure(highlightbackground="#ddd", highlightcolor="#ddd")
        test_box.pack_propagate(False)

        # Test durumu
        self.current_question = 0
        self.test_questions = questions
        self.test_answers = []
        self.finish_callback = finish_callback

        # İlerleme çubuğu
        self.progress_var = tk.DoubleVar()
        progress_bar = tk.Canvas(test_box, width=520, height=18, bg="#eee", highlightthickness=0)
        progress_bar.pack(pady=10, padx=40)
        self.progress_bar = progress_bar
        self.progress_bar_rect = progress_bar.create_rectangle(0, 0, 0, 18, fill="#0077cc", width=0)

        # Soru frame
        self.question_frame = tk.Frame(test_box, bg="white")
        self.question_frame.pack(pady=10, padx=40, fill="both", expand=True)

        # İlk soruyu göster
        self.show_question()

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

        # Soru numarası
        question_num_label = tk.Label(self.question_frame, 
                                      text=f"Soru {self.current_question + 1}/{len(self.test_questions)}", 
                                      font=("Arial", 15, "bold"), bg="white", fg="#222")
        question_num_label.pack(pady=10, anchor="w")

        # Soru metni
        question_label = tk.Label(self.question_frame, text=question[1], font=("Arial", 13), wraplength=500, bg="white", fg="#222")
        question_label.pack(pady=20, anchor="w")

        # Cevap seçenekleri
        options = [question[2], question[3], question[4], question[5]]
        self.selected_answer = tk.StringVar()

        for i, option in enumerate(options):
            tk.Radiobutton(self.question_frame, text=option, variable=self.selected_answer, 
                           value=chr(65 + i), font=("Arial", 12), bg="white", anchor="w").pack(pady=5, anchor="w")

        # Butonlar
        button_frame = tk.Frame(self.question_frame, bg="white")
        button_frame.pack(pady=30)

        if self.current_question > 0:
            tk.Button(button_frame, text="Önceki", command=self.previous_question, font=("Arial", 12, "bold"), bg="#0077cc", fg="white", relief="flat", width=12).pack(side=tk.LEFT, padx=10)

        if self.current_question < len(self.test_questions) - 1:
            tk.Button(button_frame, text="Sonraki", command=self.next_question, font=("Arial", 12, "bold"), bg="#222", fg="white", relief="flat", width=12).pack(side=tk.LEFT, padx=10)
        else:
            tk.Button(button_frame, text="Testi Bitir", command=self.finish_test, font=("Arial", 12, "bold"), bg="#27ae60", fg="white", relief="flat", width=12).pack(side=tk.LEFT, padx=10)

        # İlerleme çubuğunu güncelle
        total = len(self.test_questions)
        done = self.current_question + 1
        width = int(520 * done / total)
        self.progress_bar.coords(self.progress_bar_rect, 0, 0, width, 18)

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
        # Kullanıcı kontrolü
        if not self.current_user:
            messagebox.showerror("Hata", "Kullanıcı oturumu bulunamadı!")
            self.show_main_menu()
            return

        self.clear_window()

        # Başlık ve alt başlık
        title_label = tk.Label(self.root, text="Profil", font=("Arial", 32, "bold"), fg="#222", bg="#f0f0f0")
        title_label.pack(pady=(40, 0))
        subtitle_label = tk.Label(self.root, text="Kullanıcı bilgileri ve istatistikler", font=("Arial", 16), fg="#444", bg="#f0f0f0")
        subtitle_label.pack(pady=(0, 30))

        # Profil kutusu (Frame)
        profile_box = tk.Frame(self.root, bg="white", bd=0, relief="flat", highlightthickness=0)
        profile_box.pack(pady=10)
        profile_box.place(relx=0.5, rely=0.5, anchor="center", width=420, height=320)
        profile_box.configure(highlightbackground="#ddd", highlightcolor="#ddd")
        profile_box.pack_propagate(False)

        tk.Label(profile_box, text=f"E-posta: {self.current_user['email']}", font=("Arial", 15), bg="white", fg="#222").pack(pady=10)

        # Seviye bilgisi
        if self.user_level:
            level_names = {1: "Başlangıç", 2: "Orta", 3: "İleri"}
            tk.Label(profile_box, text=f"Seviye: {level_names[self.user_level]}", font=("Arial", 15), bg="white", fg="#0077cc").pack(pady=10)
        else:
            tk.Label(profile_box, text="Seviye: Belirlenmemiş", font=("Arial", 15), bg="white", fg="#888").pack(pady=10)

        # Test istatistikleri
        self.cursor.execute('''
            SELECT COUNT(*) as total_tests, AVG(score * 100.0 / total_questions) as avg_score
            FROM test_results 
            WHERE user_id = ?
        ''', (self.current_user['id'],))
        stats = self.cursor.fetchone()

        if stats[0] > 0:
            tk.Label(profile_box, text=f"Toplam Test: {stats[0]}", font=("Arial", 15), bg="white", fg="#444").pack(pady=10)
            tk.Label(profile_box, text=f"Ortalama Başarı: %{stats[1]:.1f}", font=("Arial", 15), bg="white", fg="#444").pack(pady=10)
        else:
            tk.Label(profile_box, text="Henüz test çözülmemiş", font=("Arial", 15), bg="white", fg="#888").pack(pady=10)

        # Geri dön butonu
        back_btn = tk.Button(profile_box, text="Ana Menüye Dön", command=self.show_main_menu, font=("Arial", 12, "bold"), bg="#0077cc", fg="white", relief="flat", height=2)
        back_btn.pack(pady=20)

def main():
    root = tk.Tk()
    app = EhliyetGoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 