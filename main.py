from XRPLib.lineFollow import lineFollow
from XRPLib.differential_drive import DifferentialDrive
from XRPLib.board import Board


line = lineFollow()
board = Board.get_default_board()
diffDrive = DifferentialDrive.get_default_differential_drive()

while not board.is_button_pressed():
    if line.lineDetect():
        line.PIDLineFollow()



