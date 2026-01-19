import React from 'react';
import { View, StyleSheet, Dimensions } from 'react-native';
import { Card, Text } from 'react-native-paper';
import { PieChart, BarChart } from 'react-native-chart-kit';
import { Colors } from '../constants/Colors';

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
  const screenWidth = Dimensions.get('window').width - 32;

  const chartData = data.map((item, index) => ({
    name: item.name,
    population: item.count,
    color: item.color || Colors.chartColors[index % Colors.chartColors.length],
    legendFontColor: Colors.onSurface,
    legendFontSize: 12,
  }));

  const barData = {
    labels: data.map((item) => item.name),
    datasets: [
      {
        data: data.map((item) => item.count),
      },
    ],
  };

  const chartConfig = {
    backgroundColor: Colors.surface,
    backgroundGradientFrom: Colors.surface,
    backgroundGradientTo: Colors.surface,
    color: (opacity = 1) => `rgba(98, 0, 238, ${opacity})`,
    labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
    strokeWidth: 2,
    barPercentage: 0.7,
    useShadowColorFromDataset: false,
    decimalPlaces: 0,
  };

  if (data.length === 0) {
    return (
      <Card style={styles.card}>
        <Card.Content>
          <Text style={styles.title}>{title}</Text>
          <Text style={styles.noData}>No data available</Text>
        </Card.Content>
      </Card>
    );
  }

  return (
    <Card style={styles.card}>
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
    marginHorizontal: 16,
    elevation: 2,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 16,
    color: Colors.onSurface,
  },
  chartContainer: {
    alignItems: 'center',
  },
  noData: {
    textAlign: 'center',
    color: Colors.placeholder,
    paddingVertical: 32,
  },
});
