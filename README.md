# TonLucky - Telegram-казино бот на TON

🎉 **Ставь. Играй. Выигрывай в TON.**

## 📋 Описание

TonLucky - это развлекательный Telegram-бот с элементами азартных игр на базе **TON (The Open Network)**, где пользователи:
- покупают **игровые фишки за TON**,
- играют в **18+ мини-игр**,
- могут **выводить выигрыш в TON или NFT** (с ограничениями),
- участвуют в **турнирах и социальных активностях**.

> ⚠️ **Важно**: Бот позиционируется как **игровой симулятор**, а не реальное азартное заведение. Все ставки — на виртуальные фишки.

## 🧩 Игры

- 🎲 **TonDice** - Выбери число от 1 до 6 → бросок кубика → выигрыш при совпадении
- 🎰 **TonRoulette** - Европейская рулетка (0–36), ставки на цвет, чёт/нечет, число
- 🪙 **TonCoinFlip** - Орёл/решка, множитель x1.95
- 🎰 **TonSlots** - 3 барабана, 5 тем (космос, Египет, киберпанк, джунгли, неон)
- 👑 **TonBlackjack** - Против ИИ-дилера, страховка, удвоение ставки
- 📈 **TonCrash** - График растёт → нажми «забрать» до обвала
- 💣 **TonMines** - Поле 5×5, мин от 1 до 24 → открывай безопасные клетки
- 📏 **TonHiLo** - Карта открыта → угадай, следующая выше или ниже
- 🧮 **TonKeno** - Выбери до 10 чисел из 80 → рандомный розыгрыш
- 🃏 **TonBaccarat** - Ставка на Player/Banker/Tie, автоматический раздающий
- 🎯 **TonPlinko** - Шарик падает по доске → попадает в ячейку с множителем (x0.5–x100)
- 🎡 **TonWheel** - Колесо фортуны: фишки, NFT, бустеры, x2
- 🎫 **TonLottery** - Ежедневный розыгрыш — билет за 0.1 TON
- 🎳 **TonBingo** - Карточка 5×5, совпадения по линиям, чат-турниры
- 🤞 **TonScratch** - Виртуальный «почесать» билет → мгновенный результат
- ↔️ **TonOver/Under** - Число от 1 до 100 → ставка >50 или <50
- 7️⃣ **TonLucky7** - Ставка на выпадение семёрки в комбинациях
- 🃏 **TonPoker** - Texas Hold’em против ботов, еженедельные турниры

## 🛠 Архитектура

### Фронтенд:
- **Telegram Bot API** (BotFather, Webhook)
- Интерфейс: кнопки, меню, инлайн-клавиатуры
- Поддержка мультимедиа (анимации для слотов, Plinko и т.д.)

### Бэкенд:
- Язык: **Python (aiogram 3.x)**
- База данных: **PostgreSQL** (пользователи, балансы, игры, транзакции)
- Кэширование: **Redis** (для активных сессий)

### Интеграция с TON:
- **TON Connect** — авторизация через TON Wallet
- **TON Wallet API** — приём TON → зачисление фишек
- **Smart Contract** — для прозрачности розыгрышей
- **TON DNS** — красивый адрес: `tonlucky.ton`

## 💰 Монетизация

- **Продажа фишек** - 1 TON = 1000 фишек (курс фиксированный или с небольшой наценкой)
- **Комиссия на вывод** - Вывод выигрыша: до 5 TON/день, комиссия 3%
- **Премиум-подписка** - 2 TON/мес: без рекламы, x1.1 к выигрышам, эксклюзивные игры
- **NFT-маркетплейс** - Редкие скины, аватары, билеты — комиссия 5%
- **Реферальная система** - Пригласи друга → 10% от его первых покупок
- **Boost-предметы** - x2 на следующую игру за 0.2 TON

## 🚀 Запуск проекта

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта и укажите следующие переменные:

```
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
DATABASE_URL=postgresql://tonlucky_user:tonlucky_password@localhost/tonlucky
REDIS_URL=redis://localhost:6379
TON_CONNECT_API_KEY=your_ton_connect_api_key
TON_WALLET_ADDRESS=your_ton_wallet_address
ADMIN_CHAT_ID=your_admin_chat_id
```

### 3. Настройка базы данных

Убедитесь, что PostgreSQL запущен и настроен. При запуске бота таблицы будут созданы автоматически.

### 4. Запуск бота

```bash
python -m bot.main
```

## 📅 Этапы разработки

| Этап | Срок | Описание |
|------|------|--------|
| **MVP (1.0)** | 2 недели | TonDice, TonCoinFlip, TonRoulette + пополнение/вывод TON |
| **Beta (2.0)** | 2 недели | Добавить 5 игр, админку, рефералку |
| **Launch (3.0)** | 1 неделя | Запуск всех 18 игр, NFT-призы, турниры |
| **Growth** | Постоянно | Маркетинг в TON-чатах, коллабы с NFT-проектами, геймификация |

## 🔐 Безопасность и честность

- Все игры — **на основе криптографически безопасного RNG** (лучше — с открытой верификацией)
- Возможность **проверить честность розыгрыша** (хэш + сид)
- **Ограничение ставок** для новых пользователей (например, макс. 1 TON в первые 24 ч)
- **Daily loss limit** (по желанию пользователя)
- **2FA для вывода** (подтверждение в Telegram)

