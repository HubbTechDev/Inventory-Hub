# Inventory Hub Mobile - Quick Start Guide

## Prerequisites Check
- [ ] Node.js 18+ installed (`node --version`)
- [ ] Backend running at http://localhost:5000
- [ ] iOS Simulator or Android Emulator installed (or physical device with Expo Go)

## Quick Start (5 minutes)

### 1. Install Dependencies
```bash
cd mobile
npm install
```

### 2. Configure Backend URL

**Option A: Using localhost (emulators only)**
```bash
cp .env.example .env
# Edit .env if backend is not on localhost:5000
```

**Option B: Using physical device**
```bash
# Find your computer's IP address
# macOS/Linux: ifconfig | grep inet
# Windows: ipconfig

# Create .env file
echo "API_BASE_URL=http://YOUR_IP:5000" > .env
echo "API_TIMEOUT=30000" >> .env
```

### 3. Start Backend
```bash
# In a separate terminal
cd ../backend
python app.py
# Backend should be running on http://localhost:5000
```

### 4. Start Mobile App
```bash
# Back in mobile directory
npm start
```

### 5. Run on Device

**iOS Simulator (macOS only):**
- Press `i` in the terminal, or
- Run `npm run ios`

**Android Emulator:**
- Press `a` in the terminal, or
- Run `npm run android`

**Physical Device:**
- Install Expo Go from App Store/Play Store
- Scan the QR code shown in terminal
- Make sure device is on same WiFi as computer

## First Time Setup

### 1. Create Account
- Open the app
- Tap "Don't have an account? Register"
- Fill in username, email, password
- Tap "Register"

### 2. Explore Dashboard
- View inventory statistics
- See charts and analytics
- Access quick actions

### 3. Add Inventory
You can add inventory in two ways:

**Method 1: Scrape from marketplace**
- Tap "Scrape" tab
- Enter a Mercari or Depop search URL
- Select merchant type
- Set number of pages (start with 1)
- Tap "Start Scraping"
- Check "History" tab for job status

**Method 2: Manual entry** (via API)
- Use the backend API directly
- Or extend the mobile app with a create form

### 4. Browse Inventory
- Tap "Inventory" tab
- Search by title/SKU
- Filter by merchant/condition
- Sort by price/date
- Tap item for details

## Common URLs for Scraping

**Mercari:**
```
https://www.mercari.com/search/?keyword=vintage
https://www.mercari.com/search/?keyword=nike+shoes
https://www.mercari.com/search/?keyword=electronics
```

**Depop:**
```
https://www.depop.com/search/?q=vintage
https://www.depop.com/search/?q=streetwear
```

## Troubleshooting

### Backend Connection Issues

**Error: "Network request failed"**

1. Check backend is running:
   ```bash
   curl http://localhost:5000/api/auth/login
   # Should return 405 Method Not Allowed (that's good, means it's running)
   ```

2. Check .env file:
   ```bash
   cat .env
   # Should show API_BASE_URL=http://localhost:5000 (or your IP)
   ```

3. For physical devices, ping your computer:
   ```bash
   # On device, open browser and visit: http://YOUR_IP:5000
   # Should see "404 Not Found" (that's good, means backend is reachable)
   ```

4. Update API URL in app:
   - Open app
   - Go to Profile tab
   - Tap "API Configuration"
   - Enter correct URL
   - Tap "Update"

### Metro Bundler Issues

**Error: "Metro bundler failed to start"**
```bash
# Clear cache and restart
npx expo start -c
```

**Error: "Unable to resolve module"**
```bash
# Reinstall dependencies
rm -rf node_modules
npm install
npx expo start -c
```

### Build Errors

**TypeScript errors:**
```bash
# Check types
npm run type-check
```

**Missing dependencies:**
```bash
# Reinstall everything
npm install
```

## Testing Checklist

After setup, test these features:

- [ ] Register new account
- [ ] Login with credentials
- [ ] View dashboard stats
- [ ] Browse inventory list
- [ ] Search inventory
- [ ] Filter by merchant/condition
- [ ] View item details
- [ ] Start a scraping job
- [ ] View scraping history
- [ ] Check profile info
- [ ] Update API URL in settings
- [ ] Logout and login again

## Performance Tips

1. **Start Small:** Begin with 1-2 pages when scraping
2. **Use Filters:** Narrow down inventory lists with filters
3. **Refresh Wisely:** Pull-to-refresh updates data but uses API quota
4. **Cache Aware:** App caches data, but refreshes on navigation

## Development Tips

**Hot Reload:**
- Press `r` to reload the app
- Shake device (or Cmd+D/Cmd+M) for dev menu
- Enable "Fast Refresh" for automatic reloads

**Debugging:**
- Open React DevTools: `npm install -g react-devtools && react-devtools`
- View console logs in terminal
- Use `console.log()` for debugging

**Testing on Multiple Platforms:**
```bash
# Test on both platforms
npm run ios    # macOS only
npm run android
```

## Next Steps

1. **Customize:** Edit colors in `src/constants/Colors.ts`
2. **Extend:** Add new features in `src/screens/`
3. **API:** Add more endpoints in `src/api/`
4. **Deploy:** Build production apps with EAS Build

## Resources

- [Expo Documentation](https://docs.expo.dev/)
- [React Navigation](https://reactnavigation.org/)
- [React Native Paper](https://callstack.github.io/react-native-paper/)
- [Backend API Docs](../backend/README.md)

---

**Happy Coding! 🚀**
