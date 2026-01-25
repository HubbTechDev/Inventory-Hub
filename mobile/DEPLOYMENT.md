# Mobile App Deployment Guide

This guide provides step-by-step instructions for deploying the Inventory Hub mobile application to production.

## Prerequisites

Before deploying, ensure you have:

- ✅ **Node.js** 18.x or higher
- ✅ **npm** or **yarn**
- ✅ **Expo CLI** (installed via npx)
- ✅ **Expo Account** ([signup here](https://expo.dev/signup))
- ✅ **EAS CLI** (`npm install -g eas-cli`)

## Pre-Deployment Checklist

### 1. Environment Configuration

- [ ] Update `mobile/.env` with production API URL
  ```env
  API_BASE_URL=https://your-production-api.com
  API_TIMEOUT=30000
  ```

- [ ] Verify API is accessible via HTTPS (required for production)
- [ ] Test API endpoints with production credentials

### 2. Assets

- [ ] Replace placeholder assets with branded images:
  - `mobile/assets/icon.png` (1024x1024 px)
  - `mobile/assets/splash.png` (2048x2048 px)
  - `mobile/assets/adaptive-icon.png` (1024x1024 px)

### 3. Configuration Files

- [ ] Update `mobile/eas.json` production environment:
  ```json
  {
    "build": {
      "production": {
        "env": {
          "API_BASE_URL": "https://your-production-api.com"
        }
      }
    }
  }
  ```

- [ ] Update `mobile/app.json` with correct package identifiers:
  - iOS: `expo.ios.bundleIdentifier`
  - Android: `expo.android.package`

### 4. Code Quality

Run the following commands to ensure code quality:

```bash
cd mobile

# TypeScript type checking
npm run type-check

# ESLint
npm run lint

# Both should pass without errors
```

### 5. Security Review

- [ ] All sensitive data stored securely
- [ ] No hardcoded credentials in source code
- [ ] HTTPS enforced for all API calls
- [ ] Review npm audit report (note: some vulnerabilities in dev dependencies are acceptable)

## Building for Production

### Setup EAS

1. **Login to Expo**
   ```bash
   eas login
   ```

2. **Configure the project**
   ```bash
   cd mobile
   eas build:configure
   ```

### Build for Android

1. **Create production build**
   ```bash
   eas build --platform android --profile production
   ```

2. **Download the APK/AAB**
   - APK: For direct distribution or testing
   - AAB: Required for Google Play Store submission

3. **Submit to Google Play Store** (optional)
   ```bash
   eas submit --platform android
   ```

### Build for iOS

1. **Create production build**
   ```bash
   eas build --platform ios --profile production
   ```

2. **Submit to App Store** (optional)
   ```bash
   eas submit --platform ios
   ```

**Note:** iOS builds require an Apple Developer account ($99/year)

## Testing the Build

### Preview Build (Recommended)

Before creating a production build, create a preview build for testing:

```bash
# Android preview (APK)
eas build --platform android --profile preview

# iOS preview (simulator build)
eas build --platform ios --profile preview
```

### Install Preview Build

1. Download the build from EAS dashboard
2. Install on test device:
   - **Android:** Transfer APK and install
   - **iOS:** Use TestFlight or simulator

3. Test all features:
   - [ ] Login/Register
   - [ ] Dashboard loads
   - [ ] Inventory list and details
   - [ ] Scraping functionality
   - [ ] Profile and settings

## Deployment Profiles

The app has three build profiles configured in `eas.json`:

### Development
- For development with Expo Go
- Includes development tools
- Fast builds

### Preview
- For internal testing
- Creates installable APK (Android)
- Creates simulator build (iOS)

### Production
- For App Store/Play Store submission
- Optimized and minified
- Production environment variables
- Auto-incremented version numbers

## Environment Variables

The app uses the following environment variables:

| Variable | Description | Default | Production |
|----------|-------------|---------|------------|
| `API_BASE_URL` | Backend API URL | `http://localhost:5000` | `https://your-api.com` |
| `API_TIMEOUT` | Request timeout (ms) | `30000` | `30000` |

## Post-Deployment

### Monitor the App

1. **Check crash reports** in Expo dashboard
2. **Monitor API logs** for errors
3. **Review user feedback** from stores
4. **Track analytics** (if implemented)

### Update Process

To release an update:

1. Make changes in the codebase
2. Run quality checks (type-check, lint)
3. Test locally with `expo start`
4. Build new version with EAS
5. Submit to stores (or use OTA updates for minor changes)

### Over-The-Air (OTA) Updates

For JavaScript-only changes, use OTA updates:

```bash
eas update --branch production
```

**Note:** OTA updates don't require app store approval but only work for JavaScript changes, not native code.

## Troubleshooting

### Build Fails

- Check EAS build logs in the dashboard
- Verify all dependencies are compatible
- Ensure `package.json` and `package-lock.json` are committed

### App Crashes on Startup

- Check environment variables in `eas.json`
- Verify API URL is accessible
- Review crash logs in Expo dashboard

### "Network request failed"

- Verify API_BASE_URL is correct
- Check that API is accessible from the internet
- Ensure HTTPS is used for production

### Asset Loading Issues

- Verify asset files exist and are properly sized
- Check `app.json` asset paths are correct
- Clear Metro cache: `npx expo start -c`

## Security Considerations

### Production Security Checklist

- [ ] API uses HTTPS only
- [ ] No console.log statements in production code (already removed)
- [ ] No hardcoded API keys or secrets
- [ ] JWT tokens stored securely in AsyncStorage
- [ ] Proper error handling (no sensitive data in error messages)
- [ ] API endpoints have proper authentication/authorization

### Future Security Improvements

For enhanced security in future versions, consider:

1. **Migrate to expo-secure-store** for token storage
2. **Implement certificate pinning** for API requests
3. **Add biometric authentication** (Face ID/Touch ID)
4. **Enable code obfuscation** in production builds

## Support and Resources

- **Expo Documentation:** https://docs.expo.dev/
- **EAS Build Docs:** https://docs.expo.dev/build/introduction/
- **React Native Docs:** https://reactnative.dev/docs/getting-started
- **Project README:** See `mobile/README.md` for development setup

## Version History

- **v1.0.0** (Initial Release)
  - Authentication system
  - Inventory management
  - Web scraping functionality
  - Dashboard with analytics

---

**For questions or issues with deployment, please contact the development team or open an issue in the repository.**
