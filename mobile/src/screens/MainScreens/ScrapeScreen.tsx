import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, KeyboardAvoidingView, Platform } from 'react-native';
import { Text, TextInput, Button, Menu, Snackbar } from 'react-native-paper';
import { Formik } from 'formik';
import { scrapingApi } from '../../api/scraping';
import { scrapeValidationSchema } from '../../utils/validators';
import { Config } from '../../constants/Config';
import { Colors } from '../../constants/Colors';

export const ScrapeScreen: React.FC<{ navigation: any }> = ({ navigation }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [merchantMenuVisible, setMerchantMenuVisible] = useState(false);

  const handleScrape = async (values: { url: string; merchant: string; max_pages: number }) => {
    setLoading(true);
    setError('');
    setSuccess('');
    
    try {
      const response = await scrapingApi.startScrape({
        url: values.url,
        merchant: values.merchant,
        max_pages: values.max_pages,
      });
      
      setSuccess(response.message);
      
      // Navigate to history after a short delay
      setTimeout(() => {
        navigation.navigate('History');
      }, 2000);
    } catch (err: any) {
      setError(err.message || 'Failed to start scraping job');
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <Text style={styles.title}>Upload Inventory</Text>
          <Text style={styles.subtitle}>
            Enter a URL from a supported marketplace to upload product listings.
          </Text>
        </View>

        <Formik
          initialValues={{
            url: '',
            merchant: Config.MERCHANTS[0],
            max_pages: Config.DEFAULT_SCRAPING_PAGES,
          }}
          validationSchema={scrapeValidationSchema}
          onSubmit={handleScrape}
        >
          {({ handleChange, handleBlur, handleSubmit, values, errors, touched, setFieldValue }) => (
            <View style={styles.form}>
              <TextInput
                label="URL *"
                value={values.url}
                onChangeText={handleChange('url')}
                onBlur={handleBlur('url')}
                error={touched.url && !!errors.url}
                mode="outlined"
                style={styles.input}
                placeholder="https://www.mercari.com/search/?keyword=vintage"
                autoCapitalize="none"
                keyboardType="url"
                disabled={loading}
              />
              {touched.url && errors.url && (
                <Text style={styles.errorText}>{errors.url}</Text>
              )}

              <Menu
                visible={merchantMenuVisible}
                onDismiss={() => setMerchantMenuVisible(false)}
                anchor={
                  <TextInput
                    label="Merchant *"
                    value={values.merchant}
                    mode="outlined"
                    style={styles.input}
                    editable={false}
                    right={<TextInput.Icon icon="chevron-down" onPress={() => setMerchantMenuVisible(true)} />}
                    onPressIn={() => setMerchantMenuVisible(true)}
                  />
                }
              >
                {Config.MERCHANTS.map((merchant) => (
                  <Menu.Item
                    key={merchant}
                    onPress={() => {
                      setFieldValue('merchant', merchant);
                      setMerchantMenuVisible(false);
                    }}
                    title={merchant}
                  />
                ))}
              </Menu>
              {touched.merchant && errors.merchant && (
                <Text style={styles.errorText}>{errors.merchant}</Text>
              )}

              <TextInput
                label="Maximum Pages"
                value={values.max_pages.toString()}
                onChangeText={(text) => setFieldValue('max_pages', parseInt(text) || 1)}
                onBlur={handleBlur('max_pages')}
                error={touched.max_pages && !!errors.max_pages}
                mode="outlined"
                keyboardType="number-pad"
                style={styles.input}
                disabled={loading}
              />
              {touched.max_pages && errors.max_pages && (
                <Text style={styles.errorText}>{errors.max_pages}</Text>
              )}
              <Text style={styles.helperText}>
                Max {Config.MAX_SCRAPING_PAGES} pages. More pages = longer upload time.
              </Text>

              <View style={styles.infoBox}>
                <Text style={styles.infoTitle}>Supported Merchants:</Text>
                <Text style={styles.infoText}>
                  • Mercari - Search results and product pages{'\n'}
                  • Depop - Search results and product pages{'\n'}
                  • Generic - Most e-commerce sites (experimental)
                </Text>
              </View>

              <Button
                mode="contained"
                onPress={() => handleSubmit()}
                loading={loading}
                disabled={loading}
                style={styles.button}
                icon="play"
              >
                Start Upload
              </Button>

              <Button
                mode="text"
                onPress={() => navigation.navigate('History')}
                disabled={loading}
                style={styles.linkButton}
              >
                View Upload History
              </Button>
            </View>
          )}
        </Formik>

        <View style={styles.tipsBox}>
          <Text style={styles.tipsTitle}>💡 Tips:</Text>
          <Text style={styles.tipsText}>
            • Use search result pages for best results{'\n'}
            • Start with 1-2 pages to test{'\n'}
            • Check upload history for job status{'\n'}
            • Failed jobs may indicate unsupported site structure
          </Text>
        </View>
      </ScrollView>

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
        duration={4000}
        style={{ backgroundColor: Colors.success }}
      >
        {success}
      </Snackbar>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  scrollContent: {
    padding: 20,
  },
  header: {
    marginBottom: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: Colors.primary,
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 14,
    color: Colors.placeholder,
  },
  form: {
    width: '100%',
  },
  input: {
    marginBottom: 8,
  },
  errorText: {
    color: Colors.error,
    fontSize: 12,
    marginBottom: 8,
    marginLeft: 12,
  },
  helperText: {
    fontSize: 12,
    color: Colors.placeholder,
    marginBottom: 16,
    marginLeft: 12,
  },
  infoBox: {
    backgroundColor: Colors.primary + '10',
    padding: 16,
    borderRadius: 8,
    marginBottom: 16,
  },
  infoTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: Colors.primary,
    marginBottom: 8,
  },
  infoText: {
    fontSize: 12,
    color: Colors.onSurface,
    lineHeight: 18,
  },
  button: {
    marginTop: 8,
    marginBottom: 8,
  },
  linkButton: {
    marginTop: 8,
  },
  tipsBox: {
    backgroundColor: Colors.info + '10',
    padding: 16,
    borderRadius: 8,
    marginTop: 24,
  },
  tipsTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: Colors.info,
    marginBottom: 8,
  },
  tipsText: {
    fontSize: 12,
    color: Colors.onSurface,
    lineHeight: 18,
  },
});