## ⚖️ Юридические аспекты

- В описании бота:  
  > «TonLucky — развлекательный симулятор. Все ставки производятся на виртуальные фишки. Не является азартной игрой. Для пользователей 18+»
- **Запрет на вывод свыше 5 TON/день** (для минимизации рисков)
- **Не принимаем фиат** — только TON → фишки → TON
- Сервера — в юрисдикции, дружественной к крипте (например, ОАЭ, Сингапур)

## 📊 Метрики успеха

- **DAU > 1000** через 30 дней  
- **Средний чек пополнения** — 0.3 TON  
- **Retention D7** — >25%  
- **ARPPU (доход на платящего)** — >0.5 TON/мес

## 📣 Продвижение

- Запуск в TON-сообществах (@ton_coin, @ton_blockchain_ru)  
- Розыгрыши NFT в каналах  
- Интеграция с TON DNS и TON Sites  
- Партнёрка с TON-кошельками (Tonkeeper, MyTonWallet)  
- Виральные механики: «поделись выигрышем — получи x2»

## 🧠 Дополнительно

- Поддержка **мультиязычности** (RU, EN, TR, PT)  
- Возможность **играть без кошелька** (только на демо-фишки)  
- **Ежедневные бонусы** за вход  
- **Система уровней** (чем больше играешь — тем выше кэшбэк)

---

✅ **Итог**: TonLucky — это не просто казино, а **социальная игровая экосистема на TON**, сочетающая развлечение, коллекционирование, турниры и микро-монетизацию.

# Production Deployment Guide

This guide will help you deploy the TonLucky Telegram casino bot in a production environment.

## 🚀 Quick Start with Docker

### 1. Environment Setup
First, copy the example environment file and fill in your values:
```bash
cp .env .env.production
```

Edit `.env.production` and set your values:
- `BOT_TOKEN`: Your Telegram bot token
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `TON_WALLET_ADDRESS`: Your TON wallet address for deposits/withdrawals
- `SECRET_KEY`: A long, random secret key
- `JWT_SECRET`: A long, random JWT secret

### 2. Run with Docker Compose
```bash
# Build and start the services
docker-compose up -d

# View logs
docker-compose logs -f bot
```

## 🛠️ Manual Deployment

### 1. Prerequisites
- Python 3.11+
- PostgreSQL 12+
- Redis 6+
- TON Connect API key (optional)

### 2. Setup Instructions
```bash
# Clone the repository
git clone <your-repo-url>
cd tonlucky

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables in .env file
cp .env .env.production

# Run the bot
python -m bot.main
```

### 3. Using the Startup Script
```bash
# Make the script executable
chmod +x start.sh

# Run the bot
./start.sh
```

## 📁 Project Structure
```
/workspace/
├── bot/                    # Main bot source code
│   ├── main.py            # Main bot entry point
│   ├── config.py          # Configuration settings
│   ├── handlers/          # Bot command handlers
│   ├── database/          # Database models and connection
│   ├── games/             # Game implementations
│   └── keyboards/         # Inline keyboards
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
└── start.sh              # Production startup script
```

## 🛡️ Security Best Practices

1. **Environment Variables**: Never commit `.env` files to version control
2. **Secret Keys**: Use strong, randomly generated keys for SECRET_KEY and JWT_SECRET
3. **Database**: Use strong passwords and restrict database access
4. **Redis**: Configure authentication and restrict access
5. **Bot Token**: Keep your bot token secure

## 📊 Monitoring & Logging

- Logs are stored in the `logs/` directory when using Docker
- Configure log rotation based on your needs
- Monitor database connections and Redis usage
- Set up alerts for critical errors

## 🔧 Configuration Options

### Game Settings
- `DICE_MIN_BET` / `DICE_MAX_BET`: Minimum and maximum bet amounts for dice game
- `DICE_MULTIPLIER`: Multiplier for dice game wins
- `MAX_BET_AMOUNT`: Maximum bet allowed across all games

### Limits
- `MAX_WITHDRAWAL_PER_DAY`: Maximum TON withdrawal per day
- `WITHDRAWAL_FEE_PERCENT`: Percentage fee for withdrawals
- `MIN_DEPOSIT_AMOUNT`: Minimum deposit amount

### TON Network
- `TON_NETWORK`: Set to "mainnet" for production, "testnet" for testing
- `TON_WALLET_ADDRESS`: Your TON wallet address for deposits/withdrawals

## 🚨 Troubleshooting

### Common Issues
1. **Database Connection**: Ensure PostgreSQL is running and accessible
2. **Redis Connection**: Check Redis is running and URL is correct
3. **Bot Token**: Verify your bot token is correct and bot is not banned
4. **Environment Variables**: Make sure all required environment variables are set

### Checking Status
```bash
# Docker containers status
docker-compose ps

# View bot logs
docker-compose logs bot

# Check database connection
docker-compose exec postgres psql -U tonlucky_user -d tonlucky -c "SELECT 1;"
```

## 🔄 Updates

To update the bot:
1. Pull the latest code
2. Update dependencies if needed: `pip install -r requirements.txt`
3. Restart the bot service

## 📞 Support

For issues or questions, please check:
- The logs for error messages
- Ensure all environment variables are properly set
- Database and Redis are accessible
- Bot token is valid and the bot is not restricted