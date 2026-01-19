#!/bin/bash
# Verification script to ensure all required files exist

echo "🔍 Verifying Inventory Hub Mobile App Structure..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Counter
MISSING=0

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
    else
        echo -e "${RED}✗${NC} $1"
        ((MISSING++))
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
    else
        echo -e "${RED}✗${NC} $1/"
        ((MISSING++))
    fi
}

echo "Configuration Files:"
check_file "package.json"
check_file "app.json"
check_file "tsconfig.json"
check_file "babel.config.js"
check_file "metro.config.js"
check_file ".env.example"
check_file ".gitignore"

echo ""
echo "Documentation:"
check_file "README.md"
check_file "QUICKSTART.md"
check_file "SUMMARY.md"

echo ""
echo "Main App:"
check_file "App.tsx"

echo ""
echo "API Layer:"
check_file "src/api/client.ts"
check_file "src/api/auth.ts"
check_file "src/api/inventory.ts"
check_file "src/api/scraping.ts"
check_file "src/api/stats.ts"

echo ""
echo "Components:"
check_file "src/components/InventoryCard.tsx"
check_file "src/components/StatsCard.tsx"
check_file "src/components/ChartComponent.tsx"
check_file "src/components/SearchBar.tsx"
check_file "src/components/FilterModal.tsx"
check_file "src/components/LoadingSpinner.tsx"

echo ""
echo "Auth Screens:"
check_file "src/screens/AuthScreens/LoginScreen.tsx"
check_file "src/screens/AuthScreens/RegisterScreen.tsx"

echo ""
echo "Main Screens:"
check_file "src/screens/MainScreens/DashboardScreen.tsx"
check_file "src/screens/MainScreens/InventoryListScreen.tsx"
check_file "src/screens/MainScreens/InventoryDetailScreen.tsx"
check_file "src/screens/MainScreens/ScrapeScreen.tsx"
check_file "src/screens/MainScreens/ScrapingHistoryScreen.tsx"
check_file "src/screens/MainScreens/ProfileScreen.tsx"

echo ""
echo "Navigation:"
check_file "src/navigation/AppNavigator.tsx"
check_file "src/navigation/AuthNavigator.tsx"
check_file "src/navigation/TabNavigator.tsx"

echo ""
echo "Contexts:"
check_file "src/contexts/AuthContext.tsx"

echo ""
echo "Utils:"
check_file "src/utils/storage.ts"
check_file "src/utils/formatters.ts"
check_file "src/utils/validators.ts"

echo ""
echo "Types:"
check_file "src/types/index.ts"

echo ""
echo "Constants:"
check_file "src/constants/Colors.ts"
check_file "src/constants/Config.ts"

echo ""
echo "Assets:"
check_dir "assets"
check_file "assets/icon.png"
check_file "assets/splash.png"
check_file "assets/adaptive-icon.png"

echo ""
echo "================================================"
if [ $MISSING -eq 0 ]; then
    echo -e "${GREEN}✅ All files present! Structure is complete.${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. cd mobile"
    echo "  2. npm install"
    echo "  3. cp .env.example .env"
    echo "  4. npm start"
else
    echo -e "${RED}❌ Missing $MISSING file(s)!${NC}"
    exit 1
fi
