# GUI Code for the Python baseball web scraper
# Orion McLain 
# 8/20/23

import sys

### File imports
from playerScraper import find_player_id, get_player_full_name, scrape_hitter_stats, scrape_pitcher_stats

### Visualization Importst
from PyQt6.QtWidgets import QMainWindow, QTabWidget, QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QTableWidget, QTableWidgetItem, QScrollArea
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MLB Player Stat Application")

        self.tab_widget = QTabWidget()
        self.resize(800,800)
        # Create and add the first tab (Player Stats)
        player_stats_tab = PlayerStatsWindow()
        self.tab_widget.addTab(player_stats_tab, "Player Lookup")

        # Create and add the second tab (Another Window)
        second_tab = AnalysisWindow()
        self.tab_widget.addTab(second_tab, "Analysis Tab")

        self.setCentralWidget(self.tab_widget)

class PlayerStatsWindow(QWidget):      # Player Lookup for Recent + Season Stats
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("MLB Player Stat Finder")
        self.setContentsMargins(20,20,20,20)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        top_layout = QHBoxLayout()

        self.label1 = QLabel("Search an MLB Player")
        top_layout.addWidget(self.label1, alignment=Qt.AlignmentFlag.AlignTop)  # Align to the top)

        self.playerSearch = QLineEdit()
        self.playerSearch.returnPressed.connect(self.displayPlayerStats)
        top_layout.addWidget(self.playerSearch, alignment=Qt.AlignmentFlag.AlignTop)  # Align to the top)

        searchButton = QPushButton("Search")
        searchButton.setFixedWidth(50)
        searchButton.clicked.connect(self.displayPlayerStats)
        top_layout.addWidget(searchButton, alignment=Qt.AlignmentFlag.AlignTop)  # Align to the top)

        self.layout.addLayout(top_layout)

         # Create a scroll area to contain the statistics layout
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allow the content to be resized
        self.layout.addWidget(scroll_area)

        # Create a widget to hold the statistics layout
        scroll_widget = QWidget()
        self.statistics_layout = QGridLayout(scroll_widget)
        scroll_area.setWidget(scroll_widget)



    def clearLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
    def displayPlayerStats(self):
        self.clearLayout(self.statistics_layout)   # clear layout before adding next player

        playerID, positions, indicators = find_player_id(self.playerSearch.text())
        self.playerSearch.clear()
        fullName = get_player_full_name(playerID)
        playerTitle = QLabel(fullName + " Stats: " + positions)
        playerTitle.setFont(QFont('Arial', 20))
        playerTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.statistics_layout.addWidget(playerTitle, 0, 0)

        if 'hitter' in indicators:

            playerStats = scrape_hitter_stats(playerID)    # [{Game Stats} , {Last 10} , {Last 20} , {Last 30} , {Season}]
            
            ############  Get 5 most recent games
            gameStats = playerStats['game_stats']
        
            self.recents = QTableWidget(10, 16)
            self.recents.setHorizontalHeaderLabels(['Date', 'Opp', 'Results', 'AB', 'H', 'BB', 'K', 'R', 'RBI', 'HR', 'SB', 'CS', 'BAA', 'OBP', 'SLG', 'OPS'])
            self.recents.verticalHeader().setVisible(False)

             # Set column widths using a loop
            column_widths = [70, 44, 58, 20, 20, 20, 20, 20, 20, 20, 20, 20, 30, 30, 30, 35]  # Adjust these values as needed
            
            for col, width in enumerate(column_widths):
                self.recents.setColumnWidth(col, width)


            for i, game_stat in enumerate(gameStats):
                row = [
                    game_stat['Date'], game_stat['Opp'], game_stat['Results'],
                    game_stat['AB'], game_stat['H'], game_stat['BB'], game_stat['K'],
                    game_stat['R'], game_stat['RBI'], game_stat['HR'], game_stat['SB'],
                    game_stat['CS'], game_stat['BAA'], game_stat['OBP'],
                    game_stat['SLG'], game_stat['OPS']
                ]
                for j, item in enumerate(row):
                    tableEntry = QTableWidgetItem(item)
                    tableEntry.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
                    self.recents.setItem(i, j, tableEntry)
        


            #########  Get last 10 games
            last10 = playerStats['last_10_stats']

            self.last10stats = QTableWidget(1, 10)
            self.last10stats.setHorizontalHeaderLabels(['AB', 'H', 'BB', 'K', 'R', 'RBI', 'HR', 'SB', 'CS', 'BAA'])
            self.last10stats.verticalHeader().setVisible(False)

             # Set column widths using a loop
            column_widths2 = [70, 70, 69, 69, 69, 69, 70, 70, 70, 70]  # Adjust these values as needed
            
            for col, width in enumerate(column_widths2):
                self.last10stats.setColumnWidth(col, width)


            row10 = [
                last10['AB'], last10['H'], last10['BB'], last10['K'],
                last10['R'], last10['RBI'], last10['HR'], last10['SB'],
                last10['CS'], last10['BAA']
            ]
            for j, item in enumerate(row10):
                tableEntry = QTableWidgetItem(str(item))
                tableEntry.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
                self.last10stats.setItem(0, j, tableEntry)

            

            ######### Get last 20 games totals
            last20 = playerStats['last_20_stats']

            self.last20stats = QTableWidget(1, 10)
            self.last20stats.setHorizontalHeaderLabels(['AB', 'H', 'BB', 'K', 'R', 'RBI', 'HR', 'SB', 'CS', 'BAA'])
            self.last20stats.verticalHeader().setVisible(False)

            
            for col, width in enumerate(column_widths2):
                self.last20stats.setColumnWidth(col, width)

            row20 = [
                last20['AB'], last20['H'], last20['BB'], last20['K'],
                last20['R'], last20['RBI'], last20['HR'], last20['SB'],
                last20['CS'], last20['BAA']
            ]
            for j, item in enumerate(row20):
                tableEntry = QTableWidgetItem(str(item))
                tableEntry.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
                self.last20stats.setItem(0, j, tableEntry)
                

            

            ##########  Get last 30 game totals
            last30 = playerStats['last_30_stats']

            self.last30stats = QTableWidget(1, 10)
            self.last30stats.setHorizontalHeaderLabels(['AB', 'H', 'BB', 'K', 'R', 'RBI', 'HR', 'SB', 'CS', 'BAA'])
            self.last30stats.verticalHeader().setVisible(False)

            
            for col, width in enumerate(column_widths2):
                self.last30stats.setColumnWidth(col, width)

            row30 = [
                last30['AB'], last30['H'], last30['BB'], last30['K'],
                last30['R'], last30['RBI'], last30['HR'], last30['SB'],
                last30['CS'], last30['BAA']
            ]
            for j, item in enumerate(row30):
                tableEntry = QTableWidgetItem(str(item))
                tableEntry.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
                self.last30stats.setItem(0, j, tableEntry)

            ############# Get season totals
            season = playerStats['season_stats']
    
            self.seasonS = QTableWidget(1, 10)
            self.seasonS.setHorizontalHeaderLabels(['AB','H','BB','K','R','RBI','HR','SB','CS','BAA','OBP','SLG','OPS'])
            self.seasonS.verticalHeader().setVisible(False)

            
            # Set column widths using a loop
            column_widths3 = [70, 70, 69, 69, 69, 69, 70, 70, 70, 70]  # Adjust these values as needed

            for col, width in enumerate(column_widths3):
                self.seasonS.setColumnWidth(col, width)

            rowS = [
                season['AB'], season['H'], season['BB'], season['K'],
                season['R'], season['RBI'], season['HR'], season['SB'],
                season['CS'], season['BAA'], season['OBP'], season['SLG'], season['OPS']
            ]
            for j, item in enumerate(rowS):
                tableEntry = QTableWidgetItem(item)
                tableEntry.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
                self.seasonS.setItem(0, j, tableEntry)

            

            ################ Display everything in GUI 

            # Add title to distinguish hitting statistics
            self.hitter_title = QLabel("Hitting Statistics")
            self.hitter_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.hitter_title.setFont(QFont('Arial', 16))
            self.statistics_layout.addWidget(self.hitter_title, 1, 0)

            # Add title label for recent games
            recent_title = QLabel("Recent Games")
            self.statistics_layout.addWidget(recent_title, 2, 0)

            self.statistics_layout.addWidget(self.recents, 3, 0)
            self.statistics_layout.setRowMinimumHeight(3, 200)

            # Add title label for last 10 games
            last10_title = QLabel("Last 10 Games Totals")
            self.statistics_layout.addWidget(last10_title, 4, 0,)

            self.statistics_layout.addWidget(self.last10stats, 5, 0)

            # Add title label for last 20 games
            last20_title = QLabel("Last 20 Games Totals")
            self.statistics_layout.addWidget(last20_title, 6, 0)

            self.statistics_layout.addWidget(self.last20stats, 7, 0)

            # Add title label for last 30 games
            last30_title = QLabel("Last 30 Games Totals")
            self.statistics_layout.addWidget(last30_title, 8, 0)

            self.statistics_layout.addWidget(self.last30stats, 9, 0)

            
            # Add title label season
            season_title = QLabel("Season Totals")
            self.statistics_layout.addWidget(season_title, 10, 0)

            self.statistics_layout.addWidget(self.seasonS, 11, 0,)
                

        if 'pitcher' in indicators: 

            playerStatsP = scrape_pitcher_stats(playerID)    # [{Game Stats} , {Last 10} , {Last 20} , {Last 30} , {Season}]
            
            ############  Get 5 most recent games
            gameStatsP = playerStatsP['game_stats']
        
            self.recentsP = QTableWidget(10, 15)
            self.recentsP.setHorizontalHeaderLabels(['Date', 'Opp', 'Results', 'Dec', 'IP', 'H', 'R', 'ER', 'BB', 'SO', 'HR', 'HBP', 'ERA', 'Pitches', 'Strikes'])
            self.recentsP.verticalHeader().setVisible(False)

             # Set column widths using a loop
            column_widthsP = [60, 45, 65, 65, 30, 25, 25, 25, 25, 25, 30, 35, 35, 47, 47]  # Adjust these values as needed
            
            for col, width in enumerate(column_widthsP):
                self.recentsP.setColumnWidth(col, width)


            for i, game_stat in enumerate(gameStatsP):
                row = [
                    game_stat['Date'], game_stat['Opponent'], game_stat['Result'],
                    game_stat['Decision'], game_stat['IP'], game_stat['H'], game_stat['R'],
                    game_stat['ER'], game_stat['BB'], game_stat['SO'], game_stat['HR'],
                    game_stat['HBP'], game_stat['ERA'], game_stat['Pitches'],
                    game_stat['Strikes']
                ]
                for j, item in enumerate(row):
                    tableEntry = QTableWidgetItem(item)
                    tableEntry.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
                    self.recentsP.setItem(i, j, tableEntry)
                    
        
            
            ######### Get last 5 games totals

            last5 = playerStatsP['last_5_stats']

            self.last5stats = QTableWidget(1, 12)
            self.last5stats.setHorizontalHeaderLabels(['IP', 'R', 'ER', 'BB', 'SO', 'H', 'HR', 'HBP', 'ERA', 'WHIP', 'Pitches', 'Strikes'])
            self.last5stats.verticalHeader().setVisible(False)

            # Set column widths using a loop
            column_widthsP2 = [58]*len(last5)  # Adjust these values as needed

            for col, width in enumerate(column_widthsP2):
                self.last5stats.setColumnWidth(col, width)

            row5 = [
                last5['IP'], last5['R'], last5['ER'], last5['BB'],
                last5['SO'], last5['H'], last5['HR'], last5['HBP'],
                last5['ERA'], last5['WHIP'], last5['Pitches'], last5['Strikes']
            ]
            for j, item in enumerate(row5):
                tableEntry = QTableWidgetItem(str(item))
                tableEntry.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
                self.last5stats.setItem(0, j, tableEntry)


            #########  Get last 10 games
            last10P = playerStatsP['last_10_stats']

            self.last10statsP = QTableWidget(1, 12)
            self.last10statsP.setHorizontalHeaderLabels(['IP', 'R', 'ER', 'BB', 'SO', 'H', 'HR', 'HBP', 'ERA', 'WHIP', 'Pitches', 'Strikes'])
            self.last10statsP.verticalHeader().setVisible(False)

            
            for col, width in enumerate(column_widthsP2):
                self.last10statsP.setColumnWidth(col, width)


            row10P = [
                last10P['IP'], last10P['R'], last10P['ER'], last10P['BB'],
                last10P['SO'], last10P['H'], last10P['HR'], last10P['HBP'],
                last10P['ERA'], last10P['WHIP'], last10P['Pitches'], last10P['Strikes']
            ]
            for j, item in enumerate(row10P):
                tableEntry = QTableWidgetItem(str(item))
                tableEntry.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
                self.last10statsP.setItem(0, j, tableEntry)

            
            ######### Get last 15 games totals

            last15 = playerStatsP['last_15_stats']

            self.last15stats = QTableWidget(1, 12)
            self.last15stats.setHorizontalHeaderLabels(['IP', 'R', 'ER', 'BB', 'SO', 'H', 'HR', 'HBP', 'ERA', 'WHIP', 'Pitches', 'Strikes'])
            self.last15stats.verticalHeader().setVisible(False)

            
            for col, width in enumerate(column_widthsP2):
                self.last15stats.setColumnWidth(col, width)

            row15 = [
                last15['IP'], last15['R'], last15['ER'], last15['BB'],
                last15['SO'], last15['H'], last15['HR'], last15['HBP'],
                last15['ERA'], last15['WHIP'], last15['Pitches'], last15['Strikes']
            ]
            for j, item in enumerate(row15):
                tableEntry = QTableWidgetItem(str(item))
                tableEntry.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
                self.last15stats.setItem(0, j, tableEntry)
           
            

            ############# Get season totals
            seasonP = playerStatsP['season_stats']
    
            self.seasonSP = QTableWidget(1, 13)
            self.seasonSP.setHorizontalHeaderLabels(['W/L','IP','R','ER','BB','SO','H','HR','HBP','ERA','WHIP','Strike %','Opp BAA'])
            self.seasonSP.verticalHeader().setVisible(False)

            
            # Set column widths using a loop
            column_widths3 = [65, 50, 50, 50, 50, 50, 50, 50, 50, 51, 51, 65, 65]  # Adjust these values as needed

            for col, width in enumerate(column_widths3):
                self.seasonSP.setColumnWidth(col, width)

            rowSP = [
                seasonP['W/L'], seasonP['IP'], seasonP['R'], seasonP['ER'],
                seasonP['BB'], seasonP['SO'], seasonP['H'], seasonP['HR'],
                seasonP['HBP'], seasonP['ERA'], seasonP['WHIP'], seasonP['Strike %'], seasonP['Opp BAA']
            ]
            for j, item in enumerate(rowSP):
                tableEntry = QTableWidgetItem(str(item))
                tableEntry.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
                self.seasonSP.setItem(0, j, tableEntry)

            

            ################ Display everything in GUI 

            # Add title to distinguish pitching statistics
            self.pitcher_title = QLabel("Pitching Statistics")
            self.pitcher_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.pitcher_title.setFont(QFont('Arial', 16))
            self.statistics_layout.addWidget(self.pitcher_title, 12, 0)

            # Add title label for recent games
            recent_titleP = QLabel("Recent Games")
            self.statistics_layout.addWidget(recent_titleP, 13, 0)

            self.statistics_layout.addWidget(self.recentsP, 14, 0)
            self.statistics_layout.setRowMinimumHeight(14, 200)

            
            # Add title label for last 5 games
            last5_titleP = QLabel("Last 5 Games Totals")
            self.statistics_layout.addWidget(last5_titleP, 15, 0)

            self.statistics_layout.addWidget(self.last5stats, 16, 0)
            
            
            # Add title label for last 10 games
            last10_titleP = QLabel("Last 10 Games Totals")
            self.statistics_layout.addWidget(last10_titleP, 17, 0,)

            self.statistics_layout.addWidget(self.last10statsP, 18, 0)

            

            # Add title label for last 30 games
            last15_title = QLabel("Last 15 Games Totals")
            self.statistics_layout.addWidget(last15_title, 20, 0)

            self.statistics_layout.addWidget(self.last15stats, 21, 0)

            
            # Add title label season
            season_titleP = QLabel("Season Totals")
            self.statistics_layout.addWidget(season_titleP, 23, 0)

            self.statistics_layout.addWidget(self.seasonSP, 24, 0,)



class AnalysisWindow(QWidget):         # Overall Analysis of baseball
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)



app = QApplication(sys.argv)
window = MainWindow()


app.setStyleSheet(""" 
    QWidget {
                  background-color: 
    }              
    
    QPushButton {
                  font-size: 12px;
                  background-color: "lightblue";
    }
    
    QPushButton:hover {
                  background: #0b7dda
    }
                  
    QLineEdit {
                  background-color: 
    }
                  
""")

window.show()
sys.exit(app.exec())