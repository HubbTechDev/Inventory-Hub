import React from 'react';
import { View, StyleSheet, Image } from 'react-native';
import { Card, Text, Chip, IconButton } from 'react-native-paper';
import { InventoryItem } from '../types';
import { formatCurrency } from '../utils/formatters';
import { Colors } from '../constants/Colors';

interface InventoryCardProps {
  item: InventoryItem;
  onPress: (item: InventoryItem) => void;
  onDelete?: (id: number) => void;
}

export const InventoryCard: React.FC<InventoryCardProps> = ({ item, onPress, onDelete }) => {
  return (
    <Card style={styles.card} onPress={() => onPress(item)}>
      <Card.Content style={styles.content}>
        <View style={styles.row}>
          {item.image_url ? (
            <Image source={{ uri: item.image_url }} style={styles.image} />
          ) : (
            <View style={[styles.image, styles.noImage]}>
              <Text style={styles.noImageText}>No Image</Text>
            </View>
          )}
          
          <View style={styles.details}>
            <Text style={styles.title} numberOfLines={2}>
              {item.title}
            </Text>
            
            <Text style={styles.price}>
              {formatCurrency(item.price, item.currency)}
            </Text>
            
            <View style={styles.chips}>
              <Chip mode="outlined" compact style={styles.chip}>
                {item.merchant}
              </Chip>
              {item.condition && (
                <Chip mode="outlined" compact style={styles.chip}>
                  {item.condition}
                </Chip>
              )}
            </View>
            
            <View style={styles.footer}>
              <Chip
                icon={item.in_stock ? 'check-circle' : 'close-circle'}
                compact
                style={[
                  styles.stockChip,
                  { backgroundColor: item.in_stock ? Colors.success + '20' : Colors.error + '20' },
                ]}
                textStyle={{ color: item.in_stock ? Colors.success : Colors.error }}
              >
                {item.in_stock ? 'In Stock' : 'Out of Stock'}
              </Chip>
              
              <Text style={styles.quantity}>Qty: {item.quantity}</Text>
            </View>
          </View>
          
          {onDelete && (
            <IconButton
              icon="delete"
              size={20}
              iconColor={Colors.error}
              onPress={() => onDelete(item.id)}
            />
          )}
        </View>
      </Card.Content>
    </Card>
  );
};

const styles = StyleSheet.create({
  card: {
    marginVertical: 8,
    marginHorizontal: 16,
    elevation: 2,
  },
  content: {
    padding: 12,
  },
  row: {
    flexDirection: 'row',
    gap: 12,
  },
  image: {
    width: 80,
    height: 80,
    borderRadius: 8,
    backgroundColor: Colors.disabled,
  },
  noImage: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  noImageText: {
    fontSize: 10,
    color: Colors.placeholder,
  },
  details: {
    flex: 1,
    gap: 6,
  },
  title: {
    fontSize: 16,
    fontWeight: 'bold',
    color: Colors.onSurface,
  },
  price: {
    fontSize: 18,
    fontWeight: '600',
    color: Colors.primary,
  },
  chips: {
    flexDirection: 'row',
    gap: 6,
    flexWrap: 'wrap',
  },
  chip: {
    height: 24,
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 4,
  },
  stockChip: {
    height: 24,
  },
  quantity: {
    fontSize: 12,
    color: Colors.placeholder,
  },
});
