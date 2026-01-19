import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { Provider as PaperProvider } from 'react-native-paper';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { AuthProvider } from './src/contexts/AuthContext';
import { AppNavigator } from './src/navigation/AppNavigator';
import { Colors } from './src/constants/Colors';

const theme = {
  colors: {
    primary: Colors.primary,
    accent: Colors.secondary,
    background: Colors.background,
    surface: Colors.surface,
    error: Colors.error,
    text: Colors.onSurface,
    onSurface: Colors.onSurface,
    disabled: Colors.disabled,
    placeholder: Colors.placeholder,
    backdrop: Colors.backdrop,
    notification: Colors.primary,
  },
  roundness: 8,
};

export default function App() {
  return (
    <SafeAreaProvider>
      <PaperProvider theme={theme}>
        <AuthProvider>
          <AppNavigator />
          <StatusBar style="auto" />
        </AuthProvider>
      </PaperProvider>
    </SafeAreaProvider>
  );
}
