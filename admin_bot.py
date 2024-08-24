import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from main import get_wpm_accuracy,get_user_info,get_users_wpm_accuracy
from prettytable import PrettyTable

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send a message to the group
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text="Hello, everyone!")

async def send_results(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    users = get_user_info('monkeytype.csv')



    users_wpm_accuracy = get_users_wpm_accuracy(users,15)
    results=''
    for idx,user in enumerate(users_wpm_accuracy):
        if idx==0:
            results+=f'🥇 {user["full_name"]}\t WPM: {user["wpm"]} Accuracy: {user["accuracy"]}\n'
        elif idx==1:
            results+=f'🥈 {user["full_name"]}\t WPM: {user["wpm"]} Accuracy: {user["accuracy"]}\n'
        elif idx==2:
            results+=f'🥉 {user["full_name"]}\t WPM: {user["wpm"]} Accuracy: {user["accuracy"]}\n'
        else:
            results+=f'{idx+1}. {user["full_name"]}\t WPM: {user["wpm"]} Accuracy: {user["accuracy"]}\n'
        
    # Send a message to the group
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=results)
# GROUP chat ID
GROUP_CHAT_ID =-4503928327
TOKEN = os.environ['TOKEN']
#pretty table for displaying results
table = PrettyTable()
table.field_names = ['full_name', 'wpm', 'accuracy']
table.add_rows=[]
for i in get_users_wpm_accuracy(get_user_info('monkeytype.csv'),15):
    table.add_row([i['full_name'], i['wpm'], i['accuracy']])
#send table to group
async def send_table(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     # Send a message to the group
    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=table)
print(table)
#html image to python code

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("sendResults", send_results))
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hello", hello))

app.run_polling()