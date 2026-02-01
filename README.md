# 🤖 Telegram Bot : Member Scraper, Group Adder & Bulk SMS

A comprehensive Telegram automation toolkit for scraping group members, adding them to your groups, and sending bulk messages.

## 🚀 Features

- **Multi-account management** with session persistence
- **Advanced member scraping** with activity filtering
- **Automated member addition** with rate limiting
- **Bulk messaging** with flood protection
- **Windows automation** for parallel processing
- **Colorful console interface** with detailed progress tracking

## 📋 Prerequisites

- Python 3.7+
- Telegram API credentials
- Windows OS (for full automation features)

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/aashishgrinds/Telegram-bot-Scrape-member-add-them-and-bulk-sms.git
   cd Telegram-bot-Scrape-member-add-them-and-bulk-sms
   ```

2. **Create virtual environment**

   ```bash
   python -m venv env
   # Windows
   .\env\Scripts\activate
   # Linux/macOS
   source env/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Get Telegram API credentials**
   - Visit [my.telegram.org/auth](https://my.telegram.org/auth)
   - Create an app to get API ID and API Hash

## 📖 Usage Guide

### Step 1: Account Management

Run `python authenticate.py` to manage your Telegram accounts:

**Options:**

- `[1] Add new accounts` - Enter API ID, API Hash, and phone number
- `[2] Filter banned accounts` - Remove suspended accounts
- `[3] List all accounts` - View stored credentials
- `[4] Delete specific accounts` - Remove selected accounts
- `[5] Quit` - Exit the program

### Step 2: Member Scraping

Run `python member_scraper.py` to extract group members:

**Features:**

- Choose from multiple authenticated accounts
- Support for public and private groups
- Activity-based filtering:
  - All users
  - Active users (online today/yesterday)
  - Users active in last week/month
  - Non-active users
- Optional admin separation
- Data saved to `members/members.csv`

**Group Input:**

- **Public groups**: Enter username without `@` (e.g., `PythonHub`)
- **Private groups**: Paste invite link

### Step 3: Member Addition

Run `python member_adder.py` for automated member invitation:

**Process:**

1. Creates sessions for all accounts
2. Joins target group from all accounts
3. Distributes members across accounts (60 per account)
4. Launches parallel `user_adder.py` instances
5. Automated Windows CMD execution

**Features:**

- Multi-account parallel processing
- CSV file distribution
- Rate limiting (30s between additions)
- Flood protection
- Progress tracking and resume capability

### Step 4: Bulk Messaging

Run `python bulk_sms.py` to send messages to scraped members:

**Options:**

- Send by username or user ID
- Custom message content
- Random delays (15-25 seconds)
- Flood wait handling
- Error recovery

## 📁 Project Structure

```
├── authenticate.py      # Account management system
├── member_scraper.py    # Group member extraction
├── member_adder.py      # Automated member addition coordinator
├── user_adder.py        # Individual member addition worker
├── bulk_sms.py          # Bulk messaging system
├── account_info.txt     # Stored account credentials
├── members/             # Scraped member data
│   ├── members.csv      # Main member database
│   └── admins.csv       # Separated admin data
├── sessions/            # Telegram session files
├── target_group.txt     # Last scraped group info
└── requirements.txt     # Python dependencies
```

## ⚙️ Configuration

### Rate Limiting

- **Member addition**: 25-35 seconds between additions
- **Bulk messaging**: 15-25 seconds between messages
- **Batch processing**: 60 users per account
- **Flood protection**: Automatic handling of Telegram limits

### Error Handling

- **Phone number bans**: Automatic filtering
- **Flood wait errors**: Automatic retry with proper delays
- **Privacy restrictions**: Skip users with privacy settings
- **Network interruptions**: Resume capability with progress saving

## 🔧 Troubleshooting

### Common Issues

**Members not getting added:**

- Check if accounts are banned (use option 2 in authenticate.py)
- Verify target group permissions
- Try with different accounts

**Login errors:**

- Disable two-factor authentication temporarily
- Verify phone number format (country code + number)
- Check API credentials

**Flood errors:**

- Wait for the specified time period
- Reduce the number of concurrent accounts
- Increase delay intervals

**Session issues:**

- Delete corrupted session files from `sessions/` folder
- Re-authenticate affected accounts

### Safety Tips

- Use aged Telegram accounts (6+ months old)
- Don't exceed 10 concurrent accounts
- Monitor for Telegram warnings
- Respect rate limits and user privacy

## 📊 Data Format

### members.csv Structure

```csv
username,user_id,access_hash,group,group_id,status
john_doe,123456789,987654321,TargetGroup,-100123456789,UserStatusOnline
```

### account_info.txt Format

Binary file storing tuples of: `(api_id, api_hash, phone_number)`

## 🚨 Important Notes

- **Windows Only**: Full automation features require Windows
- **API Limits**: Respect Telegram's rate limits
- **Legal Compliance**: Use responsibly and comply with ToS
- **Backup Data**: Regularly backup `account_info.txt` and session files

