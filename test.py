from PyMailCloud import PyMailCloud
from PyMailCloud import PyMailCloudError
import urllib3, os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

mail_cloud = PyMailCloud("ejudgetest@mail.ru", "00ejudge00")
#print(mail_cloud.get_folder_contents('/'))
#mail_cloud.delete_files([{'filename' : "1.py"}])
#mail_cloud.upload_files([{'filename' : '1.py', 'path' : '/'}])
os.remove("1.py")
#mail_cloud.download_files(["/1.py"])