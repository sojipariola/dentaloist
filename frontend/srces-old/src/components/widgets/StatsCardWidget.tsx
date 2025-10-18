// src/components/widgets/StatsCardWidget.tsx
import { WidgetConfig } from '@/types/widget';
import { useWidgetData } from '@/hooks/useWidgetData';

interface StatsCardWidgetProps {
  widget: WidgetConfig;
}

export const StatsCardWidget: React.FC<StatsCardWidgetProps> = ({ widget }) => {
  const { data, isLoading, error } = useWidgetData(widget);

  if (isLoading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-1/3 mb-2"></div>
        <div className="h-8 bg-gray-200 rounded w-1/2"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">{widget.title}</h3>
        <p className="text-red-600">Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow">
      <h3 className="text-sm font-medium text-gray-600 mb-2">{widget.title}</h3>
      <p className="text-3xl font-bold text-gray-900">{data.data?.value || 0}</p>
      {widget.description && (
        <p className="text-sm text-gray-500 mt-2">{widget.description}</p>
      )}
    </div>
  );
};