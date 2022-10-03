import yaml, os, logging, sys
from PyQt5.QtWidgets import  QLineEdit, QPushButton, QApplication, QMainWindow, \
                            QFileDialog, QInputDialog, QLabel, QMessageBox, QWidget
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPalette, QColor


logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s',
                    handlers=[logging.StreamHandler()])

THIS_FILEPATH = os.path.realpath(os.path.dirname(sys.argv[0]))

DEBUG = False




class QMainWindow2(QMainWindow):
    # if not DEBUG:
    #     def closeEvent(self,event):
    #         result = QMessageBox.question(self,
    #                       "Confirm exit", 
    #                       "Confirm exit? Save splits manually before closing.",
    #                       QMessageBox.Yes| QMessageBox.No)
    #         event.ignore()
    
    #         if result == QMessageBox.Yes:
    #             event.accept()
    pass


class MainWindow(object):
    
    size = 1
    
    if size == 1:
        SCREEN_HEIGHT = 480
        SCREEN_WIDTH = 480
        RESET_X = 125
        INPUT_X = 220
        UNDO_X = 280
        LOAD_X = 60
        CREATE_X = 195
        SAVE_X = 325
        BOTTOM_BUTTON_Y = 440
        
        CURRENT_LABEL_X = 170
        PB_LABEL_X = 290
        COMPARE_LABEL_X = 350
        LABELS_Y = 35
        
        TOTAL_CURRENT_X = 200
        TOTAL_PB_X = 297
        TOTAL_COMPARE_X = 385
                
        TOTAL_LABEL_OFFSET = 10
            
        ENTRY_CURRENT_X = TOTAL_CURRENT_X + 0
        ENTRY_PB_X = TOTAL_PB_X + 0
        ENTRY_COMPARE_X = TOTAL_COMPARE_X + 0
        
        FONT_SIZE = 16
        
        ENTRY_X_SIZE = 160
        
    if size == 2:
        SCREEN_HEIGHT = 480
        SCREEN_WIDTH = 540
        RESET_X = 140
        INPUT_X = 250
        UNDO_X = 325
        LOAD_X = 60
        CREATE_X = 230
        SAVE_X = 390
        BOTTOM_BUTTON_Y = 440
        
        CURRENT_LABEL_X = 180
        PB_LABEL_X = 320
        COMPARE_LABEL_X = 400
        LABELS_Y = 35
        
        TOTAL_CURRENT_X = 220
        TOTAL_PB_X = 330
        TOTAL_COMPARE_X = 440
        
        TOTAL_LABEL_OFFSET = 10
            
        ENTRY_CURRENT_X = TOTAL_CURRENT_X + 0
        ENTRY_PB_X = TOTAL_PB_X + 0
        ENTRY_COMPARE_X = TOTAL_COMPARE_X + 0

        
        FONT_SIZE = 16
        
        ENTRY_X_SIZE = 200
        
                
    def __init__(self):
        self.app = QApplication([])
        self.window = QMainWindow2()
        self.window.setFixedSize(self.SCREEN_WIDTH,self.SCREEN_HEIGHT)
        self.window.setWindowTitle('No Damage Tracker')
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(os.path.join(THIS_FILEPATH,"ico.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.window.setWindowIcon(self.icon)

        self.splits_path = ""
        self.splits_dict = {}
        
        for k, v in self.splits_dict.items():
            print("%s: %s" % (k,v))
    
        self.splits = list(self.splits_dict.keys())
        self.split_values = list(self.splits_dict.values())




        self.current_idx = 0
        self.current_status = "waiting_for_splits"
        
        self.end_idx = len(self.splits)
        
        self.total_hits = 0
        
        self.total_hits_pb = sum(self.split_values)

        self.start_button = QPushButton("Start",self.window)
        self.start_button.setGeometry(QtCore.QRect(5, 5, 80, 30))
        self.start_button.clicked.connect(self.start_click)


        self.reset_button = QPushButton("Reset",self.window)
        self.reset_button.setGeometry(QtCore.QRect(self.RESET_X, 5, 80, 30))
        self.reset_button.clicked.connect(self.reset_splits_click)
        

        self.undo_button = QPushButton("Undo",self.window)
        self.undo_button.setGeometry(QtCore.QRect(self.UNDO_X, 5, 80, 30))
        self.undo_button.clicked.connect(self.undo_split)
        self.undo_button.hide()


        self.load_button = QPushButton("Load",self.window)
        self.load_button.setGeometry(QtCore.QRect(self.LOAD_X, self.BOTTOM_BUTTON_Y, 80, 30))
        self.load_button.clicked.connect(self.load_splits)

        self.create_button = QPushButton("Create",self.window)
        self.create_button.setGeometry(QtCore.QRect(self.CREATE_X, self.BOTTOM_BUTTON_Y, 80, 30))
        self.create_button.clicked.connect(self.create_splits_click)

        self.save_button = QPushButton("Save",self.window)
        self.save_button.setGeometry(QtCore.QRect(self.SAVE_X, self.BOTTOM_BUTTON_Y, 80, 30))
        self.save_button.clicked.connect(self.save_splits)
        



        # self.video_button.clicked.connect(self.video_input_click)
        self.current_split_input = QLineEdit("",self.window)
        self.current_split_input.setStyleSheet("border: 2px solid green;")
        self.current_split_input.setGeometry(QtCore.QRect(self.INPUT_X, 5, 40, 30)) 
        self.current_split_input.setAlignment(QtCore.Qt.AlignCenter)
        self.current_split_input.returnPressed.connect(self.post_current_entry)
        self.current_split_input.hide()
        
        

        
            
        self.current_run_label = QLabel("Current",self.window)
        self.current_run_label.setGeometry(QtCore.QRect(self.CURRENT_LABEL_X, self.LABELS_Y, 160, 30))
        self.current_run_label.setStyleSheet("font:bold;padding-left: 5px;")
            
        self.pb_run_label = QLabel("PB",self.window)
        self.pb_run_label.setGeometry(QtCore.QRect(self.PB_LABEL_X, self.LABELS_Y, 160, 30))
        self.pb_run_label.setStyleSheet("font:bold;padding-left: 5px;")
        
        self.compare_run_label = QLabel("Compare",self.window)
        self.compare_run_label.setGeometry(QtCore.QRect(self.COMPARE_LABEL_X, self.LABELS_Y, 160, 30))
        self.compare_run_label.setStyleSheet("font:bold;padding-left: 5px;")
        
 
        OFFSET = 2
        
        
            
        self.total_label = QLabel("Total",self.window)
        self.total_label.setGeometry(QtCore.QRect(5, self.TOTAL_LABEL_OFFSET + 30 * OFFSET, 160, 30))
        self.total_label.setStyleSheet("font:bold;padding-left: 5px;")

        
        self.total_current = QLabel("", self.window)
        self.total_current.setGeometry(QtCore.QRect(self.TOTAL_CURRENT_X, self.TOTAL_LABEL_OFFSET + 30 * OFFSET, 35, 30))
        self.total_current.setAlignment(QtCore.Qt.AlignCenter)
        # self.total_current.setStyleSheet("border:2px solid rgb(255,255,255);font:bold;align:center; ")
        self.total_current.setStyleSheet("font:bold;align:center; ")

        
        self.total_pb = QLabel(str(self.total_hits_pb), self.window)
        self.total_pb.setGeometry(QtCore.QRect(self.TOTAL_PB_X, self.TOTAL_LABEL_OFFSET + 30 * OFFSET, 35, 30))
        self.total_pb.setAlignment(QtCore.Qt.AlignCenter)
        self.total_pb.setStyleSheet("font:bold;align:center;color: ")


        self.total_compare = QLabel("", self.window)
        self.total_compare.setGeometry(QtCore.QRect(self.TOTAL_COMPARE_X, self.TOTAL_LABEL_OFFSET + 30 * OFFSET, 35, 30))
        self.total_compare.setAlignment(QtCore.Qt.AlignCenter)
        self.total_compare.setStyleSheet("font:bold;align:center;color: ")
 





        self.init_splits()



        
        # Final settings
        self.app.setStyle('Fusion')
        self.app.setFont(QtGui.QFont("Segoe UI", self.FONT_SIZE))
        
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(120, 120, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.app.setPalette(palette)

        
    def init_splits(self):
        
        
    

        OFFSET = 3

        
        for idx, name in enumerate(self.splits):

            
            self.entry = QLabel(name,self.window)
            self.entry.setGeometry(QtCore.QRect(5, 5 + 30 * OFFSET, self.ENTRY_X_SIZE, 30))
            self.entry.setStyleSheet("font:bold;padding-left: 5px;font-size: %s;" % str(self.FONT_SIZE+2))
            #self.entry.setStyleSheet("border:2px solid rgb(255,255,255);font:bold;")
            self.entry.setProperty("idx",idx)
            self.entry.setProperty("widget_type","entry")
            self.entry.hide()

            # self.entry_minus = QLabel("-",self.window)
            # self.entry_minus.setGeometry(QtCore.QRect(182, 3 + 30 * OFFSET, 20, 30))
            # self.entry_minus.setStyleSheet("font:bold;color:red;")
            # self.entry_minus.setProperty("idx",idx)
            # self.entry_minus.setProperty("widget_type","entry_minus")
            # self.entry_minus.hide()
            

            # self.entry_plus = QLabel("+",self.window)
            # self.entry_plus.setGeometry(QtCore.QRect(232, 3 + 30 * OFFSET, 20, 30))
            # self.entry_plus.setStyleSheet("font:bold;color:green;")
            # self.entry_plus.setProperty("idx",idx)
            # self.entry_plus.setProperty("widget_type","entry_plus")
            # self.entry_plus.hide()
            

            self.entry_current = QLabel("", self.window)
            self.entry_current.setGeometry(QtCore.QRect(self.ENTRY_CURRENT_X, 5 + 30 * OFFSET, 30, 30))
            self.entry_current.setAlignment(QtCore.Qt.AlignCenter)
            self.entry_current.setStyleSheet("font:bold;align:center")
            self.entry_current.setProperty("idx",idx)
            self.entry_current.setProperty("widget_type","entry_current")
            self.entry_current.hide()

            
            self.entry_pb = QLabel(str(self.split_values[idx]), self.window)
            self.entry_pb.setGeometry(QtCore.QRect(self.ENTRY_PB_X, 5 + 30 * OFFSET, 30, 30))
            self.entry_pb.setAlignment(QtCore.Qt.AlignCenter)
            self.entry_pb.setStyleSheet("font:bold;align:center;color: ")
            self.entry_pb.setProperty("idx",idx)
            self.entry_pb.setProperty("widget_type","entry_pb")
            self.entry_pb.hide()
            
            self.entry_compare = QLabel("", self.window)
            self.entry_compare.setGeometry(QtCore.QRect(self.ENTRY_COMPARE_X, 5 + 30 * OFFSET, 30, 30))
            self.entry_compare.setAlignment(QtCore.Qt.AlignCenter)
            self.entry_compare.setStyleSheet("font:bold;align:center;color: ")
            self.entry_compare.setProperty("idx",idx)
            self.entry_compare.setProperty("widget_type","entry_compare")
            self.entry_compare.hide()
            
            
            # self.entry_box.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
            
            OFFSET+=1
            
                
        self.show_current_splits()





    def start_click(self):
        if self.current_status == "waiting_for_splits":
            print("WAITING FOR SPLITS")
            QMessageBox.about(self.window, "Error", "Load or create splits before starting")
            
        
        if self.current_status == "not_started":
            
            w = [i for i in self.window.children() if i.property("widget_type") == "entry"]
            for i in w:
                style = i.styleSheet()
                if i.property("idx") == self.current_idx:
                    style = "%s;background-color:teal;" % style
                else:
                    style = "%s;background-color:black;" % style
                i.setStyleSheet(style)
    
            self.current_split_input.show()    
            self.current_split_input.setFocus()
            self.start_button.hide()
            self.undo_button.show()
            
            self.show_current_splits()
            
            self.current_status = "started"
            self.total_current.setText("0")
            
        elif self.current_status == "started":
            self.reset_splits()
            
        elif self.current_status == "finished":
            # save data later
            
            self.reset_splits()
            self.current_status = "not_started"
            
            
    def reset_splits_click(self):
        if self.current_status == "waiting_for_splits":
            print("WAITING FOR SPLITS")
            QMessageBox.about(self.window, "Error", "Load splits before starting")        
        else:
            if self.current_status == "finished":
                if int(self.total_current.text()) <= int(self.total_pb.text()):
                    
                    qm = QMessageBox
                    ret = qm.question(self.window,'Keep splits?', "Use this run for PB splits?", qm.Yes | qm.No)
                    
                    if ret == qm.Yes:
                          self.update_pb_splits()
                    
            
            self.reset_splits()
        

    def create_splits_click(self):

        split_names, ok = QInputDialog().getText(self.window, "Create splits",
                                     "Enter split names with commas:", QLineEdit.Normal,"")
        
        if ok:
            
            split_names = split_names.split(",")
            
            d = {}
            for s in split_names:
                if s:
                    d[str(s).strip()] = 10
        
        self.splits_dict = d
        
        new_file = self.save_splits(True)
        
        self.load_splits(new_file)
            




    def update_pb_splits(self):
        
        new_splits = {}
        for idx in range(0, self.end_idx):
            entry_name = [i for i in self.window.children() if i.property("widget_type") == "entry" and i.property("idx") == idx][0]
            current = [i for i in self.window.children() if i.property("widget_type") == "entry_current" and i.property("idx") == idx][0]
            pb = [i for i in self.window.children() if i.property("widget_type") == "entry_pb" and i.property("idx") == idx][0]
            
            new_splits[entry_name.text()] = int(current.text())
            
            pb.setText(current.text())
        
        self.total_pb.setText(self.total_current.text())


        self.splits_dict = new_splits
        
        self.confirm_pb_save()
        
    def confirm_pb_save(self):
        qm = QMessageBox
        ret = qm.question(self.window,'Save splits?', "Save splits to current split file?", qm.Yes | qm.No)
        
        if ret == qm.Yes:
              self.save_splits(use_splits_path=True)

        
    def reset_splits(self):
        self.current_idx = 0
        w = [i for i in self.window.children() if i.property("widget_type") == "entry"]
        for i in w:
            style = i.styleSheet()
            style = "%s;background-color:black;" % style
            i.setStyleSheet(style)
        w = [i for i in self.window.children() if i.property("widget_type") == "entry_current" or i.property("widget_type") == "entry_compare"]
        for i in w:            
            i.setText("")

            style = i.styleSheet()
            style = "%s;color:%s;" % (style, "white")
            i.setStyleSheet(style)

        self.total_compare.setText("")

        style = self.total_compare.styleSheet()
        style = "%s;color:%s;" % (style, "white")
        self.total_compare.setStyleSheet(style)        
        
        self.current_split_input.hide() 
        self.undo_button.hide()
        self.total_hits = 0
        self.current_split_input.setText("")
        self.total_current.setText("")
        self.current_status = "not_started"
        self.start_button.show()
        self.start_button.setText("Start")
            
    def post_current_entry(self):
        
        # print("cur %s : limit %s" % (self.current_idx, self.end_idx))

            
        w = [i for i in self.window.children() if i.property("widget_type") == "entry"]
        for i in w:
            style = i.styleSheet()
            if i.property("idx") == self.current_idx + 1:
                style = "%s;background-color:teal;" % style
            else:
                style = "%s;background-color:black;" % style
            i.setStyleSheet(style)
            
        w = [i for i in self.window.children() if i.property("widget_type") == "entry_current" and i.property("idx") == self.current_idx][0]

        cur_num = self.current_split_input.text()
        try:
            cur_num = int(cur_num)
        except:
            cur_num = 0
        
        w.setText(str(cur_num))
        self.update_total()
        self.calculate_compare()
        self.current_split_input.setText("")

        self.current_idx = self.current_idx + 1
        if self.current_idx == self.end_idx:
            self.start_button.setText("Finish")
            self.current_status = "finished"
            self.current_split_input.hide()
        else:
            
            self.current_split_input.setFocus()
            
            self.show_current_splits()
        
    def calculate_compare(self):
        entry_compare = [i for i in self.window.children() if i.property("widget_type") == "entry_compare" and i.property("idx") == self.current_idx][0]
        entry_current = [i for i in self.window.children() if i.property("widget_type") == "entry_current" and i.property("idx") == self.current_idx][0]
        entry_pb = [i for i in self.window.children() if i.property("widget_type") == "entry_pb" and i.property("idx") == self.current_idx][0]
        
        update_num = int(entry_current.text()) - int(entry_pb.text())
        
        if update_num < 0:
            color = 'green'
        elif update_num > 0:
            color = 'red'
        else:
            color = 'white'

        style = entry_compare.styleSheet()
        style = "%s;color:%s;" % (style, color)
        entry_compare.setStyleSheet(style)
        
        update_text = str(update_num)
        entry_compare.setText(update_text)

        self.calculate_total_compare()

    def calculate_total_compare(self):
        update_num = int(self.total_current.text()) - int(self.total_pb.text())
        
        if update_num < 0:
            color = 'green'
        elif update_num > 0:
            color = 'red'
        else:
            color = 'white'

        
        update_text = str(update_num)

        self.total_compare.setText(update_text)

        style = self.total_compare.styleSheet()
        style = "%s;color:%s;" % (style, color)
        self.total_compare.setStyleSheet(style)
        
        
        
    
    def show_current_splits(self):
        
        
        
        
        cur_idx = self.current_idx
        OFFSET = 4
        
        if self.end_idx < 8:
            start = 0
            end = self.end_idx
        
        elif cur_idx <= 3:        
            # print("SHOW: Top 6 splits")
            start = 0
            end = 8
            
        elif (self.end_idx - cur_idx) <= 4:
            # print("SHOW: Middle splits")
            start = self.end_idx - 8
            end = self.end_idx
        else:
            # print("SHOW: End 6 splits")
            start = cur_idx -4
            end = cur_idx + 4
        
        # print("Range %s - %s" % (start,end))

        
        for idx in range(0, self.end_idx):
            self.hide_all_for_idx(idx)
        
        for idx in range(start, end):
            w = [i for i in self.window.children() if i.property("idx") == idx]
            
            
            
            for i in w:
                try:
                    i.move(i.x(), 5 + (34 * OFFSET))
                    i.show()
                except:
                    pass
                
            OFFSET += 1
    
    def hide_all_for_idx(self, idx):
        w = [i for i in self.window.children() if i.property("idx") == idx]
        
        for i in w:
            i.hide()
            
    def update_total(self):
        entries_current = [i for i in self.window.children() if i.property("widget_type") == "entry_current"]
        
        total_num = 0
        
        for entry in entries_current:
            try:
                num_to_add = int(entry.text())
            except:
                num_to_add = 0    
            total_num += num_to_add
        

        self.total_current.setText(str(total_num))
            
        
        
    def undo_split(self):
        self.current_idx = self.current_idx - 1
        if self.current_idx < 0:
            self.reset_splits()
            
        else:
            w = [i for i in self.window.children() if i.property("widget_type") == "entry"]
            for i in w:
                style = i.styleSheet()
                if i.property("idx") == self.current_idx:
                    style = "%s;background-color:teal;" % style
                else:
                    style = "%s;background-color:black;" % style
                i.setStyleSheet(style)
                
            entry_compare = [i for i in self.window.children() if i.property("widget_type") == "entry_compare" and i.property("idx") == self.current_idx][0]
            entry_current = [i for i in self.window.children() if i.property("widget_type") == "entry_current" and i.property("idx") == self.current_idx][0]
            
            entry_compare.setStyleSheet("%s;color:white;" % entry_compare.styleSheet())
            entry_compare.setText("")
            entry_current.setStyleSheet("%s;color:white;" % entry_current.styleSheet())
            entry_current.setText("")
            
            self.update_total()
            self.calculate_total_compare()
            self.current_split_input.show()
            

            self.show_current_splits()
            self.current_split_input.setFocus()

            self.start_button.setText("Start")
            self.current_status = "started"
    
    def save_splits(self, bypass=False, use_splits_path=False):

        if self.current_status != 'waiting_for_splits' or bypass:
            
            if not use_splits_path:
            
                dialog = QFileDialog()
                new_file = dialog.getSaveFileName(None,"Select splits","",filter="txt (*.txt);;yaml (*.yaml)")
            else:
                new_file = [self.splits_path]
            
            
            
            if new_file[0]:
                with open(new_file[0], 'w') as f:
                    yaml.dump(self.splits_dict, f, sort_keys=False)

            return new_file
    
    def load_splits(self, new_file = False):
        
        if not new_file:
            
            dialog = QFileDialog()
            new_file = dialog.getOpenFileName(None,"Select splits","",filter="txt (*.txt);;yaml (*.yaml)")
    

        
        if new_file[0] != "":
            with open(new_file[0], 'r') as f:
                d = yaml.safe_load(f)
                
            self.splits_path = new_file[0]
            
            
            self.splits_dict = d
            
            for k, v in self.splits_dict.items():
                print("%s: %s" % (k,v))
        
            self.splits = list(self.splits_dict.keys())
            self.split_values = list(self.splits_dict.values())
    
            self.current_status = "not_started"
    
            self.current_idx = 0
            self.current_status = "waiting_for_splits"
            
            self.end_idx = len(self.splits)
            
            self.total_hits = 0
            
            self.total_hits_pb = sum(self.split_values)
            self.total_pb.setText(str(self.total_hits_pb))
    
            
    
            self.reset_splits()
            
            for i in [i for i in self.window.children() if i.property("widget_type")]:
                
                i.deleteLater()
            
            self.init_splits()
        
            
            
if __name__ == '__main__':
    main_window = MainWindow()
    main_window.window.show()
    main_window.app.exec_()