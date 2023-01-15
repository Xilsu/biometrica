from ftplib import FTP

import os

class FTPServer():
    def __init__(self, host, user, password):
        self.ftp = FTP(host)
        self.ftp.login(user, password)
        
        print('FTP Connected.')
    
    def list_recent_videos(self):
        files = self.ftp.nlst()
        
        return files
    
    def get_videos(self):
        print('Listing files.')
        
        files = self.list_recent_videos()
        
        for file in files:
            if '.avi' in file:
                handle = open(os.path.join('videos', file.split('/')[-1]), 'wb')
                
                print('Getting file: ' + file)
                
                if self.ftp.size(file) != 0:
                    self.ftp.retrbinary('RETR %s' % file, handle.write)
                    
                    print('Deleting file: ' + file)
                else:
                    print('File {} has 0 bytes.'.format(file))
                    
                self.ftp.delete(file)

if __name__ == '__main__':
    ftp_service = FTPServer('192.168.0.217', 'esp', 'esp')
    ftp_service.get_videos()