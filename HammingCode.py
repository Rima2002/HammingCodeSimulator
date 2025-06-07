import tkinter as tk
from tkinter import ttk, messagebox
import math

class HammingCodeSimulator:
    def __init__(self, root):
        # Ana pencereyi başlat
        self.root = root
        self.root.title("Hamming SEC-DED Kod Simülatörü")
        self.root.geometry("1100x850")
        self.root.minsize(900, 700)
        
        # Stil ve renkleri ayarla
        self.setup_styles()
        
        # Tüm GUI bileşenlerini oluştur
        self.create_widgets()
        
        # Değişkenleri başlat
        self.memory = {}
        self.encoded_data = None
        self.last_p = 0
        self.direction = "left_to_right"
        self.show_raw_data = True

    def setup_styles(self):
        """Uygulamanın görsel stillerini yapılandır"""
        self.style = ttk.Style()
        
        # Çerçeve ve widget stilleri
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 11))
        self.style.configure('TButton', font=('Arial', 11, 'bold'), padding=5)
        self.style.configure('TEntry', font=('Arial', 11), padding=5)
        self.style.configure('TRadiobutton', background='#f0f0f0', font=('Arial', 11))
        self.style.configure('TCheckbutton', background='#f0f0f0', font=('Arial', 11))
        self.style.configure('TCombobox', font=('Arial', 11))
        
        # Renk şeması
        self.colors = {
            'background': '#f0f0f0',
            'data_bit': '#e6f3ff',
            'parity_bit': '#ffe6cc',
            'error': '#ff6666',
            'corrected': '#66cc66',
            'button': '#4a90e2',
            'button_text': 'white',
            'text_bg': 'white',
            'result_parity': '#ff9900',
            'result_error': '#ff0000',
            'result_corrected': '#009900',
            'text_data': '#333333',
            'text_error_data': '#cc0000',
            'text_highlight': '#ffffff',
            'header': '#3a7bc8',
            'font_large': ('Arial', 12),
            'font_bold': ('Arial', 11, 'bold'),
            'font_mono': ('Courier New', 11)
        }

    def create_widgets(self):
        """Tüm GUI bileşenlerini oluştur"""
        # Ana konteyner
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Grid ağırlıklarını yapılandır
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)

        # Konfigürasyon çerçevesi
        self.create_config_frame(main_frame)
        
        # Giriş çerçevesi
        self.create_input_frame(main_frame)
        
        # Buton çerçevesi
        self.create_button_frame(main_frame)
        
        # Bit görselleştirme çerçevesi
        self.create_bit_visualization_frame(main_frame)
        
        # Sonuçlar çerçevesi
        self.create_results_frame(main_frame)
        
        # Hata simülasyon çerçevesi
        self.create_error_frame(main_frame)
        
        # Menü çubuğu
        self.create_menu_bar()
        
        # Veri girişini başlat
        self.update_data_entry()

    def create_config_frame(self, parent):
        """Seçeneklerle konfigürasyon çerçevesini oluştur"""
        config_frame = ttk.LabelFrame(parent, text="Konfigürasyon", padding="10")
        config_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        # Veri boyutu seçimi
        ttk.Label(config_frame, text="Veri Boyutu:", font=self.colors['font_bold']).grid(
            row=0, column=0, padx=5, pady=5, sticky="w")
        self.data_size = ttk.Combobox(config_frame, values=["8", "16", "32"], 
                                     state="readonly", font=self.colors['font_large'])
        self.data_size.current(0)
        self.data_size.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.data_size.bind("<<ComboboxSelected>>", self.update_data_entry)

        # Bit yönü seçimi
        ttk.Label(config_frame, text="Bit Yönü:", font=self.colors['font_bold']).grid(
            row=0, column=2, padx=5, pady=5, sticky="w")
        self.direction_var = tk.StringVar(value="left_to_right")
        ttk.Radiobutton(config_frame, text="Soldan Sağa", variable=self.direction_var, 
                       value="left_to_right", command=self.update_direction).grid(
                           row=0, column=3, padx=5, sticky="w")
        ttk.Radiobutton(config_frame, text="Sağdan Sola", variable=self.direction_var, 
                       value="right_to_left", command=self.update_direction).grid(
                           row=0, column=4, padx=5, sticky="w")

        # Ham veriyi göster checkbox
        self.show_raw_var = tk.IntVar(value=1)
        ttk.Checkbutton(config_frame, text="Ham Veriyi Göster", variable=self.show_raw_var,
                       command=self.toggle_raw_data).grid(row=0, column=5, padx=5, sticky="w")

    def create_input_frame(self, parent):
        """Veri giriş çerçevesini oluştur"""
        input_frame = ttk.LabelFrame(parent, text="Veri Girişi", padding="10")
        input_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Label(input_frame, text="Veri (Binary):", font=self.colors['font_bold']).grid(
            row=0, column=0, padx=5, pady=5, sticky="w")
        self.data_input = ttk.Entry(input_frame, width=40, font=self.colors['font_mono'])
        self.data_input.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        input_frame.columnconfigure(1, weight=1)

    def create_button_frame(self, parent):
        """Aksiyon butonlarıyla buton çerçevesini oluştur"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        
        # Buton stil seçenekleri
        button_options = {
            'background': self.colors['button'],
            'foreground': self.colors['button_text'],
            'activebackground': '#3a7bc8',
            'font': self.colors['font_bold'],
            'borderwidth': 2,
            'relief': 'raised',
            'padx': 10,
            'pady': 5
        }
        
        # Tüm butonları oluştur
        self.encode_btn = tk.Button(button_frame, text="Hamming Kodunu Hesapla", 
                                  command=self.encode_data, **button_options)
        self.encode_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.store_btn = tk.Button(button_frame, text="Belleğe Kaydet", 
                                 command=self.store_to_memory, **button_options)
        self.store_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.read_btn = tk.Button(button_frame, text="Bellekten Oku", 
                                command=self.read_from_memory, **button_options)
        self.read_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.error_btn = tk.Button(button_frame, text="Hata Ekle", 
                                 command=self.introduce_error, **button_options)
        self.error_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.restart_btn = tk.Button(button_frame, text="Yeniden Başlat", 
                                   command=self.restart_simulation, **button_options)
        self.restart_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

    def create_bit_visualization_frame(self, parent):
        """Bitleri görselleştirmek için çerçeve oluştur"""
        bit_container = ttk.Frame(parent)
        bit_container.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        
        self.canvas = tk.Canvas(bit_container, height=70, bg=self.colors['background'], 
                              highlightthickness=0)
        self.scroll_x = ttk.Scrollbar(bit_container, orient="horizontal", 
                                    command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scroll_x.set)
        
        self.scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.bit_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.bit_frame, anchor="nw")
        
        self.bit_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.bit_labels = []

    def create_results_frame(self, parent):
        """Sonuçların gösterileceği çerçeveyi oluştur"""
        result_frame = ttk.LabelFrame(parent, text="Sonuçlar", padding="10")
        result_frame.grid(row=4, column=0, sticky="nsew")
        
        # Text ve Scrollbar'ı tutacak alt çerçeve oluştur
        text_scroll_frame = ttk.Frame(result_frame)
        text_scroll_frame.pack(fill=tk.BOTH, expand=True)

        # Dikey kaydırma çubuğu oluştur
        scrollbar_y = ttk.Scrollbar(text_scroll_frame, orient="vertical")
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Kaydırma çubuğu desteği ile Text widget'ı oluştur
        self.result_text = tk.Text(
            text_scroll_frame, wrap=tk.WORD, bg=self.colors['text_bg'],
            font=self.colors['font_mono'], padx=5, pady=5, yscrollcommand=scrollbar_y.set
        )
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar_y.config(command=self.result_text.yview)
        
        # Renkli çıktı için text tag'lerini yapılandır
        self.result_text.tag_config('header', foreground=self.colors['header'], 
                                  font=self.colors['font_bold'])
        self.result_text.tag_config('parity', foreground=self.colors['result_parity'], 
                                  font=self.colors['font_bold'])
        self.result_text.tag_config('error', foreground=self.colors['result_error'], 
                                  font=self.colors['font_bold'])
        self.result_text.tag_config('corrected', foreground=self.colors['result_corrected'], 
                                  font=self.colors['font_bold'])
        self.result_text.tag_config('bold', font=self.colors['font_bold'])
        self.result_text.tag_config('data', foreground=self.colors['text_data'])
        self.result_text.tag_config('error_data', foreground=self.colors['text_error_data'], 
                                  font=self.colors['font_bold'])
        self.result_text.tag_config('highlight', background=self.colors['header'], 
                                  foreground=self.colors['text_highlight'])

    def create_error_frame(self, parent):
        """Hata simülasyon çerçevesini oluştur"""
        error_frame = ttk.LabelFrame(parent, text="Hata Simülasyonu", padding="10")
        error_frame.grid(row=5, column=0, sticky="ew", pady=(10, 0))
        
        # Hata tipi seçimi
        ttk.Label(error_frame, text="Hata Tipi:", font=self.colors['font_bold']).grid(
            row=0, column=0, padx=5, pady=5, sticky="w")
        self.error_type = ttk.Combobox(error_frame, values=["Tek bit hatası", "Çift bit hatası"], 
                                     state="readonly", font=self.colors['font_large'])
        self.error_type.current(0)
        self.error_type.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.error_type.bind("<<ComboboxSelected>>", self.update_error_inputs)
        
        # Hata pozisyon girişleri
        ttk.Label(error_frame, text="Hata Bit Pozisyonu(ları):", font=self.colors['font_bold']).grid(
            row=0, column=2, padx=5, pady=5, sticky="w")
        self.error_pos1 = ttk.Entry(error_frame, width=5, font=self.colors['font_mono'])
        self.error_pos1.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        self.error_pos2_label = ttk.Label(error_frame, text="ve", font=self.colors['font_bold'])
        self.error_pos2_label.grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.error_pos2 = ttk.Entry(error_frame, width=5, font=self.colors['font_mono'])
        self.error_pos2.grid(row=0, column=5, padx=5, pady=5, sticky="w")
        self.error_pos2_label.grid_remove()
        self.error_pos2.grid_remove()

    def create_menu_bar(self):
        """Menü çubuğunu oluştur"""
        menubar = tk.Menu(self.root, font=self.colors['font_large'])
        helpmenu = tk.Menu(menubar, tearoff=0, font=self.colors['font_large'])
        helpmenu.add_command(label="Kullanım Kılavuzu", command=self.show_help)
        helpmenu.add_command(label="Hakkında", command=self.show_about)
        menubar.add_cascade(label="Yardım", menu=helpmenu)
        self.root.config(menu=menubar)

    def update_error_inputs(self, event=None):
        """Seçilen hata tipine göre hata giriş alanlarını güncelle"""
        if self.error_type.get() == "Çift bit hatası":
            self.error_pos2_label.grid()
            self.error_pos2.grid()
        else:
            self.error_pos2_label.grid_remove()
            self.error_pos2.grid_remove()

    def update_direction(self):
        """Kullanıcı seçimine göre bit yönünü güncelle"""
        self.direction = self.direction_var.get()
        if self.encoded_data:
            self.encode_data()

    def toggle_raw_data(self):
        """Ham veri ve etiketli bitler arasında geçiş yap"""
        self.show_raw_data = bool(self.show_raw_var.get())
        if self.encoded_data:
            self.visualize_bits()

    def update_data_entry(self, event=None):
        """Seçilen veri boyutuna göre veri giriş alanını güncelle"""
        try:
            data_size = int(self.data_size.get())
            self.data_input.delete(0, tk.END)
            self.data_input.insert(0, "0" * data_size)
        except:
            pass

    def calculate_parity_bits(self, data_size):
        """Verilen veri boyutu için gereken parity bit sayısını hesapla"""
        p = 0
        while (2 ** p) < (data_size + p + 1):
            p += 1
        return p

    def visualize_bits(self):
        """Bitleri renk kodlamasıyla görselleştir"""
        # Önceki bit etiketlerini temizle
        for label in self.bit_labels:
            label.destroy()
        self.bit_labels = []

        if not self.encoded_data:
            return

        total_bits = len(self.encoded_data)
        p = self.last_p
        parity_positions = [2**i for i in range(p)] + [total_bits]

        for i, bit in enumerate(self.encoded_data):
            bit_pos = i + 1 if self.direction == "left_to_right" else total_bits - i
            is_parity = (bit_pos in parity_positions) or (bit_pos == total_bits)
            
            bg_color = self.colors['parity_bit'] if is_parity else self.colors['data_bit']
            text = f"{bit}"
            
            if not self.show_raw_data:
                prefix = "P" if is_parity else "D"
                text = f"{prefix}{bit_pos}"

            label = tk.Label(self.bit_frame, text=text, bg=bg_color, relief=tk.RIDGE, 
                           width=4, height=2, font=self.colors['font_bold'])
            label.grid(row=0, column=i, padx=2, pady=2)
            self.bit_labels.append(label)
        
        # Canvas kaydırma bölgesini güncelle
        self.bit_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def encode_data(self):
        """Hamming kodu kullanarak giriş verisini kodla"""
        try:
            data_size = int(self.data_size.get())
            data_str = self.data_input.get().strip()

            # Girişi doğrula
            if not data_str or len(data_str) != data_size:
                messagebox.showerror("Hata", f"Lütfen geçerli {data_size}-bitlik binary veri girin!")
                return

            if any(bit not in '01' for bit in data_str):
                messagebox.showerror("Hata", "Veri sadece 0 ve 1'lerden oluşmalıdır.")
                return

            # Girişi integer listesine dönüştür
            data = [int(bit) for bit in data_str]
            p = self.calculate_parity_bits(data_size)
            total_bits = data_size + p
            self.last_p = p

            # Hamming kodu dizisini başlat
            hamming_code = [0] * (total_bits + 1)  # +1 genel parity biti için
            j = 0

            # Veri bitlerini 2'nin kuvveti olmayan pozisyonlara yerleştir
            for i in range(1, total_bits + 1):
                if not (i & (i - 1)) == 0:  # 2'nin kuvveti değil
                    hamming_code[i - 1] = data[j]
                    j += 1

            # Parity bitlerini hesapla
            for i in range(p):
                pos = 2 ** i
                parity = 0
                for j in range(1, total_bits + 1):
                    if j & pos:
                        parity ^= hamming_code[j - 1]
                hamming_code[pos - 1] = parity

            # Genel parity'yi hesapla
            overall_parity = 0
            for bit in hamming_code[:-1]:
                overall_parity ^= bit
            hamming_code[-1] = overall_parity

            # Sağdan-sola yönü için ters çevir
            if self.direction == "right_to_left":
                hamming_code = hamming_code[::-1]

            self.encoded_data = hamming_code.copy()

            # Sonuçları renk kodlamasıyla göster
            self.display_encoding_results(data, hamming_code, p)

            # Bitleri görselleştir
            self.visualize_bits()

        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

    def display_encoding_results(self, original_data, hamming_code, p):
        """Kodlama sonuçlarını sonuçlar text alanında göster"""
        self.result_text.delete(1.0, tk.END)
        
        # Orijinal veriyi göster
        self.result_text.insert(tk.END, "Orijinal Veri: ", 'header')
        self.result_text.insert(tk.END, f"{''.join(map(str, original_data))}\n", 'data')
        
        # Hamming kodunu göster
        self.result_text.insert(tk.END, "Hamming Kodu: ", 'header')
        self.result_text.insert(tk.END, f"{''.join(map(str, hamming_code))}\n\n", 'data')
        
        # Etiketlerle bit pozisyonlarını göster
        bit_positions = list(range(1, len(hamming_code) + 1))
        if self.direction == "right_to_left":
            bit_positions = bit_positions[::-1]
        
        self.result_text.insert(tk.END, "Bit Pozisyonları:\n", 'header')
        for i, pos in enumerate(bit_positions):
            is_parity = (pos in [2**i for i in range(p)] + [len(hamming_code)])
            prefix = "P" if is_parity else "D"
            
            if is_parity:
                self.result_text.insert(tk.END, f"{prefix}{pos}: ", 'parity')
                self.result_text.insert(tk.END, f"{hamming_code[i]}  ", 'data')
            else:
                self.result_text.insert(tk.END, f"{prefix}{pos}: {hamming_code[i]}  ", 'data')
            
            if (i+1) % 8 == 0:
                self.result_text.insert(tk.END, "\n")
        
        # Parity bit pozisyonlarını göster
        self.result_text.insert(tk.END, "\n\nParity Bit Pozisyonları: ", 'header')
        self.result_text.insert(tk.END, ", ".join(str(2**i) for i in range(p)), 'parity')
        self.result_text.insert(tk.END, f" ve {len(hamming_code)} (genel parity)", 'parity')

    def store_to_memory(self):
        """Mevcut kodlanmış veriyi belleğe kaydet"""
        if not self.encoded_data:
            messagebox.showerror("Hata", "Lütfen önce Hamming kodunu hesaplayın!")
            return
        key = f"data_{len(self.memory) + 1}"
        self.memory[key] = self.encoded_data.copy()
        self.result_text.insert(tk.END, f"\n\nVeri belleğe kaydedildi: {key}\n", 'header')

    def read_from_memory(self):
        """Bellekten son kaydedilmiş veriyi oku"""
        if not self.memory:
            messagebox.showerror("Hata", "Bellekte veri yok!")
            return
        key = list(self.memory.keys())[-1]
        self.encoded_data = self.memory[key].copy()
        self.result_text.insert(tk.END, f"\nBellekten okunan veri ({key}): ", 'header')
        self.result_text.insert(tk.END, f"{''.join(map(str, self.encoded_data))}\n", 'data')
        self.visualize_bits()

    def introduce_error(self):
        """Kodlanmış veriye kullanıcı girişine göre hata ekle"""
        if not self.encoded_data:
            messagebox.showerror("Hata", "Lütfen önce veri oluşturun veya bellekten okuyun!")
            return
            
        error_type = self.error_type.get()
        
        try:
            if error_type == "Tek bit hatası":
                self.handle_single_bit_error()
            elif error_type == "Çift bit hatası":
                self.handle_double_bit_error()

        except ValueError:
            messagebox.showerror("Hata", "Lütfen hata pozisyonları için geçerli sayılar girin!")

    def handle_single_bit_error(self):
        """Tek bit hatası simülasyonunu yönet"""
        error_pos = int(self.error_pos1.get())
        total_bits = len(self.encoded_data)
        
        if error_pos < 1 or error_pos > total_bits:
            messagebox.showerror("Hata", f"Geçersiz bit pozisyonu! 1-{total_bits} arasında olmalıdır.")
            return

        # Yöne göre pozisyonu ayarla
        actual_pos = error_pos - 1 if self.direction == "left_to_right" else total_bits - error_pos

        # Hatalı veri oluştur
        error_data = self.encoded_data.copy()
        error_data[actual_pos] ^= 1

        # Hata bilgisini göster
        self.result_text.insert(tk.END, "\n\nPozisyon ", 'header')
        self.result_text.insert(tk.END, f"{error_pos}", 'error')
        self.result_text.insert(tk.END, f" tek bit hatalı veri: ", 'header')
        
        # Hata bitini görüntüde vurgula
        for i, bit in enumerate(error_data):
            if i == actual_pos:
                self.result_text.insert(tk.END, str(bit), 'error_data')
            else:
                self.result_text.insert(tk.END, str(bit), 'data')
        self.result_text.insert(tk.END, "\n")
        
        # Hatayı tespit et ve düzelt
        info = self.detect_and_correct_error(error_data)
        self.result_text.insert(tk.END, "\nSendrom Analizi:\n", 'header')
        self.result_text.insert(tk.END, f"{info}\n", 'data')

        # Düzeltilmiş veriyi göster
        self.result_text.insert(tk.END, "\nDüzeltilmiş Veri: ", 'header')
        for i, bit in enumerate(self.encoded_data):
            if i == actual_pos:
                self.result_text.insert(tk.END, str(bit), 'corrected')
            else:
                self.result_text.insert(tk.END, str(bit), 'data')
        self.result_text.insert(tk.END, "\n")

        # Hatayı görsel olarak vurgula
        self.highlight_error(actual_pos, "error")
        self.visualize_bits()

    def handle_double_bit_error(self):
        """Çift bit hatası simülasyonunu yönet"""
        error_pos1 = int(self.error_pos1.get())
        error_pos2 = int(self.error_pos2.get())
        total_bits = len(self.encoded_data)
        
        # Pozisyonları doğrula
        if error_pos1 < 1 or error_pos1 > total_bits or error_pos2 < 1 or error_pos2 > total_bits:
            messagebox.showerror("Hata", f"Geçersiz bit pozisyonları! 1-{total_bits} arasında olmalıdır.")
            return
            
        if error_pos1 == error_pos2:
            messagebox.showerror("Hata", "Hata pozisyonları farklı olmalıdır!")
            return

        # Yöne göre pozisyonları ayarla
        if self.direction == "left_to_right":
            actual_pos1 = error_pos1 - 1
            actual_pos2 = error_pos2 - 1
        else:
            actual_pos1 = total_bits - error_pos1
            actual_pos2 = total_bits - error_pos2

        # Hatalı veri oluştur
        error_data = self.encoded_data.copy()
        error_data[actual_pos1] ^= 1
        error_data[actual_pos2] ^= 1

        # Hata bilgisini göster
        self.result_text.insert(tk.END, "\n\nPozisyon ", 'header')
        self.result_text.insert(tk.END, f"{error_pos1}", 'error')
        self.result_text.insert(tk.END, " ve ", 'header')
        self.result_text.insert(tk.END, f"{error_pos2}", 'error')
        self.result_text.insert(tk.END, f" çift bit hatalı veri: ", 'header')
        
        # Hata bitlerini görüntüde vurgula
        for i, bit in enumerate(error_data):
            if i == actual_pos1 or i == actual_pos2:
                self.result_text.insert(tk.END, str(bit), 'error_data')
            else:
                self.result_text.insert(tk.END, str(bit), 'data')
        self.result_text.insert(tk.END, "\n")
        
        # Hatayı tespit et (çift bit hataları düzeltilemez)
        info = self.detect_double_error(error_data)
        self.result_text.insert(tk.END, "\nSendrom Analizi:\n", 'header')
        self.result_text.insert(tk.END, f"{info}\n", 'data')

        # Hataları görsel olarak vurgula
        self.highlight_error(actual_pos1, "error")
        self.highlight_error(actual_pos2, "error")

    def detect_double_error(self, data):
        """Veride çift bit hatalarını tespit et"""
        working_data = data.copy()
        
        if self.direction == "right_to_left":
            working_data = working_data[::-1]

        total_bits = len(working_data) - 1
        p = self.last_p
        syndrome = 0

        # Syndrome'u hesapla
        for i in range(p):
            pos = 2 ** i
            parity = 0
            for j in range(1, total_bits + 1):
                if j & pos:
                    parity ^= working_data[j - 1]
            if parity != 0:
                syndrome += pos

        # Genel parity'yi hesapla
        overall_parity = 0
        for bit in working_data:
            overall_parity ^= bit

        # Hata tipini belirle
        if syndrome == 0 and overall_parity == 0:
            return "Hata tespit edilmedi (çift bit hatası ile olası değil)."
        elif syndrome == 0 and overall_parity == 1:
            return "Çift bit hatası tespit edildi (sendrom 0 ama genel parity tek)."
        else:
            return f"Çift bit hatası tespit edildi (sendrom = {syndrome}, genel parity = {overall_parity}). Not: Çift bit hataları düzeltilemez."

    def highlight_error(self, pos, error_type):
        """Görselleştirmede bir hata bitini vurgula"""
        if pos < 0 or pos >= len(self.bit_labels):
            return
            
        if error_type == "corrected":
            color = self.colors['corrected']
        elif error_type == "error":
            color = self.colors['error']
        else:
            return
        
        self.bit_labels[pos].config(bg=color)
        self.root.after(2000, lambda: self.reset_highlight(pos))

    def reset_highlight(self, pos):
        """Bir bitin vurgusunu orijinal rengine sıfırla"""
        if pos < 0 or pos >= len(self.bit_labels):
            return
            
        total_bits = len(self.encoded_data)
        p = self.last_p
        parity_positions = [2**i for i in range(p)] + [total_bits]
        
        bit_pos = pos + 1 if self.direction == "left_to_right" else total_bits - pos
        is_parity = (bit_pos in parity_positions) or (bit_pos == total_bits)
        
        bg_color = self.colors['parity_bit'] if is_parity else self.colors['data_bit']
        self.bit_labels[pos].config(bg=bg_color)

    def detect_and_correct_error(self, data):
        """Verideki tek bit hatalarını tespit et ve düzelt"""
        working_data = data.copy()
        
        if self.direction == "right_to_left":
            working_data = working_data[::-1]

        total_bits = len(working_data) - 1
        p = self.last_p
        syndrome = 0

        # Syndrome'u hesapla
        for i in range(p):
            pos = 2 ** i
            parity = 0
            for j in range(1, total_bits + 1):
                if j & pos:
                    parity ^= working_data[j - 1]
            if parity != 0:
                syndrome += pos

        # Genel parity'yi hesapla
        overall_parity = 0
        for bit in working_data:
            overall_parity ^= bit

        # Hatayı belirle ve düzelt
        if syndrome == 0 and overall_parity == 0:
            return "Hata tespit edilmedi."
        elif syndrome == 0 and overall_parity == 1:
            working_data[-1] ^= 1
            self.encoded_data = working_data.copy() if self.direction == "left_to_right" else working_data[::-1].copy()
            return "Genel parity bitinde tek bit hatası tespit edildi ve düzeltildi."
        elif syndrome != 0 and overall_parity == 1:
            working_data[syndrome - 1] ^= 1
            self.encoded_data = working_data.copy() if self.direction == "left_to_right" else working_data[::-1].copy()
            self.highlight_error(syndrome - 1 if self.direction == "left_to_right" else len(working_data) - syndrome, "corrected")
            return f"{syndrome}. pozisyonda tek bit hatası tespit edildi ve düzeltildi."
        else:
            return f"Çift bit hatası tespit edildi (düzeltilemez). Sendrom {syndrome} pozisyonundaki bitlerle ilgili hataları gösteriyor."

    def restart_simulation(self):
        """Simülasyonu başlangıç durumuna sıfırla"""
        self.encoded_data = None
        self.data_input.delete(0, tk.END)
        self.data_input.insert(0, "0" * int(self.data_size.get()))
        self.error_pos1.delete(0, tk.END)
        self.error_pos2.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)
        
        for label in self.bit_labels:
            label.destroy()
        self.bit_labels = []

    def show_help(self):
        """Yardım mesajını göster"""
        help_text = """Hamming SEC-DED Kod Simülatörü - Kullanım Kılavuzu

