// src/components/widgets/ChartWidget.tsx
import { useState, useEffect } from 'react';
import { WidgetConfig } from '@/types/widget';
import { useWidgetData } from '@/hooks/useWidgetData';

interface ChartWidgetProps {
  widget: WidgetConfig;
}

export const ChartWidget: React.FC<ChartWidgetProps> = ({ widget }) => {
  const { data, isLoading, error, refresh } = useWidgetData(widget);
  const [chartData, setChartData] = useState<any>(null);

  useEffect(() => {
    if (data?.data) {
      // Transform data for charting library
      const transformedData = transformChartData(data.data, widget.type);
      setChartData(transformedData);
    }
  }, [data, widget.type]);

  const transformChartData = (rawData: any, chartType: string) => {
    // Basic data transformation - you'd integrate with your actual charting library
    switch (chartType) {
      case 'line_chart':
        return {
          labels: rawData.labels || ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
          datasets: [
            {
              label: widget.title,
              data: rawData.values || [65, 59, 80, 81, 56, 55],
              borderColor: 'rgb(75, 192, 192)',
              tension: 0.1,
            },
          ],
        };
      
      case 'bar_chart':
        return {
          labels: rawData.labels || ['Category 1', 'Category 2', 'Category 3'],
          datasets: [
            {
              label: widget.title,
              data: rawData.values || [30, 45, 60],
              backgroundColor: 'rgba(53, 162, 235, 0.5)',
            },
          ],
        };
      
      case 'pie_chart':
        return {
          labels: rawData.labels || ['Red', 'Blue', 'Yellow'],
          datasets: [
            {
              label: widget.title,
              data: rawData.values || [30, 50, 20],
              backgroundColor: [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)',
              ],
            },
          ],
        };
      
      default:
        return rawData;
    }
  };

  if (isLoading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
        <div className="h-40 bg-gray-200 rounded"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">{widget.title}</h3>
          <button
            onClick={refresh}
            className="text-blue-600 hover:text-blue-800 text-sm"
          >
            Retry
          </button>
        </div>
        <div className="text-red-600 bg-red-50 p-4 rounded">
          <p>Error: {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{widget.title}</h3>
        <button
          onClick={refresh}
          className="text-gray-500 hover:text-gray-700 text-sm"
          title="Refresh data"
        >
          ↻
        </button>
      </div>
      
      {widget.description && (
        <p className="text-sm text-gray-600 mb-4">{widget.description}</p>
      )}

      <div className="h-64">
        {chartData ? (
          <div className="w-full h-full flex items-center justify-center">
            {/* This would be replaced with your actual chart component */}
            <div className="text-center">
              <p className="text-sm text-gray-500 mb-2">Chart: {widget.type}</p>
              <div className="bg-gray-100 p-4 rounded">
                <p className="text-xs text-gray-600">
                  Chart data loaded: {JSON.stringify(chartData).substring(0, 100)}...
                </p>
              </div>
            </div>
          </div>
        ) : (
          <div className="h-full flex items-center justify-center text-gray-500">
            No chart data available
          </div>
        )}
      </div>

      {data?.lastUpdated && (
        <div className="text-xs text-gray-500 mt-4">
          Updated: {new Date(data.lastUpdated).toLocaleTimeString()}
        </div>
      )}
    </div>
  );
};

// Example integration with Chart.js (uncomment if you have Chart.js installed)
/*
import { Line, Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

// Then replace the chart display section with:
{chartData && (
  <>
    {widget.type === 'line_chart' && <Line data={chartData} />}
    {widget.type === 'bar_chart' && <Bar data={chartData} />}
    {widget.type === 'pie_chart' && <Pie data={chartData} />}
  </>
)}
*/