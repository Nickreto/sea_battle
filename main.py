import sys
import random
from PyQt5.QtMultimedia import QSound, QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, Qt, QTimer, QSize
from PyQt5.QtWidgets import (
    QSlider,
    QApplication, QWidget, QPushButton, QGridLayout,
    QMessageBox, QVBoxLayout, QLabel, QDialog, QDialogButtonBox, QRadioButton,
    QButtonGroup, QFrame
)
from PyQt5.QtGui import QPalette, QPixmap, QBrush, QTransform, QIcon

BOARD_SIZE = 8
MAX_ATTEMPTS = 31

QUESTIONS = [
    ("Когда началась Русско-японская война?", "1904", ["1900", "1902", "1904", "1906"]),
    ("Когда закончилась Русско-японская война?", "1905", ["1904", "1905", "1906", "1907"]),
    ("Какой город был осаждён японцами в 1904 году?", "Порт-Артур", ["Владивосток", "Порт-Артур", "Дальний", "Харбин"]),
    ("Кто командовал русским флотом в Цусимском сражении?", "Рождественский", ["Макаров", "Рождественский", "Небогатов", "Скрядин"]),
    ("Какой договор завершил Русско-японскую войну?", "Портсмутский мир", ["Берлинский договор", "Портсмутский мир", "Тильзитский мир", "Сен-Жерменский договор"]),
    ("Какое сражение стало решающим в Русско-японской войне?", "Цусимское сражение", ["Мукден", "Порт-Артур", "Цусимское сражение", "Сахалин"]),
    ("Какая территория стала предметом конфликта?", "Маньчжурия", ["Корея", "Маньчжурия", "Сибирь", "Курилы"]),
    ("Кто был императором России в период войны?", "Николай II", ["Александр III", "Николай II", "Александр II", "Павел I"]),
    ("Кто был президентом США — посредник в переговорах?", "Теодор Рузвельт", ["Авраам Линкольн", "Томас Вудро Вильсон", "Теодор Рузвельт", "Гарри Трумэн"]),
    ("Какое море стало ареной Цусимского сражения?", "Японское море", ["Охотское море", "Жёлтое море", "Японское море", "Восточно-Китайское море"]),
    ("Где произошло Мукденское сражение?", "Маньчжурия", ["Корея", "Сахалин", "Маньчжурия", "Приморье"]),
    ("С какого направления шёл русский флот в Цусимском сражении?", "Из Балтийского моря", ["Из Чёрного моря", "Из Тихого океана", "Из Балтийского моря", "Из Северного моря"]),
    ("Какой русский адмирал погиб в Порт-Артуре?", "Макаров", ["Рождественский", "Макаров", "Небогатов", "Александров"]),
    ("Кто был командующим сухопутной армией России?", "Куропаткин", ["Линевич", "Стессель", "Куропаткин", "Алексеев"]),
    ("Какой город сдался японцам после длительной осады?", "Порт-Артур", ["Мукден", "Владивосток", "Харбин", "Порт-Артур"]),
    ("Кто был главнокомандующим японской армией?", "Ояма Ивао", ["Тоётоми Хидэёси", "Ояма Ивао", "Того Хэйхатиро", "Мэйдзи"]),
    ("Какой полуостров был ареной военных действий?", "Ляодунский", ["Корейский", "Ляодунский", "Камчатский", "Сахалин"]),
    ("Какой порт был важен для Японии в Маньчжурии?", "Порт-Артур", ["Владивосток", "Дальний", "Порт-Артур", "Харбин"]),
    ("Какой транспортный путь имел стратегическое значение?", "КВЖД", ["Транссиб", "КВЖД", "БАМ", "Амурская дорога"]),
    ("Почему Россия потерпела поражение?", "Слабая подготовка и логистика", ["Малочисленная армия", "Голод", "Слабая подготовка и логистика", "География"]),
    ("Как назывался русский флот, пришедший из Балтики?", "2-я Тихоокеанская эскадра", ["1-я Балтийская флотилия", "2-я Тихоокеанская эскадра", "Каспийская эскадра", "Дальневосточная флотилия"]),
    ("Кто командовал японским флотом?", "Того Хэйхатиро", ["Того Хэйхатиро", "Ояма Ивао", "Сайго Такамори", "Мэйдзи"]),
    ("Что стало следствием поражения России?", "Рост революционных настроений", ["Присоединение Кореи", "Реформы армии", "Рост революционных настроений", "Экономический рост"]),
    ("Кто подписал капитуляцию Порт-Артура?", "Стессель", ["Рождественский", "Куропаткин", "Стессель", "Макаров"]),
    ("Какой остров был оккупирован Японией в 1905?", "Южный Сахалин", ["Хоккайдо", "Кунашир", "Южный Сахалин", "Камчатка"]),
    ("Какой корабль был флагманом Рождественского?", "Князь Суворов", ["Цесаревич", "Александр III", "Князь Суворов", "Бородино"]),
    ("Какое вооружение активно использовали японцы?", "Артиллерию", ["Лёгкую кавалерию", "Артиллерию", "Бронепоезда", "Воздушные шары"]),
    ("Сколько длилась война?", "1 год и 7 месяцев", ["6 месяцев", "2 года", "1 год и 7 месяцев", "3 года"]),
    ("Какой тип войск особенно страдал на Дальнем Востоке?", "Пехота", ["Пехота", "Флот", "Кавалерия", "Артиллерия"]),
    ("Почему Портсмутский договор был невыгоден для России?", "Потеря территорий", ["Россия выиграла", "Ничего не потеряла", "Потеря территорий", "Япония капитулировала"]),
    ("Какое влияние война оказала на Японию?", "Рост статуса как державы", ["Упадок", "Раздел", "Рост статуса как державы", "Инфляция"]),
    ("Что произошло с русским флотом в Цусиме?", "Почти полностью уничтожен", ["Одержал победу", "Отступил", "Почти полностью уничтожен", "Спасён союзниками"]),
    ("Где велись главные боевые действия на суше?", "Маньчжурия", ["Корея", "Сибирь", "Маньчжурия", "Япония"]),
    ("Какой генерал был критикуем за бездействие?", "Куропаткин", ["Макаров", "Рождественский", "Куропаткин", "Стессель"]),
    ("Как называли солдат, участвующих в штурме Порт-Артура?", "Смертники", ["Добровольцы", "Десант", "Смертники", "Разведчики"]),
    ("Что стало поводом к войне?", "Конфликт интересов", ["Гибель дипломатов", "Конфликт интересов", "Экономический кризис", "Захват Сибири"]),
    ("Какой город был центром снабжения России?", "Харбин", ["Харбин", "Порт-Артур", "Владивосток", "Чита"]),
    ("Кто возглавлял японскую делегацию в Портсмуте?", "Комура Дзютаро", ["Того", "Комура Дзютаро", "Ояма", "Мэйдзи"]),
    ("Кто был министром иностранных дел России?", "Витте", ["Столыпин", "Витте", "Плеве", "Горчаков"]),
    ("Сколько человек насчитывала русская армия в начале войны?", "300 тыс.", ["100 тыс.", "200 тыс.", "300 тыс.", "500 тыс."]),
    ("Какой символ считался позором после Цусимы?", "Белый флаг", ["Флаг Японии", "Царский флаг", "Белый флаг", "Гюйс"]),
    ("Сколько кораблей было у Рождественского в бою?", "40", ["10", "20", "40", "60"]),
    ("Какое значение имел Сахалин?", "Стратегическое", ["Экономическое", "Символическое", "Стратегическое", "Культурное"]),
    ("Какое новое оружие применялось японцами?", "Миномёты", ["Огнемёты", "Танки", "Миномёты", "Подлодки"]),
    ("Чем закончилась битва под Мукденом?", "Отступление русских", ["Победа русских", "Поражение японцев", "Отступление русских", "Победа союзников"]),
    ("Сколько погибло русских в Цусимском сражении?", "5000", ["1000", "2500", "5000", "7000"]),
    ("Какая тактика привела японцев к успеху?", "Флотская блокада", ["Партизанская война", "Зимняя кампания", "Флотская блокада", "Позиционная война"]),
    ("Какое влияние имело поражение на внутреннюю политику России?", "Начало революции", ["Рост доверия", "Начало реформ", "Начало революции", "Укрепление власти"])
]




