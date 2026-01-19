import React, { useState, useEffect, useCallback } from 'react';
import { View, StyleSheet, FlatList, RefreshControl } from 'react-native';
import { Card, Text, Chip, Button, Snackbar } from 'react-native-paper';
import { LoadingSpinner } from '../../components/LoadingSpinner';
import { scrapingApi } from '../../api/scraping';
import { ScrapingJob } from '../../types';
import { formatDateTime, formatDuration } from '../../utils/formatters';
import { Colors } from '../../constants/Colors';

export const ScrapingHistoryScreen: React.FC<{ navigation: any }> = ({ navigation }) => {
  const [jobs, setJobs] = useState<ScrapingJob[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState('');
  
  const [currentPage, setCurrentPage] = useState(1);
  const [hasMore, setHasMore] = useState(false);

  const fetchJobs = useCallback(async (page = 1, isRefresh = false) => {
    try {
      if (isRefresh) {
        setRefreshing(true);
      } else if (page === 1) {
        setLoading(true);
      }

      const response = await scrapingApi.getJobs(page, 20);
      
      if (page === 1) {
        setJobs(response.jobs);
      } else {
        setJobs(prev => [...prev, ...response.jobs]);
      }
      
      setCurrentPage(response.pagination.page);
      setHasMore(response.pagination.has_next);
      setError('');
    } catch (err: any) {
      setError(err.message || 'Failed to load jobs');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    fetchJobs(1);
  }, [fetchJobs]);

  const handleLoadMore = () => {
    if (hasMore) {
      fetchJobs(currentPage + 1);
    }
  };

  const handleJobPress = (job: ScrapingJob) => {
    // Could navigate to job details screen
    console.log('Job pressed:', job.id);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return Colors.statusCompleted;
      case 'failed':
        return Colors.statusFailed;
      case 'running':
        return Colors.statusRunning;
      case 'pending':
        return Colors.statusPending;
      default:
        return Colors.placeholder;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return 'check-circle';
      case 'failed':
        return 'close-circle';
      case 'running':
        return 'progress-clock';
      case 'pending':
        return 'clock-outline';
      default:
        return 'help-circle';
    }
  };

  const renderJob = ({ item }: { item: ScrapingJob }) => (
    <Card style={styles.card} onPress={() => handleJobPress(item)}>
      <Card.Content>
        <View style={styles.header}>
          <View style={styles.headerLeft}>
            <Text style={styles.merchant}>{item.merchant}</Text>
            <Chip
              icon={getStatusIcon(item.status)}
              mode="outlined"
              compact
              style={[styles.statusChip, { backgroundColor: getStatusColor(item.status) + '20' }]}
              textStyle={{ color: getStatusColor(item.status) }}
            >
              {item.status.toUpperCase()}
            </Chip>
          </View>
          <Text style={styles.date}>{formatDateTime(item.created_at)}</Text>
        </View>

        <Text style={styles.url} numberOfLines={2}>
          {item.url}
        </Text>

        <View style={styles.stats}>
          <View style={styles.stat}>
            <Text style={styles.statLabel}>Items Scraped</Text>
            <Text style={styles.statValue}>{item.items_scraped}</Text>
          </View>
          
          {item.duration_seconds && (
            <View style={styles.stat}>
              <Text style={styles.statLabel}>Duration</Text>
              <Text style={styles.statValue}>{formatDuration(item.duration_seconds)}</Text>
            </View>
          )}
        </View>

        {item.error_message && (
          <View style={styles.errorBox}>
            <Text style={styles.errorMessage} numberOfLines={2}>
              ⚠️ {item.error_message}
            </Text>
          </View>
        )}
      </Card.Content>
    </Card>
  );

  const renderEmpty = () => {
    if (loading) return null;
    return (
      <View style={styles.emptyContainer}>
        <Text style={styles.emptyText}>No upload jobs found</Text>
        <Button mode="outlined" onPress={() => navigation.navigate('Scrape')}>
          Start New Upload
        </Button>
      </View>
    );
  };

  const renderFooter = () => {
    if (!hasMore) return null;
    return (
      <View style={styles.footer}>
        <Button mode="outlined" onPress={handleLoadMore}>
          Load More
        </Button>
      </View>
    );
  };

  if (loading) {
    return <LoadingSpinner message="Loading upload history..." />;
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={jobs}
        renderItem={renderJob}
        keyExtractor={(item) => item.id.toString()}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={() => fetchJobs(1, true)} />
        }
        ListEmptyComponent={renderEmpty}
        ListFooterComponent={renderFooter}
        contentContainerStyle={jobs.length === 0 ? styles.emptyList : undefined}
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
  card: {
    marginVertical: 8,
    marginHorizontal: 16,
    elevation: 2,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  headerLeft: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  merchant: {
    fontSize: 18,
    fontWeight: 'bold',
    color: Colors.onSurface,
  },
  statusChip: {
    height: 24,
  },
  date: {
    fontSize: 12,
    color: Colors.placeholder,
  },
  url: {
    fontSize: 12,
    color: Colors.placeholder,
    marginBottom: 12,
  },
  stats: {
    flexDirection: 'row',
    gap: 24,
  },
  stat: {
    flex: 1,
  },
  statLabel: {
    fontSize: 12,
    color: Colors.placeholder,
    marginBottom: 4,
  },
  statValue: {
    fontSize: 16,
    fontWeight: '600',
    color: Colors.onSurface,
  },
  errorBox: {
    marginTop: 12,
    padding: 8,
    backgroundColor: Colors.error + '10',
    borderRadius: 4,
  },
  errorMessage: {
    fontSize: 12,
    color: Colors.error,
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
  footer: {
    padding: 16,
    alignItems: 'center',
  },
});
