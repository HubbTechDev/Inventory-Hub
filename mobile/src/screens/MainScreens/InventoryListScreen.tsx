import React, { useState, useEffect, useCallback } from 'react';
import { View, StyleSheet, FlatList, RefreshControl } from 'react-native';
import { FAB, Menu, IconButton, Snackbar, Text, Button } from 'react-native-paper';
import { InventoryCard } from '../../components/InventoryCard';
import { SearchBar } from '../../components/SearchBar';
import { FilterModal } from '../../components/FilterModal';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { inventoryApi } from '../../api/inventory';
import { InventoryItem, InventoryFilters } from '../../types';
import { Config } from '../../constants/Config';
import { Colors } from '../../constants/Colors';

export const InventoryListScreen: React.FC<{ navigation: any }> = ({ navigation }) => {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState('');
  
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState<InventoryFilters>({});
  const [showFilterModal, setShowFilterModal] = useState(false);
  const [showSortMenu, setShowSortMenu] = useState(false);
  
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [hasMore, setHasMore] = useState(false);

  const fetchItems = useCallback(async (page = 1, isRefresh = false) => {
    try {
      if (isRefresh) {
        setRefreshing(true);
      } else if (page === 1) {
        setLoading(true);
      } else {
        setLoadingMore(true);
      }

      const appliedFilters = { ...filters };
      if (searchQuery) {
        appliedFilters.search = searchQuery;
      }

      const response = await inventoryApi.getItems(page, Config.DEFAULT_PAGE_SIZE, appliedFilters);
      
      if (page === 1) {
        setItems(response.items);
      } else {
        setItems(prev => [...prev, ...response.items]);
      }
      
      setCurrentPage(response.pagination.page);
      setTotalPages(response.pagination.total_pages);
      setHasMore(response.pagination.has_next);
      setError('');
    } catch (err: any) {
      setError(err.message || 'Failed to load items');
    } finally {
      setLoading(false);
      setRefreshing(false);
      setLoadingMore(false);
    }
  }, [filters, searchQuery]);

  useEffect(() => {
    fetchItems(1);
  }, [fetchItems]);

  const handleSearch = () => {
    setCurrentPage(1);
    fetchItems(1);
  };

  const handleApplyFilters = (newFilters: InventoryFilters) => {
    setFilters(newFilters);
    setCurrentPage(1);
  };

  const handleSort = (sortBy: string, sortOrder: 'asc' | 'desc') => {
    setFilters(prev => ({ ...prev, sort_by: sortBy, sort_order: sortOrder }));
    setShowSortMenu(false);
    setCurrentPage(1);
  };

  const handleLoadMore = () => {
    if (!loadingMore && hasMore) {
      fetchItems(currentPage + 1);
    }
  };

  const handleItemPress = (item: InventoryItem) => {
    navigation.navigate('InventoryDetail', { itemId: item.id });
  };

  const handleDeleteItem = async (id: number) => {
    try {
      await inventoryApi.deleteItem(id);
      setItems(prev => prev.filter(item => item.id !== id));
    } catch (err: any) {
      setError(err.message || 'Failed to delete item');
    }
  };

  const renderItem = ({ item }: { item: InventoryItem }) => (
    <InventoryCard item={item} onPress={handleItemPress} onDelete={handleDeleteItem} />
  );

  const renderFooter = () => {
    if (!loadingMore) return null;
    return (
      <View style={styles.footer}>
        <LoadingSpinner message="Loading more..." />
      </View>
    );
  };

  const renderEmpty = () => {
    if (loading) return null;
    return (
      <View style={styles.emptyContainer}>
        <Text style={styles.emptyText}>No items found</Text>
        <Button mode="outlined" onPress={() => fetchItems(1)}>
          Refresh
        </Button>
      </View>
    );
  };

  if (loading) {
    return <LoadingSpinner message="Loading inventory..." />;
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <SearchBar
          value={searchQuery}
          onChangeText={setSearchQuery}
          placeholder="Search items..."
          onSubmit={handleSearch}
        />
        
        <View style={styles.actions}>
          <IconButton
            icon="filter"
            size={24}
            onPress={() => setShowFilterModal(true)}
            mode="contained-tonal"
          />
          
          <Menu
            visible={showSortMenu}
            onDismiss={() => setShowSortMenu(false)}
            anchor={
              <IconButton
                icon="sort"
                size={24}
                onPress={() => setShowSortMenu(true)}
                mode="contained-tonal"
              />
            }
          >
            {Config.SORT_OPTIONS.map((option) => (
              <Menu.Item
                key={`${option.value}-${option.order}`}
                onPress={() => handleSort(option.value, option.order)}
                title={option.label}
              />
            ))}
          </Menu>
        </View>
      </View>

      <FlatList
        data={items}
        renderItem={renderItem}
        keyExtractor={(item) => item.id.toString()}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={() => fetchItems(1, true)} />
        }
        onEndReached={handleLoadMore}
        onEndReachedThreshold={0.5}
        ListFooterComponent={renderFooter}
        ListEmptyComponent={renderEmpty}
        contentContainerStyle={items.length === 0 ? styles.emptyList : undefined}
      />

      <FilterModal
        visible={showFilterModal}
        onDismiss={() => setShowFilterModal(false)}
        onApply={handleApplyFilters}
        initialFilters={filters}
      />

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
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingRight: 8,
  },
  actions: {
    flexDirection: 'row',
  },
  footer: {
    paddingVertical: 20,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  emptyList: {
    flexGrow: 1,
  },
  emptyText: {
    fontSize: 16,
    color: Colors.placeholder,
    marginBottom: 16,
  },
});
