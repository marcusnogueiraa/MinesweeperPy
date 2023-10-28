from src.core.minesweeper import Minesweeper, TheSlotIsAMineException, MinesweeperStatus
from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QPushButton, QApplication

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MinesweeperPy")
        self.setGeometry(100, 100, 360, 360)
        
        self.ROWS = 9
        self.COLUMNS = 9
        self.MINES = 10

        self.mine_sweeper = Minesweeper(self.ROWS, self.COLUMNS, 10)
        self.gridButtons = []
        
        self.setup_ui()

    def setup_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        central_widget.setLayout(self.grid_layout)

        self.build_button_grid()

    def build_button_grid(self):
        for row in range(self.ROWS):
            buttons_row = []
            for column in range(self.COLUMNS):
                slot = QPushButton()
                slot.setFixedSize(40, 40)

                slot.clicked.connect(lambda i=row, j=column: self.select_button(i, j))

                self.grid_layout.addWidget(slot, row, column)
                buttons_row.append(slot)
            self.gridButtons.append(buttons_row)

    def print_p(self):
        print("P")

    def select_button(self, i, j):
        if self.mine_sweeper.get_status() == MinesweeperStatus.NOT_INITIALIZED:
            self.mine_sweeper.build_field(i, j)

        try:
            unlocked_buttons_positions = self.mine_sweeper.select_slot(i, j)
            for button_position in unlocked_buttons_positions:
                position_i, position_j = button_position
                current_button = self.gridButtons[position_i][position_j]
                current_button.setDisabled(True)
                
                button_value = str(self.mine_sweeper.get_value(position_i, position_j))

                if self.mine_sweeper.status == MinesweeperStatus.VICTORY:
                    print("PARABENS VOCE GANHOU")

                if button_value == "0":
                    button_value = ""
                
                current_button.setText(button_value)

        except TheSlotIsAMineException:
            mine_button = self.gridButtons[i][j]
            mine_button.setDisabled(True)
            mine_button.setText("*")
            print("Deu ruim")