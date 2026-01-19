import React, { useState } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Modal, Portal, Text, Button, Chip, Divider } from 'react-native-paper';
import { InventoryFilters } from '../types';
import { Config } from '../constants/Config';
import { Colors } from '../constants/Colors';

interface FilterModalProps {
  visible: boolean;
  onDismiss: () => void;
  onApply: (filters: InventoryFilters) => void;
  initialFilters?: InventoryFilters;
}

export const FilterModal: React.FC<FilterModalProps> = ({
  visible,
  onDismiss,
  onApply,
  initialFilters,
}) => {
  const [selectedMerchant, setSelectedMerchant] = useState<string | undefined>(
    initialFilters?.merchant
  );
  const [selectedCondition, setSelectedCondition] = useState<string | undefined>(
    initialFilters?.condition
  );
  const [inStock, setInStock] = useState<boolean | undefined>(initialFilters?.in_stock);

  const handleApply = () => {
    const filters: InventoryFilters = {};
    if (selectedMerchant) filters.merchant = selectedMerchant;
    if (selectedCondition) filters.condition = selectedCondition;
    if (inStock !== undefined) filters.in_stock = inStock;
    
    onApply(filters);
    onDismiss();
  };

  const handleClear = () => {
    setSelectedMerchant(undefined);
    setSelectedCondition(undefined);
    setInStock(undefined);
  };

  return (
    <Portal>
      <Modal
        visible={visible}
        onDismiss={onDismiss}
        contentContainerStyle={styles.modal}
      >
        <ScrollView>
          <Text style={styles.title}>Filter Items</Text>
          
          <Divider style={styles.divider} />
          
          <Text style={styles.sectionTitle}>Merchant</Text>
          <View style={styles.chipContainer}>
            {Config.MERCHANTS.map((merchant) => (
              <Chip
                key={merchant}
                selected={selectedMerchant === merchant}
                onPress={() =>
                  setSelectedMerchant(selectedMerchant === merchant ? undefined : merchant)
                }
                style={styles.chip}
              >
                {merchant}
              </Chip>
            ))}
          </View>
          
          <Divider style={styles.divider} />
          
          <Text style={styles.sectionTitle}>Condition</Text>
          <View style={styles.chipContainer}>
            {Config.CONDITIONS.map((condition) => (
              <Chip
                key={condition}
                selected={selectedCondition === condition}
                onPress={() =>
                  setSelectedCondition(selectedCondition === condition ? undefined : condition)
                }
                style={styles.chip}
              >
                {condition}
              </Chip>
            ))}
          </View>
          
          <Divider style={styles.divider} />
          
          <Text style={styles.sectionTitle}>Stock Status</Text>
          <View style={styles.chipContainer}>
            <Chip
              selected={inStock === true}
              onPress={() => setInStock(inStock === true ? undefined : true)}
              style={styles.chip}
            >
              In Stock
            </Chip>
            <Chip
              selected={inStock === false}
              onPress={() => setInStock(inStock === false ? undefined : false)}
              style={styles.chip}
            >
              Out of Stock
            </Chip>
          </View>
          
          <View style={styles.buttonContainer}>
            <Button mode="outlined" onPress={handleClear} style={styles.button}>
              Clear
            </Button>
            <Button mode="contained" onPress={handleApply} style={styles.button}>
              Apply
            </Button>
          </View>
        </ScrollView>
      </Modal>
    </Portal>
  );
};

const styles = StyleSheet.create({
  modal: {
    backgroundColor: Colors.surface,
    margin: 20,
    padding: 20,
    borderRadius: 8,
    maxHeight: '80%',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 16,
    color: Colors.onSurface,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 12,
    marginTop: 8,
    color: Colors.onSurface,
  },
  chipContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
  },
  chip: {
    marginRight: 8,
    marginBottom: 8,
  },
  divider: {
    marginVertical: 12,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 24,
    gap: 12,
  },
  button: {
    flex: 1,
  },
});
