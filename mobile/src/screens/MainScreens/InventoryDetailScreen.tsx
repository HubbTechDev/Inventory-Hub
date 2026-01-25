import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, Image } from 'react-native';
import { Text, Button, Chip, Divider, Snackbar } from 'react-native-paper';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { inventoryApi } from '../../api/inventory';
import { InventoryItem } from '../../types';
import { formatCurrency, formatDateTime } from '../../utils/formatters';
import { Colors } from '../../constants/Colors';

export const InventoryDetailScreen: React.FC<{ route: any; navigation: any }> = ({
  route,
  navigation,
}) => {
  const { itemId } = route.params;
  const [item, setItem] = useState<InventoryItem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchItem = async () => {
      try {
        setLoading(true);
        const data = await inventoryApi.getItem(itemId);
        setItem(data);
        setError('');
      } catch (err: any) {
        setError(err.message || 'Failed to load item');
      } finally {
        setLoading(false);
      }
    };
    
    fetchItem();
  }, [itemId]);

  const handleDelete = async () => {
    try {
      await inventoryApi.deleteItem(itemId);
      navigation.goBack();
    } catch (err: any) {
      setError(err.message || 'Failed to delete item');
    }
  };

  if (loading) {
    return <LoadingSpinner message="Loading item details..." />;
  }

  if (!item) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Item not found</Text>
        <Button mode="contained" onPress={() => navigation.goBack()}>
          Go Back
        </Button>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {item.image_url && (
        <Image source={{ uri: item.image_url }} style={styles.image} resizeMode="cover" />
      )}

      <View style={styles.content}>
        <Text style={styles.title}>{item.title}</Text>
        
        <Text style={styles.price}>{formatCurrency(item.price, item.currency)}</Text>

        <View style={styles.chips}>
          <Chip icon="store" mode="outlined" style={styles.chip}>
            {item.merchant}
          </Chip>
          
          {item.condition && (
            <Chip icon="tag" mode="outlined" style={styles.chip}>
              {item.condition}
            </Chip>
          )}
          
          <Chip
            icon={item.in_stock ? 'check-circle' : 'close-circle'}
            mode="outlined"
            style={[
              styles.chip,
              { backgroundColor: item.in_stock ? Colors.success + '20' : Colors.error + '20' },
            ]}
            textStyle={{ color: item.in_stock ? Colors.success : Colors.error }}
          >
            {item.in_stock ? 'In Stock' : 'Out of Stock'}
          </Chip>
        </View>

        <Divider style={styles.divider} />

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Details</Text>
          
          <View style={styles.row}>
            <Text style={styles.label}>SKU:</Text>
            <Text style={styles.value}>{item.sku}</Text>
          </View>
          
          <View style={styles.row}>
            <Text style={styles.label}>Quantity:</Text>
            <Text style={styles.value}>{item.quantity}</Text>
          </View>
          
          {item.brand && (
            <View style={styles.row}>
              <Text style={styles.label}>Brand:</Text>
              <Text style={styles.value}>{item.brand}</Text>
            </View>
          )}
          
          {item.category && (
            <View style={styles.row}>
              <Text style={styles.label}>Category:</Text>
              <Text style={styles.value}>{item.category}</Text>
            </View>
          )}
        </View>

        {item.description && (
          <>
            <Divider style={styles.divider} />
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Description</Text>
              <Text style={styles.description}>{item.description}</Text>
            </View>
          </>
        )}

        {item.custom_fields && Object.keys(item.custom_fields).length > 0 && (
          <>
            <Divider style={styles.divider} />
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Additional Information</Text>
              {Object.entries(item.custom_fields).map(([key, value]) => (
                <View key={key} style={styles.row}>
                  <Text style={styles.label}>{key}:</Text>
                  <Text style={styles.value}>{String(value)}</Text>
                </View>
              ))}
            </View>
          </>
        )}

        <Divider style={styles.divider} />

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Metadata</Text>
          
          <View style={styles.row}>
            <Text style={styles.label}>Created:</Text>
            <Text style={styles.value}>{formatDateTime(item.created_at)}</Text>
          </View>
          
          <View style={styles.row}>
            <Text style={styles.label}>Updated:</Text>
            <Text style={styles.value}>{formatDateTime(item.updated_at)}</Text>
          </View>
          
          {item.scraped_at && (
            <View style={styles.row}>
              <Text style={styles.label}>Uploaded:</Text>
              <Text style={styles.value}>{formatDateTime(item.scraped_at)}</Text>
            </View>
          )}
        </View>

        {item.product_url && (
          <Button
            mode="outlined"
            icon="open-in-new"
            onPress={() => {}}
            style={styles.button}
          >
            View Original Listing
          </Button>
        )}

        <Button
          mode="contained"
          buttonColor={Colors.error}
          onPress={handleDelete}
          style={styles.button}
        >
          Delete Item
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
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  image: {
    width: '100%',
    height: 320,
    backgroundColor: Colors.backgroundAlt,
  },
  content: {
    padding: 20,
  },
  title: {
    fontSize: 26,
    fontWeight: '800',
    color: Colors.textPrimary,
    marginBottom: 12,
    lineHeight: 34,
    letterSpacing: -0.5,
  },
  price: {
    fontSize: 32,
    fontWeight: '800',
    color: Colors.primary,
    marginBottom: 16,
    letterSpacing: -0.5,
  },
  chips: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 10,
    marginBottom: 20,
  },
  chip: {
    marginRight: 0,
  },
  divider: {
    marginVertical: 20,
    backgroundColor: Colors.border,
  },
  section: {
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: Colors.textPrimary,
    marginBottom: 16,
    letterSpacing: -0.3,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
    alignItems: 'flex-start',
  },
  label: {
    fontSize: 15,
    color: Colors.textSecondary,
    fontWeight: '600',
  },
  value: {
    fontSize: 15,
    color: Colors.textPrimary,
    fontWeight: '500',
    textAlign: 'right',
    flex: 1,
    marginLeft: 16,
  },
  description: {
    fontSize: 15,
    color: Colors.textPrimary,
    lineHeight: 24,
  },
  button: {
    marginVertical: 8,
    borderRadius: 12,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
    backgroundColor: Colors.background,
  },
  errorText: {
    fontSize: 16,
    fontWeight: '600',
    color: Colors.error,
    marginBottom: 20,
    textAlign: 'center',
  },
});
