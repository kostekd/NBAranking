from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

#DEBUG
import time

#CURRENT STATES
CURRENT_SEASON = 2020
#maximum number of bits that can be read by function
MAX_BITS_PER_GAME = 160000
WEB_URL = "https://www.basketball-reference.com"
SEARCH_URL = "https://www.basketball-reference.com/search/search.fcgi?hint=&search={}&pid=&idx="
PLAYER_URL = "https://www.basketball-reference.com/players/{}/{}01.html"

class Player:
    def __init__(self,first_name, last_name, games, games_started, min_per_game, FGm, FGa, pt3m, pt3a, pt2m, pt2a, eFG_per, ft_per_g, fta_per_g, off_reb, def_reb, ast, stl, blk, tov, pf, pts):
        self.first_name = first_name
        self.last_name = last_name
        self.games = games
        self.games_started = games_started
        self.min_per_game = min_per_game
        self.FGm = FGm
        self.FGa = FGa
        self.pt3m = pt3m
        self.pt3a = pt3a
        self.pt2m = pt2m
        self.pt2a = pt2a
        self.eFG_per = eFG_per
        self.ft_per_g = ft_per_g
        self.fta_per_g = fta_per_g
        self.off_reb = off_reb
        self.def_reb = def_reb
        self.ast = ast
        self.stl = stl
        self.blk = blk
        self.tov = tov
        self.pf = pf
        self.pts = pts

    def printStats(self):
        print(self.first_name + " " + self.last_name + " " + str(self.games) + " " + str(self.games_started) + " " + str(self.min_per_game) + " "
             + str(self.FGm) + " " + str(self.FGa) + " " + str(self.pt3m) + " " + str(self.pt3a) + " " +  str(self.pt2m) + " " + str(self.pt2a) + " " + str(self.eFG_per) +
              " " + str(self.ft_per_g) + " " + str(self.fta_per_g) + " " + str(self.off_reb) + " " + str(self.def_reb) +  " " + str(self.ast) + " " + str(self.stl) + " " + str(self.blk) +
              " " + str(self.tov) + " " + str(self.pf) + " " + str(self.pts))

    def freeThrowPer(self):
        self.ft_percentage = self.ft_per_g / self.fta_per_g

    def trueShootingPer(self):
        self.true_per = round((self.pts) / (2*((self.pt3a + self.pt2a) + (0.44 * self.fta_per_g))), 4)

class URLControl():
    def __init__(self,first_name, last_name ,season, url, container = "tr", clss = "class", id = "full_table", page = "", html_name = ""):
        self.first_name = first_name.lower()
        self.last_name = last_name.lower()
        self.season = season
        self.page = page
        self.container = container
        self.clss = clss
        self.id = id
        self.url = url
        #we use it to make sure the player we want is the same player on the html page
        self.html_name = html_name

    #Controls whether we are on the right web or not
    def controlFunction(self):
        self.getNameHTML()
        if self.html_name.find(self.first_name) != -1:
            return True
        else:
            return False

    def getNameHTML(self):
        self.html_name = str(self.page.find('h1', {'itemprop':'name'}).get_text()).lower()

    def returnPage(self, url, max_bits = None):
        uClient = uReq(url)
        html_page = uClient.read(max_bits)
        uClient.close()
        #adjusting html_page to html standards
        soup_page = soup(html_page, 'html.parser')
        return soup_page

    #function only used when we do not get to the correct player in the first try which means that the name of the player we
    #found has really similar or identical name to our player
    def findAllPlayers(self):
        url_adress = SEARCH_URL.format(self.last_name)
        my_page = self.returnPage(url_adress)
        array = my_page.find('div', {'id': 'players'})
        players_container = array.findAll('div', {'class':'search-item'})

        for x in players_container:

            if str(x).lower().find(self.first_name + " " + self.last_name) != -1:
                self.url = WEB_URL + x.find('a').get('href')
                break

        return self.getData()


    def getData(self):
        self.page = self.returnPage(self.url, MAX_BITS_PER_GAME)
        if self.controlFunction() == True:
            #extracting the numbers from soup page
            con = self.page.findAll(self.container, {self.clss : self.id})
            for x in range(0, len(con)):
                if str(con[x]).find('per_game.' + str(self.season)) != -1:
                    return con[x]
        else:
            #return cause we want to end up in assingBasicData function
            return self.findAllPlayers()


    #assing the per game data
    def assingBasicData(self):
        statistics = self.getData()
        g = int(statistics.find('td', {'data-stat':'g'}).get_text())
        gs = int(statistics.find('td', {'data-stat':'gs'}).get_text())
        mp_per_g = float(statistics.find('td', {'data-stat':'mp_per_g'}).get_text())
        fg_per_g = float(statistics.find('td', {'data-stat': 'fg_per_g'}).get_text())
        fga_per_g = float(statistics.find('td', {'data-stat': 'fga_per_g'}).get_text())
        fg3_per_g = float(statistics.find('td', {'data-stat': 'fg3_per_g'}).get_text())
        fg3a_per_g = float(statistics.find('td', {'data-stat': 'fg3a_per_g'}).get_text())
        fg2_per_g = float(statistics.find('td', {'data-stat': 'fg2_per_g'}).get_text())
        fg2a_per_g = float(statistics.find('td', {'data-stat': 'fg2a_per_g'}).get_text())
        efg_pct = float(statistics.find('td', {'data-stat': 'efg_pct'}).get_text())
        ft_per_g = float(statistics.find('td', {'data-stat': 'ft_per_g'}).get_text())
        fta_per_g = float(statistics.find('td', {'data-stat': 'fta_per_g'}).get_text())
        orb_per_g = float(statistics.find('td', {'data-stat': 'orb_per_g'}).get_text())
        drb_per_g = float(statistics.find('td', {'data-stat': 'drb_per_g'}).get_text())
        ast_per_g = float(statistics.find('td', {'data-stat': 'ast_per_g'}).get_text())
        stl_per_g = float(statistics.find('td', {'data-stat': 'stl_per_g'}).get_text())
        blk_per_g = float(statistics.find('td', {'data-stat': 'blk_per_g'}).get_text())
        tov_per_g = float(statistics.find('td', {'data-stat': 'tov_per_g'}).get_text())
        pf_per_g = float(statistics.find('td', {'data-stat': 'pf_per_g'}).get_text())
        pts_per_g = float(statistics.find('td', {'data-stat': 'pts_per_g'}).get_text())
        #creating a player and pushing him into the list of players
        p = Player(self.first_name, self.last_name, g, gs, mp_per_g, fg_per_g, fga_per_g, fg3_per_g, fg3a_per_g, fg2_per_g, fg2a_per_g, efg_pct,
                   ft_per_g, fta_per_g, orb_per_g, drb_per_g, ast_per_g, stl_per_g, blk_per_g, tov_per_g, pf_per_g, pts_per_g)
        return p


