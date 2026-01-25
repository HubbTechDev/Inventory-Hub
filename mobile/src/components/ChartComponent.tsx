import React from 'react';
import { View, StyleSheet, Dimensions } from 'react-native';
import { Card, Text } from 'react-native-paper';
import { PieChart, BarChart } from 'react-native-chart-kit';
import { Colors, Theme } from '../constants/Colors';

interface ChartData {
  name: string;
  count: number;
  color?: string;
}

interface ChartComponentProps {
  title: string;
  data: ChartData[];
  type: 'pie' | 'bar';
}

export const ChartComponent: React.FC<ChartComponentProps> = ({ title, data, type }) => {
  const screenWidth = Dimensions.get('window').width - 40;

  const chartData = data.map((item, index) => ({
    name: item.name,
    population: item.count,
    color: item.color || Colors.chartColors[index % Colors.chartColors.length],
    legendFontColor: Colors.textPrimary,
    legendFontSize: 13,
  }));

  const barData = {
    labels: data.map((item) => item.name),
    datasets: [
      {
        data: data.map((item) => item.count),
        color: (opacity = 1) => Colors.primary,
      },
    ],
  };

  const chartConfig = {
    backgroundColor: Colors.surface,
    backgroundGradientFrom: Colors.surface,
    backgroundGradientTo: Colors.surface,
    color: (opacity = 1) => `rgba(79, 70, 229, ${opacity})`,
    labelColor: (opacity = 1) => `rgba(17, 24, 39, ${opacity})`,
    strokeWidth: 2,
    barPercentage: 0.7,
    useShadowColorFromDataset: false,
    decimalPlaces: 0,
    propsForLabels: {
      fontSize: 12,
      fontWeight: '600',
    },
  };

  if (data.length === 0) {
    return (
      <Card style={styles.card} mode="elevated">
        <Card.Content>
          <Text style={styles.title}>{title}</Text>
          <Text style={styles.noData}>No data available</Text>
        </Card.Content>
      </Card>
    );
  }

  return (
    <Card style={styles.card} mode="elevated">
      <Card.Content>
        <Text style={styles.title}>{title}</Text>
        <View style={styles.chartContainer}>
          {type === 'pie' ? (
            <PieChart
              data={chartData}
              width={screenWidth - 32}
              height={220}
              chartConfig={chartConfig}
              accessor="population"
              backgroundColor="transparent"
              paddingLeft="15"
              absolute
            />
          ) : (
            <BarChart
              data={barData}
              width={screenWidth - 32}
              height={220}
              chartConfig={chartConfig}
              verticalLabelRotation={30}
              yAxisLabel=""
              yAxisSuffix=""
              fromZero
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
    marginHorizontal: 20,
    backgroundColor: Colors.surface,
    borderRadius: 16,
    ...Theme.shadows.medium,
  },
  title: {
    fontSize: 18,
    fontWeight: '700',
    marginBottom: 16,
    color: Colors.textPrimary,
    letterSpacing: -0.3,
  },
  chartContainer: {
    alignItems: 'center',
    paddingVertical: 8,
  },
  noData: {
    textAlign: 'center',
    color: Colors.textSecondary,
    paddingVertical: 40,
    fontSize: 15,
  },
});
