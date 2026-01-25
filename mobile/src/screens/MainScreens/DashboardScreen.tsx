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
        <Text style={styles.sectionTitle}>Upload Jobs</Text>
        
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
          Start New Upload
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
    marginVertical: 12,
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: '700',
    marginLeft: 20,
    marginTop: 20,
    marginBottom: 12,
    color: Colors.textPrimary,
    letterSpacing: -0.3,
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
    color: Colors.error,
    marginBottom: 20,
    textAlign: 'center',
  },
  actionSection: {
    padding: 20,
    gap: 16,
    marginBottom: 32,
  },
  actionButton: {
    marginVertical: 0,
    paddingVertical: 6,
    borderRadius: 12,
  },
});
