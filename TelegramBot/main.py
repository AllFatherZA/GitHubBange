import os
import time
import telebot
import yfinance as yf
import MetaTrader5 as mt5



API_KEY='5912955028:AAHNcRvY6mHuHvRW1S6sSAyZ6YEYWF_VXsQ'
if not mt5.initialize():
     print("initialize() failed, error code =",mt5.last_error())
     quit()
print("Hit")
bot=telebot.TeleBot(API_KEY)
print("Hit")

#event handler for funtion
@bot.message_handler(commands=['Greet'])
#function method


def BuyRequest(message):
     request=message=message.text.split()
     print(str(request))
     if request[1]!='Buy' or request[1]!='Sell' :
         print("Hit Request failed")
         return False
         
     else:
         print("Hit Request Succeed")
         return True
         
@bot.message_handler(func=BuyRequest)
def ExecuteBuy(message):
     symbol=message.text.split()[0]
     ordertype=message.text.split()[1]
     lots=message.text.split()[2]
     print(str(ordertype))
     print("Hit Order processing")
     symbol_info = mt5.symbol_info(symbol)
     time.sleep(10)
     print(symbol_info)
     if mt5.symbol_select(symbol):
         if ordertype=='Buy':
             if(BuyOrder(symbol,lots)):
                 print("Hit Buy succeed")
                 bot.send_message(message.chat.id,"Order executed")
         elif ordertype=='Sell':
             if(SellOrder(symbol,lots)):
                 print("Hit Sell succeed")
                 bot.send_message(message.chat.id,"Order executed")
                   
         else:
             bot.send_message(message.chat.id,"Symbol not found")
     else:
         bot.send_message(message.chat.id,"Symbol not found")
         print("Hit Buy failed")
   
def BuyOrder(symbol,lots):
     print("Buy Order Hit")
     lot = float(lots)
     point = mt5.symbol_info(symbol).point
     price = mt5.symbol_info_tick(symbol).ask
     print(price)
     deviation = 20
     request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "tp":price+27.24,
        "sl":price-27.24,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,}
        
     result=mt5.order_send(request) 
     print(result)
     return True
     
     
def SellOrder(symbol,lots):
     print("Sell Order Hit")
     lot = float(lots)
     point = mt5.symbol_info(symbol).point
     price = mt5.symbol_info_tick(symbol).bid
     print(price)
     deviation = 20
     request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "tp":price-27.24,
        "sl":price+27.24,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,}
        
     result=mt5.order_send(request) 
     print(result)
     return True
def stock_request(message):
     request=message.text.split()
     if request[0].lower() not in "price" or len(request)<2:
         return False
     else:
         return True
def greet(message):
     bot.reply_to(message,"Hey! Hows it going?")

@bot.message_handler(commands=['Hello'])
def Stock(message):
     bot.send_message(message.chat.id,"Hello")
        
@bot.message_handler(func=stock_request)
def send_price(message):
     request=message.text.split()[1]
     data=yf.download(tickers=request,period="5m",interval='1m')
     if data.size>0:
         data=data.reset_index()
         data["format_date"]=data['Datetime'].dt.strftime('%m/%d %I:%M %p')
         data.set_index('format_date',inplace=True)
         print(data.to_string())
         bot.send_message(message.chat.id,data['Close'].to_string(header=False))
         
     else:
         bot.send_message(message.chat.id,"No data")

bot.polling()


'''
@bot.message_handler(commands=['wsb'])
def get_stocks(message):
     response=""
     stocks=['gme','amc','nok']
     stock_data=[]
     for stock in stocks:
         data=yf.download(tickers=stock,period="2d",interval="1d")
         data=data.reset_index()
         response+=f"----{stock}----\n"
         stock_data.append([stock])
         columns=['stock']
         for index,row in data.iterrows():
             stock_position=len(stock_data)-1
             price=round(row['Close'],2)
             format_date=row['Date'].strftime('%m/%d')
             response+=f"{format_date}:{price}\n"
             stock_data[stock_position].append(price)
             columns.append(format_date)
             
         print(stock)

         for row in stock_data:
             response+=f"{row[0]:<10}{row[1]:^10}{row[2]:>10}\n"

         print(response)
         
     bot.send_message(message.chat.id,response)
     



def get_stocks(message):
     interger=1
     response=""
     stocks=['gme','amc','nok']
     stock_data=[]
     for stock in stocks:
         #downloading price
         data=yf.download(tickers=stock,period="2d",interval="1d")
         #reset index
         data=data.reset_index()
         #build response string
         response+=f"----{stock}----\n"
         #create stock key for dictionary
         stock_data.append([stock])
         #print dicttionary content
         print(stock_data)
         #create new stock coloumn
         columns=['stock']
         for index,row in data.iterrows():
             #print(row,"====================",str(interger))
             interger=interger+1
             #get last position in the dictionary
             stock_position=len(stock_data)-1
             #get stock coloumn data 
             price=round(row['Close'],2)
             #get date data
             format_date=row['Date'].strftime('%m/%d')
             response+=f"{format_date}:{price}\n"
             stock_data[stock_position].append(price)
             columns.append(format_date)
             
         print(stock)

         for row in stock_data:
             response+=f"{row[0]:<10}{row[1]:^10}{row[2]:>10}\n"
         response+="\nStock Data"
         print(response)
         
         
get_stocks("Stock")
'''