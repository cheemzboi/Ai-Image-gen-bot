# 🎨 DesiDiffusion — AI Image Generator Bot (Telegram)

> The Telegram component of the **DesiDiffusion** project — a Stable Diffusion powered AI image generator that lets users create images right inside a Telegram chat.

This bot guides users through an interactive, step-by-step prompt flow (positive prompt → steps → CFG → model → sampler → negative prompt → aspect ratio) and generates images

### 1. Clone the repository

```bash
git clone https://github.com/cheemzboi/Ai-Image-gen-bot.git
cd Ai-Image-gen-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Firebase

1. In the [Firebase Console](https://console.firebase.google.com/), create a project and enable the **Realtime Database**.
2. Go to **Project Settings → Service Accounts** and generate a new **private key**. This downloads a JSON credentials file.
3. Place that JSON file in the project root.
4. Update `bot.py` (and `keygen.py`) with your credentials filename and database URL:

   ```python
   cred = credentials.Certificate("your-firebase-adminsdk-credentials.json")
   firebase_admin.initialize_app(cred, {
       'databaseURL': 'https://your-project-default-rtdb.firebasedatabase.app/'
   })
   ```

### 4. Set up environment variables

Copy the example file and fill in your own values:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
tk=<your telegram bot token>
apikey=<your prodia api token>
apiofgp=<your gplinks api token>
```

### 5. Add admin IDs

Open `verifiedadmins.txt` and add the Telegram chat ID of each admin, one per line. Users can find their ID by sending the bot the `/id` command.

```
123456789
987654321
```

### 6. Run the bot

```bash
python bot.py
```

You should see `Bot Started...` in the console once it's running.

---

## 💬 Bot Commands

| Command | Description |
|---|---|
| `/start` | Starts the bot and shows the welcome message. Also redeems a key when passed as a parameter. |
| `/help` | Shows the list of available commands. |
| `/diffuse` | Begins the interactive image generation flow. |
| `/id` | Returns the user's Telegram chat ID. |
| `/premium` | Shows information about premium subscriptions. |
| `/howtousebot` | Detailed guide on prompts, steps, CFG, models, samplers, and more. |
| `/keygen <hours>` | **Admin only** — generates a redeemable key worth the given number of hours. |

---



## 📦 Dependencies

- `firebase-admin` — Firebase Realtime Database access
- `pyTelegramBotAPI` — Telegram Bot framework
- `python-dotenv` — environment variable loading
- `requests` — HTTP requests to the Prodia and GPLinks APIs

---

## ⚠️ Notes

- The Firebase credentials JSON and your `.env` file contain secrets — never commit them. `.env` is already in `.gitignore`; add your credentials filename too.
- This is the **Telegram side** of DesiDiffusion; a separate Discord bot exists as part of the wider project.