class Chart:
    def __init__(self, name, xdata = list(), ydata = list(), plotname = list(), xlabel = 'x', ylabel = 'y', plot = None):
        self.name = name
        self.xdata = xdata
        self.ydata = ydata
        self.plotname = plotname
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.plot = plot

        #functions during inicialization
        self.createDataFrame()
        self.createPlot()
        self.labelChart(self.xlabel, self.ylabel)
        self.namePlots()


    def createDataFrame(self):
        #create a data structure using panda
        self.dataframe = pd.DataFrame({
            'x' : self.xdata,
            'y' : self.ydata,
        })

    def createPlot(self):
        self.plot = sns.regplot(data=self.dataframe, x="x", y="y", fit_reg=True, marker="o", color="skyblue")

    def labelChart(self, x = 'x' , y = 'y'):
        #label the (x and y)-axis
        plt.title(self.name)
        plt.xlabel(str(x))
        plt.ylabel(str(y))

    def namePlots(self):
        for line in range(0, self.dataframe.shape[0]):
            self.plot.text(self.dataframe.x[line] + 0.2, self.dataframe.y[line], self.plotname[line], horizontalalignment='center', fontsize= 8,
                    color='black',
                    weight='bold')

    def showChart(self):
        plt.show()

#GLOBAL FUNCTIONS
def extractData(name):
    if name[0].isalpha():
        url_part = name[1][0:5].lower() + name[0][0:2].lower()
    else:
        tmp = ""
        for i in range(0,len(name[0])):
            if name[0][i].isalpha():
                tmp += name[0][i]
        url_part = name[1][0:5].lower() + tmp[0:2].lower()

    return(url_part)


if __name__ == "__main__":
    GLOBAL_PLAYERS = []
    xstat = []
    ystat = []
    plots = []
    '''
    name = input("What players stats do you want to see: ").lower().split()
    season  = int(input("What season: "))
    player_link = PLAYER_URL.format(name[1][0].lower(), extractData(name))
    print('Loading data for {} ...'.format(str(name[0] + ' ' + name[1])))
    player = URLControl(name[0], name[1], int(season), player_link).assingBasicData()
    player.printStats()
'''
    name = [['J.J.', 'Redick'], ['James','Harden'] ,['Duncan','Robinson'] ,['Lebron','James'] ,['Devin','Booker'],['Jamal', 'Murray'],
            ['Kawhi','Leonard'],['Buddy','Hield'], ['Jordan', 'Poole'], ['Bryn', 'Forbes'], ['Bradley', 'Beal'],
            ["Devonte'", "Graham"], ['Justin' ,'Holiday'], ['Kyle', 'Lowry'], ['Giannis', 'Antetokounmpo'],
            ['Zach', 'LaVine'], ['Danilo', 'Gallinari'],['Marcus','Morris'], ['Luka', 'Doncic'], ['Bogdan','Bogdanovic'],
            ['Taurean', 'Prince'], ['Jordan', 'Clarkson'], ['Luke', 'Kennard'], ['Karl', 'Towns'], ['Evan', 'Fournier'],
            ['Jae', 'Crowder'], ['Kemba', 'Walker'], ['Furkan', 'Korkmaz'], ['Trae', 'Young'], ['Damian', 'Lillard']]
    season = [2020, 2020, 2020, 2020, 2020,
              2020, 2020, 2020, 2020, 2020,
              2020, 2020, 2020, 2020, 2020,
              2020, 2020, 2020, 2020, 2020,
              2020, 2020, 2020, 2020, 2020,
              2020, 2020, 2020, 2020, 2020]

    for i in range(0, len(season)):
        player_link = PLAYER_URL.format(name[i][1][0].lower(), extractData(name[i]))
        print('Loading data for {} ...'.format(str(name[i][0] + ' ' + name[i][1])))
        player = URLControl(name[i][0], name[i][1], int(season[i]),player_link).assingBasicData()
        GLOBAL_PLAYERS.append(player)

    for i in range(0 ,len(season)):
        xstat.append(GLOBAL_PLAYERS[i].pt3a * GLOBAL_PLAYERS[i].games)
        ystat.append(GLOBAL_PLAYERS[i].pt3m * GLOBAL_PLAYERS[i].games)
        plots.append(GLOBAL_PLAYERS[i].last_name)


    print(sum(xstat) / sum(ystat))
    charcik = Chart('Leading volume 3-pt scorer of each team',xstat,ystat,plots,'3pta','3ptm')
    charcik.showChart()