class QuestionDialog(QDialog):
    def __init__(self, question, correct_answer, options, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Исторический вопрос")
        self.correct_answer = correct_answer
        layout = QVBoxLayout()

        layout.addWidget(QLabel(question))
        self.buttons = QButtonGroup(self)
        for option in options:
            rb = QRadioButton(option)
            layout.addWidget(rb)
            self.buttons.addButton(rb)

        self.buttons.buttonClicked.connect(self.enable_buttons)
        self.submit = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.submit.accepted.connect(self.accept)
        self.submit.rejected.connect(self.reject)
        self.submit.button(QDialogButtonBox.Ok).setEnabled(False)
        layout.addWidget(self.submit)

        self.setLayout(layout)

    def enable_buttons(self):
        self.submit.button(QDialogButtonBox.Ok).setEnabled(True)

    def selected_answer(self):
        btn = self.buttons.checkedButton()
        return btn.text() if btn else None


class BattleshipGame(QWidget):
    def __init__(self):
        super().__init__()
        self.ship_parts = {}
        self.ship_orientations = {}
        self.effect_volume = 100
        self.music_volume = 30
        self.setWindowTitle("Исторический Морской Бой")
        self.board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.questions_map = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.attempted = [[False] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.buttons = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.ship_cells = {}
        self.hits = 0
        self.destroyed_ships = 0
        self.attempts = 0
        self.total_ship_cells = 2 * 3 + 3 * 2 + 3 * 1
        self.available_questions = QUESTIONS.copy()
        random.shuffle(self.available_questions)
        self.initUI()
        self.place_all_ships()
        self.assign_questions()
        self.music = QMediaPlayer()
        self.music.setMedia(QMediaContent(QUrl.fromLocalFile("Back.mp3")))
        self.music.setVolume(self.music_volume)
        self.music.play()
        self.effect = QMediaPlayer()
        self.effect.setMedia(QMediaContent(QUrl.fromLocalFile("попадание.wav")))
        self.effect.setVolume(self.effect_volume)

    def initUI(self):
        layout = QVBoxLayout()
        self.info_label = QLabel(
            f"Попытки: {self.attempts}/{MAX_ATTEMPTS} | Попаданий: {self.hits}/{self.total_ship_cells} | Уничтожено кораблей: {self.destroyed_ships}")
        layout.addWidget(self.info_label)

        grid = QGridLayout()
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                btn = QPushButton()
                btn.setFixedSize(40, 40)
                btn.clicked.connect(lambda _, r=row, c=col: self.cell_clicked(r, c))
                grid.addWidget(btn, row, col)
                self.buttons[row][col] = btn

        layout.addLayout(grid)
        self.setLayout(layout)

    def play_effect(self, sound_file):
        if self.effect_volume > 0:
            self.effect.setMedia(QMediaContent(QUrl.fromLocalFile(sound_file)))
            self.effect.play()

    def update_info(self):
        self.info_label.setText(
            f"Попытки: {self.attempts}/{MAX_ATTEMPTS} | Попаданий: {self.hits}/{self.total_ship_cells} | Уничтожено кораблей: {self.destroyed_ships}")

    def place_all_ships(self):
        for count, size in [(2, 3), (3, 2), (3, 1)]:
            for _ in range(count):
                self.place_ship(size)

    def is_adjacent_occupied(self, coords):
        for x, y in coords:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                        if self.board[nx][ny] == 1 and (nx, ny) not in coords:
                            return True
        return False

    def place_ship(self, size):
        placed = False
        while not placed:
            vertical = random.choice([True, False])
            r = random.randint(0, BOARD_SIZE - (size if vertical else 1))
            c = random.randint(0, BOARD_SIZE - (1 if vertical else size))
            coords = [(r + i if vertical else r, c if vertical else c + i) for i in range(size)]
            if all(self.board[x][y] == 0 for x, y in coords) and not self.is_adjacent_occupied(coords):
                for i, (x, y) in enumerate(coords):
                    self.board[x][y] = 1
                    self.ship_cells[(x, y)] = coords
                    if size == 1:
                        part_type = "bow"
                        degr = 0
                    elif (vertical and i == 0) or (not vertical and i == 0):
                        part_type = "bow"
                        if vertical:
                            degr = 0
                        else:
                            degr = 1
                    elif (vertical and i == size-1) or (not vertical and i == size-1):
                        part_type = "bow"
                        if vertical:
                            degr = 2
                        else:
                            degr = 3
                    else:
                        part_type = "mid"
                        if vertical:
                            degr = 0
                        else:
                            degr = 1
                    self.ship_parts[(x, y)] = (part_type, vertical, degr)
                    self.ship_orientations[(x, y)] = vertical
                placed = True

    def show_ship_part(self, row, col):
        part_info = self.ship_parts.get((row, col), ("bow", False, 1))
        part_type, vertical, degr = part_info
        transform = QTransform()
        if degr==0:
            transform.rotate(90)
        elif degr==1:
            transform.rotate(0)
        elif degr == 2:
            transform.rotate(270)
        elif degr == 3:
            transform.rotate(180)
        if part_type == "single":
            pixmap = QPixmap("ship_single.png")
        elif part_type == "bow":
            pixmap = QPixmap("ship_bow.png")
        else:
            pixmap = QPixmap("ship_mid.png")
        pixmap = pixmap.transformed(transform)
        icon = QIcon(pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.buttons[row][col].setIcon(icon)
        self.buttons[row][col].setIconSize(QSize(40, 40))
        self.buttons[row][col].setStyleSheet("background-color: transparent;")

    def assign_questions(self):
        flat_questions = self.available_questions * ((BOARD_SIZE * BOARD_SIZE) // len(self.available_questions) + 1)
        index = 0
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.questions_map[r][c] = flat_questions[index % len(flat_questions)]
                index += 1


    def cell_clicked(self, row, col):
        if self.attempted[row][col] or self.attempts >= MAX_ATTEMPTS:
            return

        question, answer, options = self.questions_map[row][col]
        dialog = QuestionDialog(question, answer, options, self)
        if dialog.exec_():
            user_ans = dialog.selected_answer()
            self.attempts += 1
            if user_ans == answer:

                self.play_effect("попадание.wav") if self.board[row][col] == 1 else self.play_effect("промах.wav")
                self.attempted[row][col] = True
                if self.board[row][col] == 1:
                    self.board[row][col] = 2
                    self.hits += 1
                    explosion = QPixmap("explosion.png").scaled(40, 40)
                    self.buttons[row][col].setIcon(QIcon(explosion))
                    self.buttons[row][col].setIconSize(QSize(40, 40))
                    self.buttons[row][col].setStyleSheet("background-color: red;")
                    self.buttons[row][col].setEnabled(False)
                    QTimer.singleShot(2000, lambda r=row, c=col: self.show_ship_part(r, c))

                    self.check_ship_destroyed(row, col)
                else:
                    self.buttons[row][col].setStyleSheet("background-color: blue")
                    self.buttons[row][col].setEnabled(False)
            else:
                self.play_effect("промах.wav")
                QMessageBox.information(self, "Промах", "Неверный ответ. Попробуйте ещё раз позже.")
            self.update_info()
            self.check_end_game()
    def check_ship_destroyed(self, row, col):
        ship = self.ship_cells.get((row, col), [])
        if all(self.board[x][y] == 2 for x, y in ship):
            self.destroyed_ships += 1
            for x, y in ship:
                self.buttons[x][y].setStyleSheet("background-color: gray")
            self.play_effect("уничтожение.wav")
            self.update_info()

    def check_end_game(self):
        if self.hits == self.total_ship_cells:
            QMessageBox.information(self, "Победа!", "Вы уничтожили весь флот врага! Поздравляем!")
            self.close()
        elif self.attempts >= MAX_ATTEMPTS:
            QMessageBox.information(self, "Поражение", "Попытки закончились. Вы проиграли.")
            self.close()


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Главное меню")
        self.setFixedSize(800, 600)
        self.effect_volume = 100
        self.music_volume = 30
        content_frame = QFrame(self)
        content_frame.setGeometry(0, 0, 800, 600)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap("background.jpg").scaled(800, 600)))
        self.setPalette(palette)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        button_style = """
            QPushButton {
                font-size: 16px;
                padding: 10px;
                margin: 10px;
                border-radius: 5px;
                background-color: rgba(0, 0, 100, 150);
                color: white;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 100, 200);
            }
            QSlider::groove:horizontal {
            height: 8px;
            background: #444;
            margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: #fff;
                width: 15px;
                margin: -5px 0;
                border-radius: 7px;
            }
            QSlider::sub-page:horizontal {
                background: #4CAF50;
            }
        """

        play_btn = QPushButton("Играть")
        play_btn.setStyleSheet(button_style)
        info_btn = QPushButton("Информация")
        info_btn.setStyleSheet(button_style)
        exit_btn = QPushButton("Выйти")
        exit_btn.setStyleSheet(button_style)
        self.music_label = QLabel(f"Фоновая музыка: {self.music_volume}")
        self.music_slider = QSlider()
        self.music_slider.setOrientation(Qt.Horizontal)
        self.music_slider.setRange(0, 100)
        self.music_slider.setValue(self.music_volume)
        self.music_slider.valueChanged.connect(self.update_music_volume)
        self.music_slider.setStyleSheet(button_style)
        self.effect_label = QLabel(f"Эффекты: {self.effect_volume}")
        self.effect_slider = QSlider()
        self.effect_slider.setOrientation(Qt.Horizontal)
        self.effect_slider.setRange(0, 100)
        self.effect_slider.setValue(self.effect_volume)
        self.effect_slider.valueChanged.connect(self.update_effect_volume)
        self.effect_slider.setStyleSheet(button_style)
        self.music_label.setStyleSheet("color: white; font-size: 18px;")
        self.effect_label.setStyleSheet("color: white; font-size: 18px;")
        play_btn.clicked.connect(self.play_sound)
        play_btn.clicked.connect(self.start_game)
        info_btn.clicked.connect(self.play_sound)
        info_btn.clicked.connect(self.show_info)
        exit_btn.clicked.connect(self.play_sound)
        exit_btn.clicked.connect(self.close)

        layout.addStretch()
        layout.addWidget(play_btn)
        layout.addWidget(info_btn)
        layout.addWidget(self.music_label)
        layout.addWidget(self.music_slider)
        layout.addWidget(self.effect_label)
        layout.addWidget(self.effect_slider)
        layout.addWidget(exit_btn)
        layout.addStretch()

        self.setLayout(layout)

    def play_sound(self):
        if self.effect_volume > 0:
            QSound.play("кнопка.wav")
    def start_game(self):
        self.hide()
        self.game_window = BattleshipGame()
        self.game_window.effect_volume = self.effect_volume
        self.game_window.music_volume = self.music_volume
        self.game_window.music.setVolume(self.music_volume)
        self.game_window.effect.setVolume(self.effect_volume)
        self.game_window.show()

    def show_info(self):
        info = (
            """Правила игры:\n\n- Поле 8x8, размещены корабли разной длины.\n- Чтобы выстрелить, ответьте на вопрос.\n- Верный ответ = выстрел.\n- Победа: все корабли уничтожены.\n- Поражение: 48 попыток израсходованы."""
        )
        QMessageBox.information(self, "Информация", info)

    def update_music_volume(self, value):
        self.music_volume = value
        self.music_label.setText(f"Фоновая музыка: {value}")

    def update_effect_volume(self, value):
        self.effect_volume = value
        self.effect_label.setText(f"Эффекты: {value}")




if __name__ == '__main__':
    app = QApplication(sys.argv)

    menu = MainMenu()
    menu.show()
    sys.exit(app.exec_())
