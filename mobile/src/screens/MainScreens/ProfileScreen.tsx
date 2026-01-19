import React, { useState } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, Button, Divider, TextInput, Snackbar, Avatar, List } from 'react-native-paper';
import { useAuth } from '../../contexts/AuthContext';
import { setApiBaseUrl, getApiBaseUrl } from '../../api/client';
import Config from '../../constants/Config';
import { Colors } from '../../constants/Colors';
import { formatDateTime } from '../../utils/formatters';

export const ProfileScreen: React.FC<{ navigation: any }> = ({ navigation }) => {
  const { user, logout } = useAuth();
  const [apiUrl, setApiUrl] = useState(getApiBaseUrl());
  const [showApiSettings, setShowApiSettings] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loggingOut, setLoggingOut] = useState(false);

  const handleLogout = async () => {
    setLoggingOut(true);
    try {
      await logout();
    } catch (err: any) {
      setError(err.message || 'Failed to logout');
      setLoggingOut(false);
    }
  };

  const handleUpdateApiUrl = () => {
    try {
      setApiBaseUrl(apiUrl);
      setSuccess('API URL updated successfully');
      setShowApiSettings(false);
    } catch (err: any) {
      setError('Failed to update API URL');
    }
  };

  const handleResetApiUrl = () => {
    const defaultUrl = Config.API_BASE_URL;
    setApiUrl(defaultUrl);
    setApiBaseUrl(defaultUrl);
    setSuccess('API URL reset to default');
  };

  if (!user) {
    return null;
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Avatar.Text
          size={80}
          label={user.username.substring(0, 2).toUpperCase()}
          style={styles.avatar}
        />
        <Text style={styles.username}>{user.username}</Text>
        <Text style={styles.email}>{user.email}</Text>
        <Text style={styles.memberSince}>
          Member since {formatDateTime(user.created_at)}
        </Text>
      </View>

      <Divider style={styles.divider} />

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Account</Text>
        
        <List.Item
          title="User ID"
          description={user.id.toString()}
          left={(props) => <List.Icon {...props} icon="account" />}
        />
        
        <List.Item
          title="Email"
          description={user.email}
          left={(props) => <List.Icon {...props} icon="email" />}
        />
        
        <List.Item
          title="Username"
          description={user.username}
          left={(props) => <List.Icon {...props} icon="account-circle" />}
        />
      </View>

      <Divider style={styles.divider} />

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Settings</Text>
        
        <List.Item
          title="API Configuration"
          description={showApiSettings ? 'Hide settings' : 'Configure backend URL'}
          left={(props) => <List.Icon {...props} icon="server" />}
          right={(props) => (
            <List.Icon {...props} icon={showApiSettings ? 'chevron-up' : 'chevron-down'} />
          )}
          onPress={() => setShowApiSettings(!showApiSettings)}
        />

        {showApiSettings && (
          <View style={styles.apiSettings}>
            <TextInput
              label="API Base URL"
              value={apiUrl}
              onChangeText={setApiUrl}
              mode="outlined"
              style={styles.input}
              autoCapitalize="none"
              placeholder="http://localhost:5000"
            />
            
            <View style={styles.buttonRow}>
              <Button mode="outlined" onPress={handleResetApiUrl} style={styles.halfButton}>
                Reset
              </Button>
              <Button mode="contained" onPress={handleUpdateApiUrl} style={styles.halfButton}>
                Update
              </Button>
            </View>
            
            <Text style={styles.helperText}>
              Current URL: {getApiBaseUrl()}
            </Text>
          </View>
        )}
        
        <List.Item
          title="App Version"
          description="1.0.0"
          left={(props) => <List.Icon {...props} icon="information" />}
        />
      </View>

      <Divider style={styles.divider} />

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>About</Text>
        
        <Text style={styles.aboutText}>
          Inventory Hub is a powerful mobile application for managing your e-commerce inventory
          across multiple platforms. Track items, scrape marketplaces, and analyze your inventory
          with ease.
        </Text>
      </View>

      <View style={styles.logoutSection}>
        <Button
          mode="contained"
          onPress={handleLogout}
          loading={loggingOut}
          disabled={loggingOut}
          buttonColor={Colors.error}
          icon="logout"
          style={styles.logoutButton}
        >
          Logout
        </Button>
      </View>

      <Snackbar
        visible={!!error}
        onDismiss={() => setError('')}
        duration={4000}
        action={{
          label: 'Dismiss',
          onPress: () => setError(''),
        }}
      >
        {error}
      </Snackbar>

      <Snackbar
        visible={!!success}
        onDismiss={() => setSuccess('')}
        duration={3000}
        style={{ backgroundColor: Colors.success }}
      >
        {success}
      </Snackbar>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  header: {
    alignItems: 'center',
    paddingVertical: 32,
    paddingHorizontal: 16,
  },
  avatar: {
    backgroundColor: Colors.primary,
    marginBottom: 16,
  },
  username: {
    fontSize: 24,
    fontWeight: 'bold',
    color: Colors.onSurface,
    marginBottom: 4,
  },
  email: {
    fontSize: 16,
    color: Colors.placeholder,
    marginBottom: 8,
  },
  memberSince: {
    fontSize: 12,
    color: Colors.placeholder,
  },
  divider: {
    marginVertical: 8,
  },
  section: {
    paddingVertical: 16,
    paddingHorizontal: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: Colors.onSurface,
    marginBottom: 12,
  },
  apiSettings: {
    paddingLeft: 16,
    paddingRight: 16,
    paddingTop: 8,
    paddingBottom: 16,
  },
  input: {
    marginBottom: 12,
  },
  buttonRow: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 8,
  },
  halfButton: {
    flex: 1,
  },
  helperText: {
    fontSize: 12,
    color: Colors.placeholder,
    marginLeft: 4,
  },
  aboutText: {
    fontSize: 14,
    color: Colors.onSurface,
    lineHeight: 20,
  },
  logoutSection: {
    padding: 16,
    paddingBottom: 32,
  },
  logoutButton: {
    marginTop: 8,
  },
});
