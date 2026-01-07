# Cloud Service Referee - Deployment Guide

## 🚀 Streamlit Cloud Deployment (Recommended)

### Prerequisites
- ✅ GitHub repository: https://github.com/SRINIVASINDIA/The_referee
- ✅ Streamlit Cloud account (free): https://streamlit.io/cloud

### Step 1: Access Streamlit Cloud
1. Go to https://streamlit.io/cloud
2. Sign in with your GitHub account
3. Click "New app"

### Step 2: Deploy Configuration
- **Repository**: `SRINIVASINDIA/The_referee`
- **Branch**: `main`
- **Main file path**: `app.py`
- **App URL**: Choose your preferred subdomain (e.g., `cloud-service-referee`)

### Step 3: Advanced Settings (Optional)
- **Python version**: 3.11 (specified in runtime.txt)
- **Secrets**: None required for this application

### Step 4: Deploy
1. Click "Deploy!"
2. Wait for deployment (usually 2-5 minutes)
3. Your app will be available at: `https://your-app-name.streamlit.app`

## 🌐 Alternative Deployment Options

### Option 2: Heroku Deployment

Create `Procfile`:
```
web: sh setup.sh && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

### Option 3: Railway Deployment

1. Connect your GitHub repository to Railway
2. Railway will auto-detect the Python app
3. Set start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

### Option 4: Render Deployment

1. Connect GitHub repository to Render
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

## 📋 Deployment Checklist

### Pre-Deployment Verification
- [x] All dependencies in requirements.txt
- [x] App runs locally: `streamlit run app.py`
- [x] Tests pass: `pytest -v`
- [x] No hardcoded secrets or API keys
- [x] Proper error handling implemented
- [x] .streamlit/config.toml configured
- [x] runtime.txt specifies Python version

### Post-Deployment Verification
- [ ] App loads without errors
- [ ] All constraint inputs work
- [ ] Service comparison generates results
- [ ] UI is responsive on mobile
- [ ] No console errors in browser
- [ ] Performance is acceptable (< 3s load time)

## 🔧 Configuration Files

### .streamlit/config.toml
```toml
[global]
developmentMode = false

[server]
runOnSave = true
port = 8501

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

### runtime.txt
```
python-3.11
```

### requirements.txt
```
streamlit>=1.28.0
hypothesis>=6.88.0
pytest>=7.4.0
dataclasses-json>=0.6.0
typing-extensions>=4.8.0
```

## 🎯 Expected Deployment URL

Once deployed on Streamlit Cloud, your app will be available at:
`https://cloud-service-referee.streamlit.app` (or your chosen subdomain)

## 🚨 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are in requirements.txt
   - Check Python version compatibility

2. **Module Not Found**
   - Verify src/ directory structure
   - Check __init__.py files are present

3. **Streamlit Errors**
   - Check .streamlit/config.toml syntax
   - Verify app.py is in root directory

4. **Performance Issues**
   - Monitor resource usage in Streamlit Cloud dashboard
   - Consider caching with @st.cache_data if needed

### Debug Commands
```bash
# Test locally
streamlit run app.py

# Run tests
pytest -v

# Check dependencies
pip list

# Validate requirements
pip install -r requirements.txt
```

## 📊 Deployment Status

- ✅ **Repository**: Ready for deployment
- ✅ **Configuration**: Streamlit Cloud optimized
- ✅ **Dependencies**: All specified in requirements.txt
- ✅ **Testing**: 54 tests passing
- ✅ **Documentation**: Complete

## 🎉 Success Metrics

After deployment, your Cloud Service Referee will provide:
- **Neutral AWS service comparisons**
- **Educational trade-off explanations**
- **Independent service evaluations**
- **Responsive web interface**
- **Production-ready reliability**

Ready to deploy! Choose Streamlit Cloud for the easiest deployment experience.