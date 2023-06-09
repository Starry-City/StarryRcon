import os

class McLog:
    def __init__(self, path):
        self.path = path
        self.server_status = True
        self.server_on_line = -1
        self.server_off_line = -1
        
        self.last_line = ''
        self.new_line = False
        
        self.log = []
    
    def read(self):
        log = []
        if not os.path.exists(self.path + 'latest.log'):
            print('latest.log not found')
        else:
            with open(self.path + 'latest.log', "r", encoding="ansi") as f:
                for line in f.readlines():
                    log.append(line)

            if log[-1] == self.last_line:
                self.new_line = False
            elif log[-1] != self.last_line:
                self.last_line = log[-1]
                self.new_line = True
            # print(self.last_line)
        
        self.log = log
    
    def getPlayerMessage(self):
        '''[03:55:48 INFO]: <grapefruit_9239> test'''
        if self.new_line == False:
            return None
        last_line = self.log[-1]
        if last_line.find('[Server thread/INFO]: <') != -1:
            message = last_line.split(']: ')[1]
            return message
        else:
            return None
    
    # def getServerStatus(self):
    #     '''[Server thread/INFO]: Done'''
    #     '''[Server thread/INFO]: Stopping the server'''
    #     for line in self.log:
    #         # 伺服器開啟
    #         if line.find('[Server thread/INFO]: Done') != self.server_on_line and self.server_status != False:
    #             self.server_on_line = line.find('[Server thread/INFO]: Done')
    #             self.server_status = False
    #             return True
    #         # 伺服器關閉
    #         elif line.find('[Server thread/INFO]: Stopping the server') != self.server_off_line and self.server_status != True:
    #             self.server_off_line = line.find('[Server thread/INFO]: Stopping the server')
    #             self.server_status = False
    #             return False
    #         else:
    #             return 'idle'
    
    def getPlayerJoin(self):
        if self.new_line == False:
            return None
        if self.log[-1].find('[Server thread/INFO]: ') != -1 and self.log[-1].find('joined the game') != -1:
            return self.log[-1].split(']: ')[1].split(' joined the game')[0]
        else:
            return None
    
    def getPlayerLeft(self):
        if self.new_line == False:
            return None
        if self.log[-1].find('[Server thread/INFO]: ') != -1 and self.log[-1].find('left the game') != -1:
            return self.log[-1].split(']: ')[1].split(' left the game')[0]
        else:
            return None
    
    def getConnectStatus(self):
        if self.new_line == False:
            return None
        if self.log[-1].find('Thread') != -1 and self.log[-1].find('RCON Client') != -1 and self.log[-1].find('started') != -1:
            return True
        elif self.log[-1].find('Thread') != -1 and self.log[-1].find('RCON Client') != -1 and self.log[-1].find('disconnected') != -1:
            return False