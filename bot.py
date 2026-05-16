import telebot
from telebot import types
import dotenv
import os
import telebot.formatting

import time 
import concurrent.futures
import datetime
from prodiaapi import gen,checkjobstatus


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from gen import Key
import requests

import re
cred = credentials.Certificate("desidiffusionbot-firebase-adminsdk-j84hf-a4c27fab37.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://desidiffusionbot-default-rtdb.asia-southeast1.firebasedatabase.app/'})


ref = db.reference("/")
ref.get()
uref = ref.child('users')




def checkerthread(idofjob):
    with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(checkjobstatus, idofjob)
            return_value = future.result()
            return return_value[1]
        
        
def keymaker(hrstoadd):
    key_ref = ref.child('codes')
    # hrstoadd=(input("Enter hours to add:"))
    p=Key()
    print(p)
    p=str(p)
    p=p.split(':')[0]
    new_key = str(p)
    new_value = hrstoadd

    key_ref.update({new_key: new_value})
    return str(p)


def keychecker(keytocheck=str):
    #keytocheck=(input("Enter Your Key :"))  
    p=Key(key=keytocheck)
    
    key_ref = ref.child('codes')
    #m=p.verify(keytocheck)
    if 'Valid' in str(p):
        p=str(p)
        p=p.split(':')[0]
        hr=key_ref.child(p).get()
        
        # print("HRSTOADD:\n"+str(hr))
        # print('Found it!')
        try:
            hr=int(hr)
        except TypeError:
            return False
        return int(hr) 
    else:
        return False

dotenv.load_dotenv()
tk=str(os.getenv('tk'))
apiofgp=str(os.getenv('apiofgp'))
bot = telebot.TeleBot(tk)


def clear_chat(chat_id):
    # Get the list of messages in the chat
    messages = bot.get_history(chat_id)
    
    # Iterate over the list of messages and delete each one
    for message in messages:
        bot.delete_message(chat_id, message.message_id)


def log(error):
    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    with open("Logs.txt", "a") as f:
        f.write(f"==========================\n{dt_string}\n{error}\n==========================\n\n")


user_data = {}


models_list = [
    "absolutereality_V16.safetensors [37db0fc3]",
    "absolutereality_v181.safetensors [3d9d4d2b]",
    "analog-diffusion-1.0.ckpt [9ca13f02]",
    "anythingv3_0-pruned.ckpt [2700c435]",
    "anything-v4.5-pruned.ckpt [65745d25]",
    "anythingV5_PrtRE.safetensors [893e49b9]",
    "AOM3A3_orangemixs.safetensors [9600da17]",
    "childrensStories_v13D.safetensors [9dfaabcb]",
    "childrensStories_v1SemiReal.safetensors [a1c56dbb]",
    "childrensStories_v1ToonAnime.safetensors [2ec7b88b]",
    "cyberrealistic_v33.safetensors [82b0d085]",
    "deliberate_v2.safetensors [10ec4b29]",
    "dreamlike-anime-1.0.safetensors [4520e090]",
    "dreamlike-diffusion-1.0.safetensors [5c9fd6e0]",
    "dreamlike-photoreal-2.0.safetensors [fdcf65e7]",
    "dreamshaper_6BakedVae.safetensors [114c8abb]",
    "dreamshaper_7.safetensors [5cf5ae06]",
    "dreamshaper_8.safetensors [9d40847d]",
    "edgeOfRealism_eorV20.safetensors [3ed5de15]",
    "EimisAnimeDiffusion_V1.ckpt [4f828a15]",
    "elldreths-vivid-mix.safetensors [342d9d26]",
    "epicrealism_naturalSinRC1VAE.safetensors [90a4c676]",
    "ICantBelieveItsNotPhotography_seco.safetensors [4e7a3dfd]",
    "juggernaut_aftermath.safetensors [5e20c455]",
    "lyriel_v16.safetensors [68fceea2]",
    "mechamix_v10.safetensors [ee685731]",
    "meinamix_meinaV9.safetensors [2ec66ab0]",
    "meinamix_meinaV11.safetensors [b56ce717]",
    "openjourney_V4.ckpt [ca2f377f]",
    "portraitplus_V1.0.safetensors [1400e684]",
    "Realistic_Vision_V1.4-pruned-fp16.safetensors [8d21810b]",
    "Realistic_Vision_V2.0.safetensors [79587710]",
    "Realistic_Vision_V4.0.safetensors [29a7afaa]",
    "Realistic_Vision_V5.0.safetensors [614d1063]",
    "redshift_diffusion-V10.safetensors [1400e684]",
    "revAnimated_v122.safetensors [3f4fefd9]",
    "rundiffusionFX25D_v10.safetensors [cd12b0ee]",
    "rundiffusionFX_v10.safetensors [cd4e694d]",
    "sdv1_4.ckpt [7460a6fa]",
    "v1-5-pruned-emaonly.safetensors [d7049739]",
    "shoninsBeautiful_v10.safetensors [25d8c546]",
    "theallys-mix-ii-churned.safetensors [5d9225a4]",
    "timeless-1.0.ckpt [7c4971d4]",
    "toonyou_beta6.safetensors [980f6b15]"
]


samplers_list = [
    "Euler",
    "Euler a",
    "LMS",
    "Heun",
    "DPM2",
    "DPM2 a",
    "DPM++ 25 a",
    "DPM++ 2M",
    "DPM++ SDE",
    "DPM fast",
    "DPM adaptive",
    "LMS Karras",
    "DPM2 Karras",
    "DPM2 a Karras",
    "DPM++ 2S a Karras",
    "DPM++ 2M Karras",
    "DPM++ SDE Karras",
    "DDIM",
    "PLMS",
    
]
def check_verification_time(chatid):
    start=time.time()
    hrs_left= uref.child(str(chatid)).child('verifiedforhrs').get()
    # print(hrs_left)
    last_verified_at =uref.child(str(chatid)).child('lastverifiedat').get()
    current_time = time.time() 
    # print(last_verified_at) 
    current_time = int(datetime.datetime.now().timestamp() * 1000)
    cooldown = int(12 * 60 * 60 * 1000)
    remain_time = cooldown - int(current_time - last_verified_at)
    print(f"hrs passed = {remain_time}")
    hrs_passed = (current_time - last_verified_at) / 3600  # Convert seconds to hours
    
    if remain_time <= 0:
        return True
    else:
        hours, remaining_ms = divmod(remain_time, 3600000)
        udpata = {"verifiedforhrs": int(remaining_ms)}
        uref.child(str(chatid)).update(udpata)
    end=time.time()
    print("veriftimeinsidefucn",end-start)    
    return remain_time  # Return remaining hours for verification

# def addveriftime(chatid,timetoadd):
#     hrs_left= uref.child(str(chatid)).child('verifiedforhrs').get()
#     try :
#         hrs_left=int(hrs_left)
#         timetoadd=int(timetoadd)
#     except TypeError:
#         return "timetoadd was none"
#     udpata={
#                 'verifiedforhrs': hrs_left+timetoadd
#             }
#     uref.child(str(chatid)).update(udpata)


def addveriftime(chatid, timetoadd):
    hrs_left = uref.child(str(chatid)).child("lastverifiedat").get()
    try:
        hrs_left = int(hrs_left)
        timetoadd_ms = int(timetoadd)
    except TypeError:
        return "timetoadd was none"
    
    udpata = {"lastverifiedat": int(datetime.datetime.now().timestamp() * 1000),"verifiedforhrs": timetoadd_ms}
    uref.child(str(chatid)).update(udpata)




def codedel(codetodel):
    key_to_delete = codetodel
    code_node_ref = ref.child("codes")

    # Use the delete method to delete the specific key within the "code" node
    code_node_ref.child(str(key_to_delete)).delete()

    # print(f'Key "{key_to_delete}" deleted successfully.')
    
    

@bot.message_handler(commands=['bsdkbot'])
def send_video(message):
    chat_id = message.chat.id
    video_path = 'gaali.mp4'  # Replace with the correct path if the file is not in the same directory
    bot.send_video(chat_id,"BAACAgEAAxkBAAIGSWUhpypayOKpBNgx7T2h1vlTZEI3AAK7AwACCVUQRe_MsZ2GuXswMAQ")
    # try:
    #     with open(video_path, 'rb') as video:
    #         bot.send_video(chat_id, video)
    # except Exception as e:
    #     print(e)
    #     bot.send_message(chat_id, "Failed to send the video. Please try again later.")


@bot.message_handler(['start'])
def start_command(message):
    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    user = message.from_user
    name = user.first_name
    userid=user.username
    text = message.text 
    code = text.split()[1] if len(text.split()) > 1 else None
    if code != None :
        hrs=keychecker(code)
        
        nuno=[None,False]
        if hrs in nuno:
            bot.reply_to(message,"This code has already been Redeemed")
            return
        codedel(code)
        hrs=int(hrs)
        mili = int(hrs * 60 * 60 * 1000)
        addveriftime(message.chat.id,mili)
        
        bot.reply_to(message,f'VERIFICATION TOKEN REFRESHED SUCCESFULLY\n ADDDED TIME = {hrs}')
        return 
        
        
       
    
    
    with open('userswhostartedbot.csv','rb') as rcsv:
        if bytes(message.chat.id) in rcsv.read():
            return bot.reply_to(message,f"🔥 <u><b>Hello</b></u> @{message.from_user.username} 🔥\n\n🔹 <b>Don't forget to join our channel for updates regarding this bot -&gt;</b> https://t.me/Desidiffusion\n\n⚡️<i>DESI DIFFUSION - BEST AI IMAGE GENERATOR IN THE MARKET</i> ⚡️\n\n🟡 <u><i><b>Click</b></i></u>  /diffuse <u><b><i>to start generating images \n\n</i></b></u>⚜️ <u><i>Click</i></u> /help  <u><i>to know more about how to use this bot</i></u> ⚜️" ,parse_mode="HTML")
        else:
            with open('userswhostartedbot.csv','a',errors="ignore") as us:
                # print(message.chat.id)
                # print(name)
                # print(userid)
                # print(dt_string)
                fullstr=(f"{(message.chat.id)},{(name)},{(userid)},{(dt_string)}\n")
                print(fullstr)
                us.write(fullstr)
        
    bot.reply_to(message,f"🔥 <u><b>Hello</b></u> @{message.from_user.username} 🔥\n\n🔹 <b>Don't forget to join our channel for updates regarding this bot -&gt;</b> https://t.me/Desidiffusion\n\n⚡️<i>DESI DIFFUSION - BEST AI IMAGE GENERATOR IN THE MARKET</i> ⚡️\n\n🟡 <u><i><b>Click</b></i></u>  /diffuse <u><b><i>to start generating images \n\n</i></b></u>⚜️ <u><i>Click</i></u> /help  <u><i>to know more about how to use this bot</i></u> ⚜️" ,parse_mode="HTML")



@bot.message_handler(['help'])
def start_command(message):
    bot.reply_to(message,"""/start - Starts the bot.
/help - shows this dialog.
/diffuse  -  Used to Generate an image.
/id - use this to get your id.
/premium - Get Information about premium subscription.
/howtousebot - Get detailed information about how to use this bot to create Images.""")

@bot.message_handler(['keygen'])
def keygen_command(message):
    with open('verifiedadmins.txt', 'r') as f:
            mkk=f.read()
    if str(message.chat.id) not in mkk:
        bot.reply_to(message,"you are not allowed to access this cmd ")
        return
    text=message.text
    hrs=text.split()[1] if len(text.split()) > 1 else None
    if hrs != None:
        hrs=int(hrs)
        mili = int(hrs * 60 * 60 * 1000)
        code=keymaker(mili)
        bot.send_message(message.chat.id,f"https://t.me/DesidiffusionBot?start={code}")
    else:
        bot.send_message(message.chat.id,"Send hrs to add /keygen hrstoadd")
        
    
@bot.message_handler(['id'])
def idlelo(message):
    bot.reply_to(message,text=str(message.chat.id))
    
# @bot.message_handler(['detailedhelp'])
# def idlelo(message):
#     bot.send_message(message.chat.id,"""**_1\._** **_Positive Prompt:_** *In this part, describe what you want in the Image you are going to generate\. You can separate different words by a comma\. To give high priority to a word, write it inside brackets \(word\)\. The more brackets, the higher the weight \(\(word\)\) or you can give the weights in decimals \(word:1\.2\), \(word:0\.9\), etc\. The Bot will accept a maximum of 1024 characters, so avoid very long prompts exceeding this limit to avoid errors\.*

# **_2\._** **_Steps:_** *This is the number of steps taken to create your Image\. The maximum you can give is 50, but we recommend keeping it in the range of 20\-35 for better and faster results\.*

# **_3\._** **_CFG:_** *This value varies from 1\-10 in the bot\. It signifies how much weight you want to give to the whole prompt\. If you give it a lower value, the Model will check parts of the prompts and fill the gaps\. A higher CFG gives more refined images\. We recommend a range of 7\-10\.*

# **_4\._** **_Models:_** *There is a list of Models\. Use whichever you want and experiment with them\. For realistic people, use Realistic Vision\. For other purposes, use Dreamshaper v8 or experiment with other models\.*

# **_5\._** **_Samplers:_** *We usually use DPM\+\+ 2M, 2S, SDE\. If you want more in\-depth knowledge about this, check this [post](https://www.reddit.com/r/StableDiffusion/comments/16wykzy/ever_wondered_what_those_cryptic_sampler_names/)\.*

# **_6\._** **_Aspect Ratio:_** *Choose one of the three types: square, landscape, or portrait\.*

# **_7\._** **_Negative Prompt:_** *Here, specify what you don't want to see in the Image\. If you're lazy, the default negative prompt will be used\. Alternatively, you can create your own\. The generated image varies depending on the Negative prompt too\.*

# **_8\._** **_ALL THE BEST LOOKING FORWARD TO WHAT YOU CREATE\!_**
# """,parse_mode="MarkdownV2",disable_web_page_preview=True)   
    

@bot.message_handler(['howtousebot'])
def idlelo(message):
    bot.send_message(message.chat.id,"""<b>1. Positive Prompt:</b> <i>In this part, describe what you want in the Image you are going to generate. You can separate different words by a comma. To give high priority to a word, write it inside brackets (word). The more brackets, the higher the weight ((word)) or you can give the weights in decimals (word:1.2), (word:0.9), etc. The Bot will accept a maximum of 1024 characters, so avoid very long prompts exceeding this limit to avoid errors.</i>

<b>2. Steps:</b> <i>This is the number of steps taken to create your Image. The maximum you can give is 50, but we recommend keeping it in the range of 20-35 for better and faster results.</i>

<b>3. CFG:</b> <i>This value varies from 1-10 in the bot. It signifies how much weight you want to give to the whole prompt. If you give it a lower value, the Model will check parts of the prompts and fill the gaps. A higher CFG gives more refined images. We recommend a range of 7-10.</i>

<b>4. Models:</b> <i>There is a list of Models. Use whichever you want and experiment with them. For realistic people, use Realistic Vision. For other purposes, use Dreamshaper v8 or experiment with other models.</i>

<b>5. Samplers:</b> <i>We usually use DPM++ 2M, 2S, SDE. If you want more in-depth knowledge about this, check this <a href='https://www.reddit.com/r/StableDiffusion/comments/16wykzy/ever_wondered_what_those_cryptic_sampler_names/'>post</a>.</i>

<b>6. Aspect Ratio:</b> <i>Choose one of the three types: square, landscape, or portrait.</i>

<b>7. Negative Prompt:</b> <i>Here, specify what you dont want to see in the Image. If you're lazy, the default negative prompt will be used. Alternatively, you can create your own. The generated image varies depending on the Negative prompt too.</i>

<b>8. ALL THE BEST LOOKING FORWARD TO WHAT YOU CREATE!</b>""",parse_mode="HTML",disable_web_page_preview=True) 
 
    

@bot.message_handler(['premium'])
def idlelo(message):
    bot.send_photo(message.chat.id,photo="AgACAgEAAxkBAAIG2WUjGX0sK6k3lNfRpK30yThydZKkAALgqzEb-d8ZRYHTwrss97-3AQADAgADeAADMAQ",caption=f""" Dear {message.from_user.first_name} \n\n---------------------------------------\nPayment options : \nUPI , CRYPTO , BINANCE , GPAY , PAYTM , PHONEPE \n\n Special payment discount if paid with Indian payment methods \n\nPlease contact @Desidiffusionsupportbot to buy premium of this bot """)
    
    
    
def linkmaker():
    hoho1="https://link-hub.net/967929/code-for-ai-image-gen"
    hoho="https://t.me/DesidiffusionBot?start=0Z03-WCQ5-000L-WY7W-XCQY"
    
    
    linkbygp = f" https://gplinks.in/api?api={apiofgp}&url=yourdestinationlink.com&alias=CustomAlias"
    return hoho
def shorten_url(long_url):
    api_url = f"https://gplinks.in/api?api={apiofgp}&url={long_url}"
    response = requests.get(api_url)
    data = response.json()
    
    if data["status"] == "success":
        short_url = data["shortenedUrl"]
        return short_url
    else:
        return None
ap="aa"
forbiddenwords=["child","little","under 18","underage"]

def checkforcp(string):
    
    pattern = r'\b(?:' + '|'.join(forbiddenwords) + r')\b'
    if re.search(pattern, string, re.IGNORECASE):
            return True
    return False
        
@bot.message_handler(commands=['diffuse'])
def start(message):
    chat_id = message.chat.id
    user_id_to_create=f"{chat_id}"
    user_ref=uref.child(user_id_to_create)
    user_dataindb = user_ref.get()
    if user_dataindb:
    # User data exists, display it
        print('User data already exists:')
        print(f"User ID: {user_id_to_create}")
        print(f"Last Generated: {user_dataindb.get('last_generated')}")
        print(f"Paid: {user_dataindb.get('paid')}")
        print(f"Total Generations: {user_dataindb.get('total_generations')}")
        print(f"User Name: {user_dataindb.get('user_name')}")
        print(f"Verified for (hours): {user_dataindb.get('verifiedforhrs')}")
    else:
    # User data doesn't exist, create it
        print(f'User with ID {user_id_to_create} not found. Creating new data...')
        milihrs=(24*60*60*1000)
        new_user_data = {
            'last_generated': 0,
            'paid': False,
            'total_generations': 0,
            'user_name': message.from_user.username,
            'name' :message.from_user.first_name,
            'verifiedforhrs' : milihrs ,
            'lastverifiedat' : int(time.time())

        }
        user_ref.set(new_user_data)
        print('New user data created:')
        print(new_user_data)
    cooldown = 120000
    c_last_generated = user_ref.child('last_generated').get()
    c_status = user_ref.child('status').get()
    c_paid = user_ref.child('paid').get()
    if c_paid != True:
        start = time.time()
        verifremaintime=check_verification_time(chatid=chat_id)
        if verifremaintime==True:
            code=keymaker(12)
            longurl = f"https://t.me/DesidiffusionBot?start={code}" 
            link=shorten_url(longurl)
            bot.send_message(chat_id,f" You are Not a premium member, Buy premium click --> /premium to know more. \n-------------------\nYour verification token has expired, You need to verify to continue using the bot\n Click this link to obtain your refresh verification token {link} . \n\nHow to open this link - https://youtu.be/-DGRklEVm3Q?feature=shared ")
            end=time.time()
            print("veriftimeoutsidefunc",end-start)
            return
        else: pass
    if c_status == 'generating':
        bot.reply_to(message,"You are already Genrating an image wait  ")
        return   
    if c_paid != True:
        print(c_last_generated) 
        timeLeft = cooldown - ((int(datetime.datetime.now().timestamp() * 1000)) - c_last_generated)
        print(timeLeft)

        if timeLeft > 0:
            minutes, miliseconds = divmod(timeLeft, 60000)
            seconds = miliseconds // 1000
            if minutes > 0:
                bot.reply_to(message,f"Oi Oi, Calmdown Wait {minutes} minutes {seconds} seconds to run this command again or You could buy premium and reduce the cooldown hehe.")
                return
            else:
                bot.reply_to(message,f"Oi Oi, Calmdown Wait {int(seconds)} seconds to run this command again or You could buy premium and reduce the cooldown hehe.")
                return

    


    # if  str(chat_id) in ap :
    #     bot.reply_to(message,"You are already Genrating an image ")
    # else:
    user_data[chat_id] = {} 

    cancel_button = types.KeyboardButton("Cancel")
    markup = types.ReplyKeyboardMarkup(row_width=1)
    markup.add(cancel_button)
    bot.send_message(chat_id, "Please enter your prompt:", reply_markup=markup)
    bot.register_next_step_handler(message, get_prompt)

def get_prompt(message):
    chat_id = message.chat.id
    prompt = message.text
    if prompt.lower() == "cancel":
        
        del user_data[chat_id]
        bot.send_message(chat_id, "Process cancelled.", reply_markup=types.ReplyKeyboardRemove())
    elif checkforcp(prompt.lower()) == True:
        bot.send_message(chat_id, "Your prompt has illegal words Please comply with our usage conditions ", reply_markup=types.ReplyKeyboardRemove())
    else:
        user_data[chat_id]['prompt'] = prompt
        
        steps_markup = types.ReplyKeyboardMarkup(row_width=2)
        steps_markup.add(types.KeyboardButton("Skip"))
        steps_markup.add(types.KeyboardButton("Cancel"))
        bot.send_message(chat_id, "Choose the number of steps:", reply_markup=steps_markup)
        bot.register_next_step_handler(message, get_steps)

def get_steps(message):
    chat_id = message.chat.id
    steps_input = message.text
    if steps_input.lower() == "skip":
        
        user_data[chat_id]['steps'] = 20
    elif steps_input.lower() == "cancel":
        
        del user_data[chat_id]
        bot.send_message(chat_id, "Process cancelled.", reply_markup=types.ReplyKeyboardRemove())
        return
    
    else:
        try:
            steps = int(steps_input)
            
            if steps < 1:
                steps = 1
            elif steps > 50:
                steps = 50
            user_data[chat_id]['steps'] = steps
        except ValueError:
           
            bot.send_message(chat_id, "Invalid input. Please enter a number between 1 and 50.")
            bot.register_next_step_handler(message, get_steps)

   
    
    cfg_markup = types.ReplyKeyboardMarkup(row_width=2)
    cfg_markup.add(types.KeyboardButton("Skip"))
    cfg_markup.add(types.KeyboardButton("Cancel"))
    bot.send_message(chat_id, "Choose CFG value (between 1 to 10):",reply_markup=cfg_markup)
    bot.register_next_step_handler(message, get_cfg_value)

def get_cfg_value(message):
    chat_id = message.chat.id
    cfg_input = message.text
    if cfg_input.lower() == "skip":
        
        user_data[chat_id]['cfg_value'] = 7
    elif cfg_input.lower() == "cancel":
        
        del user_data[chat_id]
        bot.send_message(chat_id, "Process cancelled.", reply_markup=types.ReplyKeyboardRemove())
        return
    else:
        try:
            cfg_value = int(cfg_input)
            
            if cfg_value < 1:
                cfg_value = 1
            elif cfg_value > 10:
                cfg_value = 10
            user_data[chat_id]['cfg_value'] = cfg_value
        except ValueError:
            # Handle invalid input here, you can send a message or take other actions
            bot.send_message(chat_id, "Invalid input. Please enter a number between 1 and 10.")
            bot.register_next_step_handler(message, get_cfg_value)

    
    
    models_markup = types.ReplyKeyboardMarkup(row_width=1)
    
   
    for model in models_list:
        models_markup.add(types.KeyboardButton(model))
    bot.send_message(chat_id, "Choose a model from the list:",reply_markup=models_markup)
    
    bot.register_next_step_handler(message, get_chosen_model)

def get_chosen_model(message):
    chat_id = message.chat.id
    chosen_model = message.text
    user_data[chat_id]['chosen_model'] = chosen_model
    
    
    
    sampler_markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
    
   
    for sampler in samplers_list:
        sampler_markup.add(types.KeyboardButton(sampler))
    bot.send_message(chat_id, "Choose a sampler from the list:",reply_markup=sampler_markup)
    
    bot.register_next_step_handler(message, get_chosen_sampler)

def get_chosen_sampler(message):
    chat_id = message.chat.id
    chosen_sampler = message.text
    user_data[chat_id]['chosen_sampler'] = chosen_sampler
    
    
    
    negative_prompt_markup = types.ReplyKeyboardMarkup(row_width=2)
    negative_prompt_markup.add(types.KeyboardButton("Skip"))
    negative_prompt_markup.add(types.KeyboardButton("Cancel"))
    bot.send_message(chat_id, "Enter negative prompt (optional):",reply_markup=negative_prompt_markup)
    bot.register_next_step_handler(message, get_negative_prompt)

def get_negative_prompt(message):
    chat_id = message.chat.id
    negative_prompt_input = message.text
    if negative_prompt_input.lower() == "skip":
        
        user_data[chat_id]['negative_prompt'] = "((((ugly)))), (((duplicate))), ((morbid)), ((mutilated)), out of frame, extra fingers, mutated hands, ((poorly drawn hands)), ((poorly drawn face)), (((mutation))), (((deformed))), ((ugly)), blurry, ((bad anatomy)), (((bad proportions))), ((extra limbs)), cloned face, (((disfigured))), out of frame, ugly, extra limbs, (bad anatomy), gross proportions, (malformed limbs), ((missing arms)), ((missing legs)), (((extra arms))), (((extra legs))), mutated hands, (fused fingers), (too many fingers), (((long neck)))"
    elif negative_prompt_input.lower() == "cancel":
       
        del user_data[chat_id]
        bot.send_message(chat_id, "Process cancelled.", reply_markup=types.ReplyKeyboardRemove())
        return
    else:
        user_data[chat_id]['negative_prompt'] = negative_prompt_input
    
    
    
    aspect_ratio_markup = types.ReplyKeyboardMarkup(row_width=4,one_time_keyboard=True)
    aspect_ratio_markup.add(types.KeyboardButton("Square"))
    aspect_ratio_markup.add(types.KeyboardButton("Portrait"))
    aspect_ratio_markup.add(types.KeyboardButton("Landscape"))
    bot.send_message(chat_id, "Choose aspect ratio:",reply_markup=aspect_ratio_markup)
    bot.register_next_step_handler(message, get_aspect_ratio)

def get_aspect_ratio(message):
    chat_id = message.chat.id
    usernameofuser=message.from_user.username
    aspect_ratio = message.text.lower()
    user_data[chat_id]['aspect_ratio'] = aspect_ratio
    

    textmsg1=f""" * Cooking Image (0.69%) *
 * Positive Prompt : {(user_data[chat_id]['prompt'])}  *
 * Negative Prompt : {(user_data[chat_id]['negative_prompt'])}   *

```

|| Steps -> {user_data[chat_id]['steps']} ||
|| Cfg Value -> {user_data[chat_id]['cfg_value']} ||
|| Model -> {user_data[chat_id]['chosen_model']} ||
|| Sampler -> {user_data[chat_id]['chosen_sampler']} ||
|| Aspect -> {user_data[chat_id]['aspect_ratio']} || ```

Requested By : @{usernameofuser}"""
    
    # textmsg=telebot.formatting.escape_markdown(textmsg1)
    # textmsg=textmsg1.replace('.',"\.")
    
        
    genit=gen(positive_prompt=user_data[chat_id]['prompt'],aspect_ratio=user_data[chat_id]['aspect_ratio'],sampler=user_data[chat_id]['chosen_sampler'],steps=user_data[chat_id]['steps'],scale=user_data[chat_id]['cfg_value'],model=user_data[chat_id]['chosen_model'],negativeprompt=user_data[chat_id]['negative_prompt'])
    if genit[0] == 200:
    
        bot.send_message(chat_id,text=textmsg1,parse_mode="Markdown",reply_markup=types.ReplyKeyboardRemove())
        bot.send_sticker(chat_id,"CAACAgQAAxkBAAJCRmULfQ8yHjuqTTdZZmJy4i_PgYDWAAIyCAACpvFxHlgL7GVt30bJMAQ")
        # global ap #ap change
        # ap = [str(chat_id)] #ap change 
        user_ref=uref.child(str(chat_id))
        updated_data = {
                'status': "generating"
            }
        user_ref.update(updated_data)
        bot.send_chat_action(chat_id,'upload_photo')
        img=checkerthread(genit[1])
        bot.send_photo(chat_id,img)
        # ap = "aa" #ap back to normal 
        c_total_generations = user_ref.child('total_generations').get()
            
        last_generated = int(datetime.datetime.now().timestamp() * 1000) 
        new_total_generations =  c_total_generations + 1
        updated_data = {
            'last_generated': last_generated,
            'total_generations': new_total_generations,
            'status': "idle"
        }
        user_ref.update(updated_data)
        # Confirm the update
        print('User data updated successfully:')
        print(updated_data)
    else:
        try:
            bot.send_message(f"Issue In generating :{genit[1]}")
            print(genit[1],genit)
        except TypeError:
            del user_data[chat_id]
            bot.send_message(chat_id, "input is wrong , Correct your input and try again", reply_markup=types.ReplyKeyboardRemove())
            return
       
   
    
    
    
    # bot.send_document(chat_id,document=(open("cooking.gif","rb")), caption="Generating....", reply_markup=types.ReplyKeyboardRemove(),parse_mode="markdown") 
    
    
    # print(user_data)
    

if __name__ == '__main__':
    print("Bot Started...")
    bot.infinity_polling(1.0)