1. Veri Boyutu Seçin: Veriniz için 8, 16 veya 32 bit seçin
2. Binary Veri Girin: Verinizi 0 ve 1'ler olarak girin (örn., 10101010)
3. Bit Yönü: Bitlerin nasıl görüntüleneceğini seçin (soldan-sağa veya sağdan-sola)
4. Hamming Kodunu Hesapla: Kodlanmış veri oluşturmak için tıklayın
5. Belleğe Kaydet: Kodlanmış veriyi daha sonra kullanmak üzere kaydedin
6. Bellekten Oku: Daha önce kaydedilmiş veriyi geri yükleyin
7. Hata Ekle: 
   - Tek bit hataları için: Simülatör hatayı tespit edip düzeltecek
   - Çift bit hataları için: Simülatör hatayı tespit edecek ama düzeltemeyecek
8. Ham Veriyi Göster: Gerçek bit değerlerini göster (varsayılan olarak açık)

Renk Kodlaması:
- Mavi: Parity bitleri
- Açık Mavi: Veri bitleri
- Kırmızı: Hatalı bitler
- Yeşil: Düzeltilmiş bitler

Bu simülatör, Hamming kodlarının veri depolama ve iletimde hataları nasıl tespit edip düzelttiğini gösterir."""
        messagebox.showinfo("Kullanım Kılavuzu", help_text)

    def show_about(self):
        """Hakkında mesajını göster"""
        messagebox.showinfo("Hakkında", 
                          "Hamming SEC-DED Kod Simülatörü\n"
                          "Sürüm 1.1\n\n"
                          "Bu simülatör, Hamming kodlarının veri depolama ve iletimde hataları nasıl tespit edip düzelttiğini gösterir.\n\n"
                          "Özellikler:\n"
                          "- Tek Hata Düzeltme (SEC)\n"
                          "- Çift Hata Tespiti (DED)\n"
                          "- Etkileşimli görselleştirme\n"
                          "- Bellek simülasyonu\n"
                          "- Yazı tipleri ve renklerle gelişmiş arayüz")

if __name__ == "__main__":
    root = tk.Tk()
    app = HammingCodeSimulator(root)
    root.mainloop()