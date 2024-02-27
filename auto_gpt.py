
from time import sleep # Inbuilt
from selenium import webdriver # pip install selenium
from selenium.webdriver.chrome.options import Options # pip install selenium
from selenium.webdriver.common.by import By # pip install selenium
import warnings # Inbuilt
from selenium.webdriver.chrome.service import Service

warnings.simplefilter("ignore")

Link = "https://gpt4login.com/use-chatgpt-online-free/"
# chrome_driver_path = 'chromedriver.exe'
chrome_options = Options()
chrome_options.headless = True
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('--log-level=3')
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get(Link)



def FileReader():
    File = open("Chatnumber.txt","r")
    Data = File.read()
    File.close()
    return Data

def FileWriter(Data):
    File = open("Chatnumber.txt","w")
    File.write(Data)
    File.close()

# Sending The Query To The Website :-
def ChatGPTBrain(Query):
    Query = str(Query)
    driver.find_element(by=By.XPATH,value="/html/body/div[1]/div/div/main/article/div/div/div/div/div/div/div[2]/textarea").send_keys(Query)
    sleep(1)
    driver.find_element(by=By.XPATH,value="/html/body/div[1]/div/div/main/article/div/div/div/div/div/div/div[2]/button").click()
    Data = str(FileReader())
# # Getting Replies :- 
# /html[1]/body[1]/div[1]/div[1]/div[1]/main[1]/article[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]

    while True:

        sleep(0.5)
        
        try:
            AnswerXpath = f"/html/body/div[1]/div/div/main/article/div/div/div/div/div/div/div[2]/div[2]/span[2]"
            Answer = driver.find_element(by=By.XPATH,value=AnswerXpath).is_displayed()
            if str(Answer)=="True":
                break

        except:
            pass


    AnswerXpath = f"/html/body/div[1]/div/div/main/article/div/div/div/div/div/div/div[2]/div[2]/span[2]"
    # /html[1]/body[1]/div[1]/div[1]/div[1]/main[1]/article[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/span[1]
    Answer = driver.find_element(by=By.XPATH,value=AnswerXpath).text
    NewData = int(Data) + 4
    FileWriter(Data=str(NewData))
    return Answer

# # Rest Of The Code 
print("Starting The GPT4-Model.")
FileWriter(Data='3')

while True:
        
    try:
        Query = input("Enter Your Query : ")
        print("ans is here :")
        element = driver.find_element(By.XPATH, "//button[@id='submit-button']")
        print(ChatGPTBrain(Query=Query))
    
    except:
        pass

