import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import MaterialCommunityIcons from '@expo/vector-icons/MaterialCommunityIcons';
import { DashboardScreen } from '../screens/MainScreens/DashboardScreen';
import { InventoryListScreen } from '../screens/MainScreens/InventoryListScreen';
import { InventoryDetailScreen } from '../screens/MainScreens/InventoryDetailScreen';
import { ScrapeScreen } from '../screens/MainScreens/ScrapeScreen';
import { ScrapingHistoryScreen } from '../screens/MainScreens/ScrapingHistoryScreen';
import { ProfileScreen } from '../screens/MainScreens/ProfileScreen';
import { MainTabParamList, InventoryStackParamList } from '../types';
import { Colors } from '../constants/Colors';

const Tab = createBottomTabNavigator<MainTabParamList>();
const InventoryStack = createStackNavigator<InventoryStackParamList>();

const InventoryNavigator = () => {
  return (
    <InventoryStack.Navigator>
      <InventoryStack.Screen
        name="InventoryList"
        component={InventoryListScreen}
        options={{ title: 'Inventory' }}
      />
      <InventoryStack.Screen
        name="InventoryDetail"
        component={InventoryDetailScreen}
        options={{ title: 'Item Details' }}
      />
    </InventoryStack.Navigator>
  );
};

export const TabNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: Colors.primary,
        tabBarInactiveTintColor: Colors.placeholder,
        tabBarStyle: {
          backgroundColor: Colors.surface,
          borderTopColor: Colors.disabled,
        },
        headerStyle: {
          backgroundColor: Colors.primary,
        },
        headerTintColor: Colors.onPrimary,
      }}
    >
      <Tab.Screen
        name="Dashboard"
        component={DashboardScreen}
        options={{
          title: 'Dashboard',
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons name="view-dashboard" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Inventory"
        component={InventoryNavigator}
        options={{
          title: 'Inventory',
          headerShown: false,
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons name="package-variant" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Scrape"
        component={ScrapeScreen}
        options={{
          title: 'Upload',
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons name="upload" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="History"
        component={ScrapingHistoryScreen}
        options={{
          title: 'History',
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons name="history" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{
          title: 'Profile',
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons name="account" size={size} color={color} />
          ),
        }}
      />
    </Tab.Navigator>
  );
};
