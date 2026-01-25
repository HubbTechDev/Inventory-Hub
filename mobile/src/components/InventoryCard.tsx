import React from 'react';
import { View, StyleSheet, Image, Pressable } from 'react-native';
import { Card, Text, Chip, IconButton } from 'react-native-paper';
import { InventoryItem } from '../types';
import { formatCurrency } from '../utils/formatters';
import { Colors, Theme } from '../constants/Colors';

interface InventoryCardProps {
  item: InventoryItem;
  onPress: (item: InventoryItem) => void;
  onDelete?: (id: number) => void;
}

export const InventoryCard: React.FC<InventoryCardProps> = ({ item, onPress, onDelete }) => {
  return (
    <Pressable onPress={() => onPress(item)}>
      <Card style={styles.card} mode="elevated">
        <Card.Content style={styles.content}>
          <View style={styles.row}>
            {item.image_url ? (
              <Image source={{ uri: item.image_url }} style={styles.image} />
            ) : (
              <View style={[styles.image, styles.noImage]}>
                <Text style={styles.noImageText}>📦</Text>
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
                <Chip mode="outlined" compact style={styles.chip} textStyle={styles.chipText}>
                  {item.merchant}
                </Chip>
                {item.condition && (
                  <Chip mode="outlined" compact style={styles.chip} textStyle={styles.chipText}>
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
                    { backgroundColor: item.in_stock ? Colors.success + '15' : Colors.error + '15' },
                  ]}
                  textStyle={{ 
                    color: item.in_stock ? Colors.success : Colors.error,
                    fontSize: 12,
                    fontWeight: '600',
                  }}
                >
                  {item.in_stock ? 'In Stock' : 'Out of Stock'}
                </Chip>
                
                <Text style={styles.quantity}>Qty: {item.quantity}</Text>
              </View>
            </View>
            
            {onDelete && (
              <IconButton
                icon="delete"
                size={22}
                iconColor={Colors.error}
                onPress={() => onDelete(item.id)}
                style={styles.deleteButton}
              />
            )}
          </View>
        </Card.Content>
      </Card>
    </Pressable>
  );
};

const styles = StyleSheet.create({
  card: {
    marginVertical: 8,
    marginHorizontal: 20,
    backgroundColor: Colors.surface,
    borderRadius: 16,
    ...Theme.shadows.medium,
  },
  content: {
    padding: 16,
  },
  row: {
    flexDirection: 'row',
    gap: 14,
  },
  image: {
    width: 88,
    height: 88,
    borderRadius: 12,
    backgroundColor: Colors.backgroundAlt,
  },
  noImage: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  noImageText: {
    fontSize: 32,
    opacity: 0.5,
  },
  details: {
    flex: 1,
    gap: 8,
  },
  title: {
    fontSize: 16,
    fontWeight: '700',
    color: Colors.textPrimary,
    lineHeight: 22,
  },
  price: {
    fontSize: 20,
    fontWeight: '800',
    color: Colors.primary,
    letterSpacing: -0.3,
  },
  chips: {
    flexDirection: 'row',
    gap: 8,
    flexWrap: 'wrap',
  },
  chip: {
    height: 26,
    borderColor: Colors.border,
  },
  chipText: {
    fontSize: 12,
    fontWeight: '500',
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 4,
  },
  stockChip: {
    height: 26,
    borderWidth: 0,
  },
  quantity: {
    fontSize: 13,
    fontWeight: '600',
    color: Colors.textSecondary,
  },
  deleteButton: {
    margin: 0,
  },
});
