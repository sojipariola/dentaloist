// src/components/widgets/TableWidget.tsx
import { useState, useEffect } from 'react';
import { WidgetConfig } from '@/types/widget';
import { useWidgetData } from '@/hooks/useWidgetData';

interface TableWidgetProps {
  widget: WidgetConfig;
}

interface TableColumn {
  key: string;
  label: string;
  sortable?: boolean;
  render?: (value: any, row: any) => React.ReactNode;
}

export const TableWidget: React.FC<TableWidgetProps> = ({ widget }) => {
  const { data, isLoading, error, refresh } = useWidgetData(widget);
  const [tableData, setTableData] = useState<any[]>([]);
  const [columns, setColumns] = useState<TableColumn[]>([]);
  const [sortConfig, setSortConfig] = useState<{ key: string; direction: 'asc' | 'desc' } | null>(null);

  useEffect(() => {
    if (data?.data) {
      processTableData(data.data);
    }
  }, [data]);

  const processTableData = (rawData: any) => {
    if (Array.isArray(rawData)) {
      // If data is already an array, use it directly
      setTableData(rawData);
      
      // Generate columns from first item keys
      if (rawData.length > 0) {
        const firstItem = rawData[0];
        const generatedColumns = Object.keys(firstItem).map(key => ({
          key,
          label: key.split('_').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
          ).join(' '),
          sortable: true,
        }));
        setColumns(generatedColumns);
      }
    } else if (rawData.rows && rawData.columns) {
      // If data has structured rows and columns
      setTableData(rawData.rows);
      setColumns(rawData.columns.map((col: any) => ({
        key: col.key || col.field,
        label: col.label || col.header,
        sortable: col.sortable !== false,
        render: col.render,
      })));
    } else if (rawData.data && Array.isArray(rawData.data)) {
      // Handle various API response formats
      setTableData(rawData.data);
      if (rawData.columns) {
        setColumns(rawData.columns);
      }
    }
  };

  const handleSort = (key: string) => {
    let direction: 'asc' | 'desc' = 'asc';
    
    if (sortConfig && sortConfig.key === key) {
      direction = sortConfig.direction === 'asc' ? 'desc' : 'asc';
    }
    
    setSortConfig({ key, direction });
    
    const sortedData = [...tableData].sort((a, b) => {
      if (a[key] < b[key]) return direction === 'asc' ? -1 : 1;
      if (a[key] > b[key]) return direction === 'asc' ? 1 : -1;
      return 0;
    });
    
    setTableData(sortedData);
  };

  const renderValue = (value: any): React.ReactNode => {
    if (value === null || value === undefined) return '-';
    if (typeof value === 'boolean') return value ? 'Yes' : 'No';
    if (typeof value === 'object') return JSON.stringify(value);
    return value.toString();
  };

  if (isLoading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow animate-pulse">
        <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
        <div className="space-y-3">
          <div className="h-4 bg-gray-200 rounded w-full"></div>
          <div className="h-4 bg-gray-200 rounded w-5/6"></div>
          <div className="h-4 bg-gray-200 rounded w-4/6"></div>
        </div>
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

      {tableData.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          No data available
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                {columns.map((column) => (
                  <th
                    key={column.key}
                    className={`px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider ${
                      column.sortable ? 'cursor-pointer hover:bg-gray-100' : ''
                    }`}
                    onClick={() => column.sortable && handleSort(column.key)}
                  >
                    <div className="flex items-center">
                      {column.label}
                      {column.sortable && sortConfig?.key === column.key && (
                        <span className="ml-1">
                          {sortConfig.direction === 'asc' ? '↑' : '↓'}
                        </span>
                      )}
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {tableData.slice(0, 10).map((row, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  {columns.map((column) => (
                    <td
                      key={column.key}
                      className="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                    >
                      {column.render
                        ? column.render(row[column.key], row)
                        : renderValue(row[column.key])
                      }
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          
          {tableData.length > 10 && (
            <div className="mt-4 text-sm text-gray-500 text-center">
              Showing 10 of {tableData.length} records
            </div>
          )}
        </div>
      )}

      {data?.lastUpdated && (
        <div className="text-xs text-gray-500 mt-4">
          Updated: {new Date(data.lastUpdated).toLocaleTimeString()}
        </div>
      )}
    </div>
  );
};

// Example of custom column renderers you can use:
export const tableRenderers = {
  date: (value: string) => new Date(value).toLocaleDateString(),
  currency: (value: number) => `$${value.toFixed(2)}`,
  boolean: (value: boolean) => value ? '✅' : '❌',
  status: (value: string) => (
    <span className={`px-2 py-1 rounded-full text-xs ${
      value === 'completed' ? 'bg-green-100 text-green-800' :
      value === 'pending' ? 'bg-yellow-100 text-yellow-800' :
      value === 'cancelled' ? 'bg-red-100 text-red-800' :
      'bg-gray-100 text-gray-800'
    }`}>
      {value}
    </span>
  ),
};