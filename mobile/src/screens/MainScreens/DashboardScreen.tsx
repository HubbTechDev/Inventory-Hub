import React, { useState, useEffect, useCallback } from 'react';
import { View, StyleSheet, ScrollView, RefreshControl } from 'react-native';
import { Text, Button, Snackbar } from 'react-native-paper';
import { StatsCard } from '../../components/StatsCard';
import { ChartComponent } from '../../components/ChartComponent';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { statsApi } from '../../api/stats';
import { Statistics } from '../../types';
import { formatCurrency, formatNumber } from '../../utils/formatters';
import { Colors } from '../../constants/Colors';

export const DashboardScreen: React.FC<{ navigation: any }> = ({ navigation }) => {
  const [stats, setStats] = useState<Statistics | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState('');

  const fetchStats = useCallback(async (isRefresh = false) => {
    try {
      if (isRefresh) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }
      
      const data = await statsApi.getStatistics();
      setStats(data);
      setError('');
    } catch (err: any) {
      setError(err.message || 'Failed to load statistics');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  if (loading) {
    return <LoadingSpinner message="Loading dashboard..." />;
  }

  if (!stats) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Failed to load dashboard</Text>
        <Button mode="contained" onPress={() => fetchStats()}>
          Retry
        </Button>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={() => fetchStats(true)} />
      }
    >
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Inventory Overview</Text>
        
        <StatsCard
          title="Total Items"
          value={formatNumber(stats.inventory.total_items)}
          subtitle={`${stats.inventory.items_in_stock} in stock`}
          icon="📦"
          color={Colors.primary}
        />
        
        <StatsCard
          title="Total Value"
          value={formatCurrency(stats.inventory.total_value)}
          subtitle={`${stats.inventory.items_last_month} items this month`}
          icon="💰"
          color={Colors.success}
        />
        
        <StatsCard
          title="Out of Stock"
          value={formatNumber(stats.inventory.items_out_of_stock)}
          subtitle={`${((stats.inventory.items_out_of_stock / stats.inventory.total_items) * 100).toFixed(1)}% of total`}
          icon="⚠️"
          color={Colors.warning}
        />
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Distribution</Text>
        
        {stats.merchants.length > 0 && (
          <ChartComponent
            title="Items by Merchant"
            data={stats.merchants.map(m => ({ name: m.merchant, count: m.count }))}
            type="pie"
          />
        )}
        
        {stats.conditions.length > 0 && (
          <ChartComponent
            title="Items by Condition"
            data={stats.conditions.map(c => ({ name: c.condition, count: c.count }))}
            type="bar"
          />
        )}
        
        {stats.categories.length > 0 && stats.categories.length <= 8 && (
          <ChartComponent
            title="Top Categories"
            data={stats.categories.slice(0, 8).map(c => ({ name: c.category, count: c.count }))}
            type="pie"
          />
        )}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Scraping Jobs</Text>
        
        <StatsCard
          title="Total Jobs"
          value={formatNumber(stats.scraping_jobs.total_jobs)}
          subtitle={`${stats.scraping_jobs.successful_jobs} successful`}
          icon="🕷️"
          color={Colors.info}
        />
        
        {stats.scraping_jobs.failed_jobs > 0 && (
          <StatsCard
            title="Failed Jobs"
            value={formatNumber(stats.scraping_jobs.failed_jobs)}
            subtitle="Needs attention"
            icon="❌"
            color={Colors.error}
          />
        )}
        
        {stats.scraping_jobs.pending_jobs > 0 && (
          <StatsCard
            title="Pending Jobs"
            value={formatNumber(stats.scraping_jobs.pending_jobs)}
            subtitle="In queue"
            icon="⏳"
            color={Colors.statusPending}
          />
        )}
      </View>

      <View style={styles.actionSection}>
        <Button
          mode="contained"
          icon="plus"
          onPress={() => navigation.navigate('Scrape')}
          style={styles.actionButton}
        >
          Start New Scrape
        </Button>
        
        <Button
          mode="outlined"
          icon="package-variant"
          onPress={() => navigation.navigate('Inventory')}
          style={styles.actionButton}
        >
          View Inventory
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
  section: {
    marginVertical: 8,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginLeft: 16,
    marginTop: 16,
    marginBottom: 8,
    color: Colors.onSurface,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  errorText: {
    fontSize: 16,
    color: Colors.error,
    marginBottom: 16,
  },
  actionSection: {
    padding: 16,
    gap: 12,
    marginBottom: 24,
  },
  actionButton: {
    marginVertical: 4,
  },
});
