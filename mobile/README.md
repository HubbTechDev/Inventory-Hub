# Inventory-Hub Mobile App

> **Note:** This mobile app requires the Inventory-Hub backend API to be running. 
> See the [backend documentation](../backend/README.md) for setup instructions.

A complete React Native (Expo) mobile application for managing your e-commerce inventory across multiple platforms. Connect to the Flask backend API to track items, scrape marketplaces, and analyze your inventory with ease.

## 🚀 Features

### Authentication
- **Secure Login & Registration** - JWT-based authentication with token refresh
- **Auto-login** - Persistent authentication using AsyncStorage
- **Form Validation** - Real-time validation with Formik and Yup

### Dashboard
- **Inventory Statistics** - Total items, value, stock status
- **Visual Analytics** - Pie and bar charts for merchants, conditions, categories
- **Upload Job Stats** - Track successful, failed, and pending jobs
- **Quick Actions** - Fast access to common tasks

### Inventory Management
- **List View** - Paginated list with pull-to-refresh
- **Search & Filter** - Search by title/SKU, filter by merchant/condition/stock
- **Sort Options** - Sort by date, price, title
- **Item Details** - Full product information with images
- **Delete Items** - Remove items from inventory

### Web Scraping
- **Multi-Platform Support** - Mercari, Depop, Generic e-commerce sites
- **Configurable Jobs** - Set URL, merchant, and page count
- **Job History** - View all upload jobs with status
- **Real-time Status** - Track job progress and errors

### Profile & Settings
- **User Profile** - View account information
- **API Configuration** - Change backend URL on the fly
- **Logout** - Secure session termination

## 📋 Prerequisites

- **Node.js** 18.x or higher
- **npm** or **yarn**
- **Expo CLI** (optional, will be installed via npx)
- **iOS Simulator** (macOS) or **Android Emulator**
- **Physical device** with Expo Go app (optional)

## 🛠️ Installation

### 1. Clone and Navigate
```bash
cd mobile
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Configure Environment

Create a `.env` file from the example:
```bash
cp .env.example .env
```

Edit `.env` to configure your backend:
```env
API_BASE_URL=http://localhost:5000
API_TIMEOUT=30000
```

**Note:** For physical devices, replace `localhost` with your computer's IP address:
```env
API_BASE_URL=http://192.168.1.100:5000
```

### 4. Add Assets (Optional)

Add the following images to the `assets/` directory:
- `icon.png` (1024x1024) - App icon
- `splash.png` (2048x2048) - Splash screen
- `adaptive-icon.png` (1024x1024) - Android adaptive icon

You can use placeholder images for development.

## 🏃 Running the App

### Start the Backend First

Make sure the Flask backend is running:
```bash
cd ../backend
python app.py
```

The backend should be available at `http://localhost:5000`

### Start the Mobile App

```bash
# Start Expo development server
npm start
# or
npx expo start
```

This will open Expo DevTools in your browser.

### Run on Specific Platform

**iOS (macOS only):**
```bash
npm run ios
# or
npx expo start --ios
```

**Android:**
```bash
npm run android
# or
npx expo start --android
```

**Web (experimental):**
```bash
npm run web
# or
npx expo start --web
```

## 📱 Using Expo Go

1. Install **Expo Go** on your iOS or Android device
2. Scan the QR code from the terminal/browser
3. Make sure your device is on the same network as your computer
4. Update `.env` with your computer's IP address

## 🔧 Configuration

### API Endpoint

The app connects to the backend API. You can configure the endpoint in two ways:

1. **Environment Variable** (`.env` file):
```env
API_BASE_URL=http://192.168.1.100:5000
```

2. **In-App Settings** (Profile screen):
   - Navigate to Profile tab
   - Tap "API Configuration"
   - Enter new URL and tap "Update"

### Backend Requirements

The backend must expose the following endpoints:
- `POST /api/auth/login`
- `POST /api/auth/register`
- `GET /api/auth/me`
- `POST /api/auth/refresh`
- `GET /api/inventory`
- `GET /api/inventory/:id`
- `POST /api/inventory`
- `PUT /api/inventory/:id`
- `DELETE /api/inventory/:id`
- `POST /api/scraping/scrape`
- `GET /api/scraping/jobs`
- `GET /api/scraping/jobs/:id`
- `GET /api/stats`

## 📂 Project Structure

