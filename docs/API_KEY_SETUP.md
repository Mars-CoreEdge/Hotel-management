# 🔐 **Secure API Key Setup Guide**

## 🎯 **Important: OpenAI API Key Configuration**

For security reasons, the OpenAI API key is not included in the code. You need to set it up using environment variables.

### **Method 1: Environment Variable (Recommended)**

#### **On Windows:**
```bash
# Set the environment variable for current session
set OPENAI_API_KEY=your-actual-api-key-here

# Or set permanently
setx OPENAI_API_KEY "your-actual-api-key-here"
```

#### **On Mac/Linux:**
```bash
# Set the environment variable for current session
export OPENAI_API_KEY=your-actual-api-key-here

# Or add to your ~/.bashrc or ~/.zshrc for permanent setup
echo 'export OPENAI_API_KEY="your-actual-api-key-here"' >> ~/.bashrc
```

### **Method 2: Create .env File**

1. Create a file named `.env` in the project root
2. Add your API key:
```
OPENAI_API_KEY=your-actual-api-key-here
```
3. The system will automatically load this file

### **Method 3: Direct Code Configuration (Not Recommended)**

If you need to test quickly, you can temporarily modify `ai_reception.py`:
```python
# In ai_reception.py, line ~16
OPENAI_CONFIG = {
    "api_key": "your-actual-api-key-here",  # Replace with your key
    # ... rest of config
}
```

**⚠️ Warning: Don't commit this change to Git!**

---

## 🔧 **Getting Your OpenAI API Key**

1. Go to https://platform.openai.com/
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (it starts with `sk-`)

---

## 🚀 **Quick Setup**

1. Set your API key using Method 1 or 2 above
2. Restart your terminal/command prompt
3. Run the hotel management system:
```bash
python main.py
```

Your AI Reception will now work with OpenAI integration! 🤖✨

---

## 🛡️ **Security Best Practices**

- ✅ Never commit API keys to Git repositories
- ✅ Use environment variables for sensitive data
- ✅ Keep your API key private and secure
- ✅ Regenerate keys if they're ever exposed
- ❌ Don't share your API key in public repositories
- ❌ Don't include keys in screenshots or documentation 