```
mobile/
├── App.tsx                 # Main app entry point
├── app.json               # Expo configuration
├── package.json           # Dependencies
├── tsconfig.json          # TypeScript config
├── babel.config.js        # Babel config
├── metro.config.js        # Metro bundler config
├── .env.example           # Environment variables template
├── README.md              # This file
├── assets/                # Images and icons
│   ├── icon.png
│   ├── splash.png
│   └── adaptive-icon.png
└── src/
    ├── api/               # API client and services
    │   ├── client.ts      # Axios instance with interceptors
    │   ├── auth.ts        # Authentication API
    │   ├── inventory.ts   # Inventory API
    │   ├── scraping.ts    # Scraping API
    │   └── stats.ts       # Statistics API
    ├── components/        # Reusable components
    │   ├── InventoryCard.tsx
    │   ├── StatsCard.tsx
    │   ├── ChartComponent.tsx
    │   ├── SearchBar.tsx
    │   ├── FilterModal.tsx
    │   └── LoadingSpinner.tsx
    ├── screens/           # Screen components
    │   ├── AuthScreens/
    │   │   ├── LoginScreen.tsx
    │   │   └── RegisterScreen.tsx
    │   └── MainScreens/
    │       ├── DashboardScreen.tsx
    │       ├── InventoryListScreen.tsx
    │       ├── InventoryDetailScreen.tsx
    │       ├── ScrapeScreen.tsx
    │       ├── ScrapingHistoryScreen.tsx
    │       └── ProfileScreen.tsx
    ├── navigation/        # Navigation setup
    │   ├── AppNavigator.tsx
    │   ├── AuthNavigator.tsx
    │   └── TabNavigator.tsx
    ├── contexts/          # React contexts
    │   └── AuthContext.tsx
    ├── utils/             # Utility functions
    │   ├── storage.ts     # AsyncStorage helpers
    │   ├── formatters.ts  # Formatting utilities
    │   └── validators.ts  # Validation schemas
    ├── types/             # TypeScript types
    │   └── index.ts
    └── constants/         # Constants and config
        ├── Colors.ts
        └── Config.ts
```

## 🎨 UI/UX Features

- **Material Design** - React Native Paper components
- **Bottom Tab Navigation** - Easy access to main features
- **Pull to Refresh** - Refresh data on all list screens
- **Infinite Scroll** - Pagination for large datasets
- **Loading States** - Spinners and skeleton screens
- **Error Handling** - User-friendly error messages with Snackbars
- **Form Validation** - Real-time validation with helpful messages
- **Dark Mode Ready** - Color scheme supports light/dark themes

## 🔐 Security

- **JWT Authentication** - Secure token-based auth
- **Token Refresh** - Automatic token refresh on expiration
- **Secure Storage** - AsyncStorage for sensitive data
- **API Interceptors** - Automatic auth header injection
- **Input Validation** - Client-side validation for all forms

## 🧪 Testing

```bash
# Type checking
npm run type-check

# Linting (if configured)
npm run lint
```

## 📦 Building for Production

For detailed deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md).

### Quick Build Commands

```bash
# Android preview (APK)
eas build --platform android --profile preview

# iOS preview (simulator build)
eas build --platform ios --profile preview

# Android production (for Google Play)
eas build --platform android --profile production

# iOS production (for App Store)
eas build --platform ios --profile production
```

**Note:** You need an Expo account and EAS CLI configured. See [Expo docs](https://docs.expo.dev/build/setup/) for setup.

**Important:** Before building for production:
1. Update `eas.json` with your production API URL
2. Replace placeholder assets (icon.png, splash.png)
3. Run `npm run type-check` and `npm run lint`
4. Review the [DEPLOYMENT.md](./DEPLOYMENT.md) guide

## 🐛 Troubleshooting

### "Network request failed"

- Check that the backend is running
- Verify the `API_BASE_URL` in `.env`
- For physical devices, use your computer's IP instead of `localhost`
- Ensure your device/emulator can reach the backend (same network)

### "Cannot connect to Metro bundler"

- Clear Metro cache: `npx expo start -c`
- Reset the app: Delete `node_modules` and reinstall
- Check firewall settings

### "Module not found" errors

```bash
# Clear cache and reinstall
rm -rf node_modules
npm install
npx expo start -c
```

### Authentication Issues

- Clear app data (Settings > Apps > Inventory Hub > Clear Data)
- Check backend logs for authentication errors
- Verify JWT tokens are being sent in headers

### Charts Not Displaying

- Ensure `react-native-svg` is installed
- Rebuild the app after installing new dependencies
- Check that data format matches expected structure

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly on both iOS and Android
5. Submit a pull request

## 📄 License

This project is part of the Inventory Hub application.

## 🆘 Support

For issues and questions:
- Check the [Backend README](../backend/README.md) for API documentation
- Review the [Architecture Guide](../ARCHITECTURE.md)
- Open an issue on the repository

## 🎯 Roadmap

- [ ] Offline mode with data sync
- [ ] Push notifications for scraping jobs
- [ ] Barcode scanning for inventory
- [ ] Export inventory to CSV/Excel
- [ ] Bulk edit operations
- [ ] Advanced filtering with saved presets
- [ ] Image upload for custom items
- [ ] Price history tracking
- [ ] Multi-language support

## 🙏 Acknowledgments

- **Expo** - For the amazing development platform
- **React Native Paper** - For beautiful Material Design components
- **React Navigation** - For seamless navigation
- **Formik & Yup** - For form management and validation

---

**Built with ❤️ using React Native and Expo**
